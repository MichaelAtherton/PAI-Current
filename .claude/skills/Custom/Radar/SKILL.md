---
name: Radar
description: Always-on opportunity detection system. Surfaces matches and warns about mismatches against TELOS profile and psychological architecture. USE WHEN radar, opportunities, job search, career match, assess opportunity, check fit, scan for opportunities, "is this right for me".
---

# Radar - Opportunity Detection System

**Always-on system that surfaces opportunities matching your TELOS profile and warns about mismatches.**

---

## Purpose

Radar continuously monitors configured sources for opportunities that align with your:
- **TELOS Profile** - Mission, goals, beliefs, strategies, narratives
- **Architecture** - Stable psychological traits, work style, risk tolerance, hard limits

It surfaces high-confidence matches immediately and warns when you pursue opportunities that conflict with your stated architecture.

---

## Philosophy: Reminders, Not Blockers

Radar warns but never blocks. Your goals evolve with experience.

- **Frame as "what you said"** - Not "what you should do"
- **Easy bypass** - Single keystroke to proceed anyway
- **Offer updates** - When bypassed, ask if profile should change
- **Track patterns** - Repeated bypasses may indicate drift (inform Vigilance)

---

## Triggers

| Trigger | Action |
|---------|--------|
| "radar" | Show recent surfaced opportunities |
| "radar scan" | Run immediate full scan |
| "radar configure" | Set up sources and thresholds |
| "assess this opportunity" | Single opportunity fit assessment |
| "is this right for me" | Assess opportunity against profile |
| "check fit" | Assess opportunity fit |
| "radar digest" | Show daily digest |
| "radar dismiss [id]" | Dismiss surfaced opportunity |

---

## Workflows

### Scan - Full Opportunity Scan
**File:** `Workflows/Scan.md`

Runs through all configured sources, fetches new opportunities, scores against profile, and surfaces matches above threshold.

```
User: "radar scan"
→ Fetch from enabled sources
→ Score each opportunity
→ Surface matches above threshold
→ Log to surfaced.jsonl
```

### Assess - Single Opportunity Assessment
**File:** `Workflows/Assess.md`

Deep assessment of a specific opportunity against full TELOS and Architecture profile.

```
User: "assess this opportunity: [URL or description]"
→ Parse opportunity details
→ Score against all TELOS dimensions
→ Score against architecture fit
→ Check hard limits
→ Return detailed breakdown
```

### Configure - Source Configuration
**File:** `Workflows/Configure.md`

Set up opportunity sources, thresholds, and notification preferences.

```
User: "radar configure"
→ Show current sources
→ Enable/disable sources
→ Set score thresholds
→ Configure notification channels
```

### Review - Review Surfaced Opportunities
**File:** `Workflows/Review.md`

Review and act on surfaced opportunities.

```
User: "show radar" / "radar"
→ Display surfaced opportunities sorted by score
→ Allow dismiss, investigate, or save actions
```

---

## Fit Assessment Algorithm

### Scoring Dimensions

| Category | Weight | Components |
|----------|--------|------------|
| **TELOS Alignment** | 40% | Mission, Goals, Beliefs, Strategies, Narratives |
| **Architecture Fit** | 40% | Autonomy, Structure, Risk, Meaning, Work Style |
| **Hard Limits** | 20% | Pass/fail on dealbreakers (0 if any violated) |

### Score Interpretation

| Score | Recommendation | Action |
|-------|----------------|--------|
| 0.90+ | Immediate Surface | Voice + Push notification |
| 0.75-0.90 | Daily Digest | Morning review |
| 0.50-0.75 | Weekly Roundup | Weekly summary |
| < 0.50 | Dismiss | Silent log only |

### Hard Limits

Hard limits are **absolute dealbreakers**. A single violation sets the entire score to 0 regardless of other factors. These come from `ARCHITECTURE.md`.

---

## Mismatch Warning

When you express intent toward an opportunity that conflicts with your profile:

```
📡 Radar note: This differs from your current profile—

• ARCHITECTURE.md: You set "[hard limit]" as a non-negotiable
• BELIEFS.md (B2): "[relevant belief]"

These were your past goals. If they've evolved, I can update them.

[Continue anyway] [Update profile] [Tell me more]
```

**Implementation:** The warning triggers on intent detection (phrases like "I should apply to", "I'm considering", "this looks interesting").

---

## Data Files

| File | Purpose | Location |
|------|---------|----------|
| `sources.json` | Configured opportunity sources | `Data/sources.json` |
| `surfaced.jsonl` | Log of surfaced opportunities | `Data/surfaced.jsonl` |
| `dismissed.jsonl` | Log of dismissed opportunities | `Data/dismissed.jsonl` |
| `radar-state.json` | Scanner state and cooldowns | `MEMORY/STATE/radar-state.json` |

---

## Source Types

| Type | Method | Integration |
|------|--------|-------------|
| `rss` | Direct fetch | WebFetch tool |
| `scrape` | Progressive scraping | BrightData skill |
| `api` | API calls | Research skill |
| `manual` | User-submitted | Direct entry |

### Default Sources (Configurable)

- HackerNews Who's Hiring (monthly RSS)
- Custom RSS feeds (daily)
- Manual submission (immediate)

---

## Background Scanning

Radar runs automatically via StopOrchestrator with a 6-hour cooldown:

1. Check cooldown (skip if < 6 hours since last scan)
2. Spawn detached RadarScanner.ts
3. Scanner fetches from enabled sources
4. Scores against profile
5. Surfaces matches above threshold
6. Notifies via configured channels

---

## Integration Points

| Skill | Use |
|-------|-----|
| **OSINT** | Company/person background on opportunities |
| **BrightData** | Progressive scraping for bot-protected sites |
| **Research** | Multi-source verification |
| **Browser** | Web page detail extraction |
| **Agents** | Specialized analysis agents |

---

## State Management

State is persisted in `MEMORY/STATE/radar-state.json`:

```json
{
  "last_scan": "2026-02-03T12:00:00Z",
  "next_scan": "2026-02-03T18:00:00Z",
  "scan_interval_hours": 6,
  "sources_enabled": ["manual"],
  "thresholds": {
    "immediate_surface": 0.9,
    "daily_digest": 0.75,
    "weekly_roundup": 0.5
  },
  "stats": {
    "total_scanned": 0,
    "total_surfaced": 0,
    "total_dismissed": 0
  }
}
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/radar` | Show current surfaced opportunities |
| `/radar scan` | Run immediate opportunity scan |
| `/radar assess <url>` | Assess specific opportunity |
| `/radar configure` | Configure sources and thresholds |
| `/radar digest` | Show daily digest |
| `/radar dismiss <id>` | Dismiss an opportunity |
| `/radar stats` | Show scanning statistics |

---

## Tools

| Tool | Purpose |
|------|---------|
| `FitAssessor.ts` | Core fit scoring algorithm |
| `RadarScanner.ts` | Background scanning script |
| `SourceFetcher.ts` | Fetch from configured sources |

---

## Morning Integration (Optional)

If configured, Radar surfaces in the morning greeting:

```
☀️ Good morning, {principal.name}.

📡 RADAR (since last review):

HIGH MATCH (0.87):
"[Opportunity Title]"
✓ M0: [Mission alignment]
✓ Architecture: [Key fit factor]
⚠️ [Warning if any]

[N more in daily digest] → "show radar digest"
```

---

*Radar helps you find opportunities that actually fit who you are—and warns when you're chasing ones that don't.*
