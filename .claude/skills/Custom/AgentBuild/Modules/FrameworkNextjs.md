# Module: Framework — Next.js (App Router)

> The React framework for production. App Router architecture with server components, file-based routing, and built-in optimization. The foundation layer that all other modules build on.

**Module status:** BETA (v2 — updated 2026-02-21, Council + RedTeam reviewed)
**When to use:** Any project using Next.js as its framework (the default for AgentBuild TypeScript projects)
**When NOT to use:** Express-only APIs, React SPAs (Vite/CRA), non-TypeScript projects

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Routing | File-based routing with App Router (layouts, pages, loading, error boundaries) |
| Server Components | Default server rendering — zero client JS unless opted in |
| API Routes | Route Handlers for REST endpoints (`route.ts`) |
| Server Actions | Direct server mutations from client forms (`"use server"`) |
| Optimization | Image, font, and script optimization built in |
| Deployment | Standalone output for Docker/Railway, static export for CDN |
| Proxy | Request interception (formerly middleware) for auth, redirects, rewrites |

---

## Version Detection

**This module covers Next.js 14, 15, and 16+.** Version-specific differences use WHEN blocks.

### DETECT: Next.js version

```bash
# Read version from package.json
node -e "console.log(require('./package.json').dependencies?.next || require('./package.json').devDependencies?.next)" 2>/dev/null

# Or check installed version
npx next --version 2>/dev/null
```

### Version Matrix

| Version | React | Node.js | Key Convention Changes |
|---------|-------|---------|----------------------|
| 14.x | 18.x | 18.17+ | Stable App Router, Server Actions stable |
| 15.x | 18.x (Pages) / 19.x (App Router) | 18.18+ | Async request APIs (`params` is Promise), `next.config.ts` support, caching defaults reversed |
| 16.x | 19.2+ | 20.9+ (Node 18 NOT supported) | `middleware.ts` → `proxy.ts`, Turbopack default, `next lint` removed, async APIs enforced |

> **Note:** App Router in v15+ requires React 19. Pages Router in v15 still works with React 18. Upgrade incrementally: v14→v15 first, validate, then v15→v16.

---

## Project Structure

### Standard Structure (Recommended)

```
project-root/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout (REQUIRED — must have <html> and <body>)
│   │   ├── page.tsx                # Home page (/)
│   │   ├── not-found.tsx           # Custom 404
│   │   ├── error.tsx               # Root error boundary ("use client" required)
│   │   ├── loading.tsx             # Root loading UI
│   │   ├── globals.css             # Global styles
│   │   ├── _components/            # Shared components (underscore = private, not routed)
│   │   ├── (marketing)/            # Route group (parentheses = no URL impact)
│   │   │   └── about/
│   │   │       └── page.tsx        # /about
│   │   ├── dashboard/
│   │   │   ├── page.tsx            # /dashboard
│   │   │   ├── layout.tsx          # Dashboard-specific layout
│   │   │   ├── loading.tsx         # Dashboard loading UI
│   │   │   └── error.tsx           # Dashboard error boundary
│   │   └── api/
│   │       ├── health/
│   │       │   └── route.ts        # GET /api/health
│   │       └── users/
│   │           ├── route.ts        # GET, POST /api/users
│   │           └── [id]/
│   │               └── route.ts    # GET, PUT, DELETE /api/users/:id
│   ├── lib/                        # Utilities, data access, constants
│   └── types/                      # TypeScript interfaces
├── public/                         # Static assets (served at /)
│   ├── images/
│   └── fonts/
├── proxy.ts                        # WHEN: nextjs >= 16 (was middleware.ts)
├── middleware.ts                    # WHEN: nextjs < 16
├── next.config.ts                  # WHEN: nextjs >= 15 (was next.config.js)
├── next.config.js                  # WHEN: nextjs < 15
├── tsconfig.json
├── .env.local                      # Local env vars (gitignored)
└── package.json
```

### Verify: Project Structure

```bash
# Check root layout exists
[ -f "src/app/layout.tsx" ] || [ -f "app/layout.tsx" ] && echo "PASS: Root layout found" || echo "FAIL: No root layout — create src/app/layout.tsx"

# Check no conflicting directories
[ -d "src/app" ] && [ -d "app" ] && echo "FAIL: Both src/app/ and app/ exist — delete one" || echo "PASS: No directory conflict"

# Check proxy/middleware file location
if [ -d "src" ]; then
  [ -f "src/proxy.ts" ] || [ -f "src/middleware.ts" ] && echo "PASS: Proxy/middleware in src/" || echo "INFO: No proxy/middleware file (optional)"
else
  [ -f "proxy.ts" ] || [ -f "middleware.ts" ] && echo "PASS: Proxy/middleware at root" || echo "INFO: No proxy/middleware file (optional)"
fi
```

