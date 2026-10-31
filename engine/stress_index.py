"""engine/stress_index.py — Taluka Stress Index computation.

Owner: Kunal.
Pure functions over pandas DataFrames. Re-normalises weights when a component is missing.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from contracts.models import RiskResult

# TODO: Implement
# - compute_risk(taluka_id, as_of=None) -> RiskResult
# - Each component as a pure function: seasonal_deficit, dry_spell_length, spi, soil_moisture_anomaly, forecast_shortfall
# - Weight re-normalisation when components are missing (lower confidence)
# - Level mapping from stress_index to LOW/WATCH/HIGH/SEVERE
# - Trigger evaluation T1-T4
# - Per-component explanation dict


def compute_risk(taluka_id: int, as_of: date | None = None) -> RiskResult:
    """Compute the Taluka Stress Index and return a full RiskResult."""
    raise NotImplementedError
