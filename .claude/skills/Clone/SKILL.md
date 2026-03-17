---
name: Clone
description: Clone PAI instances with new identities. Full project copy, identity swap, optional memory wipe. Non-destructive — original never modified. Runs directly inside Claude Code session. USE WHEN clone, clone PAI, new instance, new identity, create copy, duplicate PAI.
---

# Clone Skill

Create full copies of your PAI project with new DA identities. The original instance is NEVER modified — read-only source.

## How It Works

When triggered inside a Claude Code session, the clone runs **natively** — no subprocesses, no scripts, no `claude -p`:

1. **AskUserQuestion** → directory name, DA name, fresh start, API key handling
2. **Bash** (`rsync`) → copy FULL project to `~/` (excluding caches, git)
3. **Bash** (`git init`, `bun install`) → fresh repo + dependencies
4. **Read + Edit** → transform identity in settings.json, .env files, skill docs
5. **Bash** (`find -delete`) → wipe memory if fresh start (files AND symlinks)
6. **Bash** (`git commit`) → clean first commit with all transforms applied
7. **Grep** → comprehensive verification across ALL file types including dotfiles

## Inputs

| Input | Description | Example |
|-------|-------------|---------|
| Directory name | Project folder in `~/` | `PAI-Instance-Executive-Assistant` |
| DA name | New DA identity | `Luna` |
| Fresh start | Wipe memory? | Yes / No |
| API keys | Copy or blank? | Copy / Blank |

## What Gets Copied

The **entire project** — not just `.claude/`:
- `.claude/` (skills, hooks, tools, memory, settings)
- `package.json`, `bun.lock` (dependencies)
- `Tools/`, `Packs/`, `Releases/`
- `README.md`, `LICENSE`, `SECURITY.md`, `PLATFORM.md`
- `.env`, `.env.example`, `.gitignore`, `.gitattributes`

**Excluded** (regenerated):
- `node_modules/` → `bun install`
- `.fastembed_cache/` → on demand
- `output/` → session artifacts
- `.git/` → `git init`

## What Changes

- **Identity**: DA name in settings.json, .env (both), all skill docs (.md files)
- **Paths**: PAI_DIR in settings.json and both .env files
- **Catchphrase**: DA name swapped in startup greeting
- **Memory** (if fresh): ALL files and symlinks deleted, directory structure preserved
- **State** (if fresh): Counters reset to zero
- **API keys** (if blanked): Replaced with `YOUR_KEY_HERE`
- **Git**: Fresh repo with clean first commit

## Files

| File | Purpose |
|------|---------|
| `Workflows/CloneInstance.md` | **Primary** — 9-step in-session workflow with verification |
| `Tools/Clone.ts` | Standalone terminal cloner (fallback) |
| `Tools/CloneAnalyze.ts` | Standalone manifest generator (fallback) |

## Known Gotchas

1. `.env` files are invisible to `*.ext` globs — need explicit `-name ".env"`
2. Symlinks survive `find -type f -delete` — use `-not -type d`
3. Session hooks write to memory during clone — wipe memory LAST
4. Clones go in `~/`, never inside the source project
5. Root `.env` contains API keys — always ask about key handling
