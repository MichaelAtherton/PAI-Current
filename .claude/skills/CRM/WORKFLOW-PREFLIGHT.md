# Twenty Workflow Pre-Flight Protocol

**READ THIS BEFORE WRITING ANY TWENTY WORKFLOW CODE.**

This document exists because in April 2026 we burned hours reverse-engineering
Twenty's workflow API across 8 bugs, only to discover the canonical patterns
were documented in Twenty's own MCP tool schemas the whole time. This protocol
stops that from happening again.

---

## The Rule

**Before writing ANY workflow mutation code (create_workflow_version_step,
create_workflow_version_edge, update_workflow_version_step, etc.), you MUST
complete the pre-flight steps below.** Skipping them is not a speed win — it
is a guarantee that you will re-derive canonical patterns the hard way.

---

## Pre-Flight Checklist

### Step 1 — Load the canonical skill

Twenty has a built-in `workflow-building` skill. It is the authoritative source.
Read it first. It is stored at:

```
.claude/skills/CRM/TWENTY-CODE-TRACES/skills/workflow-building.md
```

Time: 60 seconds. Payoff: critical rules like "create_complete_workflow does NOT
create logic functions for CODE steps — use create_workflow_version_step instead."

### Step 2 — Consult the offline schema snapshots

The exact JSON schemas for all 15 workflow tools are committed at:

```
.claude/skills/CRM/References/mcp-snapshots/tool-catalog.json      (218 tools, 7 categories)
.claude/skills/CRM/References/mcp-snapshots/workflow-tool-schemas.json (15 workflow tools)
```

Grep/read them for the tool you need. Do NOT guess parameter shapes.

### Step 3 — Refresh the schemas if stale

If the snapshots are older than 30 days OR if Twenty has been upgraded since
the last snapshot, refresh them:

```bash
# Get fresh catalog + schemas from live MCP endpoint
curl -s -X POST 'http://localhost:3030/mcp' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tool_catalog","arguments":{}}}'
```

(See `backup-workflow.py` helper pattern for the auth flow.)

### Step 4 — Read CanonicalVsOurs.md

```
.claude/skills/CRM/References/CanonicalVsOurs.md
```

This is the delta between our build-script conventions and Twenty's canonical
patterns. Read it before writing new workflow code so you start from the
verified baseline, not from memory.

### Step 5 — Read BugFindings and the failure-mode catalog

```
.claude/skills/CRM/References/BugFindings-2026-04-04.md
.claude/skills/CRM/References/WORKFLOW-FAILURE-MODES.md   (see below)
```

Each bug we hit has a "how this returns if you skip the pre-flight" note.

### Step 6 — Only now, start writing code

You have the tool names, the parameter shapes, the known quirks, and the
failure modes. Write the code.

### Step 7 — Always run graph verification

Every build script that assembles workflow graphs MUST include a
post-Phase-3 graph verification function like the one in
`build-contact-aging-workflow.py` (`verify_graph()`). It catches missing
edges BEFORE runtime. Without it, Bug 6 (silent iterator stall from
missing edges) returns in about 10 minutes.

### Step 8 — Always smoke test with LIMIT=2 or LIMIT=3 before LIMIT=500

Full production runs take 25+ minutes. A 2-item smoke test takes 45 seconds
and catches the same class of bugs. Never go straight to production limits.

---

## Red Flags — You Are Skipping The Pre-Flight

If you catch yourself thinking any of these, STOP and restart with Step 1:

| Thought | Reality |
|---------|---------|
| "I remember the GraphQL mutation shape from last time" | Memory decays. Twenty's schema doesn't. Read the snapshot. |
| "I'll just write the code and fix bugs as they come up" | That's how we burned hours last time. Pre-flight is 10 minutes. |
| "This is a small change, I don't need to check the schema" | Bug 6 (missing edges) was a small change. It silently broke everything. |
| "I can't find a canonical answer, I'll improvise" | Hit the live MCP endpoint with `learn_tools`. Do not guess. |
| "The workflow works, why verify the graph?" | Bug 6 produced a "working" workflow that processed 1 of 167 items. Graph verify is mandatory. |
| "I'll skip the smoke test, production is fine" | Full runs take 25 min. If production fails you waste 25 min. Smoke test takes 45s. |

---

## What the Pre-Flight Would Have Caught

| Bug | Would pre-flight have prevented it? | How |
|-----|-------------------------------------|-----|
| 1. outputSchema TEXT vs DATE_TIME | PARTIAL — schema doesn't say, but CanonicalVsOurs notes field-type matching |
| 2. OPENAI_API_KEY race | NO — infrastructure issue, not an API usage issue |
| 4. Iterator history stall | NO — undocumented worker bug |
| 5. FIND_MSG empty filter cascade | YES — documented in workflow-building skill (GitHub #18814) |
| 6. Missing edges | YES — MCP schema makes it obvious edges are separate from step config |
| 7. AI response not parsed | YES — workflow-building skill describes AI_AGENT output wrapper pattern |
| 8. FIND filter on wrong field | YES — `list_object_metadata_items` before referencing fieldMetadataIds |
| sourceConnectionOptions misuse | YES — schema description IS ambiguous, but `learn_tools` error message is decisive on first test call |

**Score: 5 of 8 bugs (62%) would have been prevented by a 10-minute pre-flight.**

---

## Updating This Protocol

If you discover a new class of bug or a new canonical pattern:

1. Add it to `References/BugFindings-{date}.md` with the classification
2. Add an entry to the "Red Flags" table above if it's a skip-prevention signal
3. If it's a new failure mode, add it to `References/WORKFLOW-FAILURE-MODES.md`
4. Update the MCP snapshots if the schema changed
5. Commit with a note referencing the bug

This document should grow. Each bug we never repeat is a win.
