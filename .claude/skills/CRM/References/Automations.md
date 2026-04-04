# Automations: Webhooks, Workflows, and Logic Functions

> Variables `{BASE}` and `{TOKEN}` are set by the auth preamble in SKILL.md.

## 1. Create a Webhook

Webhooks are managed via the metadata GraphQL endpoint.

```http
POST {BASE}/metadata
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "query": "mutation { createWebhook(input: { targetUrl: \"https://your-endpoint.com/hook\", operations: [\"*.created\", \"*.updated\"] }) { id targetUrl operations } }"
}
```

**Expected response** (200 OK):
```json
{
  "data": {
    "createWebhook": {
      "id": "webhook-uuid-1234",
      "targetUrl": "https://your-endpoint.com/hook",
      "operations": ["*.created", "*.updated"]
    }
  }
}
```

**Operations format:** `{objectName}.{event}` where event is `created`, `updated`, or `deleted`.

| Pattern              | Meaning                          |
|---------------------|----------------------------------|
| `*.created`          | Any object created               |
| `person.updated`     | A person record updated          |
| `company.deleted`    | A company record deleted         |
| `*.deleted`          | Any object deleted               |
| `opportunity.created`| An opportunity record created    |

---

## 2. List Webhooks

```http
POST {BASE}/metadata
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "query": "{ webhooks { edges { node { id targetUrl operations } } } }"
}
```

**Expected response** (200 OK):
```json
{
  "data": {
    "webhooks": {
      "edges": [
        {
          "node": {
            "id": "webhook-uuid-1234",
            "targetUrl": "https://your-endpoint.com/hook",
            "operations": ["*.created", "*.updated"]
          }
        }
      ]
    }
  }
}
```

---

## 3. Delete a Webhook

```http
POST {BASE}/metadata
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "query": "mutation { deleteWebhook(id: \"webhook-uuid-1234\") { id } }"
}
```

**Expected response** (200 OK):
```json
{
  "data": {
    "deleteWebhook": {
      "id": "webhook-uuid-1234"
    }
  }
}
```

---

## 4. Webhook Payload Format

When Twenty fires a webhook, it sends a POST request to your target URL.

**Headers:**

| Header                          | Purpose                              |
|--------------------------------|--------------------------------------|
| `X-Twenty-Webhook-Signature`   | HMAC SHA256 signature for verification |
| `X-Twenty-Webhook-Timestamp`   | Unix timestamp of the event          |
| `X-Twenty-Webhook-Nonce`       | Unique nonce to prevent replay attacks |

**Body:** JSON containing the record data and event type.

```json
{
  "event": "person.created",
  "data": {
    "id": "person-uuid-5678",
    "name": { "firstName": "Jane", "lastName": "Doe" },
    "email": "jane@example.com",
    "createdAt": "2026-04-02T16:00:00Z"
  }
}
```

**Requirements:**
- Your endpoint must return a 2xx status code within the timeout period.
- Non-2xx responses or timeouts may trigger retries or webhook deactivation.

**Signature verification (pseudocode):**
```
expected = HMAC_SHA256(webhook_secret, timestamp + "." + nonce + "." + raw_body)
if (signature !== expected) reject request
```

---

## 5. Create a Workflow (Full API Pattern)

**⚠️ VERIFIED LIVE (2026-04-03, updated 2026-04-04):** This entire section was validated by building a 7-step workflow with ITERATOR, CODE, IF_ELSE, AI_AGENT, and UPDATE_RECORD steps via API. Full end-to-end execution confirmed.

### ⚠️ CRITICAL: Build Order (determines success or failure)

**`updateWorkflowVersionStep` WIPES `nextStepIds` on the updated step.** This means if you create steps (which sets edges via `parentStepId`), then configure them (which wipes those edges), then add edges — the edges added before configuration are lost.

**Correct order:**
```
Phase 1: CREATE all steps (with parentStepId — sets initial edges)
Phase 2: CONFIGURE all steps (updateWorkflowVersionStep — wipes edges, that's OK)
Phase 3: ADD all edges LAST (createWorkflowVersionEdge — these persist)
Phase 4: Set trigger nextStepIds (REST PATCH — always last)
```

**Wrong order (causes broken edges):**
```
Create step → Configure step → Add edge → Create next step → Configure → Add edge
(Each configure call wipes the edges you just added)
```

