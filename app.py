"""
app.py
Flask application for the Energy Consumption Monitoring Dashboard.
"""

import os
import csv
from collections import defaultdict
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DATA_PATH = os.path.join("data", "energy.csv")


def load_data():
    """Load energy data from CSV into a list of dicts."""
    rows = []
    if not os.path.exists(DATA_PATH):
        return rows
    with open(DATA_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["consumption_kwh"] = float(row["consumption_kwh"])
            row["cost_usd"] = float(row["cost_usd"])
            rows.append(row)
    return rows


@app.route("/")
def index():
    """Render the main dashboard page."""
    data = load_data()
    buildings = sorted(set(r["building"] for r in data))
    sources = sorted(set(r["source"] for r in data))
    return render_template("index.html", buildings=buildings, sources=sources)


@app.route("/api/summary")
def api_summary():
    """Return high-level KPI metrics as JSON."""
    data = load_data()
    if not data:
        return jsonify({})

    total_kwh = sum(r["consumption_kwh"] for r in data)
    total_cost = sum(r["cost_usd"] for r in data)
    avg_kwh = total_kwh / len(data)

    source_totals = defaultdict(float)
    for r in data:
        source_totals[r["source"]] += r["consumption_kwh"]

    top_source = max(source_totals, key=source_totals.get)

    return jsonify({
        "total_kwh": round(total_kwh, 2),
        "total_cost_usd": round(total_cost, 2),
        "avg_kwh_per_record": round(avg_kwh, 2),
        "top_source": top_source,
        "record_count": len(data),
    })


@app.route("/api/consumption-by-building")
def api_by_building():
    """Return total consumption grouped by building."""
    data = load_data()
    totals = defaultdict(float)
    for r in data:
        totals[r["building"]] += r["consumption_kwh"]
    result = [{"building": k, "consumption_kwh": round(v, 2)} for k, v in sorted(totals.items())]
    return jsonify(result)


@app.route("/api/consumption-by-source")
def api_by_source():
    """Return total consumption grouped by energy source."""
    data = load_data()
    totals = defaultdict(float)
    for r in data:
        totals[r["source"]] += r["consumption_kwh"]
    result = [{"source": k, "consumption_kwh": round(v, 2)} for k, v in sorted(totals.items())]
    return jsonify(result)


@app.route("/api/consumption-over-time")
def api_over_time():
    """Return daily total consumption, optionally filtered by building."""
    data = load_data()
    building_filter = request.args.get("building", "")
    if building_filter:
        data = [r for r in data if r["building"] == building_filter]

    daily = defaultdict(float)
    for r in data:
        daily[r["date"]] += r["consumption_kwh"]

    result = [{"date": k, "consumption_kwh": round(v, 2)} for k, v in sorted(daily.items())]
    return jsonify(result)


@app.route("/api/cost-over-time")
def api_cost_over_time():
    """Return daily total cost over time."""
    data = load_data()
    building_filter = request.args.get("building", "")
    if building_filter:
        data = [r for r in data if r["building"] == building_filter]

    daily = defaultdict(float)
    for r in data:
        daily[r["date"]] += r["cost_usd"]

    result = [{"date": k, "cost_usd": round(v, 2)} for k, v in sorted(daily.items())]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
