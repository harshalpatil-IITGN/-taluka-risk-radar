# STEP-BY-STEP CHECKLIST — 2-Day Build Plan

> Companion to `01_PROJECT_CONTEXT.md` (what and why) and `03_TEAM_WORK_SPLIT.md` (who).
> Tags: **[H]** Harshal (Data & Pipelines) · **[K]** Kunal (AI, Engine & Agent) · **[M]** Mohit (Platform, API & UI) · **[ALL]** everyone.
> Priorities: **P0** must ship · **P1** if P0 is green · **P2** stretch only.
> Time is given as working-hour offsets, assuming ~12 focused hours per day. If your window is different, keep the **order and gates**, scale the blocks.

---

## How to read the plan

- Work in **vertical slices**: one taluka end-to-end first (data → risk → API → map → agent), then widen to ~50 talukas. A thin working demo on Day 1 evening beats five half-built layers.
- **Gates** are hard checkpoints. If a gate is red, stop adding features and fix it.
- If you fall behind, use the **Cut List** at the bottom — cut from the bottom up, never cut robustness (30 points) or source attribution.

---

## STEP 0 — Kickoff, accounts and Antigravity setup (Day 1, H0:00–1:30) [ALL]

### 0.1 Accounts and keys (split the work, 20 min)
- [ ] [H] data.gov.in account → **API key**; Supabase project (Postgres + pgvector enabled)
- [ ] [K] Google AI Studio → **Gemini API key**; Groq account → **Groq key**
- [ ] [M] GitHub repo (public), Vercel, Hugging Face (or Render), Telegram **BotFather** token
- [ ] [ALL] Store secrets in a shared password manager. Nothing secret in chat or in the repo.

### 0.2 Repo and Antigravity
- [ ] [M] Create repo `taluka-risk-radar`; add the three `.md` files under `docs/` (rename `01_…` → `PROJECT_CONTEXT.md`, etc.)
- [ ] [M] Create the folder skeleton from Context §8.2; add `.gitignore`, `.env.example`, `README.md` stub, `CODEOWNERS`
- [ ] [M] Protect `main` (PRs required, 1 review); invite Harshal and Kunal
- [ ] [ALL] Clone, open the folder as a workspace in Antigravity, sign in, update the IDE to the latest version
- [ ] [ALL] Add `AGENTS.md` at the repo root (snippet below). Start a **fresh** agent task afterwards so rules reload
- [ ] [ALL] Habit: use **Planning mode** for multi-step tasks, `@docs/PROJECT_CONTEXT.md` for context, and review every diff before accepting

**`AGENTS.md` snippet (keep it short; rule files have a size limit):**

```markdown
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
```

### 0.3 Problem lock (20 min) [ALL]
- [ ] Read Context §2 (rules) and §6 (scope). Agree on P0/P1/P2.
- [ ] Agree on the one-sentence problem and demo persona (FPO manager, Jalna/Yavatmal).
- [ ] Pick the pilot list of ~50 talukas (Marathwada, Vidarbha, north Maharashtra + a few control talukas).

---

## STEP 1 — Freeze the three contracts (Day 1, H1:30–3:00) [ALL, led by H + M]

Everyone codes against these; this is what makes parallel work conflict-free.

- [ ] [H] Commit `contracts/schema.sql` from Context §10; create it in Supabase
- [ ] [M] Commit `contracts/openapi.yaml` from Context §14 (all endpoints, request/response shapes, error shape)
- [ ] [K] Commit `contracts/models.py` — Pydantic models: `Taluka`, `RiskResult`, `ForecastResult`, `PriceResult`, `DocHit`, `TraceEvent`, `AgentRunRequest`, `AgentResult`, `SourceStatus` (each with `source`, `as_of`, `stale`, `error`)
- [ ] [K] Define `engine.compute_risk(taluka_id, as_of) -> RiskResult` and `agent.run_agent(req) -> AsyncIterator[TraceEvent]` as signatures (empty bodies are fine)
- [ ] [H] Define `db/repo.py` function signatures: `get_weather(taluka_id, start, end)`, `get_climatology(...)`, `get_prices(...)`, `upsert_*`, `write_source_health(...)`
- [ ] [ALL] 10-minute walkthrough of the three contracts. **Contract changes after this need an announcement in chat + PR.**

