#!/bin/bash
set -e

echo "Starting deployment..."

# Create virtual environment at root if it does not exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python -m venv .venv
fi

# Activate virtual environment (Linux & Windows Git Bash)
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
else
  echo "Virtual environment activation script not found"
  exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

# Server startup

echo "Starting server on port 8080..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

# Deployment complete
echo "Deployment complete."
echo "Server is running in the background. Check server.log for output."
