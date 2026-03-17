# Module: Deploy — Railway

> Zero-config deployment for any web service, API, or background worker. Git push to deploy, automatic HTTPS, built-in environment management, and no infrastructure YAML to write. **Lucy deploys autonomously via the Railway CLI and MCP server — Dashboard is fallback only.**

**Module status:** STABLE (v3 — updated 2026-02-22)
**Proven on:** 3+ AgentBuild projects
**When to use:** Any project needing hosted compute — APIs, web apps, background workers, cron jobs
**When NOT to use:** Static-only sites (use Vercel/Cloudflare Pages); projects requiring bare metal or custom kernel config

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Hosting | Managed containers from Git or Docker |
| Auto-deploy | Push to main → deploy automatically |
| HTTPS | Automatic TLS on all services |
| Environment management | Per-environment variables, shared variable references |
| Networking | Private network between services (no public internet exposure) |
| Scaling | Vertical and horizontal scaling from dashboard |
| Cron jobs | Scheduled tasks without a separate service |
| Databases | Postgres, Redis, MySQL add-ons (alternative to Supabase if preferred) |
| **MCP Server** | Native Railway API access from Claude for deployments, logs, and project management |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Hosting provider | Railway.app | Best DX for full-stack apps, free trial, no YAML config |
| Deploy trigger | Railway CLI (`railway up`) or Git integration | CLI for autonomous deploys, Git for ongoing auto-deploys |
| Secrets management | Railway CLI (`railway variables set`) | Programmatic, encrypted at rest, no Dashboard needed |
| Custom domain | Railway CLI (`railway domain`) | Configurable without leaving the terminal |
| **Agent integration** | Railway MCP Server | Native API access for Claude — deploy, monitor, manage without CLI |

---

## Railway MCP Server (Agent-Native Deployment)

> **The MCP server gives Lucy direct API access to Railway** — creating projects, deploying services, managing variables, reading logs, and monitoring deployments. This is the highest-autonomy path.

### Setup

```bash
# Add Railway MCP server to Claude Code
claude mcp add railway-mcp-server -- npx -y @railway/mcp-server
```

**Requires:** `RAILWAY_TOKEN` environment variable set (get from Railway Dashboard → Account → Tokens).

### MCP Capabilities

Once connected, Lucy has native access to:

| Command | What It Does |
|---------|-------------|
| `/new` | Create projects, services, databases |
| `/service` | Manage existing services |
| `/database` | Add Railway databases (Postgres, Redis) |
| `/environment` | Configure variables, replicas, startup commands |
| `/deployment` | Manage deployment history, logs, redeploys, removals |
| `/metrics` | Query resource usage (CPU, memory, network) |
| `/domain` | Configure custom domains |

### When to Use MCP vs CLI

| Scenario | Use |
|----------|-----|
| First-time setup (create project, add services) | MCP — richer API, can create from scratch |
| Deploy local code changes | CLI — `railway up` deploys working directory |
| Set environment variables | Either — CLI is simpler for bulk, MCP for individual |
| Read deployment logs | Either — CLI is faster for quick checks |
| Ongoing auto-deploy after push | Git integration — set once, forget |
| Debug failed deployment | CLI — `railway logs` + analyze + fix + redeploy |

---

## Deployment Workflow (CLI-First — Autonomous)

> **Lucy deploys programmatically via the Railway CLI.** The Dashboard is a fallback only — used when the CLI is unavailable or the user explicitly prefers it.

### Step 0: Detect and Install Railway CLI

**Lucy MUST check for the CLI before any deployment work.** This is the gate.

```bash
# Check if Railway CLI is installed
railway --version 2>/dev/null
```

**If installed:** Proceed to Step 1.

**If NOT installed:** Use AskUserQuestion to prompt:

```
"The Railway CLI is required to deploy programmatically.
Should I install it?"

Options:
1. "Yes, install via npm" → run: npm install -g @railway/cli
2. "Yes, install via Homebrew" → run: brew install railway
3. "No, I'll use the Dashboard instead" → switch to Dashboard Fallback section
```

**After installation, verify:**
```bash
railway --version
```

### Step 1: Authenticate

```bash
# Check if already authenticated
railway whoami 2>/dev/null
```

**If NOT authenticated:** Use AskUserQuestion:

```
"Railway CLI needs authentication to deploy.
Please run `railway login` in a separate terminal, then tell me when you're done."
```

**Alternative (non-interactive):** If the user has a `RAILWAY_TOKEN`:
```bash
export RAILWAY_TOKEN=your-token-here
railway whoami  # Verify it works
```

