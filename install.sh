#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "[INFO] No .env file detected. Copying from .env.example."
  cp .env.example .env
fi

echo "[INFO] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# DB initialization
python -c 'import asyncio; from app.db import init_db; asyncio.run(init_db())'
echo "[INFO] Database initialized."
