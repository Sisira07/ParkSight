#!/usr/bin/env bash
# scripts/setup.sh — one-shot environment setup for Linux/macOS.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "== Python: creating .venv and installing the package =="
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
pip install -r backend/requirements.txt

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi
if [ ! -f backend/.env ] && [ -f backend/.env.example ]; then
  cp backend/.env.example backend/.env
fi
if [ ! -f frontend/.env ] && [ -f frontend/.env.example ]; then
  cp frontend/.env.example frontend/.env
fi

echo "== Node: installing frontend dependencies =="
( cd frontend && npm install )

cat <<'EOF'

Setup complete.

  source .venv/bin/activate
  python scripts/run_pipeline.py --input data/raw/violations.csv --output outputs/
  python scripts/run_backend.py        # in one terminal
  ./scripts/run_frontend.sh            # in another terminal

EOF
