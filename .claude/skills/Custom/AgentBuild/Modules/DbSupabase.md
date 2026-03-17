# Module: Database — Supabase

> Postgres-as-a-service with real-time subscriptions, row-level security, and a built-in REST/GraphQL API. The fastest path from schema to production database.

**Module status:** STABLE (v4 — updated 2026-02-21)
**Proven on:** 3+ AgentBuild projects
**When to use:** Any project needing a relational database with auth integration, real-time features, or file storage
**When NOT to use:** Projects needing a graph database, time-series data at scale, or vendor-lock-free requirements

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Database | Fully managed Postgres with connection pooling |
| Auth integration | Row-level security ties directly to Clerk or Supabase Auth user IDs |
| REST API | Auto-generated from schema — no boilerplate for CRUD |
| Real-time | WebSocket subscriptions on any table |
| File storage | S3-compatible bucket with CDN |
| Migrations | Supabase CLI manages schema versions |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Database | Supabase (Postgres) | Free tier, instant setup, built-in RLS, great DX |
| Client | `@supabase/supabase-js` v2 | Type-safe queries, real-time built in |
| Migrations | `supabase db push` or Drizzle ORM | Schema-as-code, version controlled |
| ORM (optional) | Drizzle ORM | Type-safe, lightweight, pairs well with Supabase |

---

## Environment Variables Required

### New API Keys (Projects created after June 2025)

Supabase transitioned from JWT-based keys to a new format in mid-2025. New projects use the new format by default. Existing projects can opt-in via the Dashboard.

```bash
# .env.local (never commit)
NEXT_PUBLIC_SUPABASE_URL=https://[project-ref].supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...   # Safe for client-side (replaces anon key)
SUPABASE_SECRET_KEY=sb_secret_...                         # Server-only: bypasses RLS — NEVER expose to client
```

**New key format details:**

| Key Type | Prefix | Replaces | Privileges | Where to Use |
|----------|--------|----------|-----------|--------------|
| Publishable | `sb_publishable_` | Legacy `anon` (JWT) | Low — respects RLS | Client-side (browser, mobile) |
| Secret | `sb_secret_` | Legacy `service_role` (JWT) | Elevated — bypasses RLS | Server-only (API routes, webhooks) |

**Key differences from legacy keys:**
- Secret keys **cannot be used in browsers** (returns 401 — this is intentional security enforcement)
- Keys go in the `apikey` header, **not** the `Authorization` header
- Multiple secret keys can be created for rotation without downtime
- Secret keys can be assigned custom Postgres roles (not just `service_role`)
- Key revelation events are logged in audit trails

### Legacy API Keys (Projects created before June 2025)

Legacy JWT-based keys still work but will be **removed in late 2026**. If your project uses these, plan to migrate.

```bash
# .env.local (never commit) — LEGACY FORMAT
NEXT_PUBLIC_SUPABASE_URL=https://[project-ref].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...          # Safe for client-side (JWT format)
SUPABASE_SERVICE_ROLE_KEY=eyJ...              # Server-only: bypasses RLS (JWT format)
```

### Migration Timeline

| Date | What Happens |
|------|-------------|
| **June 2025** | New key format available on all projects (opt-in) |
| **November 2025** | Restored projects no longer receive legacy keys |
| **Late 2026** | Legacy keys deleted — mandatory migration |

**To migrate:** Substitute `sb_publishable_` anywhere you used the `anon` key, and `sb_secret_` anywhere you used the `service_role` key. No code changes needed beyond swapping the values.

### How to Detect Which Key Format to Use

