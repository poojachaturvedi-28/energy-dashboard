"""
app.py
Flask application for the Energy Consumption Monitoring Dashboard
Dataset: G-091023 / G_103101  (3P4W power quality analyzer data)
"""

import os
import re
import io
import pandas as pd
from functools import lru_cache
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DATA_3P4W   = os.path.join("data", "G-091023 (1)", "G-091023", "G_103101", "3P4W.XLS")
DATA_MINMAX = os.path.join("data", "G-091023 (1)", "G-091023", "G_103101", "MIN--MAX.XLS")


# ── Data Loaders ──────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def load_3p4w():
    """
    Load the 3P4W tab-delimited file.
    Returns a cleaned DataFrame with a proper 'datetime' column.
    """
    df = pd.read_csv(DATA_3P4W, sep="\t", skiprows=1,
                     encoding="latin1", low_memory=False)
    df.columns = df.columns.str.strip()

    # Build datetime before fragmenting the frame
    dt_series = pd.to_datetime(
        df["Date"].astype(str).str.strip() + " " + df["Time"].astype(str).str.strip(),
        format="%d/%m/%y %H:%M:%S", errors="coerce"
    )

    # Coerce all numeric columns at once
    non_numeric = {"Date", "Time", "Relay"}
    num_cols = [c for c in df.columns if c not in non_numeric]
    numeric_df = df[num_cols].apply(pd.to_numeric, errors="coerce")
    text_df    = df[list(non_numeric.intersection(df.columns))]

    df = pd.concat([text_df, numeric_df], axis=1).copy()
    df["datetime"] = dt_series

    df = df.dropna(subset=["datetime"]).sort_values("datetime").reset_index(drop=True)
    return df


@lru_cache(maxsize=1)
def load_minmax():
    """Parse Min-Max values from the MIN--MAX.XLS file."""
    records = []
    with open(DATA_MINMAX, "r", encoding="latin1") as f:
        in_section = False
        for line in f:
            line = line.replace("\x00", "").strip()
            if "Min-Max Values" in line:
                in_section = True
                continue
            if in_section and line.startswith("Interruptions"):
                break
            if in_section and line and not line.startswith("No."):
                parts = line.split("\t")
                if len(parts) >= 7:
                    try:
                        records.append({
                            "parameter": parts[1].strip(),
                            "min_val":   float(parts[2]),
                            "min_date":  parts[3].strip(),
                            "min_time":  parts[4].strip(),
                            "max_val":   float(parts[5]),
                            "max_date":  parts[6].strip(),
                            "max_time":  parts[7].strip() if len(parts) > 7 else "",
                        })
                    except (ValueError, IndexError):
                        pass
    return records


@lru_cache(maxsize=1)
def load_sagswell():
    """Parse Sag/Swell events from the MIN--MAX.XLS file."""
    events = []
    with open(DATA_MINMAX, "r", encoding="latin1") as f:
        in_section = False
        for line in f:
            line = line.replace("\x00", "").strip()
            if "Sag/Swell" in line:
                in_section = True
                continue
            if in_section and line.startswith("Run Hour"):
                break
            if in_section and line and not line.startswith("No."):
                parts = line.split("\t")
                if len(parts) >= 6:
                    try:
                        events.append({
                            "no":         int(parts[0]),
                            "start_date": parts[1].strip(),
                            "start_time": parts[2].strip(),
                            "duration_ms":int(parts[3]),
                            "type":       parts[4].strip(),
                            "value":      float(parts[5]),
                        })
                    except (ValueError, IndexError):
                        pass
    return events


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    df = load_3p4w()
    date_min = df["datetime"].min().strftime("%d %b %Y")
    date_max = df["datetime"].max().strftime("%d %b %Y")
    total_records = len(df)
    return render_template("index.html",
                           date_min=date_min,
                           date_max=date_max,
                           total_records=total_records)


@app.route("/api/summary")
def api_summary():
    df = load_3p4w()
    return jsonify({
        "total_records":    len(df),
        "date_range":       f"{df['datetime'].min().strftime('%d %b %Y')} – {df['datetime'].max().strftime('%d %b %Y')}",
        "avg_sys_kw":       round(df["Sys.KW"].abs().mean(), 3),
        "max_sys_kva":      round(df["Sys.KVA"].max(), 3),
        "avg_sys_pf":       round(df["Sys.PF"].abs().mean(), 3),
        "avg_freq_hz":      round(df["Hz"].mean(), 3),
        "avg_vrn":          round(df["Vrn"].mean(), 2),
        "avg_vyn":          round(df["Vyn"].mean(), 2),
        "avg_vbn":          round(df["Vbn"].mean(), 2),
        "imp_eb_kwh":       round(df["Imp-EB-KWh"].max(), 3),
        "exp_eb_kwh":       round(df["Exp-EB-KWh"].max(), 3),
        "avg_temp_c":       round(df["Temp.('C)"].mean(), 1) if df["Temp.('C)"].dtype != object else None,
    })