---

## Special File Conventions

### Route Segment Files (inside `app/`)

| File | Purpose | Requirements |
|------|---------|-------------|
| `page.tsx` | Makes route publicly accessible | Required for any visitable URL |
| `layout.tsx` | Wraps children, persists across navigation | Root layout MUST have `<html>` + `<body>` |
| `template.tsx` | Like layout but remounts on navigation | Creates unique key per route segment |
| `loading.tsx` | Instant loading UI (React Suspense boundary) | Optional but recommended |
| `error.tsx` | Error boundary for route segment | MUST be `"use client"` |
| `not-found.tsx` | UI when `notFound()` called or route not found | Optional |
| `route.ts` | API Route Handler | CANNOT coexist with `page.tsx` in same segment |
| `default.tsx` | Fallback for parallel route slots | Required for parallel routes in v16+ |

### Project Root Files (outside `app/`)

| File | Purpose | Version |
|------|---------|---------|
| `proxy.ts` | Request interceptor (auth, redirects, rewrites) | 16+ (replaces middleware.ts) |
| `middleware.ts` | Request interceptor (deprecated) | 14, 15 |
| `instrumentation.ts` | Server lifecycle hooks | 14 (experimental flag) / 15+ (stable) |
| `next.config.ts` | Framework configuration | 15+ (.ts), 14 (.js only) |

### Directory Conventions

| Convention | Example | Effect |
|-----------|---------|--------|
| `[slug]` | `app/blog/[slug]/page.tsx` | Dynamic route segment |
| `[...slug]` | `app/shop/[...slug]/page.tsx` | Catch-all route |
| `[[...slug]]` | `app/shop/[[...slug]]/page.tsx` | Optional catch-all (also matches parent) |
| `(group)` | `app/(marketing)/about/page.tsx` | Route group (excluded from URL) |
| `@slot` | `app/@analytics/page.tsx` | Parallel route slot |
| `_folder` | `app/_components/Button.tsx` | Private folder (not routed) |

---

## Server Components vs Client Components

### The Rule

**All components in `app/` are Server Components by default.** No directive needed.

To make a Client Component, add `'use client'` as the very first line, above all imports:

```tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### When to Use Which

| Need | Component Type | Why |
|------|---------------|-----|
| Fetch data, access DB, use secrets | Server | Direct access, zero client JS |
| `useState`, `useEffect`, `useRef` | Client | React hooks require client runtime |
| `onClick`, `onChange`, event handlers | Client | Browser events |
| `window`, `localStorage`, `navigator` | Client | Browser APIs |
| Static content, no interactivity | Server | Default — no reason to change |

### Critical Rules

1. **`'use client'` declares a boundary** — all imports below it become client-side
2. **Add it as deep as possible** — minimizes client JS bundle
3. **Server Components can import Client Components** — but not the reverse
4. **Pass Server Components as `children` to Client Components** — the interleaving pattern
5. **Props crossing the boundary must be serializable** — no functions, no classes
6. **Third-party components without `'use client'`: wrap them** in your own Client Component file

### Environment Poisoning Prevention

```bash
npm install server-only client-only
```

```tsx
// lib/db.ts — MUST never be imported client-side
import 'server-only'
import { createClient } from '@supabase/supabase-js'
// Safe: build error if imported from "use client" file
```

---

## Environment Variables

### Loading Order (highest priority first)

1. `process.env` (system/runtime)
2. `.env.$(NODE_ENV).local` (e.g., `.env.development.local`)
3. `.env.local` (NOT loaded when `NODE_ENV=test`)
4. `.env.$(NODE_ENV)` (e.g., `.env.development`)
5. `.env`

### NEXT_PUBLIC_ Prefix Rule

| Variable Type | Available Where | When Resolved |
|--------------|----------------|---------------|
| `NEXT_PUBLIC_*` | Server + Client (browser) | **Build time** (inlined during `next build`) |
| Everything else | Server only | Runtime |

**CRITICAL:** `NEXT_PUBLIC_` values are frozen at build time. Changing them requires a rebuild. For runtime-dynamic values, use server-side APIs.

### .env File Location

`.env*` files MUST be in the **project root** (same directory as `package.json`). NOT inside `src/`.

### Verify: Environment Variables

```bash
# Check .env.local exists
[ -f ".env.local" ] && echo "PASS: .env.local found" || echo "WARN: No .env.local — create from .env.example"

