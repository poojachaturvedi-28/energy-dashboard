"""
generate_energy_dataset.py
Generates a synthetic energy consumption dataset and saves it to data/energy.csv
"""

import os
import random
import csv
from datetime import datetime, timedelta

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

BUILDINGS = ["Building A", "Building B", "Building C", "Building D"]
SOURCES = ["Solar", "Grid", "Wind", "Diesel"]

start_date = datetime(2024, 1, 1)
rows = []

random.seed(42)

for i in range(365 * 4):  # ~4 years worth, one record per building per day
    for building in BUILDINGS:
        date = start_date + timedelta(days=i // len(BUILDINGS))
        source = random.choice(SOURCES)
        consumption_kwh = round(random.uniform(50, 500), 2)
        cost_usd = round(consumption_kwh * random.uniform(0.08, 0.15), 2)
        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "building": building,
            "source": source,
            "consumption_kwh": consumption_kwh,
            "cost_usd": cost_usd,
        })

output_path = os.path.join("data", "energy.csv")
fieldnames = ["date", "building", "source", "consumption_kwh", "cost_usd"]

with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset generated: {output_path} ({len(rows)} records)")
