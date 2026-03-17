# Module: Framework — React SPA

> React 18/19 + Vite 5/6 + React Router v7 (Data Mode) + TanStack Query v5 + Zustand v4/v5. Opinionated production baseline for client-only single-page applications. AI-consumable spec: every decision is deterministic, branching is explicit, no ambiguity tolerated.

**Module status:** DRAFT (v1 — created 2026-02-23)
**Proven on:** Research-phase (not yet battle-tested on a live AgentBuild project)
**When to use:** Client-only SPAs requiring routing, server-state, and client-state — no SSR, no server components, no file-based routing
**When NOT to use:** Projects needing SSR or server components (use FrameworkNextjs); projects where TanStack Router file-based routing is preferred; static marketing sites with no interactivity

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| Build tooling | Vite 5/6 with `@vitejs/plugin-react`, HMR, path aliases |
| Routing | React Router v7 in Data Mode (`createBrowserRouter` + `RouterProvider`) |
| Server state | TanStack Query v5 (`useQuery`, `useMutation`, `queryOptions`) |
| Client state | Zustand v4/v5 with selector pattern and optional devtools+persist |
| TypeScript | `strict: true`, `moduleResolution: "bundler"`, `@/*` alias |
| Env validation | Zod-validated `src/config/env.ts` — throws at startup on missing vars |
| Deployment | Railway static deploy via `railway up` (Railpack auto-detection) |
| Dev tooling | Vitest, React Testing Library, ESLint, TypeScript |

---

## Toolchain Selection

| Decision | Selection | Rationale |
|---------|-----------|-----------|
| Bundler | Vite 5/6 | Fastest HMR, native ESM, Rollup production builds |
| React plugin | `@vitejs/plugin-react` | Babel-based, stable, default for most projects |
| Router | React Router v7 — Data Mode | `createBrowserRouter` + `RouterProvider`; file-based routing NOT used |
| Server state | TanStack Query v5 | Industry standard; v5 has unified object API |
| Client state | Zustand v4/v5 | Minimal API, selector pattern, no boilerplate |
| Testing | Vitest + React Testing Library | Native Vite integration, Jest-compatible API |
| Env validation | Zod | Runtime validation at startup; no silent env failures |
| Deployment | Railway (Railpack static) | CLI-first, zero config |

---

## 🚨 Version Matrix and Mode Disambiguation

### React Router v7 has THREE distinct modes — ONLY Data Mode is used here

| Mode | Import pattern | For |
|------|---------------|-----|
| **Declarative** (avoid) | `<BrowserRouter><Routes>` | Legacy apps, simple routing with no loaders |
| **Data Mode** ✅ | `createBrowserRouter` + `RouterProvider` | This module — route loaders, code splitting, TQ integration |
| **Framework Mode** ❌ WRONG | `@react-router/dev/vite` + `react-router.config.ts` | Remix-style SSR full-stack. NEVER for plain Vite SPAs |

**Agent rule:** A plain Vite SPA NEVER installs `@react-router/dev`. If you see `import { reactRouter } from "@react-router/dev/vite"` in `vite.config.ts`, that is Framework Mode — delete it and use `@vitejs/plugin-react` instead.

### React import path (v7)

```typescript
// Correct (v7):
import { createBrowserRouter, RouterProvider, Outlet, useNavigate, Link } from 'react-router';
import { RouterProvider } from 'react-router/dom'; // DOM-specific only

// WRONG — react-router-dom is a deprecated compat shim in v7:
import { useNavigate } from 'react-router-dom';
```

### TanStack Query v5 — API unified to single object

```typescript
// WRONG (v4 pattern — TypeScript error in v5):
useQuery(['todos'], fetchTodos, { staleTime: 5000 });

// CORRECT (v5):
useQuery({ queryKey: ['todos'], queryFn: fetchTodos, staleTime: 5000 });
```

### Zustand — named import, curried TypeScript syntax

```typescript
// WRONG (v3 pattern):
import create from 'zustand';

// CORRECT (v4/v5):
import { create } from 'zustand';

// With middleware — MUST use curried call in TypeScript:
const useStore = create<State>()(devtools(persist((set) => ({ ... }), { name: 'key' })));
//                            ^^ curried: create<T>()() not create<T>()
```

---

## Step 0: Pre-Flight Validation

Lucy MUST verify this before writing any code.

```bash
# Verify Node version (Vite 5 needs Node 18+, Vite 6 needs Node 20.19+)
node --version

# Verify package manager (prefer pnpm or bun; npm is fine)
which pnpm || which bun || which npm

# Verify Vite target version
# Vite 5: Node 18+
# Vite 6: Node 20.19+ or 22.12+
```