This is the single most important pattern for API workflow creation. See `Templates/build-contact-aging-workflow.py` for the working reference implementation.

### 5a. Critical: API Key vs User Token Scope

**The API key (`TWENTY_API_KEY`) CANNOT create or modify workflow steps.** It only works for:
- REST endpoints (`/rest/*`)
- Metadata endpoint (`/metadata`) — field creation, object creation, schema queries

**Workflow step mutations require a user ACCESS token** obtained via the two-step auth flow on `/metadata` (see `Bootstrap.md` Steps 3-4). This token works on the `/graphql` workspace endpoint where workflow mutations live.

```
API Key scope:     /rest/* ✓   /metadata ✓   /graphql mutations ✗
User token scope:  /rest/* ✓   /metadata ✓   /graphql mutations ✓
```

### 5b. Create the workflow shell (API key works)

```http
POST {BASE}/rest/workflows
Authorization: Bearer {TOKEN}
Content-Type: application/json

{ "name": "Contact Aging Analysis" }
```

Response includes `id` (workflow ID). A draft version is auto-created.

**Do NOT pass `statuses` in the body** — Twenty returns "Statuses cannot be set manually."

### 5c. Set the trigger (API key works)

Find the auto-created version ID:
```http
GET {BASE}/rest/workflowVersions?limit=10
Authorization: Bearer {TOKEN}
```

Set the trigger:
```http
PATCH {BASE}/rest/workflowVersions/{VERSION_ID}
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "trigger": {
    "type": "CRON",
    "settings": { "type": "CUSTOM", "pattern": "0 8 * * 1" }
  }
}
```

**Trigger types:**

| Type | Settings | When |
|------|----------|------|
| `CRON` | `{"type": "CUSTOM", "pattern": "0 8 * * 1"}` | On schedule (cron syntax) |
| `DATABASE_EVENT` | `{"eventName": "person.upserted", "fields": ["emails"]}` | Record CRUD |
| `MANUAL` | `{}` | User-triggered or API-triggered |

### 5d. Create steps (REQUIRES user token on /graphql)

**⚠️ This is the key insight: step mutations only work on `/graphql` with a user ACCESS token, not an API key.**

```graphql
mutation CreateStep($input: CreateWorkflowVersionStepInput!) {
  createWorkflowVersionStep(input: $input) { stepsDiff }
}
```

Variables:
```json
{
  "input": {
    "workflowVersionId": "{VERSION_ID}",
    "stepType": "FIND_RECORDS",
    "parentStepId": "{PREVIOUS_STEP_ID}",
    "parentStepConnectionOptions": { "type": "loop" }
  }
}
```

- `parentStepId` — connects the new step after this step. Omit for the first step.
- `parentStepConnectionOptions` — use `{"type": "loop"}` for Iterator loop body, `{"type": "true"}` for IF_ELSE true branch, `{"type": "false"}` for IF_ELSE false branch.

**Available step types:**

| stepType | Purpose | Icon in UI |
|----------|---------|-----------|
| `FIND_RECORDS` | Query records (Search Records) | 🔍 |
| `ITERATOR` | Loop over a list | 🔄 |
| `CODE` | Run a Logic Function | ⟨/⟩ |
| `IF_ELSE` | Conditional branching | ⟨ |
| `AI_AGENT` | Invoke an AI agent | 🤖 |
| `UPDATE_RECORD` | Update a record | ↻ |
| `CREATE_RECORD` | Create a record | + |
| `DELETE_RECORD` | Delete a record | 🗑 |
| `SEND_EMAIL` | Send email | ✉ |
| `HTTP_REQUEST` | External HTTP call | 🌐 |
| `FILTER` | Filter records | ▽ |
| `FORM` | Human input form | 📋 |
| `DELAY` | Wait before proceeding | ⏱ |

### 5e. stepsDiff response format

The `createWorkflowVersionStep` mutation returns `stepsDiff` — an array of change objects:

```json
[
  {
    "type": "CREATE",
    "path": ["steps", 3],
    "value": {
      "id": "new-step-uuid",
      "name": "Search Records",
      "type": "FIND_RECORDS",
      "valid": false,
      "settings": { ... }
    }
  }
]
```

