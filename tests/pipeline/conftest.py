"""
tests/pipeline/conftest.py — fixtures for full pipeline integration tests.

These tests exercise `parksight.pipeline.run_pipeline` end-to-end against
the bundled sample dataset (`data/samples/sample_violations.csv`), the same
fixture used to validate the repo during the rebuild. They run fully offline
(`skip_external_apis=True`) so they need no network access and no API keys.
"""

from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def sample_csv() -> Path:
    path = _PROJECT_ROOT / "data" / "samples" / "sample_violations.csv"
    if not path.exists():
        pytest.skip(
            f"{path} not found — generate it first (see docs/development.md) "
            "or run scripts/run_pipeline.py once to populate data/samples/."
        )
    return path


@pytest.fixture(scope="session")
def settings_path() -> Path:
    return _PROJECT_ROOT / "config" / "settings.yaml"


@pytest.fixture()
def output_dir(tmp_path: Path) -> Path:
    out = tmp_path / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    return out


@pytest.fixture(scope="session")
def pipeline_result(sample_csv, settings_path, tmp_path_factory):
    """Run the full pipeline once per test session and share the result.

    Running once and sharing keeps the suite fast — DBSCAN, the MILP solver,
    and report generation are not free, and every test in this module only
    reads the resulting artifacts rather than mutating them.
    """
    from parksight.pipeline import run_pipeline

    out = tmp_path_factory.mktemp("pipeline_outputs")
    summary = run_pipeline(
        input_path=str(sample_csv),
        output_dir=str(out),
        config_path=str(settings_path),
        skip_external_apis=True,
    )
    return summary, out