@app.route("/api/power-over-time")
def api_power_over_time():
    """Sys.KW resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    series = df["Sys.KW"].abs().resample("15min").mean().dropna()
    return jsonify([{"time": t.isoformat(), "kw": round(v, 3)}
                    for t, v in series.items()])


@app.route("/api/voltage-over-time")
def api_voltage_over_time():
    """Phase voltages resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    out = df[["Vrn", "Vyn", "Vbn"]].resample("15min").mean().dropna()
    result = []
    for t, row in out.iterrows():
        result.append({
            "time": t.isoformat(),
            "Vrn": round(row["Vrn"], 2),
            "Vyn": round(row["Vyn"], 2),
            "Vbn": round(row["Vbn"], 2),
        })
    return jsonify(result)


@app.route("/api/current-over-time")
def api_current_over_time():
    """Phase currents resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    out = df[["Ir", "Iy", "Ib"]].resample("15min").mean().dropna()
    result = []
    for t, row in out.iterrows():
        result.append({
            "time": t.isoformat(),
            "Ir": round(row["Ir"], 3),
            "Iy": round(row["Iy"], 3),
            "Ib": round(row["Ib"], 3),
        })
    return jsonify(result)


@app.route("/api/pf-over-time")
def api_pf_over_time():
    """System power factor resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    series = df["Sys.PF"].abs().resample("15min").mean().dropna()
    return jsonify([{"time": t.isoformat(), "pf": round(v, 4)}
                    for t, v in series.items()])


@app.route("/api/kva-kvar-over-time")
def api_kva_kvar():
    """Sys KVA and KVAR resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    out = df[["Sys.KVA", "Sys.KVAR"]].abs().resample("15min").mean().dropna()
    result = []
    for t, row in out.iterrows():
        result.append({
            "time":    t.isoformat(),
            "kva":     round(row["Sys.KVA"], 3),
            "kvar":    round(abs(row["Sys.KVAR"]), 3),
        })
    return jsonify(result)


@app.route("/api/phase-kw")
def api_phase_kw():
    """Average KW per phase."""
    df = load_3p4w()
    return jsonify([
        {"phase": "Phase R", "kw": round(df["KW-r"].abs().mean(), 3)},
        {"phase": "Phase Y", "kw": round(df["KW-y"].abs().mean(), 3)},
        {"phase": "Phase B", "kw": round(df["KW-b"].abs().mean(), 3)},
    ])


@app.route("/api/thd")
def api_thd():
    """Average THD (voltage) per phase."""
    df = load_3p4w()
    return jsonify([
        {"phase": "Phase R", "thd": round(df["HVr-THD"].mean(), 2)},
        {"phase": "Phase Y", "thd": round(df["HVy-THD"].mean(), 2)},
        {"phase": "Phase B", "thd": round(df["HVb-THD"].mean(), 2)},
    ])


@app.route("/api/freq-over-time")
def api_freq():
    """System frequency resampled to 15-min averages."""
    df = load_3p4w().set_index("datetime")
    series = df["Hz"].resample("15min").mean().dropna()
    return jsonify([{"time": t.isoformat(), "hz": round(v, 3)}
                    for t, v in series.items()])


@app.route("/api/energy-cumulative")
def api_energy():
    """Cumulative imported vs exported energy (kWh) over time."""
    df = load_3p4w().set_index("datetime")
    out = df[["Imp-EB-KWh", "Exp-EB-KWh"]].resample("15min").max().dropna()
    result = []
    for t, row in out.iterrows():
        result.append({
            "time":    t.isoformat(),
            "imp_kwh": round(row["Imp-EB-KWh"], 3),
            "exp_kwh": round(row["Exp-EB-KWh"], 3),
        })
    return jsonify(result)


@app.route("/api/minmax")
def api_minmax():
    return jsonify(load_minmax())


@app.route("/api/sagswell")
def api_sagswell():
    return jsonify(load_sagswell())


@app.route("/api/harmonics")
def api_harmonics():
    """Average harmonic levels (3rd–15th) for each phase voltage."""
    df = load_3p4w()
    orders = ["3rd", "5th", "7th", "9th", "11th", "13th", "15th"]
    result = {"orders": orders, "VR": [], "VY": [], "VB": []}
    for o in orders:
        result["VR"].append(round(df[f"HVr-{o}"].mean(), 2))
        result["VY"].append(round(df[f"HVy-{o}"].mean(), 2))
        result["VB"].append(round(df[f"HVb-{o}"].mean(), 2))
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