**Decision tree:**
- Node < 18 → STOP. Ask user to upgrade Node.
- Node 18-19 → Use Vite 5 only.
- Node 20+ → Use Vite 6 (preferred).

---

## Step 1: Project Scaffold

```bash
# Scaffold with Vite's official React TypeScript template
pnpm create vite@latest my-app -- --template react-ts
cd my-app
pnpm install
```

**Initial directory after scaffold:**
```
my-app/
├── index.html              # Vite entry (at ROOT, not in public/)
├── public/
│   └── vite.svg
├── src/
│   ├── App.tsx
│   ├── App.css
│   ├── assets/
│   ├── main.tsx            # Entry point — createRoot()
│   └── vite-env.d.ts
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

**⚠️ Vite-specific file rules (never violate):**
- `index.html` lives at project ROOT (not `public/`)
- `index.html` MUST contain `<script type="module" src="/src/main.tsx"></script>`
- `public/` files are served as-is at `/filename` — no `%PUBLIC_URL%` prefix (that's a CRA pattern)

---

## Step 2: Install Core Dependencies

```bash
# Routing
pnpm add react-router

# Server state
pnpm add @tanstack/react-query

# Client state
pnpm add zustand

# Env validation
pnpm add zod

# Dev tools (dev only)
pnpm add -D @tanstack/react-query-devtools
pnpm add -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
pnpm add -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser
pnpm add -D vite-tsconfig-paths
```

**DO NOT install:**
- ❌ `react-router-dom` (deprecated compat shim in v7)
- ❌ `@react-router/dev` (Framework Mode — wrong for SPA)
- ❌ `redux`, `@reduxjs/toolkit`, `mobx` (use Zustand)
- ❌ `axios` (unless project specifically requires it — fetch is fine for new projects)
- ❌ `react-query` (old package name — must be `@tanstack/react-query`)

---

## Step 3: TypeScript Configuration

Replace `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowImportingTsExtensions": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

**Critical settings:**
- `moduleResolution: "bundler"` — NOT `"node16"`, NOT `"node"`. Vite requires this.
- `allowImportingTsExtensions: true` — enables explicit `.tsx` in imports
- `@/*` maps to `./src/*` — single alias only, not per-subdirectory
- `strict: true` — mandatory. No exceptions.

---

