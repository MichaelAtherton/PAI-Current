# Phase 0 — Repo Type Detection

**Input:** repo root path  
**Output:** repo_type decision (single or monorepo with package list)

## What to read

Read the root level only. Do not traverse into subdirectories.

Check for these signals in this order:

1. **Workspace config files** (any of these = monorepo):
   - `pnpm-workspace.yaml`
   - `lerna.json`
   - `turbo.json`
   - `nx.json`

2. **Root `package.json` with `workspaces` field** (= monorepo)

3. **Conventional monorepo directories** at root level (= likely monorepo, verify with signal 1 or 2):
   - `packages/`
   - `apps/`
   - `services/`

If none of the above are present: **single repo**.

## Output format

For a single repo:
```
repo_type: single
```

For a monorepo, list each package with its name and path:
```
repo_type: monorepo
packages:
  - name: <directory-name>
    path: <relative-path-from-root>
```

Derive package names from directory names inside `packages/`, `apps/`, or `services/`. If workspace config specifies globs (e.g., `packages/*`), enumerate the actual matching directories.

## Execution routing after Phase 0

**Single repo:** Run Phase 1 once on the repo root. Run Phase 2 once using the manifest Phase 1 produces.

**Monorepo:** For each package in the list:
1. Run Phase 1 on `<package path>` — produces `output/repo-context/<package-name>/.manifest.json`
2. Run Phase 2 using that manifest — produces `output/repo-context/<package-name>/` subsystem files

After all packages complete, write the top-level `output/repo-context/CONTEXT.md` as an index of indices using this exact format:

```markdown
---
repo: <root repo name>
generated_at: <ISO timestamp>
git_hash: <short hash from `git rev-parse --short HEAD` at repo root>
repo_type: monorepo
packages: [<package-name-1>, <package-name-2>, ...]
---

## You are reading a monorepo context pack

This repository contains multiple packages. Each has its own context pack.

Before writing any code:
1. Identify which package your task touches
2. Load that package's `CONTEXT.md` from the path listed below
3. Follow that package's context pack instructions

## Package index

| Package | Path | Owns | Load when |
|---------|------|------|-----------|
| <package-name> | `output/repo-context/<package-name>/CONTEXT.md` | <one-line from that package's CONTEXT.md ## Stack line> | <task types that touch this package> |

## Do not assume

- This is a monorepo — changes to one package may affect others via shared dependencies
- Each package has its own context pack — do not apply one package's patterns to another
```

Derive each package row by reading the package's generated `CONTEXT.md` for its stack line and subsystem names.

## What Phase 0 does NOT do

- Does not read any source files
- Does not make assumptions about technology stack
- Does not run Phase 1 or Phase 2 — it only produces the routing decision
