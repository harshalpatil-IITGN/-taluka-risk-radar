# Model Card — Taluka Stress Index

> Owner: Kunal. Fill in as the engine is built.

## Overview

The Taluka Stress Index is a weighted composite indicator (0–100) that aggregates multiple climate and market stress signals for a taluka.

## Components and Weights

| Component | Weight | Definition |
|---|---|---|
| Seasonal rainfall deficit % | 30 | (cumulative since 1 Jun − normal) / normal |
| Current dry-spell length | 25 | Consecutive days below rainy-day threshold (2.5 mm) |
| SPI (30- and 60-day) | 20 | Gamma-fit on ERA5 climatology, standard-normal transform |
| Soil-moisture anomaly | 15 | Current vs same-period climatology |
| Forecast shortfall (next 7 days) | 10 | Forecast rainfall vs normal for window |

## Levels

| Level | Range |
|---|---|
| LOW | 0–25 |
| WATCH | 25–50 |
| HIGH | 50–75 |
| SEVERE | 75–100 |

> **Note:** Thresholds are heuristic, not calibrated against historical outcomes (except via backtest).

## Triggers

_See `engine/config.py` for configurable thresholds._

## Backtest Results

_To be filled after backtest._

## Known Failure Modes

_To be filled._

## Guardrails

_See `agent/guardrails.py`._