## Step 4: Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths(), // Reads @/* alias from tsconfig.json — no duplication
  ],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.ts'],
  },
});
```

**DO NOT add:**
- ❌ `reactRouter()` plugin from `@react-router/dev/vite` — wrong mode
- ❌ Manual `resolve.alias` for `@/*` if `vite-tsconfig-paths` is installed

---

## Step 5: Project Structure

Create this directory structure before writing any feature code:

```
src/
├── app/
│   ├── index.tsx           # Root render: <AppProviders><AppRouter/>
│   ├── providers.tsx        # All global providers composed here
│   └── router.tsx           # createBrowserRouter() + AppRouter component
├── components/
│   └── layouts/            # DashboardLayout, AuthLayout, etc.
├── config/
│   ├── env.ts              # Zod-validated env (ONLY place import.meta.env is read)
│   └── paths.ts            # Typed route path registry
├── features/               # Vertical feature slices
│   └── {feature}/
│       ├── api/            # One file per API operation
│       ├── components/
│       └── types/
├── lib/
│   ├── api-client.ts       # Fetch/axios singleton
│   └── react-query.ts      # QueryConfig types + default options
├── routes/                 # Route components (mirror URL structure)
│   ├── app/
│   │   └── root.tsx        # Layout route: <DashboardLayout><Outlet/>
│   ├── auth/
│   └── not-found.tsx
├── stores/                 # Global Zustand stores (feature stores colocate)
├── types/
│   └── api.ts              # Shared entity types
├── main.tsx                # createRoot() entry point
├── setupTests.ts           # Vitest + testing-library setup
└── vite-env.d.ts           # ImportMetaEnv type extension
```

---

## Step 6: Environment Variable Setup

**Rule: `import.meta.env` is NEVER accessed raw outside `src/config/env.ts`.**

### `src/vite-env.d.ts` — TypeScript type extension

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_API_URL: string;
  readonly VITE_APP_TITLE: string;
  // Add all VITE_ vars here for editor autocomplete
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

### `src/config/env.ts` — Zod runtime validation

```typescript
import { z } from 'zod';

const EnvSchema = z.object({
  API_URL: z.string().url('API_URL must be a valid URL'),
  APP_TITLE: z.string().default('My App'),
  ENABLE_API_MOCKING: z
    .string()
    .refine((s) => s === 'true' || s === 'false')
    .transform((s) => s === 'true')
    .optional()
    .default('false'),
});

// Strip VITE_APP_ prefix so schema uses clean names
const rawEnv = Object.entries(import.meta.env).reduce<Record<string, string>>(
  (acc, [key, value]) => {
    if (key.startsWith('VITE_APP_')) {
      acc[key.replace('VITE_APP_', '')] = value;
    }
    return acc;
  },
  {}
);

const parsed = EnvSchema.safeParse(rawEnv);

if (!parsed.success) {
  const errors = Object.entries(parsed.error.flatten().fieldErrors)
    .map(([k, v]) => `  - ${k}: ${v?.join(', ')}`)
    .join('\n');
  throw new Error(`Missing or invalid environment variables:\n${errors}`);
}

export const env = parsed.data;
```

### `.env` files

```bash
# .env.example — commit this
VITE_APP_API_URL=https://api.yourapp.com
VITE_APP_TITLE=My App
VITE_APP_ENABLE_API_MOCKING=false

# .env.local — git-ignored, local overrides
VITE_APP_API_URL=http://localhost:8000

# .env.production — production values (may be set in Railway instead)
VITE_APP_API_URL=https://api.yourapp.com
```

**Env var rules:**
- ALL client-side env vars MUST have `VITE_` prefix (Vite security: non-prefixed vars are never exposed)
- Convention: `VITE_APP_` prefix for app vars (strips cleanly in env.ts)
- Variables are baked in at **build time** — not runtime. Must be set before `vite build` runs.
- For Railway: set `VITE_APP_*` vars in Railway dashboard BEFORE the build runs, not just as runtime env

---

## Step 7: Entry Point

### `src/main.tsx`

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './app/index';
import './index.css';

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error('Root element not found. Check index.html has <div id="root">');

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### `src/lib/query-client.ts` — QueryClient singleton (separate file, importable by route loaders)

```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,         // 1 minute
      gcTime: 1000 * 60 * 5,        // 5 minutes (NOT cacheTime — that's v4)
      refetchOnWindowFocus: false,
      retry: (failureCount, error: any) => {
        // Don't retry auth errors
        if (error?.status === 401 || error?.status === 403) return false;
        return failureCount < 1;
      },
    },
  },
});
```

**Why separate from providers.tsx:** Route loaders need to call `queryClient.getQueryData()` / `queryClient.fetchQuery()` directly. If `queryClient` is defined inside `providers.tsx` (a component module), importing it from route files creates circular dependencies. A dedicated `src/lib/query-client.ts` breaks the cycle.

### `src/app/providers.tsx`

```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import React, { Suspense } from 'react';
import { queryClient } from '@/lib/query-client';

export const AppProviders = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    <Suspense fallback={<div>Loading...</div>}>
      {children}
    </Suspense>
    {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
  </QueryClientProvider>
);
```

### `src/app/index.tsx`

```typescript
import React from 'react';
import { AppProviders } from './providers';
import { AppRouter } from './router';

export const App = () => (
  <AppProviders>
    <AppRouter />
  </AppProviders>
);
```

---

## Step 8: Router Setup (Data Mode)

### `src/config/paths.ts`

```typescript
export const paths = {
  home: {
    path: '/',
    getHref: () => '/',
  },
  auth: {
    login: {
      path: '/auth/login',
      getHref: (redirectTo?: string) =>
        `/auth/login${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`,
    },
    register: {
      path: '/auth/register',
      getHref: () => '/auth/register',
    },
  },
  app: {
    root: { path: '/app', getHref: () => '/app' },
    dashboard: { path: 'dashboard', getHref: () => '/app/dashboard' },
    profile: { path: 'profile', getHref: () => '/app/profile' },
  },
} as const;
```

### `src/app/router.tsx`

```typescript
import { QueryClient, useQueryClient } from '@tanstack/react-query';
import { useMemo } from 'react';
import { createBrowserRouter } from 'react-router';
import { RouterProvider } from 'react-router/dom';
import { paths } from '@/config/paths';

// Bridge: converts module's clientLoader/clientAction exports to RR v7 loader/action
const convert = (queryClient: QueryClient) => (m: any) => {
  const { clientLoader, clientAction, default: Component, ...rest } = m;
  return {
    ...rest,
    loader: clientLoader?.(queryClient),
    action: clientAction?.(queryClient),
    Component,
  };
};

export const createAppRouter = (queryClient: QueryClient) =>
  createBrowserRouter([
    {
      path: paths.home.path,
      lazy: () => import('../routes/landing').then(convert(queryClient)),
    },
    {
      path: paths.auth.login.path,
      lazy: () => import('../routes/auth/login').then(convert(queryClient)),
    },
    {
      path: paths.auth.register.path,
      lazy: () => import('../routes/auth/register').then(convert(queryClient)),
    },
    {
      // Protected section — layout route wraps all app routes
      path: paths.app.root.path,
      lazy: () => import('../routes/app/root').then(convert(queryClient)),
      children: [
        {
          path: paths.app.dashboard.path,
          lazy: () => import('../routes/app/dashboard').then(convert(queryClient)),
        },
        {
          path: paths.app.profile.path,
          lazy: () => import('../routes/app/profile').then(convert(queryClient)),
        },
      ],
    },
    {
      path: '*',
      lazy: () => import('../routes/not-found').then(convert(queryClient)),
    },
  ]);

// Component used in provider tree — router is a stable memo
export const AppRouter = () => {
  const queryClient = useQueryClient();
  const router = useMemo(() => createAppRouter(queryClient), [queryClient]);
  return <RouterProvider router={router} />;
};
```

**Router rules:**
- Router created OUTSIDE the component tree (via `useMemo` in `AppRouter`, never inside render functions)
- `queryClient` passed into router factory so route loaders can use `queryClient.getQueryData` / `queryClient.fetchQuery`
- ALL non-layout routes use `lazy:` for automatic code splitting — never `element: <Component/>`  for page routes
- Protected routes use a layout route with auth check in its component (not a redirect-only route)

### `src/routes/app/root.tsx` — protected layout route

```typescript
import { Navigate, Outlet, useLocation } from 'react-router';
import { useCurrentUser } from '@/features/auth/api/get-current-user';

export const ErrorBoundary = () => (
  <div>Something went wrong. <a href="/">Go home</a></div>
);

// Default export is what RR v7's lazy() expects
export default function AppRoot() {
  const { data: user, isLoading } = useCurrentUser();
  const location = useLocation();

  if (isLoading) return <div>Loading...</div>;

  if (!user) {
    return <Navigate to={`/auth/login?redirectTo=${encodeURIComponent(location.pathname)}`} replace />;
  }

  return (
    <div className="app-layout">
      {/* Nav/sidebar here */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}