### Step 2: Create or Link Project

```bash
# Check if already linked to a Railway project
railway status 2>/dev/null
```

**If NOT linked:**

```bash
# Option A: Link to an existing Railway project
railway link

# Option B: Create a new Railway project
railway init
```

> **`railway init` creates a new project on Railway and links the local directory.** No Dashboard needed.

### Step 3: Set Environment Variables

Lucy reads the project's `.env.example` and sets each variable programmatically:

```bash
# Set variables one at a time
railway variables set CLERK_SECRET_KEY=sk_live_...
railway variables set SUPABASE_SERVICE_ROLE_KEY=eyJ...
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set NEXT_PUBLIC_APP_URL=https://your-app.up.railway.app

# List all variables to verify
railway variables
```

**Lucy should:**
1. Read `.env.example` to identify all required variables
2. Use AskUserQuestion to collect production values for secrets
3. Set each via `railway variables set`
4. Verify with `railway variables`

**For Railway service references (databases):**
```bash
# These use Railway's interpolation syntax — set in Dashboard or via MCP
# DATABASE_URL=${{Postgres.DATABASE_URL}}
# REDIS_URL=${{Redis.REDIS_URL}}
```

### Step 4: Deploy and Generate Public URL

```bash
# Deploy the current working directory
railway up

# Generate a public URL (idempotent — returns existing domain if one exists)
railway domain
```

**`railway up` does:**
- Uploads source code to Railway
- Builds using Nixpacks (auto-detects framework)
- Deploys the built container
- Runs health checks

**`railway domain` does:**
- Generates a free Railway-provided HTTPS domain (e.g., `https://your-app-production.up.railway.app`)
- If a domain already exists, returns the existing one (safe to run every time)
- Automatic SSL certificate provisioned and renewed
- Limit: 1 Railway-provided domain per service

**The public URL is NOT optional.** Every deployed service must have a shareable URL. Without it, health checks can't run and the app can't be shared.

**For ongoing deployments:** Connect a GitHub repo via `railway link` → Railway auto-deploys on push to main. The domain persists across deploys.

### Step 5: Verify Deployment and Report URL

```bash
# Check deployment status
railway status

# Read deployment logs
railway logs

# Verify health check using the generated domain
curl -sf https://[generated-domain].railway.app/api/health
```

**After successful verification, Lucy MUST report the shareable URL to the user:**

```
✅ Deployment verified. Your app is live at:
   https://your-app-production.up.railway.app

   Share this link — it's free, persistent, and HTTPS-secured.
```

**If deployment fails:** Lucy reads logs, analyzes the error, fixes the code, and redeploys:
```bash
railway logs          # Read error
# ... fix the issue ...
railway up            # Redeploy
railway domain        # Confirm URL still active
```

### Step 6: Custom Domain (Optional — Post-MVP)

> **The Railway-generated URL from Step 4 is sufficient for demos and sharing.** Custom domains are a post-MVP concern.

```bash
# Add a custom domain (requires DNS configuration)
railway domain your-app.yourdomain.com
# Then add the CNAME record Railway provides to your DNS settings
```

**Use custom domains when:** You have a purchased domain and want branded URLs (e.g., `briefly.yourdomain.com`). This requires DNS access and is not needed for MVP sharing.

---

## Environment Variables Pattern

Railway injects variables at runtime. Structure:

```bash
# Shared across environments (set via CLI or Dashboard)
DATABASE_URL=${{Postgres.DATABASE_URL}}    # Railway reference syntax — interpolates at runtime
REDIS_URL=${{Redis.REDIS_URL}}

# Environment-specific (set per-environment)
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://myapp.up.railway.app

# Secrets (set via CLI: railway variables set, never in code)
CLERK_SECRET_KEY=sk_live_...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
STRIPE_SECRET_KEY=sk_live_...
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Deployment (Railway)

- **Deployment is CLI-first and autonomous.** Lucy checks for the Railway CLI, installs if needed (with user permission), authenticates, then deploys via `railway up`. Dashboard is fallback only.
- **Railway MCP Server available:** If configured (`claude mcp add railway-mcp-server`), Lucy has native API access for project creation, service management, variable configuration, log reading, and deployment management.
- **Public URL is mandatory.** After `railway up`, always run `railway domain` to generate a free `.railway.app` HTTPS URL. Report the shareable URL to the user.
- Deploy trigger: `railway up` + `railway domain` for manual deploys, push to `main` for auto-deploy after Git integration
- Environment variables: set via `railway variables set KEY=VALUE`, never in code or `.env` files committed to git
- Reference Railway service variables using `${{ServiceName.VARIABLE}}` syntax
- Health check endpoint: every service must expose `GET /health` returning 200 with `{ status: "ok" }`
- Build command: Railway auto-detects from `package.json` — set explicitly if needed in `railway.toml`
- Start command: set `startCommand` in `railway.toml` or via `railway variables set`
- Private networking: services communicate via `http://[service-name].railway.internal` (not public internet)
- Logs: `railway logs` from CLI, or Railway dashboard → service → Deployments tab
- Debugging: `railway logs` → analyze error → fix → `railway up` → verify
```

---

## railway.toml Configuration

Create at repo root:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "node dist/index.js"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

For Next.js:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "node .next/standalone/server.js"
healthcheckPath = "/api/health"
healthcheckTimeout = 300
```