# Check no .env files inside src/
ls src/.env* 2>/dev/null && echo "FAIL: .env files inside src/ — move to project root" || echo "PASS: No .env in src/"

# Check NEXT_PUBLIC_ vars are not secrets
grep -E "^NEXT_PUBLIC_.*SECRET|^NEXT_PUBLIC_.*PASSWORD|^NEXT_PUBLIC_.*KEY.*=.*[a-zA-Z0-9]{20,}" .env.local 2>/dev/null && echo "FAIL: Possible secret in NEXT_PUBLIC_ var" || echo "PASS: No obvious secrets in public vars"
```

---

## Configuration

### WHEN: nextjs >= 15 (TypeScript config)

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Output mode (choose one):
  // output: 'standalone',    // For Docker/Railway — minimal server bundle
  // output: 'export',        // For static hosting — no server required

  // Security
  poweredByHeader: false,

  // Images
  images: {
    remotePatterns: [
      // Object syntax (works in all versions):
      // { protocol: 'https', hostname: 'your-cdn.com', pathname: '/**' },
      // URL syntax (v15.3+ only):
      // new URL('https://your-cdn.com/**'),
    ],
  },

  // Security headers (recommended for production)
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
        ],
      },
    ]
  },
}

export default nextConfig
```

### Verify: Configuration

```bash
# Check config file exists
[ -f "next.config.ts" ] || [ -f "next.config.js" ] && echo "PASS: Config found" || echo "FAIL: No next.config file"

# Check output mode for deployment
grep -q "output.*standalone" next.config.* 2>/dev/null && echo "INFO: Standalone mode (Docker/Railway)" || echo "INFO: Default output mode"
```

### WHEN: nextjs < 15 (JavaScript config)

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
}

module.exports = nextConfig
```

---

## Proxy / Middleware Setup

### WHEN: nextjs >= 16 (proxy.ts)

> **WARNING: `proxy.ts` runs on Node.js runtime ONLY.** Edge runtime is NOT supported. If your current `middleware.ts` uses `export const config = { runtime: 'edge' }`, do NOT migrate to `proxy.ts`. Edge runtime use cases must remain in `middleware.ts` (still functional in v16, just deprecated).

```typescript
// proxy.ts (project root, or src/proxy.ts if using src/)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Example: protect dashboard routes
  // const session = request.cookies.get('session')
  // if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
  //   return NextResponse.redirect(new URL('/login', request.url))
  // }
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Match all paths except static files and Next.js internals
    '/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}
```

### WHEN: nextjs < 16 (middleware.ts)

```typescript
// middleware.ts (same location rules as proxy.ts)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)',
  ],
}
```

### Migration Codemod (middleware → proxy)

```bash
npx @next/codemod@latest middleware-to-proxy .
```

This renames the file and the exported function automatically.

---

## Request APIs (Version-Dependent)

### WHEN: nextjs >= 15 (async APIs — CRITICAL)

In Next.js 15+, `params`, `searchParams`, `cookies()`, `headers()`, and `draftMode()` are **Promises** and MUST be awaited:

```typescript
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <h1>{slug}</h1>
}
```

```typescript
// app/api/users/route.ts
import { cookies, headers } from 'next/headers'

export async function GET() {
  const cookieStore = await cookies()
  const headerList = await headers()
  const token = cookieStore.get('token')
  return Response.json({ token: token?.value })
}
```

For Client Components, use `React.use()` instead of `await`:

```tsx
'use client'
import { use } from 'react'

export default function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params)
  return <h1>{slug}</h1>
}
```

**Codemod for migration:** `npx @next/codemod@latest next-async-request-api .`

### WHEN: nextjs 14 (synchronous APIs)

```typescript
// app/blog/[slug]/page.tsx
export default function Page({ params }: { params: { slug: string } }) {
  return <h1>{params.slug}</h1>
}
```

```typescript
// app/api/users/route.ts
import { cookies, headers } from 'next/headers'

