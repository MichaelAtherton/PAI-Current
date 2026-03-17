# Review - Review Surfaced Opportunities

**Review and act on surfaced opportunities.**

---

## Trigger

- "radar" / "show radar"
- "radar review"
- "show opportunities"
- "what's in my radar"

---

## Workflow

### Step 1: Load Surfaced Opportunities

```
Read: skills/Radar/Data/surfaced.jsonl
Filter: status = "new" OR status = "saved"
Sort: by score descending
```

### Step 2: Display Summary

```
📡 RADAR - Surfaced Opportunities

─────────────────────────────────────

NEW (3)

#1 🔴 0.94 | AI Safety Research Lead
   Anthropic | Remote
   ✓ M0: Human flourishing | ✓ High autonomy
   [assess] [save] [dismiss]

#2 🟠 0.81 | Open Source Maintainer
   PAI Community | Remote
   ✓ G3: Expand PAI | ⚠️ Lower comp
   [assess] [save] [dismiss]

#3 🟡 0.76 | Technical Writer
   Vercel | NYC/Remote
   ✓ B2: Tech communication | ⚠️ Narrow scope
   [assess] [save] [dismiss]

─────────────────────────────────────

SAVED (1)

#4 🟠 0.83 | Developer Advocate
   Cloudflare | Austin
   Saved 3 days ago
   [assess] [dismiss]

─────────────────────────────────────

Actions: [assess #N] [save #N] [dismiss #N] [dismiss all below 0.7]
```

### Step 3: Handle Actions

**Assess:**
```
User: assess #1

→ Run full Assess workflow on opportunity #1
→ Show detailed breakdown
```

**Save:**
```
User: save #2

→ Update status in surfaced.jsonl to "saved"
→ Confirm: "Saved: Open Source Maintainer"
```

**Dismiss:**
```
User: dismiss #3

→ Move from surfaced.jsonl to dismissed.jsonl
→ Confirm: "Dismissed: Technical Writer"
```

**Bulk Dismiss:**
```
User: dismiss all below 0.7

→ Move all opportunities with score < 0.7 to dismissed.jsonl
→ Confirm: "Dismissed 2 opportunities below 0.70"
```

### Step 4: Show Empty State

If no surfaced opportunities:

```
📡 RADAR

No opportunities currently surfaced.

─────────────────────────────────────

Last scan: 2 hours ago
Next scan: ~4 hours

Sources enabled: manual, hn_whoishiring

─────────────────────────────────────

Actions:
- "radar scan" - Run immediate scan
- "assess [url]" - Manually assess an opportunity
- "radar configure" - Adjust sources
```

---

## Digest View

For daily/weekly digests:

```
User: radar digest

📡 RADAR DIGEST (Last 24 hours)

─────────────────────────────────────

IMMEDIATE (1)
🔴 0.94 | AI Safety Research Lead @ Anthropic

DAILY (2)
🟠 0.81 | Open Source Maintainer @ PAI
🟠 0.78 | Platform Engineer @ Render

WEEKLY (4)
🟡 0.72 | Senior Dev @ Acme Corp
🟡 0.68 | Tech Lead @ Startup X
🟡 0.65 | ...

─────────────────────────────────────

Scanned: 47 total | Surfaced: 7 | Dismissed: 40
```

---

## Data Structure

**surfaced.jsonl entries:**
```json
{
  "id": "opp_abc123",
  "title": "AI Safety Research Lead",
  "company": "Anthropic",
  "url": "https://...",
  "score": 0.94,
  "recommendation": "surface",
  "status": "new",
  "scannedAt": "2026-02-03T12:00:00Z",
  "source": "hn_whoishiring",
  "telosScore": 0.92,
  "archScore": 0.88,
  "warnings": []
}
```

**Status values:**
- `new` - Just surfaced, not reviewed
- `saved` - User saved for later
- `dismissed` - User dismissed (moved to dismissed.jsonl)