---

## Required Health Check Endpoint

Every service must implement this:

```typescript
// app/api/health/route.ts (Next.js)
export async function GET() {
  return Response.json({ status: 'ok', timestamp: new Date().toISOString() })
}

// Express
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})
```

---

## GitHub Actions Integration (Optional CI Gate)

For projects wanting CI checks before Railway deploys:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun test
      - run: bun run lint
```

Railway picks up after CI passes via the Git integration.

---

## Dashboard Fallback (Only When CLI Is Unavailable)

> **Use this ONLY when the Railway CLI cannot be installed or the user explicitly requests it.**

If Lucy cannot use the CLI:

1. Direct the user to create a project at railway.app
2. Provide a checklist of environment variables to set in the Dashboard
3. Guide them through connecting the GitHub repo
4. Instruct them to trigger a deploy via the Dashboard
5. Verify deployment via the health check URL

**Dashboard Setup Checklist (fallback only):**
- [ ] Create Railway project at railway.app
- [ ] Connect GitHub repository
- [ ] Set all environment variables in Railway dashboard (from `.env.example`)
- [ ] Configure health check path in Railway service settings
- [ ] Add `railway.toml` to repo root
- [ ] Implement `GET /health` endpoint
- [ ] Deploy once manually to verify build succeeds
- [ ] Set up custom domain (optional) in Railway → Settings → Domains

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Deploy fails with "build failed" | Missing dependency or wrong Node version | `railway logs` to diagnose; specify Node version in `package.json` engines field |
| Health check timing out | App takes >300s to start | Increase `healthcheckTimeout` in `railway.toml`; optimize startup time |
| Environment variable undefined | Variable not set | `railway variables` to list; `railway variables set KEY=VALUE` to fix |
| Private networking fails | Using public URL between services | Use `http://[service-name].railway.internal` for service-to-service calls |
| Memory crash / OOM | Service hitting memory limit | Upgrade Railway plan or optimize memory usage; check via MCP `/metrics` |
| `${{ServiceName.VAR}}` not resolving | Typo in service name or variable | Must match Railway service name exactly; case-sensitive |
| `railway up` hangs | Not authenticated | Run `railway login` or set `RAILWAY_TOKEN` |
| MCP server not responding | Missing `RAILWAY_TOKEN` env var | Set token: `export RAILWAY_TOKEN=your-token` |

---

## Test Coverage Required

```typescript
// tests/health/health.test.ts
describe('Health check', () => {
  it('should return 200 with status ok')
  it('should include timestamp in response')
  it('should respond within 1 second')
})

// tests/deploy/env.test.ts
describe('Environment configuration', () => {
  it('should have all required environment variables set')
  it('should not expose secret keys in client bundle')
})
```

---

*Module maintained by AgentBuild. Update Known Issues when new failures are discovered.*
*v1 initial: Git push deploy, Dashboard-first setup, railway.toml config.*
*v2 updated 2026-02-21: CLI-first autonomous workflow matching DbSupabase v4 pattern. Added Railway MCP Server integration for native API access. Lucy deploys via `railway up`, sets variables via `railway variables set`, debugs via `railway logs`. Dashboard demoted to fallback. 6-step flow: DETECT CLI → AUTH → LINK/INIT → SET VARS → DEPLOY → VERIFY.*
*v3 updated 2026-02-22: Public URL generation (`railway domain`) moved from optional Step 6 to mandatory part of Step 4 (Deploy). Every deployment now produces a shareable HTTPS URL. Lucy reports the live URL to the user after verification. Custom domains remain optional as Step 6 (Post-MVP).*
