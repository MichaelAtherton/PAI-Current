# Phase 1 — Discovery

**Input:** repo root path (or package root for monorepo packages)  
**Agent:** `feature-dev:code-explorer` — one instance, one pass  
**Fallback:** If `feature-dev:code-explorer` is not available, perform the discovery yourself using the Read and Glob tools directly, following the same scope constraints defined below.
**Output:** 
- `output/repo-context/.manifest.json` (working artifact, not committed)
- `output/repo-context/CONTEXT.md` (shell — frontmatter + stack + entry points + Do not assume seeds)

For monorepo packages: output goes to `output/repo-context/<package-name>/` instead.

## What the agent reads

Give the `feature-dev:code-explorer` agent these specific instructions:

> Read the following files in this order. Do not explore beyond what is listed unless a file leads to an entry point that is not yet covered:
> 1. README.md (or README.rst, README.txt)
> 2. Package manifest: package.json / go.mod / pyproject.toml / Cargo.toml — whichever is present
> 3. Main entry point(s) — look for: `main.ts`, `index.ts`, `app.ts`, `server.ts`, `src/main.*`, `src/index.*`, or the `main` field in package.json
> 4. One level of imports from each entry point — follow import statements one level deep. Edge cases:
>    - **Barrel/index files** (files that only re-export from other modules): treat the barrel as the boundary — do not follow through it. The barrel itself is the subsystem entry point.
>    - **Dynamic imports** (`import()`, `require()`): note them as entry points but do not follow them — they represent runtime boundaries.
>    - **Circular imports**: stop at the first file already visited. Do not loop.
>    - **Third-party imports** (node_modules, external packages): do not follow. Record the package name as a stack dependency only.

**Do NOT** infer subsystem names from directory names alone. Subsystem boundaries must be derived from actual import relationships and code responsibilities.

## What to extract

From the above reading, extract:

**Stack:** Programming language(s), frameworks, key libraries — with versions from the package manifest where available.

**Entry points:** File paths and line numbers where execution begins (HTTP server start, CLI entry, app bootstrap, etc.)

**Subsystems:** Each subsystem is a coherent group of files with a shared responsibility. Identify subsystems by:
- Files that are imported together by the same callers
- Files that share a clear single responsibility (auth, data access, routing, etc.)
- Files that change together (co-located by concern, not just by folder)

For each subsystem, determine:
- `name`: lowercase-hyphenated identifier (e.g., `auth`, `api-routes`, `data-models`)
- `root_files`: the 1-3 files that are the primary entry points into this subsystem
- `inferred_responsibility`: one sentence describing what this subsystem owns
- `file_count`: approximate number of files in this subsystem
- `is_cross_cutting`: true if this subsystem's code is called from most other subsystems (e.g., logging, error handling, config); false otherwise

**Do not assume** seeds: identify 3-5 things about this codebase that contradict common generic assumptions. These become the seed entries in CONTEXT.md's "Do not assume" section.

## Subsystem Manifest format

Write the manifest to `output/repo-context/.manifest.json`:

```json
{
  "repo": "<repo name from package manifest or directory name>",
  "stack": ["<technology>", "<technology>"],
  "entry_points": ["<file>:<line>", "<file>:<line>"],
  "do_not_assume_seeds": [
    "This repo does NOT use <X> — it uses <Y> at <file:line>",
    "..."
  ],
  "subsystems": [
    {
      "name": "<name>",
      "root_files": ["<file>", "<file>"],
      "inferred_responsibility": "<one sentence>",
      "file_count": <number>,
      "is_cross_cutting": <true|false>
    }
  ]
}
```

## CONTEXT.md shell

After producing the manifest, write the CONTEXT.md shell using `templates/CONTEXT.md.template`. Fill in:
- Frontmatter: `repo`, `generated_at` (current ISO timestamp), `git_hash` (run `git rev-parse --short HEAD`), `repo_type` (from Phase 0 output), `stack` (array)
  - If `git rev-parse --short HEAD` fails (target is not a git repository), set `git_hash` to `"non-git"`.
- `## Stack` section: technologies with versions
- `## Entry points` section: file:line references
- `## Do not assume` section: populate from `do_not_assume_seeds`

Leave the `## Subsystem index` table and `## Cross-cutting concerns` section empty — Phase 2 fills these.

## What Phase 1 does NOT do

- Does not read beyond one import level from entry points
- Does not write subsystem files — only the manifest and CONTEXT.md shell
- Does not make technology recommendations
- Does not explore the full directory tree
