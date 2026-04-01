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

After all packages complete, write the top-level `output/repo-context/CONTEXT.md` as an index of indices. It lists each package with a one-line description and a link to its `CONTEXT.md`.

## What Phase 0 does NOT do

- Does not read any source files
- Does not make assumptions about technology stack
- Does not run Phase 1 or Phase 2 — it only produces the routing decision
