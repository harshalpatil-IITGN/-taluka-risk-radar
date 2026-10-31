"""pipelines/ingest_weather.py — Open-Meteo weather ingestor.

Owner: Harshal.
Ingests forecast + past days -> weather_daily.
Fault tolerance: httpx timeouts, tenacity retries with backoff+jitter, circuit breaker, idempotent upserts.
"""

from __future__ import annotations

# TODO: Implement
# - httpx client with connect=5s, read=20s timeouts
# - tenacity retries (max 4, exponential backoff with jitter, respect 429/Retry-After)
# - per-source circuit breaker (open after 5 consecutive failures, half-open after 10 min)
# - idempotent upserts via db.repo.upsert_weather
# - source_health row per run via db.repo.write_source_health
# - invalid rows go to ingest_dead_letter via db.repo.write_dead_letter
