# Prompt Library

## Engineering Meeting Summary
**Use when:** After any engineering team meeting — standups, sprint planning, design reviews — to produce a consistent, scannable summary for Slack.
**Last updated:** 2026-03-06
**Element scores:** Instructions [3] | Examples [3] | Guardrails [3] | Format [3] | Ambiguity [2]

### Template
You are a staff engineer writing a meeting summary for a {{TEAM_SIZE}}-person engineering team.
The summary will be posted in {{DESTINATION}}, so it must be scannable in under 30 seconds.

#### Instructions
Summarize the meeting notes below into exactly this structure:

1. **Meeting type** — one of: {{MEETING_TYPES}}
2. **One-sentence summary** — the single most important outcome or decision, max 20 words
3. **Key decisions** — bulleted list. If no decisions were made, write "None — discussion only"
4. **Action items** — bulleted list formatted as: "- [OWNER]: [task] (by [date if mentioned])"
   If no action items exist, write "No action items captured"
5. **Open questions** — anything unresolved that needs follow-up. If none, write "None"
6. **Parking lot** — topics raised but deferred. If none, omit this section entirely

#### Guardrails
- Maximum {{MAX_WORDS}} words total. If the summary exceeds this, cut from Key Decisions first (keep Action Items intact).
- Never invent information not present in the notes. If notes are unclear on who owns an action item, write "[OWNER UNCLEAR]" instead of guessing.
- Never editorialize. No "the team had a productive discussion" or "good progress was made." Report what happened.
- If the notes are too fragmentary to produce a useful summary, say: "Notes insufficient — missing [what's missing]. Please clarify before I summarize."

#### Example summary
{{EXAMPLE_SUMMARY}}

---
Now summarize these meeting notes:

{{MEETING_NOTES}}

### Variables
| Variable | Description |
|----------|-------------|
| `{{TEAM_SIZE}}` | Number of people on the team (sets formality level) |
| `{{DESTINATION}}` | Where the summary is posted — Slack, email, Notion, etc. |
| `{{MEETING_TYPES}}` | Comma-separated list of meeting types the team uses |
| `{{MAX_WORDS}}` | Word limit for the entire summary |
| `{{EXAMPLE_SUMMARY}}` | One filled-in example showing ideal output format |
| `{{MEETING_NOTES}}` | The raw meeting notes to summarize |

### Example (filled)
You are a staff engineer writing a meeting summary for a 5-person engineering team.
The summary will be posted in Slack, so it must be scannable in under 30 seconds.

[Instructions as above, with meeting types: standup, sprint planning, design review, or other (specify)]
[Guardrails as above, with max 200 words]

Example of a good summary:

**Meeting type:** Design review
**Summary:** Team approved the new caching layer design with Redis, pending load test results.
**Key decisions:**
- Use Redis over Memcached for the session cache
- Target 50ms p99 latency for cache hits

**Action items:**
- Sarah: Run load test on Redis cluster (by Friday)
- Jake: Update the ADR with today's decision (by EOD Wednesday)

**Open questions:**
- Do we need a fallback if Redis is unavailable, or is downtime acceptable?

---
Now summarize these meeting notes:

[pasted notes]

### Known failure modes
- **No format specified = format roulette.** The model picks bullets, paragraphs, or numbered lists based on input shape. Fix: the rigid 5-section structure.
- **Missing "no decisions" fallback = phantom decisions.** The model fabricates decisions to fill the section. Fix: explicit "None — discussion only" instruction.
- **No ownership format for action items = untrackable actions.** Items like "need to run load test" have no owner. Fix: enforced "[OWNER]: [task] (by [date])" format.
- **No word limit = length lottery.** Summaries range from 3 to 30 lines. Fix: 200-word cap with priority rule.
- **Ambiguous notes + no escape hatch = confident garbage.** The model summarizes fragmentary notes as if they were complete. Fix: "Notes insufficient" fallback.
- **No anti-editorializing rule = filler.** "Productive discussion" and "great progress" pad the summary without adding information. Fix: explicit ban.
