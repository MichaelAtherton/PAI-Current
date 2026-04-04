# Bug Research Findings — 2026-04-04

Three bugs investigated in the Contact Aging Analysis workflow. All root causes identified via empirical API testing (no documentation exists for Twenty's workflow internals).

---

## Bug 1: lastContactDate (DATE_TIME) Not Persisting

### Symptom
CODE step outputs `lastContactDate` as an ISO string. UPDATE_RECORD writes it to person record. Field stays null on all 200 people. Meanwhile, `lastContactDays` (NUMBER) and `contactPriority` (SELECT) persist correctly from the same CODE step.

### Tests Performed
| Test | Result |
|------|--------|
| REST PATCH with ISO string to lastContactDate | **Works** — value persists |
| REST read-back after PATCH | **Confirmed** — `2025-09-25T16:50:34.000Z` returned |
| REST PATCH with null | **Works** — clears field |
| REST PATCH with epoch `1970-01-01` | **Works** — stores as real value, not null |
| CODE outputSchema type check | **`TEXT`** — mismatch with field type `DATE_TIME` |

### Root Cause
**CODE step `outputSchema` declares `lastContactDate` as `type: "TEXT"` but the person field is `DATE_TIME`.** Twenty's workflow engine uses the outputSchema type to determine how to pass variables to UPDATE_RECORD. TEXT-to-DATE_TIME coercion silently fails (no error, value dropped). TEXT-to-SELECT coercion works (contactPriority persists). NUMBER-to-NUMBER works (lastContactDays persists).

### Fix
Change `build-contact-aging-workflow.py` outputSchema:
```python
# Before (broken):
"lastContactDate": {"type": "TEXT", "label": "lastContactDate", "value": "", "isLeaf": True}

# After (fixed):
"lastContactDate": {"type": "DATE_TIME", "label": "lastContactDate", "value": "2025-01-01T00:00:00.000Z", "isLeaf": True}
```

### Key Learning
**CODE step outputSchema types must match destination field types for DATE_TIME.** TEXT works for SELECT coercion but NOT for DATE_TIME. Always match outputSchema type to the target field's metadata type.

---

## Bug 2: AI_AGENT "No AI Models Available"

### Symptom
AI_AGENT workflow step returns: "No AI models are available. Configure at least one AI provider." OpenAI API key was configured via admin panel and confirmed in database.

### Tests Performed
| Test | Result |
|------|--------|
| `IS_AI_ENABLED` feature flag | **true** — AI is enabled |
| Database AI tables | **No dedicated tables** — config in `core.keyValuePair` |
| `OPENAI_API_KEY` in keyValuePair | **Present** — encrypted, CONFIG_VARIABLE type |
| `ANTHROPIC_API_KEY` in keyValuePair | **Present** — encrypted, CONFIG_VARIABLE type |
| Server env vars for OPENAI | **Zero** — no AI env vars in container |
| Worker env vars for OPENAI | **Zero** — no AI env vars in container |
| Agents in database | **17 agents** — all use `modelId: 'default-smart-model'` |

### Root Cause
**Startup race condition in `AiModelRegistryService`.** The call chain:

1. `AiModelRegistryService` constructor calls `buildModelRegistry()` during dependency injection
2. `buildModelRegistry()` resolves `{{OPENAI_API_KEY}}` template via `TwentyConfigService.get()`
3. `TwentyConfigService` checks `DatabaseConfigDriver` cache — **empty** (its `onModuleInit` hasn't run yet)
4. Falls back to environment variables — **no OPENAI_API_KEY env var** → returns `undefined`
5. `isProviderConfigured()` checks `!!(config.apiKey)` → false → provider not registered
6. Model registry built with **zero providers**
7. Later, `DatabaseConfigDriver.onModuleInit()` loads encrypted keys from DB → but registry is **never rebuilt**
8. `refreshRegistry()` exists but is only called from admin panel UI, never after DB init

### Fix
**Immediate workaround:** Add `OPENAI_API_KEY` as an environment variable to both server and worker containers in `docker-compose.yml`:

```yaml
services:
  server:
    environment:
      OPENAI_API_KEY: "sk-..."
  worker:
    environment:
      OPENAI_API_KEY: "sk-..."
```

This makes the key available at constructor time before DB loads.

**Upstream fix:** Twenty should call `refreshRegistry()` after `DatabaseConfigDriver.onModuleInit()` completes. This is a known architectural issue — the source code comments even acknowledge the race: "The database driver will load config variables asynchronously via its onModuleInit lifecycle hook. In the meantime, we'll use the environment driver."

### Key Learning
**Twenty v1.20.0 has a startup race condition for AI provider config.** Keys stored via admin panel (in DB) are not available during service initialization. The env var workaround is the reliable path. This may be fixed in future versions (see GitHub #18853, #18818 — AI catalog refactoring).

---

## Bug 3: IS_EMPTY Filter Not Working for Batch Progression

### Symptom
FIND_RECORDS with `IS_EMPTY` on `lastContactDate` keeps returning all 200+ people despite running multiple batches. Expected: each batch processes 50, next batch finds remaining unprocessed.

### Tests Performed
| Test | Result |
|------|--------|
| Actual lastContactDate values | **199 null, 1 non-null** (only manual test write) |
| REST filter `lastContactDate[is]:NULL` | **Works** — correct syntax uses `:` not `=` |
| REST filter `lastContactDate[is]:NOT_NULL` | **Works** — returns only non-null records |
| Epoch `1970-01-01` treated as null? | **No** — epoch is a real value, NOT null |
| IS_EMPTY on DATE_TIME source code | Translates to `{ is: 'NULL' }` SQL check |

### Root Cause
**Not a filter bug — cascading failure from Bug 1.** The `IS_EMPTY` filter works correctly. The issue is that `lastContactDate` was never being written by the workflow (Bug 1 — outputSchema type mismatch). Since all records stay NULL, every batch finds all 200 people again, and the first 50 (by default sort) get reprocessed.

### Fix
Fix Bug 1 (outputSchema type mismatch). Once `lastContactDate` is actually written:
- Processed people → `lastContactDate = "2025-07-28T05:27:03.000Z"` → IS_EMPTY = false → excluded from next batch
- Unprocessed people → `lastContactDate = null` → IS_EMPTY = true → included in next batch

**Important:** Do NOT use epoch `1970-01-01T00:00:00.000Z` as a sentinel for "no email found." Epoch is stored as a real value, not null. For people with no email history, either:
- Leave `lastContactDate` as null (they'll get reprocessed each batch, which is fine for weekly CRON)
- Or use a different field for batch tracking (e.g., a separate `lastProcessedAt` DATE_TIME field)

### Key Learnings
- REST filter syntax uses `:` separator, not `=` (e.g., `filter=field[is]:NULL`)
- `IS_EMPTY` on DATE_TIME = SQL NULL check — works correctly
- Epoch `1970-01-01` is NOT null — it's a real stored value
- Twenty REST filter is separate from workflow FIND_RECORDS filter (different code paths, but same SQL semantics for IS_EMPTY)

---

## Related GitHub Issues (twentyhq/twenty)

| Issue | Title | Status | Relevance |
|-------|-------|--------|-----------|
| #15282 | IS_EMPTY operator not supported in workflow filters | CLOSED | Fixed — IS_EMPTY now works |
| #17483 | Patch formatResult to pass Date object through | CLOSED | DATE_TIME formatting fix |
| #18814 | Prevent FIND_RECORDS from silently dropping unresolved filter variables | CLOSED | May affect our filter |
| #18818 | Replace hardcoded AI model constants with JSON seed catalog | CLOSED | AI provider refactor |
| #18853 | Run AI catalog sync as standalone script to avoid DB dependency | CLOSED | Addresses our race condition |
| #18325 | Workflow iterator continues on failure | CLOSED | Iterator behavior fix |
| (none) | MAX_EXECUTED_STEPS_COUNT limit | N/A | No known issues — undocumented |

**Server version:** v1.20.0. Issues #18818 and #18853 may have been merged after this version.

---

## Summary of Fixes Required

| Bug | Root Cause | Fix | Effort |
|-----|-----------|-----|--------|
| 1. lastContactDate | outputSchema `TEXT` → field `DATE_TIME` mismatch | Change to `"type": "DATE_TIME"` in build script | 1 line |
| 2. AI provider | Startup race — DB keys not loaded during DI | Add `OPENAI_API_KEY` env var to docker-compose | 2 lines |
| 3. IS_EMPTY filter | Cascading from Bug 1 (field never written) | Fix Bug 1 + remove epoch sentinel | 1 line |
| 4. Iterator ~89 stall | History accumulation in state JSON → DB read timeout | Patch `history: []` in iterator.workflow-action.js on worker | 2 lines |
| 5. FIND_MSG filter "empty value" | People without emails → Find Messages returns 0 → first=null → cascading FAILED_SAFELY | Add null guard or restructure step dependencies | Architecture change |
| 6. Iterator silent failure | cfg() wipes nextStepIds; 3 edges missing in Phase 3 | Add FIND_MSG→IF_EMAIL, CODE→IF_PRIO, CODE_NOEMAIL→UPD_NOEMAIL | 3 lines |
| 7. AI response not parsed | AI_AGENT returns `{response: "JSON string"}`, not flat fields | Insert CODE_PARSE_AI step between AI_AGENT and UPD_AI | New step |
| 8. Reset oversight | FIND filter uses lastContactDate (not contactPriority); GQL reset only cleared contactPriority | Reset lastContactDate via SQL; verify FIND filter field before resets | Operator error |

---

## Bug 5: FIND_MSG Filter "Empty Value After Variable Resolution"

### Symptom
FIND_RECORDS step "Get Message Detail" fails with: "Filter condition has an empty value after variable resolution. Filter field: ae62024e, operand: IS." All downstream steps cascade to FAILED_SAFELY — person records never get updated.

### Root Cause
**NOT a filter bug. Null propagation through step chain.** The causal chain:
1. `Find Messages` queries messageParticipants for person → returns `totalCount: 0, first: null` (person has no email history)
2. `Get Message Detail` references `{{findMsgId.first.messageId}}` → `first` is null → `.messageId` is empty
3. GitHub fix #18814 (active on v1.20.0) catches empty filter values and throws `FAILED_SAFELY`
4. ALL downstream steps (CODE, IF_ELSE, AI_AGENT, UPDATE_RECORD) cascade to FAILED_SAFELY
5. Person gets zero updates — not even contactPriority or lastContactDays

### What works
- Iterator step ID references are correct (verified — IDs match)
- RELATION filter format is correct (plain UUID with IS operand works)
- Variable resolution supports nested dot paths (`{{stepId.currentItem.id}}` resolves correctly)
- Find Messages successfully queries when person has email records

### Fix
Restructure the loop so CODE step doesn't depend on Get Message Detail succeeding. Options:
1. **Add IF_ELSE guard** after Find Messages checking `totalCount > 0` → true: Get Message Detail → CODE with email; false: CODE without email
2. **Make CODE step receive person data directly from Iterator** (not through FIND_DET), and email data optionally from FIND_DET
3. **Remove Get Message Detail** and use Find Messages' `first.createdAt` as approximate date (less accurate but no null chain)

---

## Bug 4: Iterator Stalls at ~89 Iterations (Query Timeout)

### Symptom
Workflow processes ~85-89 contacts then stops. Status stays RUNNING. No errors in API. Previously misdiagnosed as stack depth, job splitting, or Node.js memory limit.

### Tests Performed
| Test | Result |
|------|--------|
| Run 1 (LIMIT=None) | Stalled at idx=87 |
| Run 2 (instrumented) | Failed at idx=89 with `Query read timeout` |
| Run 3 (history patch) | **COMPLETED idx=200** in 21 minutes |

### Root Cause
`resetStepsInLoop` in `iterator.workflow-action.js` accumulates full result objects in `history` arrays every iteration. With 7 inner steps × 89 iterations = 623 history entries with full person/message/priority data. The `workflowRun.state` JSON blob grows so large that `SELECT * FROM workflowRun WHERE id = $1` exceeds PostgreSQL's read timeout (~30s).

### Fix
Patch `iterator.workflow-action.js` on the worker container — both `buildSubStepInfosReset` and `buildIteratorStepInfoReset`:
```javascript
// Change from:
history: [...stepInfos[stepId]?.history ?? [], { result, error, status }]
// To:
history: []
```
History is write-only (nothing reads it). Verified: `grep -r "\.history" workflow/` returns only the two write sites in the Iterator itself.

**Patch lost on container recreate.** Must be reapplied or volume-mounted.