Extract the new step ID: find the entry where `type == "CREATE"` and `value.type` matches your requested `stepType`.

### 5f. Configure steps

```graphql
mutation UpdateStep($input: UpdateWorkflowVersionStepInput!) {
  updateWorkflowVersionStep(input: $input) { id name type }
}
```

Variables:
```json
{
  "input": {
    "workflowVersionId": "{VERSION_ID}",
    "step": {
      "id": "{STEP_ID}",
      "name": "Find All People",
      "type": "FIND_RECORDS",
      "valid": true,
      "settings": {
        "input": { "objectName": "person", "limit": 200 },
        "outputSchema": {},
        "errorHandlingOptions": {
          "retryOnFailure": { "value": false },
          "continueOnFailure": { "value": false }
        }
      }
    }
  }
}
```

**Step-specific settings patterns:**

ITERATOR — reference prior step output:
```json
"settings": {
  "input": {
    "items": "{{FIND_STEP_ID}}",
    "initialLoopStepIds": [],
    "shouldContinueOnIterationFailure": true
  }
}
```

IF_ELSE — filter on step output:

**⚠️ CRITICAL:** Filter `type` must match the output type. TEXT supports `CONTAINS`/`DOES_NOT_CONTAIN`/`IS_EMPTY`/`IS_NOT_EMPTY`. SELECT supports `IS`/`IS_NOT`. BOOLEAN supports `IS`. Using wrong operand for type causes "Operand not supported" error.

```json
"settings": {
  "input": {
    "branches": [...],
    "stepFilterGroups": [{"id": "fg-1", "logicalOperator": "AND"}],
    "stepFilters": [
      {"id": "f1", "type": "boolean", "stepOutputKey": "{{CODE_STEP_ID.shouldAnalyze}}", "operand": "IS", "value": "true", "stepFilterGroupId": "fg-1", "positionInStepFilterGroup": 0}
    ]
  }
}
```

Filter operands by type:
| Type | Operands |
|------|----------|
| `boolean` | `IS` |
| `TEXT` | `CONTAINS`, `DOES_NOT_CONTAIN`, `IS_EMPTY`, `IS_NOT_EMPTY` |
| `SELECT` | `IS`, `IS_NOT`, `IS_EMPTY`, `IS_NOT_EMPTY` |
| `NUMBER` / `DATE` | `IS`, `IS_BEFORE`, `IS_AFTER`, etc. |

AI_AGENT — invoke an agent:

**⚠️ CRITICAL: The field is `prompt`, NOT `agentInput`.** The engine reads `const { agentId, prompt } = step.settings.input`. Using `agentInput` causes the prompt to appear empty in the UI and the agent receives no instructions.

```json
"settings": {
  "input": {
    "agentId": "{AGENT_UUID}",
    "prompt": "Analyze this contact:\nName: {{ITERATOR_ID.currentItem.name.firstName}}\n..."
  }
}
```

UPDATE_RECORD — write fields:

**⚠️ CRITICAL: Inside an Iterator, use `{{ITERATOR_ID.currentItem.id}}` not `{{ITERATOR_ID.id}}`.** The Iterator exposes `currentItem` as the accessor for the current loop item.

```json
"settings": {
  "input": {
    "objectName": "person",
    "objectRecordId": "{{ITERATOR_ID.currentItem.id}}",
    "objectRecord": {
      "contactPriority": "{{CODE_STEP_ID.contactPriority}}",
      "lastContactDays": "{{CODE_STEP_ID.lastContactDays}}"
    }
  }
}
```

### 5g. Delete steps (cleanup)

```graphql
mutation {
  deleteWorkflowVersionStep(input: {
    workflowVersionId: "{VERSION_ID}",
    stepId: "{STEP_ID}"
  }) { stepsDiff }
}
```

**⚠️ IMPORTANT:** Creating steps often auto-generates EMPTY placeholder steps on branches (Iterator loop, IF_ELSE true/false). After building the real steps, delete any remaining EMPTY placeholders.

### 5h. Activate and run

**⚠️ Both mutations return `Boolean!`, NOT objects. Do NOT request subfields.**

```graphql
mutation { activateWorkflowVersion(workflowVersionId: "{VERSION_ID}") }
```