export async function GET() {
  const cookieStore = cookies()    // No await needed in v14
  const headerList = headers()
  return Response.json({ token: cookieStore.get('token')?.value })
}
```

---

## Route Handler Pattern

```typescript
// app/api/users/route.ts — typed Route Handler example
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const page = searchParams.get('page') ?? '1'
  // fetch data...
  return NextResponse.json({ users: [], page })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  // validate and create...
  return NextResponse.json({ id: 'new-id' }, { status: 201 })
}
```

> **Do NOT use `(req, res)` signature.** Route Handlers use Web API `Request`/`Response`, not Express-style `req, res`.

---

## Server Actions Pattern

```typescript
// app/actions.ts — Server Action file
'use server'

import { revalidatePath } from 'next/cache'

export async function createItem(formData: FormData) {
  const title = formData.get('title') as string
  // insert into database...
  revalidatePath('/items')  // Invalidate cache after mutation
}
```

```tsx
// app/items/page.tsx — using Server Action in a form
import { createItem } from '@/app/actions'

export default function ItemsPage() {
  return (
    <form action={createItem}>
      <input name="title" required />
      <button type="submit">Add Item</button>
    </form>
  )
}
```

> **`"use server"` at file level** marks ALL exports as Server Actions. At function level, marks only that function. Server Actions automatically get CSRF protection. Route Handlers (`route.ts`) do NOT — implement CSRF manually if using cookies for auth.

---

## Static Generation Pattern (replaces getStaticProps)

```typescript
// app/blog/[slug]/page.tsx — generateStaticParams replaces getStaticPaths + getStaticProps

// This generates static pages at build time for known slugs
export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

// The page itself is a regular async Server Component
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>  // WHEN: nextjs >= 15 (Promise type)
}) {
  const { slug } = await params
  const post = await getPost(slug)
  return <article><h1>{post.title}</h1><p>{post.content}</p></article>
}
```

---

## Build & Dev Commands

### WHEN: nextjs >= 16

| Command | Purpose | Notes |
|---------|---------|-------|
| `next dev` | Development server | Turbopack by default |
| `next dev --webpack` | Dev with Webpack | Only if Turbopack incompatible |
| `next build` | Production build | Turbopack by default |
| `next build --webpack` | Build with Webpack | Only if custom webpack config |
| `next start` | Start production server | Requires `next build` first |
| `next typegen` | Generate TypeScript definitions | For typed routes |

### WHEN: nextjs 14-15

| Command | Purpose | Notes |
|---------|---------|-------|
| `next dev` | Development server | Webpack by default in both v14 and v15 |
| `next dev --turbopack` | Dev with Turbopack | Explicit opt-in — stable in v15, experimental in v14 |
| `next build` | Production build | Always Webpack (Turbopack build not available) |
| `next start` | Start production server | Requires `next build` first |
| `next lint` | Run ESLint | Removed in v16 — use ESLint CLI directly |

### Verify: Build

```bash
# Dev server starts successfully
npx next dev --port 3001 &
sleep 5
curl -f http://localhost:3001 > /dev/null 2>&1 && echo "PASS: Dev server running" || echo "FAIL: Dev server failed to start"
curl -f http://localhost:3001/api/health > /dev/null 2>&1 && echo "PASS: Health endpoint responding" || echo "WARN: No /api/health endpoint"
kill %1 2>/dev/null
```

---

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Key settings:**
- `"moduleResolution": "bundler"` — required for App Router (not `"node"`)
- `"paths": { "@/*": ["./src/*"] }` — adjust to `["./*"]` if not using `src/`
- `"plugins": [{ "name": "next" }]` — enables typed routes and segment config validation
- `"jsx": "preserve"` — Next.js handles JSX transformation
- **Do not change** `jsx`, `moduleResolution`, `module`, `resolveJsonModule`, `isolatedModules`, `incremental` — Next.js overwrites these on `next dev`

---

## Docker Deployment Pattern

### Dockerfile (Standalone Output)

**Create `.dockerignore` first** (prevents secrets and bloat in image):

```
node_modules
.next
.env*.local
.git
```

```dockerfile
# Pin to minor.patch — match Node.js minimum for your Next.js version
# v14-15: node:18.18-alpine | v16+: node:20.18-alpine
FROM node:20.18-alpine AS base

# Stage 1: Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: Production runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

# Copy standalone build + static assets
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', r => process.exit(r.statusCode === 200 ? 0 : 1))" || exit 1