```

### Route file pattern — lazy-loaded page

```typescript
// src/routes/app/dashboard.tsx
import type { QueryClient } from '@tanstack/react-query';
import type { LoaderFunctionArgs } from 'react-router';
import { getDashboardDataQueryOptions } from '@/features/dashboard/api/get-dashboard-data';
import { DashboardPage } from '@/features/dashboard/components/dashboard-page';

// clientLoader receives queryClient from the router factory's convert() wrapper
export const clientLoader =
  (queryClient: QueryClient) =>
  async ({ request: _request }: LoaderFunctionArgs) => {
    const query = getDashboardDataQueryOptions();
    // Serve from cache if fresh; fetch and populate cache if stale
    return queryClient.getQueryData(query.queryKey) ?? (await queryClient.fetchQuery(query));
  };

export default DashboardPage;
```

---

## Step 9: Data Fetching Pattern (TanStack Query v5)

### `src/lib/react-query.ts`

```typescript
import type { UseMutationOptions, DefaultOptions } from '@tanstack/react-query';

export const queryConfig = {
  queries: {
    refetchOnWindowFocus: false,
    retry: 1,
    staleTime: 1000 * 60, // 1 minute
  },
} satisfies DefaultOptions;

// Utility types for query/mutation configuration
export type ApiFnReturnType<FnType extends (...args: any) => Promise<any>> =
  Awaited<ReturnType<FnType>>;

export type QueryConfig<T extends (...args: any[]) => any> = Omit<
  ReturnType<T>,
  'queryKey' | 'queryFn'
>;

export type MutationConfig<MutationFnType extends (...args: any) => Promise<any>> =
  UseMutationOptions<
    ApiFnReturnType<MutationFnType>,
    Error,
    Parameters<MutationFnType>[0]
  >;
```

### Query hook pattern — one file per API operation

```typescript
// src/features/posts/api/get-posts.ts
import { queryOptions, useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { QueryConfig } from '@/lib/react-query';
import type { Post } from '../types';

// 1. Raw fetch function
export const getPosts = (page = 1): Promise<{ data: Post[]; total: number }> =>
  apiClient.get('/posts', { params: { page } });

// 2. queryOptions factory — enables type-safe ensureQueryData, prefetchQuery, cache invalidation
export const getPostsQueryOptions = ({ page }: { page?: number } = {}) =>
  queryOptions({
    queryKey: page ? ['posts', { page }] : ['posts'],
    queryFn: () => getPosts(page),
  });

// 3. Typed custom hook
type UsePostsOptions = {
  page?: number;
  queryConfig?: QueryConfig<typeof getPostsQueryOptions>;
};

export const usePosts = ({ page, queryConfig }: UsePostsOptions = {}) =>
  useQuery({
    ...getPostsQueryOptions({ page }),
    ...queryConfig,
  });
```

### Mutation hook pattern

```typescript
// src/features/posts/api/create-post.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';
import { apiClient } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';
import type { Post } from '../types';
import { getPostsQueryOptions } from './get-posts';

export const createPostSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  body: z.string().min(1, 'Body is required'),
});
export type CreatePostInput = z.infer<typeof createPostSchema>;

