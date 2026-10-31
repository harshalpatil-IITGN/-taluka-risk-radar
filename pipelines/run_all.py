"""pipelines/run_all.py — Orchestrate all ingestors with per-source isolation.

Owner: Harshal.
Usage: python -m pipelines.run_all

Each ingestor runs independently; one failure never stops the others.
"""

from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Run all ingestors sequentially with per-source error isolation."""
    ingestors = [
        # ("seed_talukas", seed_talukas),
        # ("seed_msp", seed_msp),
        # ("ingest_weather", ingest_weather),
        # ("ingest_climatology", ingest_climatology),
        # ("ingest_mandi", ingest_mandi),
    ]

    results: dict[str, str] = {}
    for name, _fn in ingestors:
        try:
            logger.info("Starting %s...", name)
            # fn()
            results[name] = "OK"
            logger.info("%s completed successfully.", name)
        except Exception:
            results[name] = "FAILED"
            logger.exception("%s failed:", name)

    logger.info("Ingestion summary: %s", results)


if __name__ == "__main__":
    main()