**GATE 0:** contracts merged to `main`; every member can run the repo locally.

---

## STEP 2 — Vertical slice: one taluka end-to-end (Day 1, H3:00–7:00)

### 2.1 Data (Harshal)
- [ ] [H] **API smoke test** (first 90 min): call Open-Meteo forecast, archive, geocoding; data.gov.in Agmarknet resource; record exact parameter names, quotas and sample response shapes in `docs/data_sources.md`
- [ ] [H] Seed `taluka` for 5 test talukas (geocode HQ names; store `name_mr`, division); script in `pipelines/seed_talukas.py`
- [ ] [H] `pipelines/ingest_weather.py`: forecast + past days → `weather_daily` (daily precip, Tmax/Tmin, ET0, soil moisture); retries, backoff, timeout, circuit breaker, upsert, `source_health` row
- [ ] [H] `pipelines/ingest_climatology.py`: ERA5 1991–2020 for those 5 talukas → `climatology` (gamma params + cumulative normals)
- [ ] [H] Raw payload logging + dead-letter table wired in

### 2.2 Engine (Kunal)
- [ ] [K] Pure functions in `engine/` that take DataFrames (so they are testable without the DB): `seasonal_deficit`, `dry_spell_length`, `spi`, `soil_moisture_anomaly`, `forecast_shortfall`
- [ ] [K] `engine/stress_index.py`: weighted index with **weight re-normalisation** on missing components, level mapping, trigger rules T1–T4, per-component explanation dict
- [ ] [K] Unit tests using **recorded real responses** pulled once by Harshal's ingestor (`tests/fixtures_recorded/`, labelled)
- [ ] [K] Wire `compute_risk` to Harshal's `db/repo.py`; write `risk_score` rows

### 2.3 Platform (Mohit)
- [ ] [M] FastAPI skeleton: `/health`, `/sources/status`, `/talukas`, `/risk/map`, `/risk` reading the DB (with a local mock server **for UI development only**)
- [ ] [M] React + Vite + react-leaflet app: map with markers, level colours, taluka panel placeholder, footer attribution "Weather data by Open-Meteo.com"
- [ ] [M] Dockerfile for API; `docker-compose.yml` for local dev; GitHub Actions: ruff + pytest

**GATE 1 (Day 1 ~H7):** for 5 talukas, a **live** marker on the live map shows a real stress level with real components. If this isn't green, do not widen scope.

---

## STEP 3 — Widen to ~50 talukas, add prices, RAG, agent skeleton (Day 1, H7:00–10:30)

### Data (Harshal)
- [ ] [H] Seed all ~50 pilot talukas (+ `division`, `name_mr`); batch weather calls (check batching support); respect rate limits
- [ ] [H] Climatology for all pilot talukas (cache; run once, resumable)
- [ ] [H] `pipelines/ingest_mandi.py`: Agmarknet for Maharashtra, 5 commodities (soybean, cotton, tur, gram, onion); pagination, filters, retries; stale handling; dedupe on unique key
- [ ] [H] `pipelines/seed_msp.py` with `source_url`; `pipelines/run_all.py` orchestrating all ingestors with per-source isolation (one failure never stops the others)
- [ ] [H] Preprocessing: Marathi/English name normalisation (rapidfuzz), unit checks, price outlier flag (median-based), timezone IST
- [ ] [H] Find and seed the **drought-declaration list** (`taluka.drought_declared_2026`, `label_source_url`) — P1, timebox 60 min, fallback in Context §9

