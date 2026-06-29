FROM python:3.11-slim

WORKDIR /srv

# System deps for scipy/scikit-learn wheels on slim images.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install the parksight pipeline package first (used by patrol_service.py).
COPY pyproject.toml /srv/pyproject.toml
COPY parksight /srv/parksight
RUN pip install --no-cache-dir -e .

# Install backend-specific requirements (FastAPI, uvicorn, etc.).
COPY backend/requirements.txt /srv/backend/requirements.txt
RUN pip install --no-cache-dir -r /srv/backend/requirements.txt

COPY backend/app /srv/backend/app
COPY config /srv/config
COPY data /srv/data

# Run the analytics pipeline at build time so /srv/outputs always
# reflects the data + config baked into this image.
COPY data/raw/violations.csv.gz data/raw/
RUN gunzip data/raw/violations.csv.gz && \
    parksight --input data/raw/violations.csv --output outputs

WORKDIR /srv/backend
ENV PARKSIGHT_OUTPUT_DIR=/srv/outputs \
    PARKSIGHT_SETTINGS_PATH=/srv/config/settings.yaml \
    PARKSIGHT_INPUT_CSV=/srv/data/raw/violations.csv \
    FRONTEND_ORIGIN=http://localhost:5173

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]