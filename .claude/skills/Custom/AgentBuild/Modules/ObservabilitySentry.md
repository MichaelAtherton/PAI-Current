# Module: Observability — Sentry + Pino

> Real-time error tracking, performance monitoring, and structured logging. Know when your app breaks before your users tell you.

**Module status:** STABLE
**Proven on:** 3+ AgentBuild projects
**When to use:** Every project. Phase 6 of AgentBuild requires observability before MVP gate passes.
**When NOT to use:** N/A — this module is required, not optional.

---

## What This Module Provides

| Capability | Provider | What You Get |
|-----------|---------|--------------|
| Error tracking | Sentry | Automatic capture, stack traces, user context, replay |
| Performance | Sentry | Request timing, Core Web Vitals, transaction tracing |
| Structured logging | Pino | JSON logs with correlation IDs, readable in Railway logs |
| Alerting | Sentry | Slack/email on new errors, error rate spikes |
| Release tracking | Sentry | Errors linked to deploy/release version |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Error tracking | Sentry.io | Industry standard, generous free tier, best Next.js integration |
| Logging | Pino | Fastest Node.js logger, JSON output, Railway-compatible |
| Log transport | stdout → Railway | Railway captures stdout automatically — no log service needed |

---

## Environment Variables Required

```bash
# Sentry
NEXT_PUBLIC_SENTRY_DSN=https://[key]@sentry.io/[project]
SENTRY_AUTH_TOKEN=sntrys_...           # For source map upload during build
SENTRY_ORG=your-org-slug
SENTRY_PROJECT=your-project-slug

# App version (for release tracking)
NEXT_PUBLIC_APP_VERSION=1.0.0          # Set from git tag in CI
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Observability (Sentry + Pino)

- All errors are automatically captured by Sentry — do NOT add manual try/catch just to suppress errors
- Structured logging via Pino: use `logger.info()`, `logger.error()`, etc. — never use `console.log` in production code
- Every request must include a correlation ID in logs: `logger.info({ correlationId, userId }, 'message')`
- Never log: passwords, tokens, PII, full request bodies with credentials
- Log levels in use: ERROR (failure), WARN (degraded), INFO (normal), DEBUG (dev only)
- Sentry captures: uncaught exceptions, unhandled rejections, API errors, and frontend JS errors
- Source maps are uploaded at build time — never commit `.env` with SENTRY_AUTH_TOKEN
- Performance transactions: automatically traced for API routes and page loads
```

---

## Sentry Setup (Next.js)

```bash
# Install
bun add @sentry/nextjs

# Run wizard (sets up config files automatically)
bunx @sentry/wizard@latest -i nextjs
```

This creates:
- `sentry.client.config.ts` — browser error tracking
- `sentry.server.config.ts` — server error tracking
- `sentry.edge.config.ts` — edge runtime tracking
- Updates `next.config.ts` with Sentry webpack plugin

**Manual configuration if wizard fails:**

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,           // 100% in dev, reduce to 0.1 in prod at scale
  debug: false,
  replaysOnErrorSampleRate: 1.0,   // Always capture replay on error
  replaysSessionSampleRate: 0.1,   // 10% of sessions
  integrations: [Sentry.replayIntegration()],
})
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  debug: false,
})
```

---

## Pino Logger Setup

```bash
bun add pino pino-pretty
```

```typescript
// lib/logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: process.env.NODE_ENV !== 'production'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  base: {
    env: process.env.NODE_ENV,
    version: process.env.NEXT_PUBLIC_APP_VERSION,
  },
  redact: ['req.headers.authorization', 'req.body.password', 'req.body.token'],
})
```

**Usage pattern:**

```typescript
// In API routes / server code
import { logger } from '@/lib/logger'
import { nanoid } from 'nanoid'

export async function GET(req: Request) {
  const correlationId = nanoid()
  const childLogger = logger.child({ correlationId })

  childLogger.info({ path: req.url }, 'Request received')

  try {
    // ... operation
    childLogger.info({ result }, 'Request completed')
  } catch (error) {
    childLogger.error({ error }, 'Request failed')
    Sentry.captureException(error, { extra: { correlationId } })
    throw error
  }
}
```

---

## Sentry Error Boundary (React)

```typescript
// app/error.tsx (Next.js app router)
'use client'
import * as Sentry from '@sentry/nextjs'
import { useEffect } from 'react'

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    Sentry.captureException(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Source maps not uploading | Missing `SENTRY_AUTH_TOKEN` | Set in Railway environment variables (not `.env`) |
| Errors not appearing in Sentry | Wrong or missing DSN | Verify `NEXT_PUBLIC_SENTRY_DSN` matches project in Sentry dashboard |
| Pino logs not visible in Railway | Using `pino-pretty` in production | Remove `pino-pretty` transport in production — Railway reads raw JSON |
| Sentry capturing too many events | High traffic + 100% sample rate | Reduce `tracesSampleRate` to 0.1 after initial validation |
| Correlation IDs missing | Not using child logger | Always create `logger.child({ correlationId })` per request |
| PII leaking in logs | Logging full request bodies | Use Pino's `redact` option; never log `req.body` directly |

---

## Test Coverage Required

```typescript
// tests/observability/logging.test.ts
describe('Logging', () => {
  it('should include correlationId in all log entries')
  it('should not log passwords or tokens')
  it('should use appropriate log level for each operation type')
})

// tests/observability/errors.test.ts
describe('Error capture', () => {
  it('should capture unhandled API errors')
  it('should include correlationId in Sentry context')
  it('should not expose internal error details to API response')
})
```

---

## MVP Gate Verification (Phase 6)

Before MVP gate passes, verify:
- [ ] Sentry dashboard shows events (trigger a test error: `throw new Error('sentry test')`)
- [ ] Source maps uploaded (error stack traces show original TypeScript, not minified JS)
- [ ] Pino logs visible in Railway logs tab with JSON structure
- [ ] Correlation IDs present in all API log lines
- [ ] No PII visible in Sentry events or logs
- [ ] Sentry alert configured for new error spike (Dashboard → Alerts → New Alert)

---

*Module maintained by AgentBuild. Update Known Issues when new failures are discovered.*
