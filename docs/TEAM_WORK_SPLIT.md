# TEAM WORK SPLIT — Harshal, Kunal, Mohit

> Goal: three people build in parallel, in separate directories, against frozen contracts, so merges are boring.
> Companion files: `01_PROJECT_CONTEXT.md` (spec) and `02_STEP_BY_STEP_CHECKLIST.md` (timeline).

---

## 1. Roles at a glance

| Member | Role | Owns (directories) | One-line mission |
|---|---|---|---|
| **Harshal** | Data & Pipelines | `pipelines/`, `db/`, `contracts/schema.sql`, `docs/data_sources.md` | Get real, clean, fresh data into the database — and never crash when a source does |
| **Kunal** | AI, Engine & Agent | `engine/`, `rag/`, `agent/`, `evals/`, `contracts/models.py`, `docs/model_card.md` | Turn data into a trustworthy risk score and a grounded, self-verifying agent |
| **Mohit** | Platform, API & UI | `api/`, `web/`, `bot/`, `infra/`, `contracts/openapi.yaml`, `README.md`, `docs/demo_script.md`, deck | Make it deployable, demoable and impossible to break in front of judges |

**Default assignment.** The roles are modular. If your strengths differ, swap whole roles (not half-roles) in the first 30 minutes and update `CODEOWNERS`. Whoever is strongest at Python/ML takes Kunal's role; whoever is strongest at React/DevOps takes Mohit's.

---

## 2. Detailed responsibilities and deliverables

### Harshal — Data & Pipelines

**Deliverables**
1. `docs/data_sources.md` after a 90-minute API smoke test (parameters, quotas, sample shapes, known issues)
2. `contracts/schema.sql` + Supabase tables + `db/repo.py` (read/write helpers used by Kunal and Mohit)
3. Ingestors: `ingest_weather.py` (forecast + recent history + soil moisture), `ingest_climatology.py` (ERA5 1991–2020), `ingest_mandi.py` (Agmarknet via data.gov.in), `seed_talukas.py`, `seed_msp.py`, `run_all.py`
4. Fault tolerance on all of them: timeouts, tenacity retries with backoff + jitter, circuit breaker, idempotent upserts, `source_health` rows, dead-letter table
5. Preprocessing: Marathi/English name normalisation (rapidfuzz), price outlier flag, IST timezone, unit checks
6. Scheduler: GitHub Actions cron (every 3–6 h) + manual dispatch; staleness alerts
7. Backtest data: ERA5 replay for 1 Jun–26 Sep 2026; drought-declaration labels with `label_source_url` (P1)
8. Stretch (P2): Sentinel-2 NDVI for 1–3 districts

**Definition of done**
- `python -m pipelines.run_all` succeeds with one source disabled
- Every table row has a source and timestamp; no hardcoded data
- `/sources/status` reflects reality (OK / DEGRADED / DOWN)

**Antigravity starter prompt (paste in Planning mode):**
> Read @docs/PROJECT_CONTEXT.md sections 9, 10 and 11. In `pipelines/` build a fault-tolerant Open-Meteo weather ingestor that writes to `weather_daily` per `contracts/schema.sql`: httpx with timeouts, tenacity retries with exponential backoff and jitter, a per-source circuit breaker, idempotent upserts, a `source_health` row per run, and dead-letter handling for invalid rows. No mock data. Include a unit test that uses a recorded real response from `tests/fixtures_recorded/`. Only edit `pipelines/`, `db/` and `tests/`.

---

### Kunal — AI, Engine & Agent

**Deliverables**
1. `contracts/models.py`: Pydantic models for every tool/API result (includes `source`, `as_of`, `stale`, `error`)
2. `engine/`: seasonal deficit, dry-spell length, SPI (gamma fit), soil-moisture anomaly, forecast shortfall; `stress_index.py` with weight re-normalisation, levels, triggers T1–T4, explanation dict; `config.py` for weights/thresholds
3. `rag/`: ingest official PDFs → chunk → multilingual embeddings → pgvector; retrieval with low-score abstain threshold
4. `agent/`: LangGraph graph (Detect → Retrieve → Plan → Verify → Act, with Recover), typed tools, guardrails, streaming trace events, LLM fallback chain (Gemini → Groq → templated)
5. Outputs: Marathi + English farmer advisory, portfolio digest, evidence report
6. `evals/`: 20-prompt agent eval with automated checks; `backtest.py` with precision/recall/F1/lead time → `evals/results/*.md`
7. `docs/model_card.md`

