# Twenty Workflow Debugging & Logging Guide

Lessons learned from debugging the Contact Aging Analysis workflow (13-step, April 2026).

---

## Investigation Protocol

When a workflow misbehaves, follow this order — do NOT skip to fixing.

### 1. Capture the run state FIRST

```python
# Get the latest workflow run and dump ALL step statuses
q = f'{{workflowRuns(filter:{{workflowId:{{eq:"{wf_id}"}}}},first:1,orderBy:{{createdAt:DescNullsLast}}){{edges{{node{{id status state}}}}}}}}'
# Then iterate stepInfos and compare against steps
```

What to look for:
- Which steps are SUCCESS, FAILED, FAILED_SAFELY, SKIPPED, NOT_STARTED, RUNNING?
- Is the Iterator stuck? Check `result.currentItemIndex` and `result.hasProcessedAllItems`
- Are back-edge parent steps terminal? (NOT_STARTED = not terminal = Iterator won't re-enter)

### 2. Check worker logs

```bash
docker logs twenty-local-worker-1 2>&1 | grep -E '\[EXEC\]|\[SPLIT\]|\[ITER\]'
```

The `[EXEC]` logs show which steps were VISITED (not necessarily executed — `shouldExecuteStep` may return false after the log).

### 3. Verify the graph structure

```python
# Dump each step's nextStepIds — this is where missing edges hide
for s in steps:
    nxt = s.get("nextStepIds", [])
    # Check IF_ELSE branches, ITERATOR initialLoopStepIds
```

**The #1 bug was missing edges.** cfg() wipes ALL nextStepIds. If Phase 3 doesn't restore them, the graph is broken but the build script reports success.

### 4. Instrument the worker (when needed)

```bash
# Copy file out, patch, copy back, restart
docker exec twenty-local-worker-1 cat /path/to/file.js > /tmp/file.js
# Edit /tmp/file.js to add console.log statements
docker cp /tmp/file.js twenty-local-worker-1:/path/to/file.js
docker restart twenty-local-worker-1
```

Key files to instrument:
| File | What to log |
|------|------------|
| `iterator.workflow-action.js` | `resolveInput` result, `items` array length, `parsedItems` |
| `should-execute-step.util.js` | Which path taken (iterator vs regular), return value |
| `should-execute-iterator-step.util.js` | `stepsTargetingIterator`, `stepIdsInLoop` count, `stepsToCheck` with statuses |
| `get-all-step-ids-in-loop.util.js` | Each traversal step, `nextStepIds`, back-edge detection |
| `workflow-executor.workspace-service.js` | `shouldExecuteStep` return, `getNextStepIdsToExecute` result |

**Patches are lost on container restart.** Always document what you patched.

---

## Logging Checklist for Build Scripts

Every build script MUST include post-deploy verification:

### Graph verification (add to Phase 4)
```python
node = get_node(vid)
for s in node["steps"]:
    nxt = s.get("nextStepIds", [])
    # Verify every non-terminal step has at least one nextStepId
    # Verify IF_ELSE branches point to correct children
    # Verify Iterator initialLoopStepIds is set
    # Verify back-edges exist for every terminal loop step
```

### Run verification (add after activate+run)
```python
# Wait, then check:
# 1. Run status (COMPLETED vs RUNNING vs FAILED)
# 2. Iterator index vs total items
# 3. Step statuses — any NOT_STARTED that shouldn't be?
# 4. Sample person records — did fields actually update?
```

### Filter verification (before run)
```python
# ALWAYS verify the FIND filter works by testing via REST first:
# curl /rest/people?filter[field][is]=NULL&limit=1
# Compare count against GraphQL {people(filter:{field:{is:NULL}}){totalCount}}
# If they disagree, the workflow FIND_RECORDS filter will also disagree
```

---

## Known Twenty Quirks (Workflow API)

| Quirk | Impact | Workaround |
|-------|--------|------------|
| `cfg()` wipes `nextStepIds` | Edges from Phase 1 are lost | Add ALL edges in Phase 3 |
| AI_AGENT returns `{response: "JSON"}` | Can't reference sub-fields directly | Add CODE step to parse |
| Iterator history accumulates | DB timeout at ~89 iterations | Patch `history: []` on worker |
| OPENAI_API_KEY not in DI | "No AI models available" | Set env var on containers |
| IS_EMPTY on DATE_TIME vs TEXT | TEXT→DATE_TIME coercion fails silently | Match outputSchema types |
| IS_EMPTY on SELECT fields | **May not match GQL-null values** | OPEN BUG — needs investigation |
| `shouldExecuteChildStep` | Needs ALL parents SUCCESS/STOPPED/SKIPPED | NOT_STARTED blocks execution |
| SKIPPED doesn't cascade | Only direct IF_ELSE branch children get SKIPPED | FAILED_SAFELY cascades transitively |
| `continueOnFailure` on Iterator | Allows re-entry after FAILED_SAFELY | Set `shouldContinueOnIterationFailure: true` |

---

## Open Investigation: Bug 8 — IS_EMPTY on SELECT Field

**Status:** OPEN as of 2026-04-04

**Symptom:** 151 people have `contactPriority = NULL` via both GQL and REST, but FIND_RECORDS with `IS_EMPTY` on the contactPriority field (6babc91f) finds 0 of them.

**Confirmed so far:**
- GQL `{people(filter:{contactPriority:{is:NULL}})}` returns 151
- REST `/rest/people/{id}` shows `contactPriority: null` for these people
- FIND_RECORDS with IS_EMPTY on the same field finds 0
- The contactPriority field is type SELECT
- GraphQL `updatePerson(data:{contactPriority:null})` returns `contactPriority: None` (appears to work)
- But the workflow executor's FIND_RECORDS doesn't see these as empty

**Hypotheses to test:**
1. SELECT fields store an empty string `""` when "nulled", not SQL NULL — IS_EMPTY checks for NULL
2. The fieldMetadataId `6babc91f` points to the wrong field or a stale metadata entry
3. FIND_RECORDS uses a different SQL path than GraphQL for IS_EMPTY on SELECT
4. The GraphQL null mutation doesn't actually write to the database column

**Next steps:**
```sql
-- Check the actual database column value
docker exec twenty-local-db-1 psql -U postgres -d default \
  -c "SELECT \"contactPriority\" FROM core.\"person\" WHERE \"contactPriority\" IS NULL LIMIT 5;"
docker exec twenty-local-db-1 psql -U postgres -d default \
  -c "SELECT \"contactPriority\", COUNT(*) FROM core.\"person\" GROUP BY \"contactPriority\";"
```