CMD ["node", "server.js"]
```

**Requires** `output: 'standalone'` in `next.config.ts`.

> **Note:** `HOSTNAME="0.0.0.0"` is required for Docker — binds the server to all interfaces so the container is reachable. Do not remove it.

### Verify: Docker Build

```bash
docker build -t app . && docker run -p 3000:3000 app &
sleep 5
curl -f http://localhost:3000 > /dev/null 2>&1 && echo "PASS: Docker container running" || echo "FAIL: Container failed"
docker stop $(docker ps -q --filter ancestor=app) 2>/dev/null
```

---

## Breaking Change Registry

### Next.js 14 → 15

| Change | Impact | Codemod |
|--------|--------|---------|
| `params`, `searchParams` are Promises | All pages, layouts, routes, metadata | `npx @next/codemod@latest next-async-request-api .` |
| `cookies()`, `headers()` are Promises | All server-side code using these | Same codemod |
| `fetch()` no longer cached by default | Data fetching behavior changes | Add `cache: 'force-cache'` where needed |
| React 19 required | `useFormState` → `useActionState` | Update React deps |
| `useFormState` → `useActionState` | Import from `react` not `react-dom`, extra initial state arg | Manual — change import and add initial state param |
| `next.config.ts` support added | Optional — .js still works | Rename file, add types |
| `ImageResponse` import changed | Already moved to `next/og` in v14 — verify import is correct | `npx @next/codemod@latest next-og-import .` |

### Next.js 15 → 16

| Change | Impact | Codemod |
|--------|--------|---------|
| `middleware.ts` → `proxy.ts` | Auth, redirects, rewrites | `npx @next/codemod@latest middleware-to-proxy .` |
| Turbopack is default bundler | Custom webpack configs break | Use `--webpack` flag or migrate |
| `next lint` removed | CI/CD lint steps | Use ESLint CLI directly |
| Async APIs enforced (no `UnsafeUnwrapped`) | All v15 code using sync fallback | Must await all request APIs |
| `experimental.turbo` → `turbopack` (top-level) | Config structure | Move config key |
| AMP support removed entirely | Any AMP pages | Remove AMP code |
| `images.domains` deprecated | Image config | Use `images.remotePatterns` |
| `serverRuntimeConfig`/`publicRuntimeConfig` removed | Runtime config | Use `process.env` |
| `cacheLife`/`cacheTag` stable (`unstable_` removed) | Cache APIs | `npx @next/codemod@latest remove-unstable-prefix .` |
| Parallel routes require `default.tsx` | All parallel route slots | Add `default.tsx` to each slot |
| Node.js 20.9+ required | CI/CD, Docker images | Update base images |

### Full Upgrade Command

> **Recommended: Upgrade one major version at a time.** Run v14→v15 first, validate, then v15→v16. Skipping versions makes debugging codemod failures much harder.

```bash
# Upgrade to latest and run all relevant codemods
npx @next/codemod@canary upgrade latest
```

---

## Stale Pattern Detection (AI Agent Guard Rails)

These patterns are WRONG in App Router. An AI agent generating any of these has stale training data:

| Wrong Pattern | Correct Pattern | Detection Signal |
|--------------|----------------|-----------------|
| `getServerSideProps` | Async Server Component | Import or export of `getServerSideProps` |
| `getStaticProps` | Async Server Component + `generateStaticParams` | Import or export of `getStaticProps` |
| `getInitialProps` | Server Components | Import or export of `getInitialProps` |
| `pages/api/` directory | `app/api/*/route.ts` | Files in `pages/api/` |
| `import { useRouter } from 'next/router'` | `import { useRouter } from 'next/navigation'` | Import from `next/router` |
| `import Head from 'next/head'` | `export const metadata` or `generateMetadata()` | Import of `next/head` |
| `<Link><a>text</a></Link>` | `<Link>text</Link>` | `<a>` inside `<Link>` |
| `_app.tsx` or `_document.tsx` | `app/layout.tsx` | Files named `_app` or `_document` |
| `import Image from 'next/legacy/image'` | `import Image from 'next/image'` | Import from `next/legacy/image` |
| `const params = cookies()` (sync in v15+) | `const params = await cookies()` | Missing `await` on request APIs |
| `import { useFormState } from 'react-dom'` | `import { useActionState } from 'react'` | Import of `useFormState` from `react-dom` |

### Verify: No Stale Patterns

```bash
# Check for Pages Router patterns in app/ directory
grep -r "getServerSideProps\|getStaticProps\|getInitialProps" src/app/ app/ 2>/dev/null && echo "FAIL: Pages Router patterns found in App Router" || echo "PASS: No Pages Router patterns"

# Check for wrong router import
grep -r "from 'next/router'" src/ app/ 2>/dev/null && echo "FAIL: Using next/router (Pages Router) — use next/navigation" || echo "PASS: Correct router import"

# Check for next/head usage
grep -r "from 'next/head'" src/ app/ 2>/dev/null && echo "FAIL: Using next/head — use metadata export" || echo "PASS: No next/head usage"

# WHEN: nextjs >= 15 — Check for sync request API usage
grep -rn "const.*=\s*cookies()\|const.*=\s*headers()\|const.*=\s*draftMode()" src/ app/ 2>/dev/null | grep -v "await" && echo "FAIL: Sync request API usage — must await in v15+" || echo "PASS: Request APIs properly awaited"

# WHEN: nextjs >= 15 — Check for deprecated useFormState
grep -r "useFormState" src/ app/ 2>/dev/null && echo "FAIL: useFormState is deprecated — use useActionState from 'react'" || echo "PASS: No deprecated useFormState"
```

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Framework (Next.js / App Router)

- Framework: Next.js [VERSION] with App Router — NEVER use Pages Router patterns
- All components are Server Components by default — add `'use client'` only when needed
- NEVER use `getServerSideProps`, `getStaticProps`, `getInitialProps`, or `pages/api/`
- Use `import { useRouter } from 'next/navigation'` — NOT `next/router`
- Use `export const metadata` or `generateMetadata()` — NOT `next/head`
- WHEN v15+: `params`, `searchParams`, `cookies()`, `headers()` are Promises — MUST await
- WHEN v16+: Use `proxy.ts` with `export function proxy()` — NOT `middleware.ts`
- WHEN v16+: Turbopack is default — custom webpack configs require `--webpack` flag
- WHEN v16+: `next lint` removed — use ESLint CLI directly
- Environment variables: `NEXT_PUBLIC_*` = client-exposed (build-time), everything else = server-only
- `.env.local` in project root (NOT inside `src/`)
- Route Handlers: `app/api/*/route.ts` — cannot coexist with `page.tsx` in same directory
- Error boundaries (`error.tsx`) MUST have `'use client'` directive
- Docker: requires `output: 'standalone'` in next.config + copy public/ and .next/static/
- Path alias: `@/` maps to project root or `src/` — configured in tsconfig.json paths
```

