# Module: Auth — Clerk

> Drop-in authentication for any web or API project. Handles sessions, JWTs, social login, and organization management without writing an auth system.

**Module status:** STABLE (v2 — updated 2026-02-21)
**Proven on:** 3+ AgentBuild projects
**When to use:** Any project with user accounts, login, or protected routes
**When NOT to use:** Internal tools with no user accounts; projects using Supabase Auth exclusively

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Authentication | Email/password, magic link, social OAuth (Google, GitHub, etc.) |
| Session management | Cookie-based sessions, JWT issuance, sliding expiry |
| User management | Dashboard, user metadata, roles |
| Organization support | Multi-tenant orgs, invitations, member management |
| Webhooks | User created/updated/deleted events |
| Edge-compatible | Middleware works in Next.js, Remix, Express, and edge runtimes |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Auth provider | Clerk.dev | Best-in-class DX, generous free tier, handles all edge cases |
| SDK | `@clerk/nextjs@latest` (Next.js) or `@clerk/express@latest` (Express) | Matches target framework |
| Token format | JWT (RS256) | Clerk-issued, verifiable without network call |

**Important version note:** Always install `@latest`. Clerk's SDK has breaking changes across major versions. Pin to `@latest` in package.json during MVP, pin to exact version before production.

---

## Environment Variables

### Development: Keyless Mode (Recommended for MVP)

**Clerk supports keyless mode — no API keys needed to start developing.** When you install `@clerk/nextjs` and run your app without keys, Clerk auto-generates temporary development keys. This eliminates the #1 cause of first-build failures.

```bash
# .env.local — EMPTY for keyless mode
# No keys needed! Just run `npm run dev` and Clerk prompts you to claim your app.
```

**How keyless mode works:**
1. Install `@clerk/nextjs@latest`
2. Add `<ClerkProvider>` to layout
3. Add middleware file (see Critical File Locations below)
4. Run `npm run dev` — Clerk creates a temporary dev instance automatically
5. When ready, claim your app at the URL Clerk shows in terminal

### Production: Explicit Keys

When you're ready to deploy or have created your Clerk app at [clerk.com](https://clerk.com):

```bash
# .env.local (Next.js) — NEVER .env, always .env.local
# .env (Express/Node.js)

# REQUIRED — both must be present
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OPTIONAL — redirect URLs (can also set in Clerk Dashboard)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# OPTIONAL — webhooks
CLERK_WEBHOOK_SECRET=whsec_...
```

**Key format rules:**
- Publishable key: starts with `pk_test_` (dev) or `pk_live_` (prod) — must be the FULL key, not truncated
- Secret key: starts with `sk_test_` (dev) or `sk_live_` (prod) — must be the FULL key
- **The `NEXT_PUBLIC_` prefix is REQUIRED** for the publishable key — this is what exposes it to the browser. Without it, the frontend can't initialize Clerk.
- **For Next.js: use `.env.local`** not `.env`. Next.js loads `.env.local` with higher priority and it's gitignored by default.

---

## Critical File Locations (READ THIS FIRST)

**The #1 cause of Clerk build failures is putting the middleware file in the wrong location.** Follow these rules exactly:

### Next.js — Middleware/Proxy File Location

```
YOUR PROJECT STRUCTURE DETERMINES THE FILE LOCATION:

If your project has a src/ directory:
  → Place at: src/middleware.ts     (Next.js ≤15)
  → Place at: src/proxy.ts         (Next.js 16+)

If your project does NOT have a src/ directory:
  → Place at: ./middleware.ts       (Next.js ≤15)
  → Place at: ./proxy.ts           (Next.js 16+)

HOW TO CHECK:
  ls src/    # If this directory exists, middleware goes INSIDE it
```

**Next.js version detection:**
```bash
# Check your Next.js version
cat node_modules/next/package.json | grep '"version"'
# Next.js ≤15.x → use middleware.ts
# Next.js 16.x+ → use proxy.ts
# The CODE inside is identical — only the filename changes
```