### Brain (Kunal)
- [ ] [K] `rag/ingest.py`: download the official PDFs (Drought Manual, 3–5 CRIDA DACPs, one SAU advisory set, PMFBY guidelines) → chunk → embed (`multilingual-e5-small`) → `doc_chunk`
- [ ] [K] `rag/retrieve.py`: top-k with scores + low-score abstain threshold; returns `DocHit` with title/url/page
- [ ] [K] `agent/tools.py`: wrap `get_risk`, `get_forecast`, `get_prices`, `search_docs`, `resolve_place` with typed I/O + error fields
- [ ] [K] `agent/graph.py`: LangGraph skeleton (Detect → Retrieve → Plan → Verify → Act, with Recover edge) running on one taluka with the primary LLM and **streaming trace events**

### Platform (Mohit)
- [ ] [M] Endpoints `/prices`, `/agent/run`, `/agent/runs/{id}/stream` (SSE), `/agent/runs/{id}`; admin token middleware
- [ ] [M] UI: taluka detail panel (gauge, component bars, triggers, 16-day rainfall chart, price vs MSP), system-health drawer, loading/empty/error states
- [ ] [M] Deploy **v0** of API (HF Space/Render) and web (Vercel) now — find hosting problems on Day 1, not Day 2

---

## STEP 4 — Integration #1, knowledge transfer, GATE 2 (Day 1, H10:30–12:00) [ALL]

- [ ] [ALL] Merge everything into `main`; fix conflicts together (should be few thanks to directory ownership)
- [ ] [ALL] Run the full flow on the **deployed** URLs, not just localhost
- [ ] [ALL] 3 × 10-minute walkthroughs: Harshal explains data flow, Kunal explains engine + agent, Mohit explains API/UI/deploy. Others ask 2 questions each (this is the code-ownership rule in action)
- [ ] [ALL] Write tomorrow's top-5 list in `docs/day2_plan.md`

**GATE 2 (end of Day 1):**
- [ ] ~50 talukas have live risk scores on the deployed map
- [ ] Mandi prices load with MSP comparison and stale flag
- [ ] Agent can run on one taluka and stream a trace (even if the language quality is rough)
- [ ] Source-health panel shows real statuses
- [ ] No secrets in git history (run a scan now)

---

## STEP 5 — Day 2 morning: agent depth, backtest, Telegram (Day 2, H0:00–4:00)

### Agent (Kunal) — P0
- [ ] [K] **Verify node:** regex/number extraction from the draft; each number must match tool output (tolerance rules); each guidance sentence must have a `[title, p.X]` citation; banned-content checks; on failure, one retry with error list, then Recover
- [ ] [K] **Recover node:** retry → secondary LLM (Groq) → templated output from computed numbers; run marked `DEGRADED` with reason
- [ ] [K] Outputs: Marathi + English farmer advisory (≤120 words, ≤3 actions); portfolio digest; evidence report (Markdown/HTML)
- [ ] [K] Guardrails: refusal for off-topic, prompt-injection resistance (tool/doc text is data), stale-data first-line disclaimer
- [ ] [K] Cache advisories per (taluka, date, language) to save LLM quota
- [ ] [K] `evals/agent_evals.py`: the 20 scripted prompts + automated checks → `evals/results/agent_evals.md`

### Backtest (Kunal + Harshal) — P1 (high value for the accuracy pillar)
- [ ] [H] ERA5 replay data for 1 Jun–26 Sep 2026 for pilot talukas (resumable job)
- [ ] [K] `evals/backtest.py`: precision, recall, F1, lead time; threshold tuning on a subset, report on the held-out subset; honest sample size
- [ ] [K] Commit `evals/results/backtest.md`; give Mohit the 3 headline numbers for the deck