export const createPost = (data: CreatePostInput): Promise<Post> =>
  apiClient.post('/posts', data);

type UseCreatePostOptions = {
  mutationConfig?: MutationConfig<typeof createPost>;
};

export const useCreatePost = ({ mutationConfig }: UseCreatePostOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...restConfig } = mutationConfig ?? {};

  return useMutation({
    mutationFn: createPost,
    onSuccess: (...args) => {
      // Invalidate list query — causes refetch on next render
      queryClient.invalidateQueries({ queryKey: getPostsQueryOptions().queryKey });
      onSuccess?.(...args);
    },
    ...restConfig,
  });
};
```

**Critical v5 rules:**
- ALL `useQuery` calls use single object form: `useQuery({ queryKey, queryFn, ...opts })`
- NO `onSuccess`/`onError` in `useQuery` — they were removed in v5. Use `useEffect` for side effects.
- Use `gcTime` NOT `cacheTime` (renamed in v5)
- Use `status === 'pending'` NOT `status === 'loading'` (renamed in v5)
- Always wrap query options in `queryOptions()` helper — enables `ensureQueryData` and type inference

---

## Step 10: Zustand Store Pattern

### Global store

```typescript
// src/stores/ui-store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

type Notification = {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message?: string;
};

type UIStore = {
  notifications: Notification[];
  sidebarOpen: boolean;
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  dismissNotification: (id: string) => void;
  toggleSidebar: () => void;
};

export const useUIStore = create<UIStore>()(
  devtools(
    (set) => ({
      notifications: [],
      sidebarOpen: true,
      addNotification: (notification) =>
        set(
          (state) => ({
            notifications: [
              ...state.notifications,
              { id: crypto.randomUUID(), ...notification },
            ],
          }),
          false,
          'ui/addNotification'
        ),
      dismissNotification: (id) =>
        set(
          (state) => ({
            notifications: state.notifications.filter((n) => n.id !== id),
          }),
          false,
          'ui/dismissNotification'
        ),
      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen }), false, 'ui/toggleSidebar'),
    }),
    { name: 'UIStore' }
  )
);
```

### Persisted store

```typescript
// src/stores/auth-store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

type User = { id: string; email: string; name: string };

type AuthStore = {
  user: User | null;
  token: string | null;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
};

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        token: null,
        setUser: (user) => set({ user }, false, 'auth/setUser'),
        setToken: (token) => set({ token }, false, 'auth/setToken'),
        logout: () => set({ user: null, token: null }, false, 'auth/logout'),
      }),
      { name: 'auth-storage' } // key in localStorage
    ),
    { name: 'AuthStore' }
  )
);
```

**Middleware order is MANDATORY: `devtools(persist(...))` — devtools outermost.**
Reversed order (`persist(devtools(...))`) causes DevTools to be blind to rehydration events.

### Using stores — selector pattern (mandatory)

```typescript
// WRONG — re-renders on every state change:
const { user, token } = useAuthStore();

// CORRECT — granular selector:
const user = useAuthStore((state) => state.user);
const token = useAuthStore((state) => state.token);

// CORRECT — multiple fields with useShallow:
import { useShallow } from 'zustand/react/shallow';
const { user, token } = useAuthStore(
  useShallow((state) => ({ user: state.user, token: state.token }))
);
```

**Never call React hooks inside store actions.** Stores are plain JS — no `useEffect`, `useQuery`, or any hook inside the store definition.

### Zustand slices pattern (for larger apps with multiple domains)

When the app has 3+ distinct state domains, use Zustand's slices pattern to keep stores modular while sharing a single store instance:

```typescript
// src/stores/slices/auth-slice.ts
import type { StateCreator } from 'zustand';
import type { BoundStore } from '../app-store';

type User = { id: string; email: string; name: string };

export type AuthSlice = {
  user: User | null;
  setUser: (user: User | null) => void;
  logout: () => void;
};

export const createAuthSlice: StateCreator<BoundStore, [], [], AuthSlice> = (set) => ({
  user: null,
  setUser: (user) => set({ user }, false, 'auth/setUser'),
  logout: () => set({ user: null }, false, 'auth/logout'),
});
```

```typescript
// src/stores/slices/ui-slice.ts
import type { StateCreator } from 'zustand';
import type { BoundStore } from '../app-store';