### Express — No middleware file needed
Express uses route-level middleware, not a file convention. See Express section below.

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Authentication (Clerk)

- All authentication is handled by Clerk — do NOT build custom auth
- **CRITICAL: Middleware file location depends on project structure:**
  - If `src/` directory exists → `src/middleware.ts` (Next.js ≤15) or `src/proxy.ts` (Next.js 16+)
  - If NO `src/` directory → root `middleware.ts` (≤15) or `proxy.ts` (16+)
  - Getting this wrong causes: "clerkMiddleware() was not run" error
- **CRITICAL: For development, use keyless mode** — no env vars needed. Just install and run.
- **CRITICAL: For production, use `.env.local`** (not `.env`) for Next.js projects
- Protect routes using `auth.protect()` inside middleware — routes are PUBLIC by default
- Get current user: `const { userId } = await auth()` (server) or `useUser()` hook (client)
- User ID format: `user_2abc...` — always a string, never a number
- Session tokens expire and auto-refresh — never cache them long-term
- Webhooks from Clerk use `svix` for signature verification — always verify before processing
- Clerk user metadata: `publicMetadata` (readable by frontend) vs `privateMetadata` (server only)
- Organization ID: `orgId` from `auth()` — present when user is in an org context
```

---

## Standard Implementation Pattern

### Next.js (App Router) — Step by Step

**Step 1: Install**
```bash
npm install @clerk/nextjs@latest
```

**Step 2: Add middleware file (EXACT location matters)**

First, detect your project structure and Next.js version:
```bash
# Does src/ directory exist?
ls src/ 2>/dev/null && echo "USE src/" || echo "USE root"

# What Next.js version?
cat node_modules/next/package.json | grep '"version"'
```

Then create the file in the correct location:

```typescript
// FILE LOCATION: see "Critical File Locations" section above
// Next.js ≤15: middleware.ts (in src/ if it exists, otherwise root)
// Next.js 16+: proxy.ts (in src/ if it exists, otherwise root)

import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isPublicRoute = createRouteMatcher([
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',
  '/',  // Landing page is public
])

export default clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) {
    await auth.protect()
  }
})

export const config = {
  matcher: [
    // Skip Next.js internals and static files unless search params exist
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
}
```

**Step 3: Add ClerkProvider to root layout**

```typescript
// app/layout.tsx
import { ClerkProvider, SignInButton, SignUpButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header>
            <SignedOut>
              <SignInButton />
              <SignUpButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          <main>{children}</main>
        </body>
      </html>
    </ClerkProvider>
  )
}
```

**Step 4: Server-side auth check (API routes)**

```typescript
// app/api/protected/route.ts
import { auth } from '@clerk/nextjs/server'

export async function GET() {
  const { userId } = await auth()
  if (!userId) return new Response('Unauthorized', { status: 401 })
  // proceed with authenticated request
}
```

**Step 5: Client-side auth check (React components)**

```typescript
// app/dashboard/page.tsx
'use client'
import { useUser } from '@clerk/nextjs'

export default function Dashboard() {
  const { isLoaded, isSignedIn, user } = useUser()

  if (!isLoaded) return <div>Loading...</div>
  if (!isSignedIn) return <div>Please sign in</div>

  return <div>Welcome, {user.firstName}!</div>
}
```

### Express / Node.js

```typescript
// src/middleware/auth.ts
import { clerkClient } from '@clerk/express'

// Initialize Clerk Express middleware
export const clerkAuth = clerkClient.expressWithAuth()

// Require authentication on specific routes
export function requireAuth(req, res, next) {
  if (!req.auth?.userId) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  next()
}
```

```typescript
// src/index.ts — usage
import express from 'express'
import { clerkAuth, requireAuth } from './middleware/auth'

const app = express()

// Apply Clerk to all routes (parses session, doesn't block)
app.use(clerkAuth)

// Protected route
app.get('/api/profile', requireAuth, (req, res) => {
  res.json({ userId: req.auth.userId })
})