### Platform (Mohit)
- [ ] [M] UI: agent trace view (nodes, tool calls, verify pass/fail, citations), final Marathi + English message, copy button
- [ ] [M] **Chaos toggle** (admin-only) + `/admin/chaos`; UI shows `DISABLED_CHAOS` / stale / degraded states clearly
- [ ] [M] **Telegram bot** (P1): `/start`, `/risk <taluka>`, subscription to alerts; webhook into FastAPI with secret token
- [ ] [M] Portfolio tab (P1): paste list → `/portfolio/analyze` → ranked table

### Data (Harshal)
- [ ] [H] GitHub Actions cron for ingestion (every 3–6 h) + manual `workflow_dispatch`; health alert if no new data for X hours
- [ ] [H] Data quality dashboard queries (rows per source, freshness, dead-letter counts) exposed through `/sources/status`
- [ ] [H] **Stretch (P2) only if everything above is green:** Sentinel-2 NDVI for 1–3 districts

---

## STEP 6 — Robustness and edge-case testing (Day 2, H4:00–6:30) [ALL]

Run each test on the **deployed** system and tick it off:

- [ ] Disable weather via chaos toggle → map still loads, stale badge shows, agent answer says data is stale
- [ ] Disable prices → price panel degrades gracefully; advisory omits price info and says so
- [ ] Kill LLM key / simulate 429 → secondary model → templated fallback
- [ ] Marathi place name; typo ("Jlana"); ambiguous place (two matches → user chooses); place outside Maharashtra → polite message
- [ ] Off-topic question ("who will win the election?") → refusal; injection text inside a place name → ignored
- [ ] Empty data for a taluka (new/unseeded) → clear message, no crash
- [ ] Cold-start: first request after idle → UI shows "waking up", retries, succeeds
- [ ] 5 users at once (open 5 tabs, run the agent) → no crashes, SSE streams isolated
- [ ] API errors never expose stack traces; all errors follow the standard shape
- [ ] Lighthouse/mobile width sanity check on the map page

**GATE 3 (Day 2 ~H6:30): FEATURE FREEZE.** After this: bug fixes, docs, video, deck only.

---

## STEP 7 — Deployment hardening (Day 2, H6:30–7:30) [M leads, H + K support]

- [ ] [M] Final deploy of web + API from `main`; environment variables set; CORS locked to the web origin
- [ ] [H] DB: indexes on `weather_daily(taluka_id, date)`, `risk_score(as_of_date)`, `mandi_price(commodity, arrival_date)`; connection pooling; confirm free-tier limits not exceeded
- [ ] [K] Pre-warm LLM caches for demo talukas (3 talukas × 2 languages)
- [ ] [M] Add warm-up ping (cron or external uptime pinger) to avoid cold starts; confirm CI green
- [ ] [ALL] Re-run the Step 6 smoke tests on the final URLs
- [ ] [ALL] Re-check licence/attribution: Open-Meteo attribution visible in UI; data-source table in README lists licences

---

## STEP 8 — Documentation (Day 2, H7:30–9:30)

- [ ] [M] `README.md`: problem, solution, screenshots/GIF, **Mermaid architecture diagram** (copy from Context §8), setup (env, DB, ingest, run API, run web), deploy notes, data-source table with licences and limits, limitations, roadmap
- [ ] [H] `docs/data_sources.md`: endpoints, params, quotas, fallbacks, known issues
- [ ] [K] `docs/model_card.md`: stress-index definition, weights, thresholds (marked heuristic), backtest results, known failure modes, guardrails
- [ ] [M] `docs/demo_script.md` (see script below)
- [ ] [ALL] Add `LICENSE`, `.env.example` up to date, clean dead code and TODOs, remove any hardcoded sample data accidentally left in the app code
- [ ] [ALL] Fresh-clone test: on a clean machine/container, follow the README and get the app running

---

## STEP 9 — Demo video and pitch deck (Day 2, H9:30–11:00)