```graphql
mutation { runWorkflowVersion(input: { workflowVersionId: "{VERSION_ID}" }) { __typename } }
```

To deactivate (required before editing an active version):
```graphql
mutation { deactivateWorkflowVersion(workflowVersionId: "{VERSION_ID}") }
```

To create a new draft from a deactivated version:
```graphql
mutation { createDraftFromWorkflowVersion(input: { workflowId: "{WF_ID}", workflowVersionIdToCopy: "{VERSION_ID}" }) { id } }
```

**⚠️ WARNING:** `createDraftFromWorkflowVersion` copies steps but assigns NEW step IDs. All variable references (`{{stepId.field}}`) in copied steps still point to the OLD step IDs from the source version. These references may still work if the engine resolves them correctly, but this is fragile. Prefer creating fresh versions over copying when possible.

### 5i. Variable reference syntax

Steps reference outputs from prior steps using `{{STEP_UUID.fieldName}}`:
- `{{find-step-id}}` — entire output array (for ITERATOR items)
- `{{step-id.fieldName}}` — specific field from step output
- `{{iterator-id.name.firstName}}` — nested field access

---

## 6. Logic Functions

Sandboxed TypeScript functions that run server-side. When a CODE step is created in a workflow, Twenty auto-creates a Logic Function and links it via `logicFunctionId` in the step settings.

**Update a logic function's code via metadata API:**

```graphql
mutation UpdateLF($input: UpdateOneLogicFunctionInput!) {
  updateOneLogicFunction(input: $input) { id name }
}
```

**⚠️ Note:** The exact mutation name may vary by Twenty version. Check with introspection on `/metadata` if the mutation fails.

**Example cron expressions:**

| Expression      | Schedule                    |
|----------------|-----------------------------|
| `0 9 * * 1`    | Monday at 9:00 AM           |
| `0 */6 * * *`  | Every 6 hours               |
| `0 0 1 * *`    | First day of each month     |
| `*/15 * * * *` | Every 15 minutes            |

---

## 7. Workflow vs Logic Function Decision

| Criterion            | Workflow                            | Logic Function                        |
|---------------------|-------------------------------------|---------------------------------------|
| Complexity           | Multi-step with branching + AI      | Custom TypeScript logic               |
| Interface            | Visual in Workflows tab             | Code-first                            |
| Step types           | 13+ built-in action types           | Arbitrary code                        |
| AI Agent support     | AI_AGENT step type (built-in)       | Manual API calls                      |
| Creation method      | API (see §5) or UI                  | Auto-created by CODE steps or CLI     |

**Rule of thumb:** Use workflows for anything that involves records + branching + AI agents. Use standalone logic functions only for custom HTTP endpoints or heavy computation that doesn't fit the step model.

---

## 8. Gotchas

## ⚠️ Bug Investigation Protocol (MANDATORY)

**No public API documentation exists for Twenty's workflow engine.** When any workflow step fails or produces unexpected results, **STOP inline debugging after 15 minutes** and switch to formal investigation:

1. **Document the symptom:** exact error message, step name, expected vs actual behavior.
2. **Write 2-3 targeted test hypotheses** as direct API calls (curl to REST or GraphQL).
3. **Run tests in parallel** using background agents — one per hypothesis.
4. **Document findings** in `References/BugFindings-{date}.md` before attempting any fix.
5. **Search Twenty GitHub issues** (`api.github.com/search/issues?q=KEYWORD+repo:twentyhq/twenty`) for known bugs.

This protocol exists because every bug in this workflow (DATE_TIME persistence, AI provider race condition, Iterator timeout, filter operand casing, missing edges) was solved in minutes by targeted API tests after hours of fruitless inline debugging. Research first, fix second.

**For detailed logging/instrumentation guidance:** See `References/WorkflowDebugging.md` — covers worker instrumentation, graph verification, known Twenty quirks table, and the investigation checklist for every build script.

---

