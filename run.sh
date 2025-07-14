#!/usr/bin/env bash
set -euo pipefail

bash install.sh

echo "[INFO] Starting FastAPI service on http://localhost:8000 ..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