### Demo video (2–3 min, live, no cuts that hide failures)
Suggested script (≈150 s):
1. **0:00–0:15** Problem: 2026 drought, 265/358 tehsils; institutions need taluka-level early warning.
2. **0:15–0:40** Live map: filter Marathwada; open a HIGH-stress taluka; show components, triggers fired, 16-day outlook.
3. **0:40–1:20** Click "Generate advisory": show the live **agent trace** — tool calls, RAG citations, Verify pass; Marathi + English message.
4. **1:20–1:45** Portfolio paste (or Telegram alert arriving on a phone).
5. **1:45–2:10** **Chaos toggle:** disable weather source → stale badge → agent still answers, flagged degraded. Then a messy input (Marathi typo / unknown place).
6. **2:10–2:30** Backtest headline numbers + business model + roadmap (MahaVISTAAR/Agristack integration).

- [ ] [M] Record with Loom/OBS; check audio; upload; set link to "anyone with link"
- [ ] [ALL] Rehearse twice before recording; record a **fallback** take in case the live system stalls during judging

### Pitch deck (5–7 slides; follow the recommended structure)
1. Title & team (Harshal, Kunal, Mohit) + one-line USP
2. Problem & context (verified 2026 drought facts; buffer gap between states)
3. Solution & key features (map, agent, advisory, evidence report, Telegram)
4. Technical architecture & innovation (diagram, stress index, RAG + Verify loop, fault tolerance)
5. Results & robustness (backtest numbers, evals, chaos demo screenshot)
6. Customers & business model (FPOs, cooperative banks, insurers; pilot path; licensing plan)
7. Roadmap & live demo summary (NDVI, Bhashini voice, OpenAgriNet integration, other states)

- [ ] [M] Build in Google Slides/Canva; export PDF; link public
- [ ] [K] + [H] Review slides for claim accuracy against Context §4.2 (no unsourced claims)

---

## STEP 10 — Submission and judging prep (Day 2, H11:00–12:00+)

### Submission form (6 items)
- [ ] Problem statement text (Context §4.1)
- [ ] Solution description + technical architecture (Context §1, §8)
- [ ] Prototype URL — open it in a private window and test
- [ ] Demo video link — open it logged out
- [ ] GitHub URL — public, README renders, diagram visible, no secrets
- [ ] Deck link — public view access
- [ ] Submit **at least 2 hours before the deadline**; screenshot the confirmation

### Judging prep
- [ ] [ALL] Q&A drill: each person answers 5 random questions about the other two modules (data flow, why these thresholds, how Verify works, how deployment works)
- [ ] [ALL] Pre-warm the app 10 minutes before the slot; have the recorded fallback ready
- [ ] [ALL] Decide who drives the demo (suggest Mohit), who explains the AI (Kunal), who explains data and robustness (Harshal) — but everyone must be able to answer anything
- [ ] [ALL] Prepare answers for: "Why not just use MahaVISTAAR?", "Is any data hardcoded?", "How accurate is it?", "How do you make money?", "What happens when an API fails?"

---

## CUT LIST (if behind schedule — cut from the bottom, never from the top)

**Never cut:** live ingestion, stress index with explanations, agent trace with citations, Verify + Recover, source-health + stale badges, chaos toggle, deployed URL, README, video, deck.

Cut in this order:
1. NDVI / satellite (P2)
2. Bhashini voice / browser speech (P2)
3. PDF export of evidence report (keep HTML/Markdown)
4. Portfolio upload (P1)
5. Telegram bot (P1) — if cut, show the alert as a UI card and say Telegram is next
6. Backtest on all pilot talukas → backtest on a smaller verified subset (state n honestly)
7. Reduce pilot talukas from ~50 to ~25

---

## Definition of Done for the demo
- [ ] Public URL works from a phone on mobile data
- [ ] Map shows live data for pilot talukas with timestamps
- [ ] Agent run shows trace, citations and passes Verify; Marathi + English output
- [ ] Chaos toggle demonstrates graceful degradation
- [ ] README has setup + diagram; a fresh clone runs
- [ ] No dummy data anywhere in app code; test fixtures clearly labelled
- [ ] Every member can explain every module
