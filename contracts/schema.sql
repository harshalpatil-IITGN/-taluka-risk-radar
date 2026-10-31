-- contracts/schema.sql — Taluka Risk Radar
-- Owner: Harshal. Changes via PR only; announce in chat.

create extension if not exists vector;

create table taluka (
  id serial primary key,
  name_en text not null, name_mr text,
  district text not null, division text not null,
  lat double precision not null, lon double precision not null,
  lgd_code text, pilot boolean default true,
  drought_declared_2026 boolean,           -- backtest label, nullable
  label_source_url text,
  unique (name_en, district)
);

create table weather_daily (
  taluka_id int references taluka(id),
  date date not null,
  is_forecast boolean not null,
  precip_mm real, tmax_c real, tmin_c real, et0_mm real,
  soil_moisture_0_7cm real,
  source text not null, fetched_at timestamptz not null,
  primary key (taluka_id, date, is_forecast, source)
);

create table climatology (               -- from ERA5 1991-2020
  taluka_id int references taluka(id),
  window_days int not null,              -- e.g. 30, 60, season-to-date handled in code
  month int not null,
  gamma_shape double precision, gamma_scale double precision, p_zero double precision,
  normal_season_mm_by_day jsonb,         -- cumulative normal since 1 Jun, by day-of-season
  source text, computed_at timestamptz,
  primary key (taluka_id, window_days, month)
);

create table mandi_price (
  id bigserial primary key,
  state text, district text, market text, commodity text, variety text, grade text,
  arrival_date date not null,
  min_price numeric, max_price numeric, modal_price numeric,
  fetched_at timestamptz not null,
  unique (market, commodity, variety, grade, arrival_date)
);

create table msp_reference (
  commodity text, season text, price_per_quintal numeric,
  source_url text not null, loaded_at timestamptz,
  primary key (commodity, season)
);

create table source_health (
  source text primary key,
  last_attempt_at timestamptz, last_success_at timestamptz,
  status text,                           -- OK | DEGRADED | DOWN | DISABLED_CHAOS
  last_error text, latency_ms int, rows_written int
);

create table ingest_dead_letter (
  id bigserial primary key, source text, payload jsonb, error text, created_at timestamptz default now()
);

create table risk_score (
  taluka_id int references taluka(id),
  as_of_date date not null,
  stress_index real not null,            -- 0-100
  level text not null,                   -- LOW | WATCH | HIGH | SEVERE
  components jsonb not null,             -- each component value, weight, contribution
  triggers jsonb not null,               -- which rules fired and thresholds used
  data_freshness jsonb not null,         -- per-source as_of + stale flags
  confidence real,
  computed_at timestamptz not null,
  primary key (taluka_id, as_of_date)
);

create table doc_chunk (
  id bigserial primary key,
  doc_id text, title text, source_url text, page int, lang text,
  text text not null, embedding vector(384)
);

create table agent_run (
  id uuid primary key, started_at timestamptz, taluka_id int, audience text, language text,
  status text, trace jsonb, output jsonb, error text
);

create table alert (
  id bigserial primary key, taluka_id int, created_at timestamptz default now(),
  level text, channel text, audience text, language text,
  message text, evidence jsonb, delivered boolean default false
);

-- Indexes for query performance
create index idx_weather_daily_taluka_date on weather_daily(taluka_id, date);
create index idx_risk_score_as_of on risk_score(as_of_date);
create index idx_mandi_price_commodity_date on mandi_price(commodity, arrival_date);
create index idx_doc_chunk_embedding on doc_chunk using ivfflat (embedding vector_cosine_ops) with (lists = 10);