export type UISlice = {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
};

export const createUISlice: StateCreator<BoundStore, [], [], UISlice> = (set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen }), false, 'ui/toggleSidebar'),
});
```

```typescript
// src/stores/app-store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { createAuthSlice, type AuthSlice } from './slices/auth-slice';
import { createUISlice, type UISlice } from './slices/ui-slice';

export type BoundStore = AuthSlice & UISlice;

export const useAppStore = create<BoundStore>()(
  devtools(
    (...a) => ({
      ...createAuthSlice(...a),
      ...createUISlice(...a),
    }),
    { name: 'AppStore' }
  )
);

// Pre-bound selectors — import these instead of useAppStore directly
export const useUser = () => useAppStore((s) => s.user);
export const useSidebarOpen = () => useAppStore((s) => s.sidebarOpen);
```

**When to use slices vs separate stores:** Use slices when state domains need to interact (a UI slice action that reads auth state). Use separate `create()` calls when domains are fully independent (notifications store has no reason to know about auth).

---

## Step 11: Testing Setup

### `src/setupTests.ts`

```typescript
import '@testing-library/jest-dom';
```

### `vitest.config.ts` (if separate from vite.config.ts)

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.ts'],
  },
});
```

### Component test pattern

```typescript
// src/features/posts/components/post-list.test.tsx
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router';
import { PostList } from './post-list';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  );
};

test('renders post list', async () => {
  render(<PostList />, { wrapper: createWrapper() });
  expect(await screen.findByText('Posts')).toBeInTheDocument();
});
```

**Testing rules:**
- Always wrap components in `QueryClientProvider` + `MemoryRouter` (or `createMemoryRouter`)
- Set `retry: false` in test QueryClient — prevents hanging retries in tests
- Use `findBy*` (async) not `getBy*` for data that loads via queries

---

## Step 12: API Client

### `src/lib/api-client.ts`

```typescript
import { env } from '@/config/env';

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${env.API_URL}${endpoint}`;

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new ApiError(response.status, response.statusText, data);
  }

  if (response.status === 204) return undefined as T;
  return response.json();
}

export const apiClient = {
  get: <T>(endpoint: string, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: 'GET' }),
  post: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
    request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),
  patch: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
    request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    }),
  put: <T>(endpoint: string, data?: unknown, options?: RequestInit) =>
    request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    }),
  delete: <T>(endpoint: string, options?: RequestInit) =>
    request<T>(endpoint, { ...options, method: 'DELETE' }),
};
```

---

## Step 13: Deploy to Railway (Static SPA)

Railway serves SPAs as static files. The SPA routing fallback (serve `index.html` for all routes) requires explicit configuration.

### Step 13a: Detect and install Railway CLI

```bash
railway --version 2>/dev/null || echo "NOT INSTALLED"
```

If NOT installed, use AskUserQuestion:
```
"Railway CLI is required for deployment. Install via:
1. npm: npm install -g @railway/cli
2. Homebrew: brew install railway"
```

### Step 13b: Authenticate

```bash
railway whoami 2>/dev/null || echo "NOT AUTHENTICATED"
```

If not authenticated: prompt user to run `railway login` in a separate terminal.

### Step 13c: Add railway.json for Railpack SPA mode

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "RAILPACK"
  },
  "deploy": {
    "startCommand": "npx serve dist --single --listen $PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 60
  }
}
```

**CRITICAL: The `--single` flag in `serve` is what enables SPA routing fallback.** Without it, refreshing on `/dashboard` returns 404.

### Step 13d: Update package.json for Railpack detection

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  }
}
```

**DO NOT add a `start` script** — Railpack uses `startCommand` from `railway.json`. A `start` script confuses auto-detection.

### Step 13e: Set build-time environment variables

```bash
# Set VITE_ vars BEFORE the build runs (they are baked into the bundle)
railway variables set VITE_APP_API_URL=https://api.yourapp.com
railway variables set VITE_APP_TITLE="My App"

# Verify all vars are set
railway variables
```

### Step 13f: Deploy

```bash
# Build locally to verify before deploying
pnpm build

# Deploy to Railway
railway up

# Generate HTTPS URL (idempotent — safe to run every time)
railway domain
```

### Step 13g: Verify SPA routing

```bash
# Get the deployed URL
DOMAIN=$(railway domain)

# Verify root works
curl -sf "https://$DOMAIN/" | grep -c "root" || echo "FAIL: root not serving index.html"

