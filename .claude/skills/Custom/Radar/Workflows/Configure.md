# Configure - Source Configuration

**Set up opportunity sources, thresholds, and notification preferences.**

---

## Trigger

- "radar configure"
- "configure radar sources"
- "set up radar"

---

## Workflow

### Step 1: Show Current Configuration

```
📡 RADAR CONFIGURATION

─────────────────────────────────────

SOURCES

[✓] manual - Manual Submission
[✓] hn_whoishiring - HN Who's Hiring (monthly RSS)
[ ] linkedin_saved - LinkedIn Saved Searches (daily scrape)
[ ] custom_rss - Custom RSS Feeds

─────────────────────────────────────

THRESHOLDS

Immediate Surface: 0.90
Daily Digest: 0.75
Weekly Roundup: 0.50

─────────────────────────────────────

NOTIFICATIONS

Voice: Enabled (high matches only)
Push: Disabled
Digest: Morning review

─────────────────────────────────────

SCAN INTERVAL: 6 hours

─────────────────────────────────────

What would you like to configure?
[Sources] [Thresholds] [Notifications] [Interval]
```

### Step 2: Handle Configuration Changes

**Enable/Disable Source:**
```
User: enable linkedin_saved

→ Update sources.json
→ Confirm: "LinkedIn Saved Searches enabled. Note: Requires BrightData for scraping."
```

**Add Custom RSS:**
```
User: add rss feed https://example.com/jobs.xml

→ Validate feed URL
→ Add to sources.json
→ Confirm: "Added custom RSS: example.com/jobs.xml"
```

**Adjust Thresholds:**
```
User: set immediate threshold to 0.85

→ Update radar-state.json thresholds
→ Confirm: "Immediate surface threshold set to 0.85"
```

**Change Scan Interval:**
```
User: scan every 12 hours

→ Update radar-state.json scan_interval_hours
→ Confirm: "Scan interval set to 12 hours"
```

### Step 3: Validate Changes

After any change:
1. Validate configuration is consistent
2. Test source connectivity if applicable
3. Confirm change to user

---

## Source Types

### RSS Feeds
```json
{
  "id": "custom_rss_1",
  "name": "My Custom Feed",
  "type": "rss",
  "url": "https://example.com/feed.xml",
  "frequency": "daily",
  "enabled": true
}
```

### Scrape Sources (requires BrightData)
```json
{
  "id": "linkedin_jobs",
  "name": "LinkedIn Jobs",
  "type": "scrape",
  "method": "brightdata",
  "urls": ["https://linkedin.com/jobs/search?..."],
  "frequency": "daily",
  "enabled": false
}
```

### API Sources
```json
{
  "id": "github_jobs",
  "name": "GitHub Jobs",
  "type": "api",
  "endpoint": "https://api.github.com/...",
  "frequency": "weekly",
  "enabled": false
}
```

---

## Notification Options

| Channel | Description | Default |
|---------|-------------|---------|
| `voice` | TTS announcement for high matches | Enabled |
| `push` | ntfy push notification | Disabled |
| `digest` | Include in morning review | Enabled |
| `discord` | Post to Discord channel | Disabled |

---

## Output

Configuration changes are saved to:
- `Data/sources.json` - Source definitions
- `MEMORY/STATE/radar-state.json` - Thresholds, intervals, preferences