```bash
# Check if project has new keys (look for sb_ prefix in Dashboard → Settings → API)
# Or check your .env.local:
grep -q "sb_publishable_" .env.local && echo "NEW FORMAT" || echo "LEGACY FORMAT"
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Database (Supabase / Postgres)

- Database is Supabase Postgres — use standard SQL patterns
- ORM: [Drizzle / direct Supabase client — specify which]
- Row-level security (RLS) is ALWAYS enabled — never disable it
- **API Key Transition (2025-2026):** Supabase is migrating from JWT-based keys to `sb_publishable_`/`sb_secret_` format. Legacy keys removed late 2026.
- Server-side queries use `SUPABASE_SECRET_KEY` (new) or `SUPABASE_SERVICE_ROLE_KEY` (legacy) — bypasses RLS for admin ops only
- Client-side queries use `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` (new) or `NEXT_PUBLIC_SUPABASE_ANON_KEY` (legacy) — RLS filters by auth.uid()
- **New keys:** Secret keys CANNOT be used in browsers (returns 401). Use `apikey` header, not `Authorization`.
- User data isolation: every table with user data has a `user_id` column matching Clerk's `userId`
- **Database setup is CLI-first and autonomous.** Lucy checks for the Supabase CLI, installs if needed (with user permission), discusses schema recommendations based on the project, then creates tables via `supabase db push`. Dashboard SQL Editor is fallback only.
- **Migrations are a 6-step process: DETECT CLI → LINK → DISCUSS SCHEMA → WRITE → APPLY → VERIFY.** Writing the SQL file is not enough. Run `supabase db push` then verify tables exist with `supabase db inspect --schema public`. Do NOT start the app until tables are confirmed.
- Add new migration files to `supabase/migrations/` — do NOT edit existing migrations
- Never use `SELECT *` — always specify columns explicitly
- Always use prepared statements or the Supabase client — never raw string interpolation in queries
```

---

## Standard Client Setup

The client setup code works with both new (`sb_publishable_`/`sb_secret_`) and legacy (`eyJ...`) key formats — the Supabase SDK accepts either.

```typescript
// lib/supabase/client.ts — browser client
import { createBrowserClient } from '@supabase/ssr'

// Supports both new (sb_publishable_) and legacy (anon JWT) key formats
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY
  ?? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    supabaseKey
  )
}
```

```typescript
// lib/supabase/server.ts — server component / API route client
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY
  ?? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export function createClient() {
  const cookieStore = cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    supabaseKey,
    {
      cookies: {
        get(name) { return cookieStore.get(name)?.value },
        set(name, value, options) { cookieStore.set({ name, value, ...options }) },
        remove(name, options) { cookieStore.set({ name, value: '', ...options }) },
      },
    }
  )
}
```

```typescript
// lib/supabase/admin.ts — service role (server only, bypasses RLS)
import { createClient } from '@supabase/supabase-js'

// Supports both new (sb_secret_) and legacy (service_role JWT) key formats
const secretKey = process.env.SUPABASE_SECRET_KEY
  ?? process.env.SUPABASE_SERVICE_ROLE_KEY!

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  secretKey
)
```

---

## Row-Level Security Pattern (Clerk Integration)

When using Clerk for auth, RLS policies reference a custom function that extracts the user ID from the Clerk JWT:

```sql
-- Run once: function to extract Clerk user ID from JWT
create or replace function requesting_user_id()
returns text
language sql stable
as $$
  select nullif(
    current_setting('request.jwt.claims', true)::json->>'sub',
    ''
  )::text;
$$;

-- Example table with RLS
create table documents (
  id uuid default gen_random_uuid() primary key,
  user_id text not null,           -- matches Clerk userId format: "user_2abc..."
  title text not null,
  content text,
  created_at timestamptz default now()
);

alter table documents enable row level security;

-- Users can only see their own documents
create policy "users_own_documents" on documents
  for all
  using (user_id = requesting_user_id());
```

---

## Database Setup Workflow (CLI-First — Autonomous)

> **Lucy creates tables programmatically via the Supabase CLI.** The Dashboard SQL Editor is a fallback only — used when the CLI is unavailable or the user explicitly prefers it. Writing migration SQL without applying it is the #1 Supabase build failure (`PGRST205: Could not find the table`).

### Step 0: Detect and Install Supabase CLI

**Lucy MUST check for the CLI before any database work.** This is the gate.

```bash
# Check if Supabase CLI is installed
supabase --version 2>/dev/null
```

**If installed:** Proceed to Step 1.

**If NOT installed:** Use AskUserQuestion to prompt:

```
"The Supabase CLI is required to create database tables programmatically.
Should I install it?"

Options:
1. "Yes, install via npm" → run: npm install -g supabase
2. "Yes, install via Homebrew" → run: brew install supabase/tap/supabase
3. "No, I'll use the Dashboard instead" → switch to Dashboard Fallback section
```

**After installation, verify:**
```bash
supabase --version
# Expected: Supabase CLI X.X.X
```

### Step 1: Link to Supabase Project

```bash
# Check if already linked
supabase status 2>/dev/null
```

**If NOT linked:** Lucy needs the project reference ID.

```bash
# Link to the Supabase project (requires project-ref from Dashboard URL or Settings)
supabase link --project-ref [project-ref]
```

