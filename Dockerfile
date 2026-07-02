# ── Stage 1: build ────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Keep Python output unbuffered for live logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first (layer cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Generate the dataset at build time so the container ships with data
RUN python generate_energy_dataset.py

# ── Runtime ────────────────────────────────────────────────────────────────────
EXPOSE 5000

# Use gunicorn for production; 2 workers is fine for a demo
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
