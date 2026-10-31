"""tests/test_contracts.py — Sanity tests for shared contract models.

Verifies that Pydantic models can be instantiated and serialised.
"""

from datetime import date, datetime

from contracts.models import (
    AgentRunRequest,
    ComponentDetail,
    DataFreshness,
    ErrorDetail,
    ErrorResponse,
    RiskLevel,
    RiskResult,
    SourceHealthEntry,
    SourceStatus,
    TriggerDetail,
)


def test_risk_result_instantiation():
    """RiskResult can be created with all required fields."""
    result = RiskResult(
        taluka_id=1,
        taluka_name="Jalna",
        as_of_date=date(2026, 10, 31),
        stress_index=62.5,
        level=RiskLevel.HIGH,
        components=[
            ComponentDetail(
                name="seasonal_deficit",
                value=32.1,
                weight=30,
                contribution=19.3,
                description="Seasonal rainfall deficit of 32.1%",
            )
        ],
        triggers=[
            TriggerDetail(
                name="T1_DROUGHT_STRESS",
                fired=True,
                threshold="deficit > 25% AND dry spell >= 21 days",
                actual="deficit=32.1%, dry_spell=24 days",
                description="Drought stress trigger fired",
            )
        ],
        data_freshness=[DataFreshness(source="open-meteo", as_of=datetime(2026, 10, 31, 10, 0), stale=False)],
    )
    assert result.stress_index == 62.5
    assert result.level == RiskLevel.HIGH
    assert len(result.components) == 1
    assert result.error is None


def test_error_response():
    """ErrorResponse serialises to the standard shape."""
    err = ErrorResponse(error=ErrorDetail(code="NOT_FOUND", message="Taluka not found", retryable=False))
    data = err.model_dump()
    assert data["error"]["code"] == "NOT_FOUND"
    assert data["error"]["retryable"] is False


def test_agent_run_request():
    """AgentRunRequest with defaults."""
    req = AgentRunRequest(taluka_id=5)
    assert req.audience == "farmer"
    assert req.language == "en"


def test_source_health_entry():
    """SourceHealthEntry with status enum."""
    entry = SourceHealthEntry(source="open-meteo", status=SourceStatus.OK)
    assert entry.stale is False