// Public route (no requireAuth)
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})
```

---

## Webhook Setup (User Lifecycle Events)

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix'
import { WebhookEvent } from '@clerk/nextjs/server'

export async function POST(req: Request) {
  const body = await req.text()
  const svixId = req.headers.get('svix-id')
  const svixTimestamp = req.headers.get('svix-timestamp')
  const svixSignature = req.headers.get('svix-signature')

  if (!svixId || !svixTimestamp || !svixSignature) {
    return new Response('Missing svix headers', { status: 400 })
  }

  const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!)
  let event: WebhookEvent

  try {
    event = wh.verify(body, {
      'svix-id': svixId,
      'svix-timestamp': svixTimestamp,
      'svix-signature': svixSignature,
    }) as WebhookEvent
  } catch {
    return new Response('Invalid signature', { status: 400 })
  }

  // Handle events
  switch (event.type) {
    case 'user.created':
      // Sync user to your database
      break
    case 'user.updated':
      // Update user in your database
      break
    case 'user.deleted':
      // Remove or soft-delete user
      break
  }

  return new Response('OK')
}
```

---

## Pre-Flight Validation (MANDATORY Before First Build)

**Agents MUST run these checks before attempting `npm run build` or `npm run dev`:**

```bash
# CHECK 1: Middleware file exists in correct location
if [ -d "src" ]; then
  # src/ directory exists — middleware must be inside it
  if [ -f "src/middleware.ts" ] || [ -f "src/proxy.ts" ]; then
    echo "✅ Middleware file correctly placed in src/"
  else
    echo "❌ FAIL: Middleware file missing from src/ directory"
    echo "   Create src/middleware.ts (Next.js ≤15) or src/proxy.ts (Next.js 16+)"
  fi
  # Also check it's NOT in root (common mistake)
  if [ -f "middleware.ts" ] || [ -f "proxy.ts" ]; then
    echo "⚠️  WARNING: Middleware file found in BOTH root and src/ — remove the root one"
  fi
else
  # No src/ directory — middleware goes in root
  if [ -f "middleware.ts" ] || [ -f "proxy.ts" ]; then
    echo "✅ Middleware file correctly placed in root"
  else
    echo "❌ FAIL: Middleware file missing from project root"
  fi
fi

# CHECK 2: ClerkProvider in layout
grep -l "ClerkProvider" app/layout.tsx src/app/layout.tsx 2>/dev/null \
  && echo "✅ ClerkProvider found in layout" \
  || echo "❌ FAIL: ClerkProvider not found in layout.tsx"

# CHECK 3: Environment variables (skip if using keyless mode)
if [ -f ".env.local" ]; then
  grep -q "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_" .env.local \
    && echo "✅ Publishable key present" \
    || echo "⚠️  No publishable key in .env.local (OK if using keyless mode)"
  grep -q "CLERK_SECRET_KEY=sk_" .env.local \
    && echo "✅ Secret key present" \
    || echo "⚠️  No secret key in .env.local (OK if using keyless mode)"
else
  echo "ℹ️  No .env.local file — using keyless mode (OK for development)"
fi

# CHECK 4: Package installed
grep -q "@clerk/nextjs" package.json \
  && echo "✅ @clerk/nextjs installed" \
  || echo "❌ FAIL: @clerk/nextjs not in package.json — run npm install @clerk/nextjs@latest"
```

**Run this BEFORE every first build. If any check fails, fix it before proceeding.**

---

## Known Issues & Fixes