# Verify SPA fallback works (navigate to a non-root route directly)
curl -sf "https://$DOMAIN/dashboard" | grep -c "root" || echo "FAIL: SPA routing broken — 404 on refresh"
```

If SPA routing check fails, the `--single` flag is missing from the serve command. Update `railway.json` and redeploy.

---

## Stale Pattern Detection (WHEN Blocks)

Lucy MUST check generated code against each of these before declaring success.

### WHEN you see `<Switch>` or `<Route component=`
**Stale React Router v5 pattern.** Replace with `createBrowserRouter` + `RouterProvider`. `<Switch>` is not exported from `react-router` v6+.

### WHEN you see `import { ... } from 'react-router-dom'`
**Deprecated in v7.** Change to `import { ... } from 'react-router'`. Exception: DOM-specific APIs (`RouterProvider`, `HydratedRouter`) import from `react-router/dom`.

### WHEN you see `useHistory()`
**Removed in v6.** Replace with `useNavigate()`.

### WHEN you see `<Redirect to=`
**Removed in v6.** Replace with `<Navigate to= replace />`.

### WHEN you see `useQuery(['key'], fn, opts)` with 3 arguments
**v4 pattern — TypeScript error in v5.** Convert to `useQuery({ queryKey: ['key'], queryFn: fn, ...opts })`.

### WHEN you see `onSuccess:` or `onError:` inside `useQuery({ ... })`
**Removed in v5 — silently does nothing.** Move to `useEffect` watching `isSuccess`/`isError` flags.

### WHEN you see `cacheTime:` in query options
**Renamed in v5.** Replace with `gcTime:`.

### WHEN you see `status === 'loading'`
**Renamed in v5.** Replace with `status === 'pending'`.

### WHEN you see `import create from 'zustand'` (default import)
**v3 pattern.** Replace with `import { create } from 'zustand'` (named import).

### WHEN you see `create<State>(devtools(...))`  without curried call
**TypeScript v4 requirement.** Must be `create<State>()(devtools(...))` — note the extra `()`.

### WHEN you see `process.env.REACT_APP_`
**CRA pattern.** Replace with `import.meta.env.VITE_APP_` and update `.env` file keys.

### WHEN you see `import.meta.env.X` accessed outside `src/config/env.ts`
**Anti-pattern.** Move all env access through `env.ts`. The only place `import.meta.env` is read is in `src/config/env.ts`.

### WHEN you see `@react-router/dev` in dependencies
**Framework Mode package.** Remove entirely. SPAs use `react-router` only.

### WHEN you see `reactRouter()` in `vite.config.ts` plugins
**Framework Mode plugin.** Remove. Replace with `react()` from `@vitejs/plugin-react`.

### WHEN you see `useStore()` without a selector argument
**Full state subscription.** Component re-renders on every state change. Add granular selector: `useStore(state => state.specificField)`.

### WHEN you see `persist(devtools(...))` middleware order
**Wrong order — DevTools cannot see rehydration.** Must be `devtools(persist(...))` — devtools outermost.

### WHEN HMR fires (terminal shows update) but the browser DOM never changes
**React Router v7.2.0 regression in library/data mode.** Pin to `react-router@7.1.3`. Affects `createBrowserRouter` with Vite 6. Track [remix-run/react-router#13159](https://github.com/remix-run/react-router/issues/13159).

### WHEN you see anonymous default export `export default () => <div/>`
**Breaks React Fast Refresh.** Name all default exports: `export default function MyComponent()`. Anonymous exports prevent Vite from hot-patching individual components — causes full page reloads on every save.

---

## Known Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 404 on route refresh in Railway | `serve` missing `--single` flag | Add `--single` to `startCommand` in `railway.json` |
| `VITE_APP_X` is `undefined` in Railway production | Env var set as runtime var, not build-time | Set vars in Railway dashboard BEFORE running `railway up`; they must be present when `vite build` runs |
| `useNavigate()` may be used only in context of `<Router>` | Provider mounted outside `<RouterProvider>` | Move provider inside route tree using layout route pattern |
| `createBrowserRouter` inside component breaks HMR | New router instance on every render | Move router creation to `useMemo` or module level |
| TanStack Query: `No QueryClient set` | `QueryClientProvider` missing or duplicated (monorepo) | Wrap app in `QueryClientProvider`; in monorepos, add `resolve: { dedupe: ['@tanstack/react-query'] }` to vite.config.ts |
| Zustand: `Invalid hook call` in store action | React hook called inside store | Move async/query logic to components; stores use plain JS only |
| `status === 'loading'` never true | Renamed to `'pending'` in TanStack Query v5 | Replace with `status === 'pending'` or `isPending` flag |
| `onSuccess`/`onError` callbacks silently not firing | Removed from `useQuery` in v5 | Use `useEffect` watching `isSuccess`/`isError` |
| `process.env.REACT_APP_X` is `undefined` | CRA pattern doesn't work in Vite | Use `import.meta.env.VITE_APP_X` and rename `.env` keys |
| Infinite redirect loop in protected route | `<Navigate>` re-fires on every render | Use `replace` prop; ensure auth state resolves before redirecting |
| Zustand store state stale after rehydration | Wrong middleware order | Must be `devtools(persist(...))` not `persist(devtools(...))` |
| `moduleResolution` type errors | Wrong setting for Vite | Must be `"bundler"`, not `"node16"` or `"node"` |
| `allowImportingTsExtensions` required | `moduleResolution: "bundler"` requires it | Add to `tsconfig.json` |
| `[vite] Could not Fast Refresh` — full page reloads | Anonymous default export or non-component export mixed in component file | Name all default exports; move constants to separate files; set `allowConstantExport: true` in eslint-plugin-react-refresh if mixing unavoidable |
| HMR fires but DOM never updates (library/data mode) | React Router v7.2.0 regression — `createBrowserRouter` + Vite 6 | Pin to `react-router@7.1.3` until patch released; track [#13159](https://github.com/remix-run/react-router/issues/13159) |
| Imperative navigation from Axios interceptors / Zustand | `useNavigate` not callable outside React component | Export the router instance from `router.ts` and call `router.navigate()` imperatively |

---

## Health Check Endpoint

Every deployed service should expose a health check. For a pure static SPA deployed on Railway, the health check is the root HTML response. Set in `railway.json`:

```json
{
  "deploy": {
    "healthcheckPath": "/",
    "healthcheckTimeout": 60
  }
}
```

If the SPA calls a backend API, the health check should be on the API service, not the static SPA.

---

## AGENTS.md Additions

Add this block to the Domain-Specific Notes section of AGENTS.md:

```markdown
## Framework: React SPA

