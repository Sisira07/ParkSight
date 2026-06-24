#!/usr/bin/env python3
"""
scripts/run_pipeline.py — convenience wrapper around `python -m parksight.cli`.

Exists so the top-level README can show one canonical command per workflow
(pipeline / backend / frontend) without assuming the reader already knows
the package's module path.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from parksight.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
