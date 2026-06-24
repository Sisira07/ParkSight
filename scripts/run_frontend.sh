#!/usr/bin/env bash
# scripts/run_frontend.sh — installs (if needed) and starts the Vite dev server.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT/frontend"

if [ ! -d node_modules ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi

npm run dev
