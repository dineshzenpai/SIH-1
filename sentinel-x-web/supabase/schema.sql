-- SENTINEL-X audit storage: deliberately excludes document images, names,
-- document numbers, date of birth, face embeddings, and other identity data.
create table if not exists public.scan_audits (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  session_id text not null check (char_length(session_id) <= 64),
  source_type text not null check (source_type in ('SAMPLE', 'LOCAL')),
  document_type text not null check (char_length(document_type) <= 64),
  image_width integer not null check (image_width between 1 and 20000),
  image_height integer not null check (image_height between 1 and 20000),
  trust_score integer not null check (trust_score between 0 and 100),
  verdict text not null check (char_length(verdict) <= 64),
  risk_level text not null check (risk_level in ('GREEN', 'YELLOW', 'RED')),
  anomaly_index numeric(4, 3) not null check (anomaly_index between 0 and 1),
  audit_version text not null check (char_length(audit_version) <= 16)
);

create index if not exists scan_audits_created_at_idx on public.scan_audits (created_at desc);
create index if not exists scan_audits_risk_level_idx on public.scan_audits (risk_level, created_at desc);

alter table public.scan_audits enable row level security;

-- No anonymous policies: browser clients cannot access the table directly.
-- The Vercel API uses the service-role secret, kept only in deployment settings.

