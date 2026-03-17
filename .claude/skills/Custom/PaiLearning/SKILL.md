---
name: PaiLearning
description: Periodic review of accumulated learning signals — failures, low ratings, and algorithm reflections — to extract actionable improvement proposals. USE WHEN digest learnings, review failures, run digest, digest learning signals, review learning signals, process failures, learning digest.
---

# PaiLearning — Digest Learnings

**Systematically reviews accumulated learning signals and extracts actionable improvement proposals. Three phases: Digest → Classify → Track.**

---

## Purpose

PAI's learning system captures failure analyses, low-rated interactions, and algorithm reflections into `MEMORY/LEARNING/`. Capturing is only half — without periodic review, signals accumulate without driving improvement. This skill closes the loop.

---

## Triggers

| Trigger | Action |
|---------|--------|
| "digest learnings" | Run a full digest of new learning signals |
| "review failures" | Run a full digest of new learning signals |
| "run digest" | Run a full digest of new learning signals |
| "digest learning signals" | Run a full digest of new learning signals |
| "review learning signals" | Run a full digest of new learning signals |

---

## Workflow: DigestLearnings

**Single workflow.** Three sequential phases.

```
User: "digest learnings"
→ Phase 1: DIGEST — scan new files, extract proposals
→ Phase 2: CLASSIFY — group proposals by change target
→ Phase 3: TRACK — apply approved changes, write watermark
```

---

### Phase 1 — DIGEST (Scan and Extract)

1. Check if `MEMORY/LEARNING/DIGEST-LOG.jsonl` exists.
   - **If it exists:** read the last line to get the last processed timestamp (the watermark).
   - **If it does not exist (first run):** treat the watermark as epoch zero — scan all files in all subdirectories, then create the file at the end of Phase 3.
2. Scan `MEMORY/LEARNING/` subdirectories for files created **after** that watermark, in priority order:
   1. `FAILURES/` — highest signal, explicit failure records
   2. Low-rated interactions (rating ≤ 4) in `ALGORITHM/` or `SYSTEM/`
   3. Recent `ALGORITHM/` entries — algorithm reflection data
   4. Recent `SYSTEM/` entries — system-level observations
3. For each file with actionable content, extract a structured proposal:

```markdown
### Proposal N: [Short Title]

**Problem:** [What went wrong or what gap was identified]
**Proposed fix:** [Specific corrective action]
**Target files:** [File(s) to change]
**Source:** [Source file path]
```

4. Files with no actionable content are noted as reviewed but skipped.
5. **Deduplicate** before finalizing proposals — the same incident may appear as a FAILURE, an ALGORITHM reflection, and a SYSTEM sentiment signal. Two signals are the same incident if they share **two or more** of: the same date, the same described behavior, or the same affected rule/file. When duplicates are found, use the FAILURES/ entry as the canonical source; note the others as "also covered by [canonical source]".

---

### Phase 2 — CLASSIFY

Classify each proposal by what it would change:

| Classification | Target | Process |
|---------------|--------|---------|
| **USER-SAFE** | `PAI/USER/`, `MEMORY/`, `settings.json` | Apply directly if approved |
| **SYSTEM-PATCH** | `hooks/`, `PAI/Tools/`, `PAI/SYSTEM/` | Requires LOCAL_PATCHES.md entry + upstream issue |
| **UPSTREAM-ONLY** | Needs core architectural change | File upstream issue only |

Present proposals **grouped by classification** with inline context per proposal. Collect decisions via structured questions — do not present a flat report and wait.

---

### Phase 3 — TRACK

Act on approved decisions:

- **USER-SAFE (approved):** Apply changes directly, show diff.
- **SYSTEM-PATCH (approved):** Apply change + add `LOCAL_PATCHES.md` entry + file upstream issue.
- **UPSTREAM-ONLY (approved):** File upstream issue only.

After all actions are complete, append a watermark entry to `MEMORY/LEARNING/DIGEST-LOG.jsonl` (create the file if this is the first run):

```jsonl
{"timestamp":"<ISO8601>","files_reviewed":["file1.md","file2.md"],"proposals":<N>,"already_covered":["<description>"],"meta":"<pattern observation>"}
```

---

## Key Design Rules

1. **No changes without approval.** The digest presents proposals and collects decisions. Nothing is applied automatically.
2. **Deduplicate before proposing.** The capture system intentionally over-records — the same incident may appear multiple times across directories. Resolve to one proposal per unique incident.
3. **Watermark prevents drift.** Only files created after the last watermark timestamp are scanned. This prevents re-processing and keeps digests fast.
4. **Most signals are adherence failures, not rule gaps.** After initial stabilization, 80%+ of incidents map to existing rules that weren't followed, not missing rules. Note this pattern in the watermark `meta` field when observed.

---

## Data Files

| File | Purpose |
|------|---------|
| `MEMORY/LEARNING/DIGEST-LOG.jsonl` | Watermark log — tracks last processed timestamp |
| `MEMORY/LEARNING/FAILURES/` | Explicit failure records (highest priority) |
| `MEMORY/LEARNING/ALGORITHM/` | Algorithm reflection data |
| `MEMORY/LEARNING/SYSTEM/` | System-level sentiment and observations |
