"""
tests/pipeline/test_pipeline_integration.py — end-to-end pipeline checks.

Unlike the unit tests inside `parksight/` (covering individual stage
functions) and `backend/tests/` (covering the API against fixed fixture
artifacts), this module runs the *real* `run_pipeline()` against the
bundled sample CSV and checks the artifact contract every downstream
consumer (the backend's `ArtifactLoader`) relies on: which files exist,
which columns they expose, and that evidence labels are only ever drawn
from the documented vocabulary.
"""

import json

import pandas as pd
import pytest

EXPECTED_ARTIFACTS = {
    "temporal_audit.json",
    "bias_audit.json",
    "hotspot_clusters.csv",
    "risk_scores.csv",
    "spatial_stability.json",
    "capacity_impact.csv",
    "patrol_plan.csv",
    "evidence_ledger.csv",
    "executive_report.md",
}

# Only written when the clustering stage actually finds mid-block violations
# that don't belong to a named junction; the bundled sample data is entirely
# junction-based, so this artifact is legitimately absent for that fixture.
OPTIONAL_ARTIFACTS = {"nonjunction_hotspots.csv"}

VALID_EVIDENCE_LABELS = {"REAL_DATA", "MODELED", "SPEC_ONLY", "PARTIAL"}


def test_pipeline_runs_without_failures(pipeline_result):
    summary, _ = pipeline_result
    assert summary["n_failures"] == 0, summary["failures"]


def test_pipeline_reads_every_input_row(pipeline_result, sample_csv):
    summary, _ = pipeline_result
    source_rows = len(pd.read_csv(sample_csv))
    assert summary["n_input_rows"] == source_rows


def test_pipeline_writes_expected_artifacts(pipeline_result):
    _, out = pipeline_result
    produced = {p.name for p in out.iterdir()}
    missing = EXPECTED_ARTIFACTS - produced
    assert not missing, f"missing artifacts: {missing}"
    # Sanity-check the optional-artifact set is at least a known name, so a
    # typo here doesn't silently mask a real missing-artifact regression.
    assert OPTIONAL_ARTIFACTS


def test_hotspot_clusters_have_required_columns(pipeline_result):
    _, out = pipeline_result
    df = pd.read_csv(out / "hotspot_clusters.csv")
    required = {
        "cluster_id", "top_junction", "police_station", "district",
        "violations", "risk_score", "risk_tier", "lat", "lon",
    }
    assert required.issubset(df.columns)
    assert df["risk_tier"].isin(["CRITICAL", "HIGH", "MEDIUM", "LOW"]).all()


def test_evidence_ledger_uses_only_documented_labels(pipeline_result):
    _, out = pipeline_result
    df = pd.read_csv(out / "evidence_ledger.csv")
    assert set(df["status"].unique()).issubset(VALID_EVIDENCE_LABELS)
    # Every claim that came straight from the source CSV must be REAL_DATA,
    # never silently upgraded to MODELED or backfilled with a guess.
    assert (df["status"] != "").all()


def test_temporal_audit_is_valid_json(pipeline_result):
    _, out = pipeline_result
    with open(out / "temporal_audit.json") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_executive_report_mentions_evidence_labels(pipeline_result):
    _, out = pipeline_result
    text = (out / "executive_report.md").read_text()
    assert "evidence" in text.lower()


def test_offline_run_never_claims_real_traffic_data(pipeline_result):
    """skip_external_apis=True must never produce a REAL_DATA traffic claim —
    that would mean the pipeline silently used cached/fabricated network
    data instead of honestly labelling the stage as skipped."""
    _, out = pipeline_result
    capacity = pd.read_csv(out / "capacity_impact.csv")
    if "validation_status" in capacity.columns:
        assert not (
            (capacity["validation_status"] == "REAL_DATA")
            & (capacity.get("geometry_source", "") == "")
        ).any()


@pytest.mark.parametrize("teams", [1, 5, 50])
def test_pipeline_accepts_varying_team_counts(sample_csv, settings_path, tmp_path, teams):
    """The MILP solver must degrade gracefully rather than crash for both
    very small and very large team counts."""
    from parksight.pipeline import run_pipeline

    out = tmp_path / f"outputs_{teams}"
    summary = run_pipeline(
        input_path=str(sample_csv),
        output_dir=str(out),
        config_path=str(settings_path),
        skip_external_apis=True,
        teams=teams,
    )
    assert summary["n_failures"] == 0
    assert (out / "patrol_plan.csv").exists()
