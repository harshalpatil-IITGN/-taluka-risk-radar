"""db/repo.py — Database read/write helpers for Taluka Risk Radar.

Owner: Harshal.
All other modules (engine, agent, api) read data through these functions.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

# TODO: Implement database connection setup (Supabase client or asyncpg pool)


# --- Taluka ---

def get_talukas(division: str | None = None, query: str | None = None) -> list[dict[str, Any]]:
    """List/search pilot talukas, optionally filtered by division or search text."""
    raise NotImplementedError


def get_taluka_by_id(taluka_id: int) -> dict[str, Any] | None:
    """Get a single taluka by ID."""
    raise NotImplementedError


# --- Weather ---

def get_weather(taluka_id: int, start: date, end: date) -> list[dict[str, Any]]:
    """Get weather_daily rows for a taluka in a date range."""
    raise NotImplementedError


def upsert_weather(rows: list[dict[str, Any]]) -> int:
    """Idempotent upsert of weather_daily rows. Returns count written."""
    raise NotImplementedError


# --- Climatology ---

def get_climatology(taluka_id: int, window_days: int, month: int) -> dict[str, Any] | None:
    """Get climatology record for a taluka/window/month."""
    raise NotImplementedError


def upsert_climatology(rows: list[dict[str, Any]]) -> int:
    """Upsert climatology rows."""
    raise NotImplementedError


# --- Mandi Prices ---

def get_prices(commodity: str, district: str | None = None, days: int = 14) -> list[dict[str, Any]]:
    """Get recent mandi prices for a commodity, optionally filtered by district."""
    raise NotImplementedError


def upsert_prices(rows: list[dict[str, Any]]) -> int:
    """Idempotent upsert of mandi_price rows."""
    raise NotImplementedError


def get_msp(commodity: str) -> dict[str, Any] | None:
    """Get MSP reference for a commodity."""
    raise NotImplementedError


# --- Risk Score ---

def get_risk_score(taluka_id: int, as_of_date: date | None = None) -> dict[str, Any] | None:
    """Get the latest risk score for a taluka (or for a specific date)."""
    raise NotImplementedError


def get_all_risk_scores(as_of_date: date | None = None) -> list[dict[str, Any]]:
    """Get latest risk scores for all pilot talukas (for the map)."""
    raise NotImplementedError


def upsert_risk_score(row: dict[str, Any]) -> None:
    """Upsert a risk_score row."""
    raise NotImplementedError


# --- Source Health ---

def get_source_health() -> list[dict[str, Any]]:
    """Get all source_health rows."""
    raise NotImplementedError


def write_source_health(
    source: str,
    status: str,
    last_error: str | None = None,
    latency_ms: int | None = None,
    rows_written: int | None = None,
) -> None:
    """Write/update a source_health row after an ingestion run."""
    raise NotImplementedError


# --- Dead Letter ---

def write_dead_letter(source: str, payload: dict, error: str) -> None:
    """Write a failed row to the dead-letter table."""
    raise NotImplementedError


# --- Agent Run ---

def save_agent_run(run: dict[str, Any]) -> None:
    """Save an agent run record."""
    raise NotImplementedError


def get_agent_run(run_id: str) -> dict[str, Any] | None:
    """Get an agent run by ID."""
    raise NotImplementedError


# --- Alerts ---

def save_alert(alert: dict[str, Any]) -> int:
    """Save an alert and return its ID."""
    raise NotImplementedError


# --- Doc Chunks ---

def search_doc_chunks(embedding: list[float], k: int = 5) -> list[dict[str, Any]]:
    """Cosine similarity search on doc_chunk embeddings."""
    raise NotImplementedError


def upsert_doc_chunks(chunks: list[dict[str, Any]]) -> int:
    """Insert doc chunks with embeddings."""
    raise NotImplementedError