| Issue | Error Message | Cause | Fix |
|-------|--------------|-------|-----|
| **Invalid publishable key** | `The publishableKey passed to Clerk is invalid` | Key is truncated, missing, or in wrong env file | Use FULL key from Clerk Dashboard. Put in `.env.local` (not `.env`). Ensure `NEXT_PUBLIC_` prefix. Or use keyless mode (no key needed for dev). |
| **Middleware not detected** | `clerkMiddleware() was not run, your middleware or proxy file might be misplaced` | Middleware file in wrong location | If `src/` directory exists, file MUST be at `src/middleware.ts` (≤15) or `src/proxy.ts` (16+). NOT in project root. |
| **Middleware file wrong name** | `clerkMiddleware() was not run` | Using `middleware.ts` on Next.js 16+ | Next.js 16+ renamed middleware to proxy. Rename file to `proxy.ts`. |
| **auth() returns null** | No error — just null userId | Route not matched by middleware | Check `matcher` pattern includes the route. Use the updated matcher config from this module. |
| **Token verification fails** | `Token verification failed` | Wrong secret key (test vs prod mismatch) | Verify `CLERK_SECRET_KEY` matches the environment (test key for dev, live key for prod). |
| **Organization context missing** | `orgId` is undefined | User not in an org | Check `orgId` for null before using org-scoped data. |
| **Webhook signature invalid** | `Invalid signature` | Wrong webhook secret or body modified | Copy fresh secret from Clerk Dashboard → Webhooks → your endpoint. Ensure `req.text()` not `req.json()`. |
| **Social login redirect fails** | Redirect loop or 404 | Redirect URL not whitelisted | Add URL to Clerk Dashboard → Allowed redirect URLs (include `http://localhost:3000` for dev). |
| **Build fails on Vercel/Railway** | Various env-related errors | Missing env vars in deployment platform | Set `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` in deployment platform's env settings (not just `.env.local`). |
| **Hydration mismatch** | React hydration error on auth components | Server/client auth state mismatch | Ensure `<ClerkProvider>` wraps the `<html>` tag in root layout, not a child component. |

---

## Test Coverage Required

```typescript
// tests/auth/clerk.test.ts
describe('Authentication', () => {
  // Middleware
  it('should allow access to public routes without auth')
  it('should redirect to sign-in for protected routes without auth')
  it('should allow authenticated access to protected routes')

  // API routes
  it('should return 401 for unauthenticated requests to protected API routes')
  it('should return user data for authenticated requests')
  it('should return userId from auth() in server components')

  // Webhooks
  it('should verify webhook signatures before processing')
  it('should reject webhooks with invalid signatures')
  it('should reject webhooks with missing svix headers')
  it('should sync user to database on user.created webhook')

  // Client
  it('should render SignInButton when signed out')
  it('should render UserButton when signed in')
})
```

---

## Dashboard Setup Checklist

### Development (Keyless Mode — No Dashboard Needed)
- [ ] Install `@clerk/nextjs@latest`
- [ ] Add middleware file in correct location (see Critical File Locations)
- [ ] Add `<ClerkProvider>` to `app/layout.tsx`
- [ ] Run `npm run dev` — Clerk creates temporary dev instance
- [ ] Verify: sign-in button appears, clicking it opens Clerk modal

### Production (Explicit Keys)
- [ ] Create Clerk application at [clerk.com](https://clerk.com)
- [ ] Copy **full** publishable key (`pk_live_...`) to `.env.local` as `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- [ ] Copy **full** secret key (`sk_live_...`) to `.env.local` as `CLERK_SECRET_KEY`
- [ ] Set same keys in deployment platform env settings (Vercel/Railway/etc.)
- [ ] Configure allowed redirect URLs (include production domain)
- [ ] Enable desired social providers (Google, GitHub, etc.)
- [ ] Set up webhook endpoint (your domain + `/api/webhooks/clerk`)
- [ ] Copy webhook signing secret to `CLERK_WEBHOOK_SECRET` env var
- [ ] Run pre-flight validation script (see above)
- [ ] Test: `npm run build` succeeds with no Clerk errors
- [ ] Test: sign in/sign up flow works end-to-end

---

## Module Philosophy

**If this module's instructions produce a build failure, that's a bug in the module — not in the agent or the code.** Every instruction must be precise enough that an AI agent following them step-by-step produces a working authentication system on first build. If you encounter a new failure mode, add it to Known Issues with the exact error message, cause, and fix.

---

*Module maintained by AgentBuild. v2 updated 2026-02-21 — added keyless mode, fixed middleware location for src/ projects, added pre-flight validation, updated matcher config, expanded Known Issues with real failure cases.*