---

## Known Issues & Fixes

| Issue | Error Message | Version | Cause | Fix |
|-------|--------------|---------|-------|-----|
| Server/client boundary violation | `You're importing a component that needs useState` | All | Using hooks in Server Component | Add `'use client'` to the file |
| Wrong router import | `NextRouter was not mounted` | All | Using `next/router` in App Router | Change to `next/navigation` |
| Metadata in client component | `You are attempting to export "metadata" from a component marked with "use client"` | All | `metadata` export in `'use client'` file | Remove `'use client'` or extract interactive parts |
| Sync request API in v15+ | `Type 'Promise<{ slug: string }>' is not assignable` | 15+ | Not awaiting `params`/`cookies`/`headers` | Add `await` — run codemod: `npx @next/codemod@latest next-async-request-api .` |
| Middleware not running | (silent — no error, just ignored) | All | File in wrong location | Must be at project root (or `src/` root), NOT inside `app/` |
| Middleware deprecated warning | `The "middleware" file convention is deprecated` | 16+ | Using `middleware.ts` instead of `proxy.ts` | Run: `npx @next/codemod@latest middleware-to-proxy .` |
| Webpack config breaks build | `Turbopack does not support custom webpack configurations` | 16+ | Turbopack is now default | Use `next build --webpack` or migrate config |
| Hydration mismatch | `Text content does not match server-rendered HTML` | All | Server/client render different content | Use `useEffect` for client-only values, `suppressHydrationWarning` on `<body>` for extension injection |
| Image optimization in static export | `Image Optimization using the default loader is not compatible with output: 'export'` | All | `<Image>` needs server for optimization | Add `images: { unoptimized: true }` to config |
| Missing static assets in Docker | Static files return 404 in production | All | `output: 'standalone'` doesn't copy `public/` or `.next/static/` | Copy manually in Dockerfile |
| `@/` path alias not found | `Cannot find module '@/components/Button'` | All | tsconfig.json misconfigured | Set `"paths": { "@/*": ["./src/*"] }` and `"moduleResolution": "bundler"` |
| Both `app/` and `src/app/` exist | Routes in `src/app/` silently 404 | All | Next.js uses root `app/` and ignores `src/app/` | Delete one — never have both |
| Heap out of memory during build | `FATAL ERROR: Reached heap limit` | All | Default Node.js heap too small | `NODE_OPTIONS="--max-old-space-size=8192" next build` |
| Parallel route 404 on hard nav | 404 for unmatched parallel route slots | 16+ | Missing `default.tsx` in slot | Add `default.tsx` to every `@slot` directory |
| Sass tilde imports fail | `Module not found: Can't resolve '~bootstrap/scss/bootstrap'` | 16+ | Turbopack doesn't support `~` prefix | Remove tilde: `@import 'bootstrap/scss/bootstrap'` |