**Definition of done**
- Verify node demonstrably blocks a draft with a wrong number or missing citation
- Agent finishes (marked `DEGRADED`) with the primary LLM disabled
- Backtest and eval results are committed with honest sample sizes

**Antigravity starter prompt:**
> Read @docs/PROJECT_CONTEXT.md sections 11, 12 and 13. In `engine/` implement the Taluka Stress Index as pure functions over pandas DataFrames, re-normalising weights when a component is missing, with unit tests. Then in `agent/` build the LangGraph graph with Detect, Retrieve, Plan, Verify, Act and Recover nodes using the typed tools in `contracts/models.py`. The Verify node must check that every number in the draft matches tool output and every guidance sentence has a citation. Only edit `engine/`, `rag/`, `agent/`, `evals/` and `contracts/models.py`.

---

### Mohit — Platform, API & UI

**Deliverables**
1. Repo bootstrap (Step 0): skeleton, `CODEOWNERS`, branch protection, `.env.example`, CI (ruff, pytest, build, secret scan)
2. `contracts/openapi.yaml` + FastAPI app implementing every endpoint in Context §14, SSE for agent traces, admin-token middleware, standard error shape (never a stack trace)
3. `web/`: Leaflet map, taluka panel (gauge, components, triggers, 16-day rainfall chart, price vs MSP), agent trace view, portfolio tab, system-health drawer, chaos toggle, loading/empty/error states, mobile layout, Open-Meteo attribution
4. `bot/`: Telegram bot (`/start`, `/risk <taluka>`, alert subscription) via webhook (P1)
5. `infra/`: Dockerfile, docker-compose, deployment to Vercel + HF Space/Render, warm-up ping, env var setup
6. `README.md` with Mermaid architecture diagram, setup steps, data-source table; `docs/demo_script.md`; demo video; pitch deck

**Definition of done**
- Public URL works from a phone on mobile data; cold start handled gracefully
- A fresh clone runs by following the README alone
- Chaos toggle visibly demonstrates degradation without a crash

**Antigravity starter prompt:**
> Read @docs/PROJECT_CONTEXT.md sections 14 and 15 and `contracts/openapi.yaml`. Build the FastAPI app in `api/` implementing the listed endpoints with Pydantic response models from `contracts/models.py`, a standard error shape, an admin-token dependency, and an SSE endpoint that streams `TraceEvent`s from `agent.run_agent`. Read data only through `db/repo.py`. For local UI development only, you may add a mock server behind `MOCK_MODE=true`; CI must fail if it is enabled in a production build. Only edit `api/`, `web/`, `bot/` and `infra/`.

---

## 3. Dependency map and handoff schedule

```
Harshal (data)  ──►  Kunal (engine/agent)  ──►  Mohit (API/UI)
   db/repo.py          engine.compute_risk         /risk, /agent/*
                       agent.run_agent
        ▲                                              │
        └──────────── source_health ◄──────────────────┘ (health UI, chaos toggle)
```

| When | From → To | What is handed over | Unblocks |
|---|---|---|---|
| D1 H3 | Harshal → Kunal | 5 talukas of **real** weather + climatology in DB; `db/repo.py` read functions | Kunal tests the engine on real data |
| D1 H3 | Kunal → Mohit | `RiskResult` shape (already in contracts) | Mohit builds the UI against the contract |
| D1 H7 | Kunal → Mohit | `engine.compute_risk` writing `risk_score` | Gate 1: live marker with real components |
| D1 H8 | Harshal → Kunal | Full ~50-taluka dataset + mandi prices | Kunal's tools and agent skeleton |
| D1 H9 | Kunal → Mohit | `agent.run_agent` streaming `TraceEvent`s (even rough) | SSE + trace UI |
| D2 H1 | Harshal → Kunal | ERA5 replay for backtest; drought labels | Backtest |
| D2 H3 | Mohit → ALL | Chaos toggle + `/admin/chaos` | Everyone tests failure modes |
| D2 H6:30 | ALL | **Feature freeze** | Docs, video, deck |

**Rule of thumb:** if you are waiting on someone for more than 20 minutes, switch to the contract (use recorded real data in a local test) and keep moving.

---

## 4. Conflict-avoidance rules

