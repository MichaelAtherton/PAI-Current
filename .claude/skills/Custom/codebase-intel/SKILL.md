---
name: codebase-intel
description: "Generate a committed, machine-first context pack for any codebase. Produces structured subsystem files an AI loads before implementation to work from actual source rather than training memory. Trigger when: 'run codebase-intel on <path>', 'generate context pack for <repo>', 'analyze this codebase for implementation context', 'codebase-intel'."
---

# codebase-intel

Transform any codebase into a committed, machine-first context pack — structured subsystem files an AI loads before implementation to work from actual source rather than training memory.

## What this produces

```
output/repo-context/
  CONTEXT.md          ← cold-start index with subsystem routing and "Do not assume"
  <subsystem>.md      ← one file per discovered subsystem, dense and source-grounded
```

All output is committed to the repo. It is a project artifact, not a temporary cache.

## Invocation

- Local path: `"run codebase-intel on ./my-project"`
- GitHub URL: `"run codebase-intel on https://github.com/user/repo"` — clone to `/tmp/<repo-name>` first
- Current directory: `"run codebase-intel here"` or just `"codebase-intel"`

## Execution order

Run phases in sequence. Each phase's output feeds the next.

| Phase | Workflow | Input | Output |
|-------|----------|-------|--------|
| 0 | `workflows/Phase0-RepoType.md` | repo root | repo_type: single or monorepo with package list |
| 1 | `workflows/Phase1-Discovery.md` | repo root (per package if monorepo) | `.manifest.json` + `CONTEXT.md` shell |
| 2 | `workflows/Phase2-Extract.md` | `.manifest.json` | subsystem files + completed `CONTEXT.md` |

Read each workflow file before executing that phase.

## Rules

- **Never skip Phase 0.** A repo that looks single-package may be a monorepo.
- **Never infer subsystem names from folder names.** Phase 1 derives subsystems from code dependencies.
- **Never modify source files.** All output goes to `output/repo-context/` only.
- **Commit output after generation.** The context pack is a project artifact.
- **Manual invocation only.** Never auto-regenerate, never poll for changes.
- **Staleness:** The `git_hash` in `CONTEXT.md` frontmatter shows the repo state at generation. Regenerate when the codebase has changed significantly enough that the context pack would mislead an AI.

## After generation

Tell the developer:
1. What was generated (file count, subsystem list)
2. The output path
3. How to use it: "Load `output/repo-context/CONTEXT.md` at the start of any implementation session. The index will tell the AI which subsystem files to load for the current task."
