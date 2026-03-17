---
name: briefing-pro
description: BriefingPro Context Loader — loads full project context for the BriefingPro coaching platform. USE WHEN starting any BriefingPro session, working on coach profile pages, revising HTML reference pages, updating specs, or any task related to the briefing-pro project.
---

## Why This Skill Exists

Claude Code is always opened from the PAI directory, not the briefing-pro project directory. This means the briefing-pro `CLAUDE.md` never auto-loads. This skill bridges that gap — it reads the project context file at its absolute path and gives Lucy a genuine understanding of the project before any work begins.

## Execution

**Step 1 — Read the project context file:**

Read this file in full:
```
/Users/michaelatherton/projects/briefing-pro/CLAUDE.md
```


**Step 2 — Synthesize and explain the project out loud.**

Do NOT just list the files and directories. Instead, write a genuine project briefing in your own words — the kind of summary a senior engineer would give a new teammate before their first day. Cover:

- **What BriefingPro is** — the product, who it's for, the core value proposition
- **Who the key personas are** — Steve (the coach using the product), Sarah Chen (demo client persona)
- **What the current work is** — the V6 coach profile, what it is, why it matters, what tabs exist and how they relate to each other
- **What's already built** — the 7 HTML reference pages, the Log Conversation slide-over, the spec library
- **Where things live** — specs, reference pages, design system, memory/PRD files (absolute paths)
- **How revision sessions work** — the pattern for applying feedback from stakeholders to the HTML pages

This should read like a lucid, confident orientation — not a directory listing.

**Step 3 — Output the orientation block:**

After your narrative, output this quick-reference block:

```
════ BriefingPro Loaded ══════════════════════════
Project root:   /Users/michaelatherton/projects/briefing-pro
Specs:          /Users/michaelatherton/projects/briefing-pro/docs/specs/
New Working Specs: /Users/michaelatherton/projects/briefing-pro/docs/specs/new-coach-profile-specs/overview
Pages:          /Users/michaelatherton/projects/briefing-pro/design-system/pages/
Design system:  /Users/michaelatherton/projects/briefing-pro/design-system/MASTER.md
Preview:        http://localhost:8181/design-system/pages/
Algorithm:      PAI Algorithm v{version} loaded
═════════════════════════════════════════════════
Ready. What are we working on?
```

**Step 4 — Load the current Algorithm.**

Read the LATEST pointer file to determine which algorithm version is active:
```
/Users/michaelatherton/Personal_AI_Infrastructure-v2+/.claude/PAI/Algorithm/LATEST
```

Then read the algorithm file it points to (e.g. if LATEST contains `v3.5.0`, read `v3.5.0.md` from the same directory). This ensures the correct algorithm version is loaded regardless of future upgrades.

Add the algorithm version to the orientation block:
```
Algorithm:      PAI Algorithm v{version} loaded
```

**Step 5 — Stop and wait.**

Do not read any additional files. Do not preemptively ask clarifying questions. Wait for Michael to tell you which tab, page, or spec we're working on — then read those specific files on demand.

Once Michael specifies the task, classify it immediately:
- **Single-file, quick change** → NATIVE mode
- **Anything else** (multi-file, spec update, new feature, debugging) → ALGORITHM mode, run the full algorithm using the version loaded in Step 4


