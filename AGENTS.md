# AGENTS.md — Taluka Risk Radar

Read `@docs/PROJECT_CONTEXT.md` before planning. It is the source of truth.

## Project in one line
Agentic early-warning system for Maharashtra farm-climate risk: live data -> Taluka Stress Index -> LangGraph agent (RAG + verify) -> API/UI/Telegram.

## Hard rules
1. NO dummy/hardcoded/mock data in app code. Only live APIs, the live DB, or official open datasets loaded by seed scripts with source_url. Mocks only in local dev; never when MOCK_MODE=true in prod.
2. Only edit files inside the directory you were asked to work in. Shared contracts live in /contracts and change only via PR.
3. Every tool/API result carries: source, as_of, stale, error.
4. All network calls: timeout + tenacity retry w/ backoff + circuit breaker; never crash on a failed source.
5. Python 3.11, type hints, Pydantic v2, ruff+black. TypeScript strict. Small functions, docstrings on public functions.
6. Never commit secrets. Read config from env (.env.example lists keys).
7. No pesticide/fertiliser doses, no buy/sell advice. Guidance must cite a retrieved document.

## Commands
- API: `uvicorn api.main:app --reload`
- Tests: `pytest -q`
- Lint: `ruff check . && black --check .`
- Ingest: `python -m pipelines.run_all`
- Web: `cd web && npm run dev`

## Ownership (see docs/TEAM_WORK_SPLIT.md)
pipelines/ db/ = Harshal | engine/ rag/ agent/ evals/ = Kunal | api/ web/ bot/ infra/ = Mohit
