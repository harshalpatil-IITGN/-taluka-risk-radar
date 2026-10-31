"""api/main.py — FastAPI application entry point.

Owner: Mohit.
Implements endpoints per contracts/openapi.yaml.
Standard error shape: never returns a stack trace.
"""

from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from contracts.models import ErrorDetail, ErrorResponse

app = FastAPI(
    title="Taluka Risk Radar API",
    version="0.1.0",
    description="Agentic early-warning system for Maharashtra farm-climate risk.",
)

# CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global error handler (never expose stack traces) ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unhandled exceptions and return the standard error shape."""
    error = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again.",
            retryable=True,
        )
    )
    return JSONResponse(status_code=500, content=error.model_dump())


# --- Health ---

@app.get("/health")
async def health():
    """Liveness check."""
    return {"status": "ok"}


# TODO: Import and include routers for:
# - /sources/status
# - /talukas
# - /risk/map, /risk
# - /prices
# - /agent/run, /agent/runs/{id}/stream, /agent/runs/{id}
# - /portfolio/analyze
# - /telegram/webhook
# - /admin/chaos, /admin/refresh