- **Stack:** React 18/19 + Vite 5/6 + React Router v7 (Data Mode) + TanStack Query v5 + Zustand v4/v5
- **Router mode:** Data Mode ONLY. Never use Framework Mode (`@react-router/dev`). Import from `react-router`, not `react-router-dom`.
- **Router setup:** `createBrowserRouter` + `RouterProvider`. Router created at module level or via `useMemo` — NEVER inside render functions.
- **Query API:** All `useQuery` calls use single object form: `{ queryKey, queryFn, ...opts }`. No 3-argument form. No `onSuccess`/`onError` in `useQuery` — use `useEffect`.
- **Env vars:** Access via `import.meta.env.VITE_APP_X` only. All env access goes through `src/config/env.ts` (Zod-validated). Never `process.env` in Vite.
- **Zustand:** Named import `{ create }`. TypeScript with middleware requires curried `create<T>()()`. Selector pattern mandatory — never `useStore()` without selector. Middleware order: `devtools(persist(...))`.
- **Deployment:** Railway static SPA via `railway up`. Requires `--single` flag in serve command for SPA routing. Env vars must be set BEFORE build runs (baked at build time).
- **Code splitting:** All page routes use `lazy:` property in route object. Never `React.lazy()` directly for routes.
- **TypeScript:** `moduleResolution: "bundler"`, `strict: true`, `@/*` alias via `vite-tsconfig-paths`.
```

---

## Test Coverage Required

```typescript
// src/features/{feature}/api/get-posts.test.ts
describe('getPostsQueryOptions', () => {
  it('should return queryKey ["posts"] when no page')
  it('should return queryKey ["posts", { page }] when page provided')
  it('should return data from API on successful fetch')
})

// src/features/{feature}/components/{component}.test.tsx
describe('{Component}', () => {
  it('renders loading state while query is pending')
  it('renders data after successful fetch')
  it('renders error state on query failure')
})

// src/config/env.test.ts
describe('env validation', () => {
  it('throws on missing required env var')
  it('provides default values for optional vars')
  it('transforms ENABLE_API_MOCKING string to boolean')
})

// src/app/router.test.tsx
describe('AppRouter', () => {
  it('renders landing page at root path')
  it('redirects unauthenticated user to login')
  it('renders protected route when authenticated')
})
```

---

*Module created by AgentBuild. Update Known Issues when new failures are discovered.*
*v1 created 2026-02-23: Initial DRAFT. Research: 5 parallel agents (Docs, Migration, Community, Pattern, CLI/MCP). Pattern source: bulletproof-react (34k stars). Council + RedTeam: React Router v7 Data Mode, TanStack Query v5, Zustand confirmed. Not yet battle-tested on live AgentBuild build.*
