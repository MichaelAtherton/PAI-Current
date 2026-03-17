# DigestLearnings — Periodic Review of Learning Signals

> A PAI skill that systematically reviews accumulated learning signals (failures, low ratings, algorithm reflections) and extracts actionable improvement proposals. Three phases: **Digest → Classify → Track.**

## Why

PAI's learning system captures failure analyses, low-rated interactions, and algorithm reflections into `MEMORY/LEARNING/`. But capturing is only half — without periodic review, the signals accumulate without driving improvement. This skill closes the loop.

## How It Works

### Watermark-Based Incremental Processing

Each digest run reads `MEMORY/LEARNING/DIGEST-LOG.jsonl` for the last processed timestamp. Only files created after that watermark are scanned. This prevents re-processing and keeps digests fast.

```jsonl
{"timestamp":"2026-03-12T20:30:00+01:00","files_reviewed":["file1.md","file2.md"],"proposals":0,"already_covered":["F1 by existing rule X"],"meta":"Pattern: adherence failures, not rule gaps"}
```

### Phase 1 — DIGEST (Scan and Extract)

Scans `MEMORY/LEARNING/` subdirectories in priority order:

1. **`FAILURES/`** — highest signal, explicit failure records
2. **Low-rated interactions** (rating ≤ 4 in `ALGORITHM/` or `SYSTEM/`)
3. **Recent `ALGORITHM/` entries** — algorithm reflection data
4. **Recent `SYSTEM/` entries** — system-level observations

For each file with actionable content, extracts a structured proposal:

```markdown
### Proposal 1: Check Before Creating Files

**Problem:** AI created new files without checking if related files already existed
**Proposed fix:** Add rule to glob target directory before Write operations
**Target files:** PAI/USER/AISTEERINGRULES.md
**Source:** FAILURES/2026-03-01-135514_...
```

Files with no actionable content (e.g., correctly handled but still low-rated) are noted as reviewed but skipped.

### Phase 2 — CLASSIFY

Each proposal is classified by what it would change:

| Classification | Target | Process |
|---------------|--------|---------|
| **USER-SAFE** | `PAI/USER/`, `MEMORY/`, `settings.json` | Apply directly if approved |
| **SYSTEM-PATCH** | `hooks/`, `PAI/Tools/`, `PAI/SYSTEM/` | Requires LOCAL_PATCHES.md entry + upstream issue |
| **UPSTREAM-ONLY** | Needs core architectural change | File upstream issue only |

Results are presented grouped by classification with inline context per proposal, then decisions collected via structured questions (not a flat report-and-wait).

### Phase 3 — TRACK

- **USER-SAFE (approved):** Apply changes directly, show diff
- **SYSTEM-PATCH (approved):** Apply change + add LOCAL_PATCHES.md entry + file upstream issue
- **UPSTREAM-ONLY (approved):** File upstream issue only

Finally, append a watermark entry to `DIGEST-LOG.jsonl`.

## Key Design Decisions

1. **Deduplication matters.** The capture system intentionally over-records — the same incident may appear as a FAILURE, an ALGORITHM reflection, and a SYSTEM sentiment signal. The digest must deduplicate before proposing.

2. **Most signals are adherence failures, not rule gaps.** After ~7 digests, we found that 80%+ of incidents map to existing rules that weren't followed, not missing rules. This is the expected mature state — the rule set stabilizes and the challenge shifts to execution consistency.

3. **No changes without approval.** The digest presents proposals and collects decisions. Nothing is applied automatically.

4. **Watermark prevents drift.** Without incremental processing, each digest would re-scan everything and potentially re-propose already-resolved items.

## Adapting for Your Setup

The skill assumes:
- Learning signals in `MEMORY/LEARNING/` with subdirectories (FAILURES/, ALGORITHM/, SYSTEM/)
- A `DIGEST-LOG.jsonl` watermark file
- Steering rules or behavioral rules that proposals can target
- A LOCAL_PATCHES.md system for tracking modifications to upstream files

If your PAI instance captures learning signals differently, adjust the scan paths in Phase 1. The three-phase pattern (scan → classify → track) works regardless of signal format.

## Results After 7 Digests

| Digest | Files | Unique Incidents | Proposals | Applied |
|--------|-------|-----------------|-----------|---------|
| #1 (2026-02-28) | 8 | 2 | 0 | 0 |
| #2 (2026-03-02) | 14 | 7 | 3 | 3 |
| #3 (2026-03-05) | 12 | 6 | 0 | 0 |
| #4 (2026-03-09) | 27 | 8 | 3 | 3 |
| #5–#7 | 11-14 | 3-5 | 0 | 0 |

**Pattern:** Early digests found genuine rule gaps. After ~4 digests, the rule set stabilized. Subsequent digests confirm adherence is the challenge, not coverage.

## File Structure

```
skills/Digest/
├── SKILL.md              # Skill metadata and trigger words
└── Workflows/
    └── DigestLearnings.md  # Full workflow instructions
```