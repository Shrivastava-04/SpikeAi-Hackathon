#!/bin/bash
set -e

echo "Starting deployment..."

python -m venv .venv || true
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Starting server on port 8080..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

