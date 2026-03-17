# AgentBuild Project Registry

This directory contains one JSON file per active AgentBuild project. Lucy reads these on startup to know which projects exist, where they live, and what phase they're in.

## How It Works

- **Created during:** Phase 1a (Project Location & Registration)
- **Updated at:** Every phase transition (currentPhase, phaseHistory)
- **Read on:** Every AgentBuild invocation (to list active projects and route correctly)
- **Archived when:** BuildRetrospective completes and project is marked done

---

## Project ID (PID) — The Non-Negotiable Identifier

Every project gets an immutable **Project ID (PID)** at creation. Format: `PID-{8 hex characters}`.

**Example:** `PID-a7f3b2e1`

**Rules:**
- Generated once during Phase 1a. Never changes.
- Project name can change. Slug can change. Repo can move. PID is permanent.
- Every artifact references the PID: commits, specs, PRDs, AGENTS.md.
- The registry filename uses the PID: `PID-a7f3b2e1.json` (not the slug).

**Generation:** `openssl rand -hex 4` produces 8 hex characters. Collision probability across reasonable project counts (~1000) is effectively zero.

### The PID Gate (Mandatory — No Exceptions)

**Before ANY write operation to a project repo, Lucy must have a valid PID context loaded.**

This is the same pattern as Clerk authentication — no `userId`, no access. No `projectId`, no changes.

**Gate check sequence (runs before every workflow):**

```
1. Is there an active project context? (PID loaded in session)
   → NO: "Which project are you working on?" List active projects.

2. Does the PID match a registered project in projects/?
   → NO: "PID-{id} not found in registry. Has this project been archived?"

3. Does the repoPath in the registry match where we're about to write?
   → NO: "Warning: You're about to write to {path} but PID-{id} is registered at {repoPath}. Proceed?"
```

**If any check fails → HALT. Do not write. Resolve first.**

**Why this exists:** Without the gate, Lucy can silently write project A's code into project B's repo when multiple projects are active. The PID gate makes this structurally impossible.

---

## Schema

Each file is named `PID-{8hex}.json` and contains:

```json
{
  "id": "PID-a7f3b2e1",
  "name": "Human-Readable Project Name",
  "slug": "project-slug",
  "repoPath": "/absolute/path/to/local/repo",
  "repoRemote": "https://github.com/user/repo",
  "currentPhase": "1c",
  "phaseHistory": [
    { "phase": "0", "completedAt": "2026-02-20" },
    { "phase": "0b", "completedAt": "2026-02-20" }
  ],
  "orientation": {
    "what": "One sentence — what does this do for whom",
    "done": "One sentence — how do you know it worked"
  },
  "modules": ["AuthClerk", "DbSupabase", "DeployRailway", "ObservabilitySentry"],
  "stack": {
    "language": "typescript",
    "framework": "express",
    "deploy": "railway",
    "external": ["slack"]
  },
  "personas": ["alex-the-time-poor-leader"],
  "maturityScore": null,
  "status": "active",
  "prdPath": null,
  "createdAt": "2026-02-20",
  "updatedAt": "2026-02-20"
}
```

## Field Reference

| Field | Purpose | Updated When |
|-------|---------|-------------|
| `id` | **Immutable project identifier (PID-{8hex}).** The primary key. Never changes. | Phase 1a (set once, never modified) |
| `name` | Human-readable project name | Phase 0 (can be updated) |
| `slug` | URL/file-safe identifier | Phase 0 (can be updated) |
| `repoPath` | Absolute path to local repo | Phase 1a (can be updated if repo moves) |
| `repoRemote` | GitHub remote URL | Phase 1b (after first push) |
| `currentPhase` | Which ABF phase the project is in | Every phase transition |
| `phaseHistory` | Ordered list of completed phases with dates | Every phase completion |
| `orientation` | The two Phase 0 sentences (what + done) | Phase 0, updated if Phase 0b sharpens them |
| `modules` | Which IaC modules are in use | Phase 1 |
| `stack` | Language, framework, deploy target, external services | Phase 1 |
| `personas` | User persona slugs from Phase 0b | Phase 0b |
| `maturityScore` | Score from MeasureSuccess (N/18) | MeasureSuccess workflow |
| `status` | `active`, `paused`, `complete`, `archived` | Manual or BuildRetrospective |
| `prdPath` | Path to Algorithm PRD if one exists | Algorithm integration |
| `createdAt` | Project creation date | Phase 1a (never changes) |
| `updatedAt` | Last modification date | Every update |

## Multi-Project Behavior

When AgentBuild is invoked, Lucy reads all `PID-*.json` files in this directory:

- **0 projects:** Route to `Workflows/FullBuild.md` Phase 0 (new project)
- **1 active project:** Ask "Continue with **[name]** (`PID-{id}`, Phase [X])?" or start new
- **2+ active projects:** List all with PID, phase, and path. Ask which to continue or start new.

**Example multi-project listing:**

```
You have 3 active AgentBuild projects:

1. Personalized Briefing Platform (PID-a7f3b2e1) — Phase 1c — ~/projects/briefing-platform
2. Bookmark Saver (PID-c4d8e9f0) — Phase 2a — ~/projects/bookmark-saver
3. Invoice Tool (PID-1b2c3d4e) — Phase 0b — ~/projects/invoice-tool

Which project would you like to continue, or start a new one?
```

## PID in Artifacts

Once a PID is assigned, it should appear in:

- **AGENTS.md:** `**Project ID:** PID-a7f3b2e1` in the header
- **Commit messages:** `[PID-a7f3b2e1] Add user onboarding flow`
- **PRD files:** `project_id: PID-a7f3b2e1` in frontmatter
- **Spec files:** Reference PID in header for traceability
- **Build task briefs:** Include PID so agents know which project context to load

This creates a complete audit trail — any artifact can be traced back to its project.

## Phase Update Protocol

At the end of every phase, update the project registry:

```
1. Verify PID gate (confirm you're updating the right project)
2. Set currentPhase to next phase
3. Append completed phase to phaseHistory with date
4. Update updatedAt
5. Save the JSON file as PID-{id}.json
```

This is not optional. A stale registry means the next session starts blind.