- **Webhook operations use dot notation.** Format is `objectName.event` — for example, `person.created`, `company.updated`, `*.deleted`.
- **Verify webhook signatures in production.** The `X-Twenty-Webhook-Signature` header uses HMAC SHA256.
- **API key CANNOT create workflow steps.** Step mutations (`createWorkflowVersionStep`, `updateWorkflowVersionStep`, etc.) require a user ACCESS token on `/graphql`. The API key returns "Forbidden resource" for these. Use the two-step auth flow in Bootstrap.md.
- **User ACCESS tokens expire in ~30 minutes.** For multi-step workflow builds, get a **fresh token before EVERY GraphQL call**. The `getLoginTokenFromCredentials` → `getAuthTokensFromLoginToken` flow takes ~200ms total — just re-auth every time.
- **Creating steps auto-generates EMPTY placeholders.** Iterator creates an EMPTY in its loop body, IF_ELSE creates EMPTYs on both branches. Delete these after adding real steps.
- **2FA blocks token exchange.** If `getAuthTokensFromLoginToken` returns "Two factor authentication verification required", remove the 2FA record from `core.twoFactorAuthenticationMethod` in the database and retry.
- **Cron triggers use standard 5-field cron syntax.** Minute, hour, day-of-month, month, day-of-week.
- **Do NOT pass `statuses` when creating a workflow.** The API rejects it — status is managed by Twenty internally via activate/deactivate mutations.
- **`updateWorkflowVersionStep` WIPES `nextStepIds`.** If you update a step's settings, the step's `nextStepIds` may be cleared. Do NOT include `nextStepIds` in the step object — use `createWorkflowVersionEdge` to manage connections separately.
- **`createWorkflowVersionStep` with `parentStepId` does NOT always set `nextStepIds` on the parent.** Always use `createWorkflowVersionEdge` explicitly after creating a step to ensure the connection exists.
- **✅ RESOLVED (2026-04-04): `createWorkflowVersionEdge` DOES work — but only if called AFTER `updateWorkflowVersionStep`.** The original issue was that edges were created, then `updateWorkflowVersionStep` was called to configure settings, which wiped `nextStepIds`. Solution: create all steps → configure all steps → add all edges LAST. See the Critical Build Order section above.
- **Iterator `initialLoopStepIds` must NOT point to itself.** It must point to the first step INSIDE the loop body (e.g., the CODE step). Self-reference causes `RangeError: Maximum call stack size exceeded` in `getAllStepIdsInLoop`.
- **Iterator `items` must use `.all` suffix.** FIND_RECORDS returns `{result: {first, all, totalCount}}`. The Iterator needs `{{findStepId.all}}` not `{{findStepId}}`. Without `.all`, the Iterator gets an object instead of an array and fails with "Iterator input items must be an array".
- **Inside an Iterator, reference current item via `currentItem`.** Use `{{iteratorId.currentItem.fieldName}}` not `{{iteratorId.fieldName}}`.
- **AI_AGENT field is `prompt`, NOT `agentInput`.** The engine reads `const { agentId, prompt } = step.settings.input`. Using `agentInput` causes the UI to show empty "Instructions for AI" and the agent receives no instructions.
- **IF_ELSE filter operand must match the type.** Boolean uses `IS`, TEXT uses `CONTAINS`, SELECT uses `IS`. Using `IS` on TEXT causes "Operand IS not supported for this filter type". Best practice: output a boolean `shouldAnalyze` from the CODE step and filter on that.
- **First step in empty version uses `CHANGE` diff format.** `createWorkflowVersionStep` on an empty version returns `stepsDiff` with `type: "CHANGE"` and `value` as an array, not `type: "CREATE"` with `value` as an object. Parse both formats.
- **`activateWorkflowVersion`, `deactivateWorkflowVersion`, `updateOneLogicFunction` return `Boolean!`.** Do NOT request subfields — they have none.
- **Workflow must be DRAFT to edit.** Active workflows must be deactivated first, then a new draft created with `createDraftFromWorkflowVersion`.
- **✅ RESOLVED: Iterator requires back-edges from every terminal loop step back to the Iterator step.** Without these edges, the executor completes one iteration's loop body, finds no `nextStepIds` on the terminal step, and never re-invokes the Iterator — the workflow hangs in RUNNING forever. Fix: in Phase 3 (edges), add edges from every leaf step inside the loop back to the Iterator ID: `createWorkflowVersionEdge(source: lastLoopStepId, target: iteratorStepId)`. The `getAllStepIdsInLoop` utility specifically looks for `step.nextStepIds.includes(iteratorStepId)` to identify the loop boundary.
- **✅ RESOLVED: Iterator stalls at ~89 iterations due to state blob growth → DB query timeout.** Root cause: `resetStepsInLoop` accumulates full result objects in `history` arrays on every inner step, every iteration. By ~89 iterations the `workflowRun.state` JSON is so large that `getWorkflowRunOrFail` exceeds the PostgreSQL read timeout. **Fix:** Patch the worker's `iterator.workflow-action.js` — change both `history: [...]` accumulation sites to `history: []`. History is write-only (nothing reads it) so this is safe. With the patch, 200+ items complete in a single run (~21 minutes). **Patch command:**
  ```bash
  # On the worker container, replace history accumulation with empty arrays
  # in /app/packages/twenty-server/dist/modules/workflow/workflow-executor/workflow-actions/iterator/iterator.workflow-action.js
  # Both buildSubStepInfosReset and buildIteratorStepInfoReset: change history: [...spread, {result, error, status}] to history: []
  docker restart twenty-local-worker-1
  ```
  **Note:** This patch is lost on container recreate. Add to a startup script or volume-mount the patched file. The `MAX_EXECUTED_STEPS_COUNT = 20` job-split still fires every ~3 iterations but works correctly with the history patch in place.