---

## Test Coverage Required

```typescript
// tests/framework/structure.test.ts
describe('Next.js project structure', () => {
  it('should have a root layout with html and body tags')
  it('should have no Pages Router patterns in app/ directory')
  it('should use next/navigation imports, not next/router')
  it('should have error.tsx marked as "use client"')
})

// tests/framework/env.test.ts
describe('Environment variables', () => {
  it('should have .env.local at project root, not inside src/')
  it('should not expose secrets via NEXT_PUBLIC_ prefix')
  it('should have all required env vars defined')
})

// tests/framework/api-routes.test.ts
describe('API Route Handlers', () => {
  it('should respond to GET /api/health with 200')
  it('should use route.ts convention, not pages/api/')
  it('should not have route.ts and page.tsx in same directory')
})
```

---

## Dashboard Setup Checklist

### New Project Setup
- [ ] Run `npx create-next-app@latest` with App Router, TypeScript, Tailwind, src/ directory
- [ ] Verify root layout has `<html>` and `<body>` tags
- [ ] Create `.env.local` from `.env.example`
- [ ] Add `loading.tsx` and `error.tsx` to key route segments
- [ ] Set `output: 'standalone'` if deploying to Docker/Railway
- [ ] Configure `images.remotePatterns` for external image hosts
- [ ] Remove `x-powered-by` header: `poweredByHeader: false`
- [ ] Install `server-only` package for server-side data access files

### Version Upgrade
- [ ] Run `npx @next/codemod@canary upgrade latest` — applies all relevant codemods
- [ ] Check for async request API changes (v14→15): `params`, `cookies()`, `headers()` now Promises
- [ ] Check for middleware→proxy rename (v15→16): `middleware.ts` → `proxy.ts`
- [ ] Check for Turbopack compatibility (v16): custom webpack configs need `--webpack` flag
- [ ] Update Node.js to 20.9+ (required for v16)
- [ ] Update React to 19.2+ (required for v16)
- [ ] Run `npx next typegen` to regenerate TypeScript definitions

---

## Module Cross-References

This is a **foundation module**. Other modules reference Next.js conventions documented here:

| Module | What It References |
|--------|--------------------|
| `AuthClerk.md` | Proxy/middleware file location, route protection patterns |
| `DbSupabase.md` | Server/client component patterns, env variable rules |
| `DeployRailway.md` | Build commands, standalone output mode, health check route |
| `ObservabilitySentry.md` | Error boundary integration, `instrumentation.ts` hook |
| `ChatInterface.md` | API route patterns, server/client component split |

When this module's conventions change (e.g., middleware→proxy), check all referencing modules for stale instructions.

---

*Module created by ModuleBuilder. v1 created 2026-02-21.*
*v2 updated 2026-02-21: Council (5-perspective) + RedTeam review applied. Fixed: React version matrix (App vs Pages Router), Turbopack not default in v15, proxy.ts Node.js-only runtime warning, instrumentation.ts v14 availability, Docker base image pinning + HEALTHCHECK + .dockerignore, security headers in next.config, remotePatterns version gating, useFormState stale detection, ImageResponse version correction, incremental upgrade recommendation. Added: Route Handler pattern, Server Actions pattern, generateStaticParams pattern, CSRF guidance. Promoted to BETA.*
*Research sources: Official Next.js documentation (nextjs.org/docs), Next.js GitHub releases, Next.js blog posts, community issue threads. See research agent outputs for full citations.*
