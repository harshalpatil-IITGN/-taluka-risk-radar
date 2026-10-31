"""engine/config.py — Configurable weights and thresholds for the Stress Index.

Owner: Kunal.
All thresholds are heuristic and documented as such in docs/model_card.md.
"""

from __future__ import annotations

# Component weights (must sum to 100 when all present)
WEIGHTS = {
    "seasonal_deficit": 30,
    "dry_spell_length": 25,
    "spi": 20,
    "soil_moisture_anomaly": 15,
    "forecast_shortfall": 10,
    # Stretch: "ndvi_anomaly": re-normalise when present
}

# Risk level thresholds
LEVEL_THRESHOLDS = {
    "LOW": (0, 25),
    "WATCH": (25, 50),
    "HIGH": (50, 75),
    "SEVERE": (75, 100),
}

# Trigger thresholds (configurable, reported criterion)
TRIGGERS = {
    "T1_DROUGHT_STRESS": {
        "seasonal_deficit_pct": 25,   # > 25%
        "dry_spell_days": 21,         # >= 21 days
    },
    "T2_DRY_SPELL_CRITICAL": {
        "dry_spell_days": 14,         # >= 14 days during sensitive window
    },
    "T3_FORECAST_DRY": {
        "forecast_pct_of_normal": 20, # < 20% of normal
    },
    "T4_UNSEASONAL_RAIN": {
        "precip_mm_threshold": 100,   # > X mm in 24-48h outside normal season
    },
}

# Rainy-day threshold (mm)
RAINY_DAY_THRESHOLD_MM = 2.5

# Staleness thresholds (hours)
STALENESS = {
    "weather": 12,
    "prices": 48,
}