- **FIND_RECORDS filter requires `fieldMetadataId` (UUID), not field name.** Query the `/metadata` API: `fields(filter: { objectMetadataId: { eq: "..." } })` to get field UUIDs. System fields like `id` require `isSystem: true` and may need larger paging to find.
- **FIND_RECORDS filter operands must be ALL CAPS.** `IS`, `IS_NOT`, `IS_EMPTY`, `IS_NOT_EMPTY`, `CONTAINS`, `IS_BEFORE`, `IS_AFTER`, etc. Lowercase (e.g., `is`) causes "Unknown operand" errors.
- **FIND_RECORDS for RELATION fields uses the relation field's metadata ID.** E.g., to filter `messageParticipant` by `person`, use the `person` RELATION field's UUID (`d19518ca-...`), not `personId`.
- **FIND_RECORDS returns flat records — no relation expansion.** To get related data (e.g., `message.receivedAt` from a `messageParticipant`), you need a second FIND_RECORDS step that queries the related object by ID.
- **CODE step `logicFunctionInput` must use `{{iteratorId.currentItem}}` (not `{{iteratorId}}`).** Without `.currentItem`, the CODE step receives the Iterator's wrapper object (`{currentItem, currentItemIndex, hasProcessedAllItems}`) instead of the actual record.
- **✅ RESOLVED: CODE step outputSchema type must match destination field type for DATE_TIME.** If CODE outputs a date as `"type": "TEXT"` in outputSchema but the target field is `DATE_TIME`, UPDATE_RECORD silently drops the value (no error). Fix: set `"type": "DATE_TIME"` in outputSchema. TEXT-to-SELECT coercion works, but TEXT-to-DATE_TIME does not.
- **Email contact dates come from `message.receivedAt`, not `messageParticipant.createdAt`.** The `createdAt` on `messageParticipant` is when Twenty imported the record (all same day). The `receivedAt` on `message` is the actual email date. Requires two FIND_RECORDS: (1) find messageParticipant by personId → get messageId, (2) find message by id → get receivedAt.
- **No public workflow API documentation exists.** Twenty documents REST/GraphQL for CRUD but NOT workflow step creation, configuration, Iterator behavior, or filter syntax. All patterns in this file were reverse-engineered from compiled server source code.
- **FIND_RECORDS with 0 results sets `first: null`.** If a subsequent step references `{{prevStep.first.fieldName}}`, and the previous step returned no records, the variable resolves to empty. GitHub fix #18814 (v1.20.0+) catches this as `FAILED_SAFELY` instead of silently querying all records. This cascades to ALL downstream steps. **Guard against this** with an IF_ELSE checking `totalCount > 0` before referencing `.first` properties.
- **RELATION IS filter accepts plain UUID strings.** The workflow engine's `arrayOfUuidOrVariableSchema` catches plain UUIDs and wraps them in an array. The `IS` operand on a RELATION field generates `{ fieldNameId: { in: [uuid] } }`. Use the RELATION field's metadata ID (e.g., `person` not `personId`), and the engine auto-appends `Id` for the GQL filter.
