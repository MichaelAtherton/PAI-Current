---
name: CRM
description: "Twenty CRM operator — CRUD, pipeline, automations, search, data hygiene, and AI agent integration via direct API. USE WHEN CRM, Twenty, contact, company, person, deal, opportunity, pipeline, lead, note, task, webhook, automation, workflow, duplicate, merge, search CRM, pipeline report, onboard client, log call, close deal, set up automation, clean data, configure MCP, AI agent, add contact, update deal, check pipeline"
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_DIR}/PAI/USER/SKILLCUSTOMIZATIONS/CRM/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## MANDATORY: Voice Notification

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the CRM skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **CRM** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# CRM Skill — Twenty CRM Operator

Operate Twenty CRM through natural language. CRUD on entities, pipeline management, automations, search, data hygiene, and AI agent integration — all via verified direct API calls.

## MANDATORY: Workflow Pre-Flight Protocol

**If the user's request touches Twenty workflows (creating, modifying, debugging, or extending any automation), READ `WORKFLOW-PREFLIGHT.md` BEFORE writing any mutation code.**

The pre-flight protocol exists because we burned hours in April 2026 reverse-engineering canonical patterns that were already documented in Twenty's MCP tool schemas. The protocol stops that from recurring.

Key pre-flight artifacts (all in this skill directory):
- `WORKFLOW-PREFLIGHT.md` — the step-by-step pre-flight checklist
- `References/CanonicalVsOurs.md` — delta between our conventions and canonical Twenty patterns
- `References/mcp-snapshots/tool-catalog.json` — offline snapshot of all 218 MCP tools
- `References/mcp-snapshots/workflow-tool-schemas.json` — offline snapshot of 15 workflow tool schemas
- `References/WORKFLOW-FAILURE-MODES.md` — concrete failure modes catalog with diagnostics
- `References/WorkflowDebugging.md` — investigation protocol and worker instrumentation guide
- `References/BugFindings-2026-04-04.md` — classified history of 8 bugs we hit
- `TWENTY-CODE-TRACES/skills/workflow-building.md` — Twenty's own built-in skill (verbatim)
- `Templates/build-contact-aging-workflow.py` — canonical build-script pattern to copy
- `Templates/backup-workflow.py` — JSON snapshot tool; always run before schema changes

**Pre-flight violations are a critical failure class.** Skipping pre-flight produces workflows that silently fail in ways we've already seen before. See `WORKFLOW-PREFLIGHT.md` §Red Flags for the specific rationalizations that indicate skip-in-progress.

## MANDATORY: Bug Investigation Protocol

**No public API documentation exists for Twenty's workflow engine.** All API behavior must be verified empirically. When any step fails or produces unexpected results:

1. **STOP after 15 minutes of inline debugging.** Do not continue guessing.
2. **Document the symptom:** exact error message, step name, what was expected vs actual.
3. **Write 2-3 targeted test hypotheses** (e.g., "Does REST accept ISO strings for DATE_TIME?", "Is the filter operand case-sensitive?").
4. **Run the tests via direct API calls** — curl to REST or GraphQL. Not source code reading.
5. **Document findings** in `References/BugFindings-{date}.md` before attempting any fix.

This protocol is mandatory for all automation/workflow work. Formal investigation with parallel test agents saves hours over inline debugging.

## Auth Check (runs before any operation)

1. Read `TWENTY_API_KEY` from environment
   - If set → use as `Bearer {TWENTY_API_KEY}` for all API calls
   - If not set → read `TWENTY_BASE_URL`, `TWENTY_EMAIL`, `TWENTY_PASSWORD` from env
     → Read `References/Bootstrap.md` and execute the JWT login flow
     → Use the returned token for this session
2. Set `BASE` from `TWENTY_BASE_URL` (default: `http://localhost:3030`)
3. Verify connection: `GET {BASE}/healthz`
   - If fails → tell Michael: "Twenty CRM is not running. Start it with: `~/Desktop/twenty.sh start`"
   - If succeeds → proceed to routing
4. Set `TOKEN` to the API key or JWT token obtained above. Use `Authorization: Bearer {TOKEN}` and `Content-Type: application/json` on all API calls.
5. **If the task involves workflow step creation/modification:** The API key is NOT sufficient — workflow mutations require a user ACCESS token. Follow `References/Bootstrap.md` Steps 3-4 (`getLoginTokenFromCredentials` → `getAuthTokensFromLoginToken`) to get a user token. Use env vars `TWENTY_EMAIL` and `TWENTY_PASSWORD` or credentials `michael@pai.local` / `pai2026!`.

## Workflow Routing

Route to **Workflows** for multi-step operations, **References** for single operations.

| User intent | Route to |
|---|---|
| "Onboard [client/company]", "new client", "new customer" | `Workflows/OnboardClient.md` |
| "Log [call/meeting/interaction]", "meeting notes" | `Workflows/LogInteraction.md` |
| "Close [deal]", "deal won/lost", "mark as won" | `Workflows/CloseDeal.md` |
| "Set up [automation/webhook/trigger]", "when X happens do Y" | `Workflows/SetupAutomation.md` |
| "Build [workflow]", "create workflow", "workflow steps", "workflow API" | `References/Automations.md` |
| "Clean [data]", "find duplicates", "merge", "bulk import" | `Workflows/CleanupData.md` |
| "Pipeline report", "forecast", "how's the pipeline" | `Workflows/DailyPipelineReport.md` |
| "Set up AI agent", "configure MCP", "connect AI" | `Workflows/ConfigureAIAgent.md` |
| Simple CRUD (add/get/update/delete contact/company) | `References/Entities.md` |
| Pipeline ops (deal stages, opportunities) | `References/Pipeline.md` |
| Task/note management | `References/Activities.md` |
| Search, filter, query | `References/SearchReport.md` |
| Error, something broke | `References/Errors.md` |
| First connection, auth issue | `References/Bootstrap.md` |
| Custom objects, fields, schema | `References/DataHygiene.md` |
| AI/MCP reference lookup | `References/AIAgents.md` |

**If unsure**, route to `References/Entities.md` — most CRM tasks start there.

**Multi-file tasks:** Some intents load multiple files. For example:
- "Add a contact and create a deal" → `References/Entities.md` + `References/Pipeline.md`
- "Something broke" → `References/Errors.md`
