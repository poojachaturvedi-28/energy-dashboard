# ⚡ Energy Consumption Monitoring Dashboard

A beginner-level cloud-deployable web dashboard that visualises energy consumption data across multiple buildings and sources.

Built with **Flask**, **Chart.js**, and **Docker** — ready to run locally or deploy to any cloud provider that supports containers (AWS ECS, GCP Cloud Run, Azure Container Apps, Railway, Render, etc.).

---

## Features

| Feature | Details |
|---|---|
| KPI Cards | Total kWh, Total Cost, Avg per Record, Top Source |
| Line Charts | Daily consumption & cost over time |
| Bar Chart | Consumption per building |
| Doughnut Chart | Consumption by energy source |
| Building Filter | Filter all time-series charts by building |
| REST API | JSON endpoints for every metric |
| Docker-ready | Single `docker compose up` to run |

---

## Project Structure

```
energy-dashboard/
├── app.py                    # Flask application & API routes
├── generate_energy_dataset.py # Synthetic data generator
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build instructions
├── docker-compose.yml        # Local multi-container orchestration
├── .dockerignore             # Files excluded from Docker build
├── README.md                 # This file
├── data/
│   └── energy.csv            # Generated dataset (auto-created)
├── templates/
│   └── index.html            # Jinja2 dashboard template
└── static/
    └── style.css             # Dark-theme stylesheet
```

---

## Quick Start

### Option 1 — Docker Compose (recommended)

```bash
# 1. Clone / enter the project directory
cd energy-dashboard

# 2. Build and start
docker compose up --build

# 3. Open your browser
open http://localhost:5000
```

### Option 2 — Plain Python

```bash
cd energy-dashboard

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_energy_dataset.py

# Run the development server
flask run --host=0.0.0.0 --port=5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard HTML page |
| GET | `/api/summary` | KPI metrics (totals, averages) |
| GET | `/api/consumption-by-building` | kWh grouped by building |
| GET | `/api/consumption-by-source` | kWh grouped by energy source |
| GET | `/api/consumption-over-time?building=X` | Daily kWh (optionally filtered) |
| GET | `/api/cost-over-time?building=X` | Daily cost USD (optionally filtered) |

---

## Cloud Deployment

### AWS ECS / ECR

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker build -t energy-dashboard .
docker tag energy-dashboard:latest <account>.dkr.ecr.us-east-1.amazonaws.com/energy-dashboard:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/energy-dashboard:latest
```

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/<project>/energy-dashboard
gcloud run deploy energy-dashboard \
  --image gcr.io/<project>/energy-dashboard \
  --platform managed \
  --allow-unauthenticated \
  --port 5000
```

### Railway / Render

Push the repo to GitHub and connect it to Railway or Render — both will auto-detect the `Dockerfile` and deploy.

---

## Tech Stack

- **Backend**: Python 3.12, Flask 3, Gunicorn
- **Frontend**: Vanilla JS, Chart.js 4, CSS custom properties
- **Containerisation**: Docker, Docker Compose
- **Data**: Synthetic CSV (generated via `generate_energy_dataset.py`)

---

## License

MIT
