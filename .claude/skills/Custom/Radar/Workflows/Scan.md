# Scan - Full Opportunity Scan

**Run through all configured sources, fetch new opportunities, and surface matches.**

---

## Trigger

- "radar scan"
- "scan for opportunities"
- "check for new opportunities"
- Background: StopOrchestrator (6-hour cooldown)

---

## Workflow

### Step 1: Load Configuration

```
Read: skills/Radar/Data/sources.json
Read: MEMORY/STATE/radar-state.json
```

Check enabled sources and last scan time.

### Step 2: Fetch From Sources

For each enabled source:

| Source Type | Method |
|-------------|--------|
| `rss` | WebFetch with RSS parsing |
| `scrape` | BrightData progressive tiers |
| `api` | Direct API calls |
| `manual` | Skip (user-submitted only) |

```typescript
interface RawOpportunity {
  id: string;
  title: string;
  description: string;
  url?: string;
  source: string;
  fetchedAt: string;
}
```

### Step 3: Deduplicate

Compare against previously scanned (by URL/title hash):
- Skip if already in `surfaced.jsonl` or `dismissed.jsonl`
- Only process new opportunities

### Step 4: Score Each Opportunity

For each new opportunity:
1. Call FitAssessor.ts
2. Get overall score and breakdown
3. Determine recommendation

### Step 5: Route by Score

| Score | Action |
|-------|--------|
| >= 0.90 | Immediate notification (voice + push) |
| >= 0.75 | Add to daily digest |
| >= 0.50 | Add to weekly roundup |
| < 0.50 | Log and dismiss silently |

### Step 6: Log Results

Append to appropriate log:

**surfaced.jsonl** (score >= 0.50):
```json
{
  "id": "opp_123",
  "title": "...",
  "score": 0.87,
  "recommendation": "surface",
  "scannedAt": "2026-02-03T12:00:00Z",
  "source": "hn_whoishiring",
  "status": "new"
}
```

**dismissed.jsonl** (score < 0.50):
```json
{
  "id": "opp_456",
  "title": "...",
  "score": 0.32,
  "reason": "Hard limit violation: finance industry",
  "scannedAt": "2026-02-03T12:00:00Z"
}
```

### Step 7: Update State

```json
{
  "last_scan": "2026-02-03T12:00:00Z",
  "stats": {
    "total_scanned": 1247,
    "total_surfaced": 23,
    "total_dismissed": 89
  }
}
```

### Step 8: Notify

**Immediate (score >= 0.90):**
```
Voice: "High match opportunity found: [title]"
Push: ntfy notification with details
```

**Daily Digest:**
Queue for morning review integration.

---

## Output

```
📡 RADAR SCAN COMPLETE

Scanned: 47 opportunities from 3 sources
New: 12 (35 previously seen)

─────────────────────────────────────

SURFACED (3):

🔴 HIGH (0.94): "AI Safety Research Lead" @ Anthropic
🟠 MEDIUM (0.81): "Open Source Maintainer" @ PAI
🟡 MEDIUM (0.76): "Technical Writer" @ Vercel

─────────────────────────────────────

DISMISSED (9):
- Finance industry (3)
- Low mission alignment (4)
- Insufficient autonomy (2)

─────────────────────────────────────

Next scan: ~6 hours
```

---

## Background Mode

When triggered by StopOrchestrator:

1. Check cooldown (6 hours)
2. If in cooldown, skip silently
3. If ready, spawn detached RadarScanner.ts
4. Scanner runs independently
5. Notifications fire if high matches found

---

## Source Configuration

Sources are defined in `Data/sources.json`:

```json
{
  "sources": [
    {
      "id": "hn_whoishiring",
      "name": "HN Who's Hiring",
      "type": "rss",
      "url": "https://hnrss.org/whoishiring/jobs",
      "frequency": "monthly",
      "enabled": true
    },
    {
      "id": "manual",
      "name": "Manual Submission",
      "type": "manual",
      "enabled": true
    }
  ]
}
```
