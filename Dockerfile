ARG VARIANT=3.13-slim-bookworm

# Base stage
FROM python:${VARIANT} AS base

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1
COPY gunicorn.conf.py pyproject.toml ./

## Dev with mounted volumes and dev deps
FROM base AS dev
COPY requirements-dev.lock ./
RUN pip install -r requirements-dev.lock
VOLUME ["/app/src", "/app/tests"]
CMD ["gunicorn", "data_deidentifier.adapters.api.main:app"]

# Standalone dev with code included
FROM dev AS dev-standalone
COPY src ./src
COPY tests ./tests
RUN pip install --no-deps -e .

## Prod with copied code and minimal deps
FROM base AS prod
COPY requirements.lock ./
RUN pip install --no-deps --no-compile -r requirements.lock
COPY src ./src
CMD ["gunicorn", "data_deidentifier.adapters.api.main:app"]
