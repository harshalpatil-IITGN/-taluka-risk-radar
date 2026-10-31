"""contracts/models.py — Shared Pydantic models for Taluka Risk Radar.

Owner: Kunal. Changes via PR only; announce in chat.
Every result model carries: source, as_of, stale, error.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

# --- Enums ---


class RiskLevel(str, Enum):
    LOW = "LOW"
    WATCH = "WATCH"
    HIGH = "HIGH"
    SEVERE = "SEVERE"


class SourceStatus(str, Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    DISABLED_CHAOS = "DISABLED_CHAOS"


class AgentRunStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


# --- Core Models ---


class Taluka(BaseModel):
    id: int
    name_en: str
    name_mr: str | None = None
    district: str
    division: str
    lat: float
    lon: float
    lgd_code: str | None = None
    pilot: bool = True
    drought_declared_2026: bool | None = None


class TalukaMatch(BaseModel):
    """Fuzzy match result for place resolution."""

    taluka: Taluka
    score: float
    matched_name: str


# --- Risk & Engine ---


class ComponentDetail(BaseModel):
    name: str
    value: float
    weight: float
    contribution: float
    description: str


class TriggerDetail(BaseModel):
    name: str
    fired: bool
    threshold: str
    actual: str
    description: str


class DataFreshness(BaseModel):
    source: str
    as_of: datetime | None = None
    stale: bool = False


class RiskResult(BaseModel):
    taluka_id: int
    taluka_name: str
    as_of_date: date
    stress_index: float = Field(ge=0, le=100)
    level: RiskLevel
    components: list[ComponentDetail]
    triggers: list[TriggerDetail]
    data_freshness: list[DataFreshness]
    confidence: float | None = None
    source: str = "engine"
    as_of: datetime | None = None
    stale: bool = False
    error: str | None = None


# --- Forecast ---


class DailyForecast(BaseModel):
    date: date
    precip_mm: float | None = None
    tmax_c: float | None = None
    tmin_c: float | None = None
    et0_mm: float | None = None
    soil_moisture: float | None = None


class ForecastResult(BaseModel):
    taluka_id: int
    taluka_name: str
    days: list[DailyForecast]
    source: str = "open-meteo"
    as_of: datetime | None = None
    stale: bool = False
    error: str | None = None


# --- Prices ---


class PriceEntry(BaseModel):
    market: str
    commodity: str
    variety: str | None = None
    arrival_date: date
    modal_price: float | None = None
    min_price: float | None = None
    max_price: float | None = None


class PriceResult(BaseModel):
    commodity: str
    district: str | None = None
    entries: list[PriceEntry]
    msp: float | None = None
    trend: str | None = None  # e.g. "rising", "falling", "stable"
    source: str = "agmarknet"
    as_of: datetime | None = None
    stale: bool = False
    error: str | None = None


# --- RAG ---


class DocHit(BaseModel):
    doc_id: str
    title: str
    source_url: str | None = None
    page: int | None = None
    text: str
    score: float
    lang: str | None = None


# --- Agent ---


class TraceEvent(BaseModel):
    """Single event in an agent run's trace stream (SSE)."""

    node: str
    event_type: str  # e.g. "enter", "tool_call", "tool_result", "verify", "output", "error"
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime | None = None


class AgentRunRequest(BaseModel):
    taluka_id: int | None = None
    place_text: str | None = None
    audience: str = "farmer"  # farmer | portfolio | evidence
    language: str = "en"  # en | mr | hi


class AgentResult(BaseModel):
    run_id: UUID
    status: AgentRunStatus
    taluka_id: int | None = None
    audience: str | None = None
    language: str | None = None
    output: dict[str, Any] | None = None
    trace: list[TraceEvent] = Field(default_factory=list)
    error: str | None = None
    source: str = "agent"
    as_of: datetime | None = None
    stale: bool = False


# --- Source Health ---


class SourceHealthEntry(BaseModel):
    source: str
    status: SourceStatus
    last_attempt_at: datetime | None = None
    last_success_at: datetime | None = None
    last_error: str | None = None
    latency_ms: int | None = None
    rows_written: int | None = None
    stale: bool = False


# --- Alert ---


class AlertResult(BaseModel):
    alert_id: int
    taluka_id: int
    level: str
    channel: str
    delivered: bool = False
    source: str = "alert"
    as_of: datetime | None = None
    stale: bool = False
    error: str | None = None


# --- Evidence Report ---


class ReportResult(BaseModel):
    taluka_id: int
    as_of_date: date
    content: str  # Markdown/HTML
    format: str = "markdown"
    source: str = "report"
    as_of: datetime | None = None
    stale: bool = False
    error: str | None = None


# --- API Error Shape ---


class ErrorDetail(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ErrorResponse(BaseModel):
    error: ErrorDetail
