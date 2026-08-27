# SENTINEL-X

AI-assisted identity-document screening prototype for SIH. The browser demo analyses uploaded evidence locally and can save a minimal audit record to Supabase.

## Live demo

[Open SENTINEL-X on Vercel](https://sentinel-x-identity-forensics.vercel.app/)

## Privacy boundary

The database schema intentionally excludes identity images, extracted names, document numbers, dates of birth, and face embeddings. It stores only the session identifier, source type, document category, dimensions, risk score, risk tier, anomaly index, and timestamp.

## Connect Supabase to Vercel

1. Create a Supabase project and run [`supabase/schema.sql`](supabase/schema.sql) in its SQL Editor.
2. In Supabase Project Settings → API, copy the Project URL and `service_role` key.
3. In Vercel Project Settings → Environment Variables, add `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` for Production, Preview, and Development.
4. Redeploy the site. After a scan, **Save audit to database** writes a protected metadata-only audit record.

`SUPABASE_SERVICE_ROLE_KEY` must remain only in Vercel environment variables. The browser never receives it.

## Before operational deployment

Add officer authentication, role-based access, rate limiting, retention controls, and a formal privacy/security review before processing real identity documents.

