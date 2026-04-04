# Twenty Workflow Failure Modes Catalog

Concrete failure modes we've hit and how to recognize them. Use this as a
diagnostic lookup table when a workflow misbehaves.

---

## FM-1: Iterator processes 1 item then workflow silently COMPLETES

**Visible symptom:** Workflow run status = COMPLETED. Iterator step shows
`currentItemIndex: 0, hasProcessedAllItems: true`. All inner steps are
NOT_STARTED.

**Root cause classes:**
- **6a — Missing forward edges.** `cfg()` wipes nextStepIds. If Phase 3 doesn't
  re-add every forward edge, `getAllStepIdsInLoop` traversal stops early,
  back-edge parents are treated as non-loop parents, `shouldExecuteChildStep`
  requires ALL to be terminal, they're NOT_STARTED → Iterator never re-enters.
- **6b — SKIPPED propagation dead-ends.** When an IF_ELSE branch is taken,
  the other branch's first step is SKIPPED but SKIPPED does not cascade
  through multi-step sub-chains. If a skipped-branch back-edge step stays
  NOT_STARTED, the Iterator's parent check fails.

**How to confirm:** Query the workflow run state, dump stepInfos, check which
steps have non-terminal status. Inspect each step's `nextStepIds` to verify
the graph is wired correctly.

**Prevention:** Call `verify_graph(vid)` between Phase 3 and Phase 4 in every
build script. It asserts non-IF_ELSE non-terminal steps have forward edges.

---

## FM-2: FIND_RECORDS returns empty or the wrong set

**Visible symptoms:**
- "Filter condition has an empty value after variable resolution"
- FIND returns 0 when you expect results
- FIND returns a stale set after running the workflow multiple times

**Root cause classes:**
- **2a — fieldMetadataId points at wrong field.** FIND filter uses
  fieldMetadataId not field name. A copy-paste from another filter leaves
  you filtering on a different field entirely.
- **2b — Reset didn't clear the filter field.** FIND uses `IS_EMPTY` on a
  specific field. If your reset cleared a different field, FIND's view of
  "unprocessed" doesn't update.
- **2c — Null propagation through step chain.** FIND returns 0, subsequent
  step references `{{prev.first.xyz}}`, resolves to empty, downstream cascade
  FAILS_SAFELY.

**How to confirm:** Query the metadata schema for the fieldMetadataId to see
which field it actually points to. Run the same filter shape against the
GraphQL API to verify it returns what FIND should return. Check DB directly
if still unclear.

**Prevention:** Before using a fieldMetadataId, verify it with
`{objects(filter:{nameSingular:{eq:"person"}}){edges{node{fields{edges{node{id name type}}}}}}}`.
Never hardcode field IDs without a comment naming the field.

---

## FM-3: AI_AGENT "No AI models available"

**Visible symptom:** AI_AGENT step errors with "No AI models are available.
Configure at least one AI provider."

**Root cause:** Twenty's `AiModelRegistryService` is built at DI time. If the
OPENAI_API_KEY is only in `core.keyValuePair` (via admin UI) and not as an
env var, the DI phase happens before the DB driver loads and the registry is
built with zero providers. `refreshRegistry()` exists but never runs after
DB init.

**Fix:** Set `OPENAI_API_KEY` as an env var on both `server` and `worker`
containers via docker-compose. Rebuild containers.

**Prevention:** Pre-flight checklist item: verify
`docker exec twenty-local-worker-1 env | grep OPENAI_API_KEY` returns a value
before building any workflow with AI_AGENT steps.

---

## FM-4: AI_AGENT returns data but UPD step doesn't write it

**Visible symptom:** AI_AGENT step succeeds with `result.response` containing
JSON text. UPDATE_RECORD step references `{{ai_id.relationshipStatus}}` and
it resolves to empty.

**Root cause:** AI_AGENT returns `{response: "...JSON string..."}`. The model
output is a single string field, not a structured object. References to
sub-fields of the string don't work.

**Fix:** Insert a CODE step between AI_AGENT and the UPD step. The CODE
step's logic function: `JSON.parse(params.aiResponse)` and return the parsed
fields as outputs. UPDATE step references the CODE step's outputs.

**Prevention:** Every time you use AI_AGENT to generate structured data,
include a parser CODE step. This is documented in CanonicalVsOurs.md §6.

---

## FM-5: Iterator stalls at ~89 iterations with "Query read timeout"

**Visible symptom:** Workflow processes 85-89 items then stops. Status stays
RUNNING. No API errors visible. Worker logs eventually show `Query read timeout`
or `Missing lock for job`.

**Root cause:** `resetStepsInLoop` in `iterator.workflow-action.js`
accumulates full result objects in `history[]` every iteration. With N inner
steps × M iterations, `workflowRun.state` JSON grows unbounded. At ~89
iterations the SELECT query exceeds PostgreSQL's read timeout.

**Fix:** Patch `iterator.workflow-action.js` on the worker container at both
history accumulation sites to write `history: []`. Restart worker.

**Prevention:** Verify the patch is applied before running any workflow with
LIMIT > 50:
```bash
docker exec twenty-local-worker-1 grep -c 'history: \[\]' \
  /app/packages/twenty-server/dist/modules/workflow/workflow-executor/workflow-actions/iterator/iterator.workflow-action.js
# Must return 2
```

**Patch is lost on container recreate.** Document as a post-restart checklist.

---

## FM-6: lastContactDate (DATE_TIME) silently doesn't persist

**Visible symptom:** CODE step outputs `lastContactDate` as an ISO string.
UPDATE step writes it. Field stays null on all person records. Meanwhile,
contactPriority and lastContactDays (TEXT/NUMBER) persist correctly from the
same CODE step.

**Root cause:** CODE step `outputSchema.lastContactDate.type` set to `"TEXT"`
but the target field is `DATE_TIME`. Twenty's workflow engine uses
outputSchema type for type coercion. TEXT→DATE_TIME silently fails (value
dropped, no error). TEXT→SELECT coercion DOES work (that's why contactPriority
persists).

**Fix:** Match outputSchema types to target field types.
```python
OUTPUT_SCHEMA = {
    "lastContactDate": {"type": "DATE_TIME", ...}  # NOT "TEXT"
}
```

**Prevention:** When writing a CODE step that updates a record field, look up
the target field's `type` in the metadata schema and match it in outputSchema.

---

## FM-7: Workflow build reports success but Iterator never fires

**Visible symptom:** Build script prints ✓ for all steps, configs, edges, and
EMPTY cleanup. Workflow activates. First run: FIND succeeds, Iterator gets
`[EXEC]` log but never writes stepInfo. Workflow completes immediately.

**Root cause:** `shouldExecuteIteratorStep` returned false. Usually because
`getAllStepIdsInLoop` returned an incomplete set (see FM-1 6a), making the
back-edge parents look like non-loop parents that must all be terminal.

**How to confirm:** Instrument `should-execute-iterator-step.util.js` on
the worker to log `stepsTargetingIterator`, `stepIdsInLoop.length`, and
`stepsToCheck` statuses. The `stepsToCheck` list will show NOT_STARTED steps
that should be inside the loop.

**Prevention:** Graph verification catches missing edges before runtime.
See FM-1 prevention.

---

## Template for New Entries

When you hit a new failure mode, add an entry here:

```markdown
## FM-N: Short descriptive title

**Visible symptom:** What the operator sees.

**Root cause:** Technical explanation.

**How to confirm:** Commands/queries that prove the diagnosis.

**Fix:** Concrete change to make.

**Prevention:** What to put in a build script or checklist to stop it
recurring.
```