> **Where to find project-ref:** It's the subdomain in the project URL: `https://[project-ref].supabase.co`. If the user doesn't have a Supabase project yet, direct them to create one at supabase.com first — project creation requires a human (account, billing).

### Step 2: Discuss Schema and Recommend Tables

**Before writing any SQL, Lucy analyzes the project and recommends the schema.** This is where Lucy applies database design expertise to the project's specific needs.

**Lucy should:**

1. **Read the project orientation** (PID file's `orientation.what` and `orientation.done`)
2. **Read feature specs** if they exist (e.g., `docs/specs/features/*.md`)
3. **Identify data entities** from the feature requirements
4. **Present schema recommendations** to the user:

```
Based on [project name]'s requirements, here's the recommended schema:

**Tables:**
- `[table_name]` — [purpose]. Columns: [list with types].
- `[table_name]` — [purpose]. Columns: [list with types].
- ...

**Row-Level Security:**
- All user-data tables get RLS with `requesting_user_id()` policy
- [Any tables that need different access patterns]

**Indexes:**
- [Which columns need indexes and why]

**Relationships:**
- [Foreign keys between tables]

Should I create these tables?
```

**Schema design principles Lucy should follow:**
- Every user-data table gets a `user_id text not null` column (matches Clerk format: `user_2abc...`)
- Every table gets `created_at timestamptz default now()`
- Use `uuid` primary keys with `gen_random_uuid()`
- Use `text` for flexible string fields, `jsonb` for structured data
- Use `check` constraints for status/enum fields
- Add indexes on `user_id` and any column used in WHERE clauses
- Use `CREATE TABLE IF NOT EXISTS` for idempotent migrations

### Step 3: Write Migration SQL

After user approves the schema (or Lucy proceeds based on approved specs):

```bash
# Create a new timestamped migration file
supabase migration new [descriptive_name]
# This creates: supabase/migrations/[timestamp]_[descriptive_name].sql
```

**Lucy writes the migration SQL** to the created file. Example:

```sql
-- Auth helper function (run once per project — Clerk integration)
create or replace function requesting_user_id()
returns text
language sql stable
as $$
  select nullif(
    current_setting('request.jwt.claims', true)::json->>'sub',
    ''
  )::text;
$$;

-- Example table
create table if not exists documents (
  id uuid default gen_random_uuid() primary key,
  user_id text not null,
  title text not null,
  content text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table documents enable row level security;

create policy "users_own_documents" on documents
  for all using (user_id = requesting_user_id());

create index documents_user_id_idx on documents(user_id);
```

### Step 4: Apply Migration via CLI (NON-NEGOTIABLE)

```bash
# Apply to remote Supabase project
supabase db push
```

**If `supabase db push` fails:**

| Error | Fix |
|-------|-----|
| Auth error / not linked | Run `supabase link --project-ref [ref]` first |
| Connection refused | Check project is active in Supabase Dashboard |
| SQL syntax error | Fix the migration SQL, then retry |
| Permission denied | Check that the linked project has the correct access token |

### Step 5: Verify Tables Exist (NON-NEGOTIABLE)

```bash
# List all tables in public schema — project's tables MUST appear
supabase db inspect --schema public
```

**Programmatic verification via REST API** (use when `db inspect` is unavailable):

```bash
# Verify specific table exists
curl -sf "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/[table_name]?select=*&limit=0" \
  -H "apikey: ${NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY:-$NEXT_PUBLIC_SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY:-$NEXT_PUBLIC_SUPABASE_ANON_KEY}"
# Expected: 200 OK with empty array []. If 404 or PGRST205 → migration was NOT applied.
```

> **Do NOT start the application until Step 5 confirms tables exist.** The app will crash with `PGRST205` if tables are missing.

### Step 6: Generate TypeScript Types (Optional but Recommended)

```bash
# Generate types from the live schema
supabase gen types typescript --linked > src/types/database-generated.ts
```

This gives type-safe queries. If the project already has manually written types (like `src/types/database.ts`), compare and reconcile.

### Applying Migrations to Production

```bash
# Same as dev — migrations are idempotent
supabase db push --db-url postgresql://[production-connection-string]

# Always verify after applying
supabase db inspect --schema public
```

---

## Dashboard Fallback (Only When CLI Is Unavailable)

> **Use this ONLY when the Supabase CLI cannot be installed or the user explicitly requests it.** The CLI path above is the primary and preferred workflow.

If the user chose "No, I'll use the Dashboard" in Step 0, or the CLI fails for infrastructure reasons:

1. Lucy writes the migration SQL to `supabase/migrations/` (for version control)
2. Lucy presents the SQL to the user with instructions:
   ```
   Copy the SQL below and run it in your Supabase Dashboard:
   1. Go to supabase.com → your project → SQL Editor
   2. Click "New Query"
   3. Paste the SQL below
   4. Click "Run"
   5. Verify: go to Table Editor and confirm the tables appear

   [SQL here]
   ```
3. Lucy waits for user confirmation before proceeding
4. Lucy verifies via the REST API probe (Step 5 above) — this works regardless of how the SQL was applied

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `PGRST205: Could not find the table` | Migration SQL was written but never applied to the Supabase project | Run `supabase db push` then verify with `supabase db inspect --schema public`. See Migration Workflow above. |
| RLS blocks all queries | `requesting_user_id()` returns null | Ensure Clerk JWT is being passed; check JWKS URL in Supabase dashboard |
| Connection pool exhausted | Too many server-side clients | Create client per-request (not singleton) in server components |
| Real-time not working | Table not in realtime publication | Run: `alter publication supabase_realtime add table [table_name]` |
| Migration fails | Existing migration edited | Never edit applied migrations — create a new one |
| TypeScript types stale | Schema changed without regenerating | Run: `supabase gen types typescript --local > types/database.ts` |
| Service role key exposed | Used in client-side code | `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_SECRET_KEY` must NEVER appear in client bundles |
| Secret key returns 401 in browser | New `sb_secret_` keys cannot be used client-side (intentional security enforcement) | Use `sb_publishable_` key for client-side; secret keys are server-only |
| Wrong header for API key | New keys use `apikey` header, not `Authorization` | Check header name — new format: `apikey`, legacy format: `Authorization: Bearer` |
| Real-time stops after 24hrs | Unsigned users on new key format have a 24-hour Realtime connection limit | Ensure users are signed in for persistent real-time connections |

---

## Test Coverage Required

```typescript
// tests/db/data-isolation.test.ts
describe('Database data isolation', () => {
  it('should only return documents owned by the authenticated user')
  it('should return 0 results for documents owned by other users')
  it('should prevent writes to documents owned by other users')
  it('should allow admin operations using service role key')
})

// tests/db/migrations.test.ts
describe('Migrations', () => {
  it('should apply migrations idempotently')
  it('should not drop data on re-application')
})
```

---

## Dashboard Setup Checklist

Before first deployment:
- [ ] Create Supabase project at supabase.com
- [ ] Check key format: Dashboard → Settings → API → look for `sb_` prefix (new) or `eyJ` prefix (legacy)
- [ ] **New keys:** Copy `sb_publishable_` key to `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` in `.env`
- [ ] **New keys:** Copy `sb_secret_` key to `SUPABASE_SECRET_KEY` in `.env` (server-only)
- [ ] **Legacy keys:** Copy anon key to `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env`
- [ ] **Legacy keys:** Copy service role key to `SUPABASE_SERVICE_ROLE_KEY` in `.env` (server-only)
- [ ] Copy project URL to `NEXT_PUBLIC_SUPABASE_URL` in `.env`
- [ ] If using Clerk: add Clerk JWKS URL to Supabase → Settings → Auth → JWT Secret
- [ ] Create `requesting_user_id()` function (if using Clerk + RLS)
- [ ] Run initial migrations
- [ ] Enable RLS on all user-data tables
- [ ] **Plan migration:** If using legacy keys, schedule migration before late 2026 deadline

---

*Module maintained by AgentBuild. Update Known Issues when new failures are discovered.*
*v2 updated 2026-02-21: Added new Supabase API key format (sb_publishable_/sb_secret_), migration timeline, fallback client setup, and new key breaking changes.*
*v3 updated 2026-02-21: Migration section rewritten as mandatory 3-step workflow (WRITE → APPLY → VERIFY). Added PGRST205 to Known Issues. Added migration execution reminder to AGENTS.md additions. Prevents the most common Supabase build failure.*
*v4 updated 2026-02-21: CLI-first autonomous workflow. Lucy detects CLI, installs if needed (with permission), discusses schema recommendations based on project specs, creates tables programmatically via `supabase db push`. Dashboard demoted to fallback. Added schema discussion step (Step 2) and TypeScript type generation (Step 6). 6-step flow: DETECT → LINK → DISCUSS → WRITE → APPLY → VERIFY.*