1. **Directory ownership** is law. You may read anything; you edit only your directories. Need a change elsewhere? Open a GitHub issue or message the owner; the owner makes it (or approves your PR).
2. **Contracts** (`contracts/`) are shared: changes go through a PR, are announced in chat, and must be reviewed by every consumer of that contract.
3. **Single writers:** only Harshal touches migrations/schema; only Mohit touches `README.md`, `docker-compose.yml`, CI workflows and `CODEOWNERS`; only Kunal touches `contracts/models.py` (others request fields).
4. **Small PRs** (< ~300 lines), merged at least daily, rebased on `main` before merging.
5. **Branch names:** `feat/data-…`, `feat/engine-…`, `feat/agent-…`, `feat/api-…`, `feat/web-…`, `fix/…`.
6. **Commit style:** conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
7. **Agent discipline in Antigravity:** always give the agent a directory scope in the prompt; reject diffs that touch files outside it; commit before starting a large agent task so you can revert cleanly; one agent task per directory at a time.
8. **Secrets:** never in git; use `.env` locally and platform secrets in deployment.
9. **Generated data:** never commit generated datasets or large model files; scripts regenerate them. Recorded real fixtures live only in `tests/fixtures_recorded/`.

---

## 5. Review rotation (consumer reviews producer)

| Reviewer | Reviews PRs from | Why |
|---|---|---|
| **Kunal** | Harshal | Kunal consumes Harshal's data and repo functions |
| **Mohit** | Kunal | Mohit consumes the engine/agent through the API |
| **Harshal** | Mohit | Harshal's data is exposed through Mohit's API and health UI |

Review SLA: 30 minutes during working hours. A reviewer who is blocked pings the author; if nobody responds in 30 minutes, merge after a self-review for non-contract changes.

---

## 6. Code-ownership readiness (judging rule)

Every member must be able to explain the whole system. Build it into the schedule:

- **D1 H10:30:** three 10-minute walkthroughs (data flow / engine + agent / API + UI + deploy); the other two each ask 2 questions.
- **Daily 15-minute sync** (start of each half-day): done / doing / blocked, plus one thing each person learned about another module.
- **D2 final drill:** each person answers 5 random questions about the other two modules. Practise answering "where does this number come from?" by tracing a single risk score from API call back to the source response.

**Cheat-sheet each person must be able to say in 60 seconds:**
- *Data:* sources → ingestors (retry/circuit breaker) → raw + cleaned tables → climatology/baselines → `risk_score`.
- *AI:* Stress Index components and weights, triggers, RAG retrieval and abstain threshold, agent graph, Verify checks, Recover chain, backtest result.
- *Platform:* endpoints, SSE trace stream, health/chaos mechanism, deployment topology, how cold starts and failures are handled.

---

## 7. Buddy cover (if someone is blocked, ill or behind)

| Primary | Backup | What the backup can take over |
|---|---|---|
| Harshal | Kunal | Mandi ingestion and preprocessing (Kunal already understands the data shapes) |
| Kunal | Mohit | RAG ingestion scripts and eval harness (Mohit wires them into the API anyway) |
| Mohit | Harshal | Deployment, cron and CI setup (Harshal already runs the scheduler) |

If a P0 item is at risk at a gate, the owner says so **immediately**; the team either swaps tasks or uses the cut list in `02_STEP_BY_STEP_CHECKLIST.md`.

---

## 8. Communication protocol

- One group chat for quick pings; one GitHub Projects board (columns: Backlog / Doing / Review / Done) with every checklist item as an issue tagged `P0/P1/P2` and `H/K/M`.
- Announce in chat before: merging to `main`, changing a contract, rotating keys, deploying to production.
- Use a shared doc `docs/BLOCKERS.md` for anything blocked > 20 minutes.
- Sleep schedule: plan at least 5–6 hours of rest between Day 1 and Day 2; a fresh team beats a tired one during the live demo.

---

## 9. Quick-start commands (after Step 0)

```bash
git clone <repo-url> && cd taluka-risk-radar
cp .env.example .env            # fill in keys from the password manager
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q                        # sanity check
python -m pipelines.run_all      # Harshal's ingest (needs DATABASE_URL, DATA_GOV_IN_API_KEY)
uvicorn api.main:app --reload    # Mohit's API
cd web && npm install && npm run dev
```

Branch workflow:
```bash
git checkout -b feat/data-weather-ingestor
# work, commit often
git fetch origin && git rebase origin/main
git push -u origin feat/data-weather-ingestor   # open PR, request the reviewer from section 5
```
