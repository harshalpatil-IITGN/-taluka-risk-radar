"""agent/tools.py — Typed tools for the LangGraph agent.

Owner: Kunal.
Each tool wraps a function from db/repo.py or engine/ and returns typed models from contracts/models.py.
"""

from __future__ import annotations

# TODO: Implement each tool function:
# - resolve_place(text) -> list[TalukaMatch]
# - get_risk(taluka_id, as_of=None) -> RiskResult
# - get_forecast(taluka_id, days=7) -> ForecastResult
# - get_prices(commodity, district=None, days=14) -> PriceResult
# - search_docs(query, k=5, lang=None) -> list[DocHit]
# - send_alert(taluka_id, level, message, channel, language) -> AlertResult
# - render_evidence_report(taluka_id, as_of) -> ReportResult
