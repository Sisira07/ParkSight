#!/usr/bin/env python3
"""scripts/run_backend.py — starts the FastAPI backend with uvicorn."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    return subprocess.call(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--reload", "--port", "8000"],
        cwd=str(REPO_ROOT),
    )


if __name__ == "__main__":
    sys.exit(main())
