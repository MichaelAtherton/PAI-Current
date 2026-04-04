# Build Script vs Twenty Canonical Patterns

**Date:** 2026-04-04
**Sources:**
- `TWENTY-CODE-TRACES/skills/workflow-building.md` — Twenty's own guidance skill
- `TWENTY-CODE-TRACES/twenty-ai-skills-pipeline.md` — MCP pipeline architecture
- Live MCP endpoint at `POST localhost:3030/mcp` — authoritative schemas
- `.claude/skills/CRM/Templates/build-contact-aging-workflow.py` — our current script

---

## TL;DR

Our build script is **mostly canonical**. The operations we use (`createWorkflowVersionStep`, `createWorkflowVersionEdge`, `updateWorkflowVersionStep`, `updateLogicFunctionFromSource`) are the exact GraphQL mutations that Twenty's MCP tools (`create_workflow_version_step`, `create_workflow_version_edge`, `update_workflow_version_step`, `update_logic_function_source`) wrap.

**6 of our 8 bugs** were genuine Twenty behaviors we discovered empirically but that are documented/implicit in the canonical schemas. **2 of our 8** were operator errors, not Twenty issues.

The main divergence: we're hitting the raw GraphQL API via user token, while canonical Twenty AI hits the MCP endpoint via API key with the same tools wrapped. **Functionally equivalent** — the MCP layer calls the same underlying GraphQL mutations.

**Recommendation: Keep our script. Do not rewrite to MCP unless we need multi-workspace portability.**

---

## Point-by-Point Comparison

### 1. Build Order (Phases)

**Ours:** 4 phases — Create all steps → Configure all steps → Add all edges → Cleanup EMPTY
**Canonical:** Same approach implied by the tool set — `create_workflow_version_step` (create) + `update_workflow_version_step` (configure) + `create_workflow_version_edge` (wire) + `delete_workflow_version_step` (cleanup).

**There's also `create_complete_workflow`** — a single-call shortcut that handles steps + edges + trigger in one operation. BUT the schema description explicitly says:
> "Including CODE steps in this tool — this tool does NOT create the underlying logic function needed by CODE steps. Instead, create the workflow without CODE steps first, then add CODE steps individually using create_workflow_version_step (which properly creates the logic function), then call update_logic_function_source to define the code."

**Verdict: ✅ CANONICAL.** Our contact aging workflow has 3 CODE steps, so `create_complete_workflow` is unusable for us. Twenty's own docs say use the individual tools. Our 4-phase approach is correct.

---

### 2. `cfg()` Wipes `nextStepIds` (Bug 6)

**Ours:** Discovered by instrumented runtime logs. We document this loudly in the build script header.
**Canonical:** The `update_workflow_version_step` schema does not explicitly warn about this, but the existence of a separate `create_workflow_version_edge` tool implies edges are managed as first-class objects, not as side effects of step config.

**Verdict: ✅ CANONICAL with hidden contract.** The separate edge tool IS the documentation. Twenty's frontend would also call edges separately. Our "cfg wipes nextStepIds" finding is really "cfg() doesn't manage edges at all — edges are a separate concern."

**Action:** Keep our Phase 3 pattern. Consider updating the comment in our script from "cfg wipes nextStepIds" to "cfg doesn't manage edges — use createWorkflowVersionEdge for all forward connections."

---

### 3. Iterator Back-Edges (`sourceConnectionOptions`)

**Ours:**
```python
edge(vid, upd_ai_id, iter_id, "UPD_AI→ITER (back-edge)")
# Creates edge with just source+target, no connection options
```

**Canonical:**
```json
{
  "workflowVersionId": "...",
  "source": "upd_ai_id",
  "target": "iter_id",
  "sourceConnectionOptions": {
    "connectedStepType": "ITERATOR",
    "settings": { "isConnectedToLoop": true }
  }
}
```

**Verdict: ⚠️ POTENTIALLY DIFFERENT.** Our back-edges work in practice (verified — 235 people processed with Iterator re-entry). But the canonical schema has a dedicated field for "this edge re-enters an iterator loop." We're not setting it.

**Hypothesis:** The `isConnectedToLoop` flag may be used by the frontend for visual rendering (dashed line vs solid), or by validation. Since the Iterator's `initialLoopStepIds` in its own settings is what the executor reads to drive iteration, the back-edge's purpose is mostly graph completion for the traverser. Our back-edges work because `getAllStepIdsInLoop` reads both `nextStepIds` forward AND detects edges pointing back to the iterator via `connectsBackToIterator` check.

**Action:** Add `sourceConnectionOptions` to our back-edge calls for safety/canonical-correctness. Low risk. Test and confirm nothing breaks.

---

### 4. FIND Filter Structure

**Ours:**
```python
"filter": {
    "recordFilterGroups": [{"id": fg_find, "logicalOperator": "AND"}],
    "recordFilters": [{
        "id": "f-find-1",
        "fieldMetadataId": "897f05a3-...",  # contactPriority
        "operand": "IS_EMPTY",
        "value": "",
        "recordFilterGroupId": fg_find
    }]
}
```

**Canonical:** The `create_complete_workflow` schema describes FIND_RECORDS settings via `input.filter.recordFilters[]` with `fieldMetadataId`, `operand`, `value`, `recordFilterGroupId`, and groups via `recordFilterGroups[]`. Same structure.

**Verdict: ✅ CANONICAL.** Our structure matches exactly. We discovered this shape by reading existing workflows (e.g., the "Create company" default workflow), which is the correct discovery path when schemas aren't public.

**Bug 8 (FIND filter on wrong field) was operator error** — we pointed at lastContactDate instead of contactPriority. Not a Twenty quirk.

---

### 5. IF_ELSE Branches

**Ours:**
```python
fixed_email_branches = [
    {**if_email_branches[0], "nextStepIds": [find_det_id]},
    {**if_email_branches[1], "nextStepIds": [code_noemail_id]}]
cfg(vid, {"id": if_email_id, ..., "settings": {"input": {"branches": fixed_email_branches, ...}}})
```

**Canonical:** We read Twenty's default workflows and copied their branch structure. The MCP `create_complete_workflow` schema confirms: `IF_ELSE` steps have `settings.input.branches[]` each with `id`, `filterGroupId`, `nextStepIds[]`.

**Verdict: ✅ CANONICAL.** Our approach — capture auto-generated branches from `createWorkflowVersionStep`, mutate `nextStepIds`, write back — is the correct pattern.

---

### 6. AI_AGENT Output Wrapper (Bug 7)

**Ours:** Discovered AI_AGENT returns `{response: "...JSON string..."}`. Added CODE_PARSE_AI step to parse it.
**Canonical:** Not documented in the MCP schemas (AI_AGENT is in the stepType enum but we didn't fetch its specific output contract). The `workflow-building.md` skill mentions AI_AGENT briefly but doesn't document the output shape.

**Verdict: ✅ REAL QUIRK.** AI_AGENT returns a single `response` field containing the raw model output. If the prompt asks for structured JSON, the caller must parse it. Our CODE_PARSE_AI step is a valid pattern — likely what Twenty's own workflows do when they need structured AI output.

**Worth verifying:** Check if Twenty has a built-in JSON-parse logic function in `list_logic_function_tools`. We checked — the list is empty in our workspace. If we install the default logic functions via seed data, this may exist as a pre-built tool.

---

### 7. Iterator `shouldContinueOnIterationFailure`

**Ours:**
```python
"shouldContinueOnIterationFailure": True
```

**Canonical:** Documented in the Iterator settings type via `create_complete_workflow` schema (we saw this in the earlier bugs investigation — it's in the shared ITERATOR settings type).

**Verdict: ✅ CANONICAL.** Correct usage.

---

### 8. Missing Edges (Bug 6)

**Ours:** Initially missed 3 forward edges in Phase 3 (FIND_MSG→IF_EMAIL, CODE→IF_PRIO, CODE_NOEMAIL→UPD_NOEMAIL). Found via worker instrumentation.
**Canonical:** The `create_complete_workflow` schema lets you specify `edges[]` explicitly. If we used that tool, edges would be declarative rather than imperative, making it harder to forget them. But we can't use that tool (CODE steps).

**Verdict: ✅ REAL BUG we introduced by forgetting edges.** Not Twenty's fault. The fix (explicit edge list in Phase 3) is correct.

**Action:** Add a Phase 3 verification step that dumps the final graph and checks every non-terminal step has `nextStepIds.length > 0` OR is an IF_ELSE with populated branches. Would catch missing edges at build time.

---

## Our 8 Bugs — Classified

| Bug | Description | Classification |
|-----|-------------|---------------|
| 1 | lastContactDate outputSchema TEXT vs DATE_TIME | **Real Twenty behavior** — outputSchema types affect type coercion. Canonical approach would use typed schemas. |
| 2 | OPENAI_API_KEY startup race | **Real Twenty bug** (known issue #18853). Env var workaround is canonical. |
| 3 | IS_EMPTY filter (cascading from Bug 1) | **Downstream of Bug 1.** Not a separate bug. |
| 4 | Iterator ~89 stall (history accumulation) | **Real Twenty bug** — worker patch is a workaround. Upstream fix pending. |
| 5 | FIND_MSG "empty value" filter cascade | **Real Twenty behavior** (GitHub #18814). We restructured with IF_ELSE guard — canonical pattern. |
| 6 | Missing edges / cfg wipes nextStepIds | **Invented workaround for correct model.** Edges ARE separate from step config in canonical. We just forgot 3. |
| 7 | AI response not parsed | **Real quirk.** AI_AGENT wraps output in `{response: string}`. Parse step is canonical. |
| 8 | FIND filter on wrong field | **Operator error.** Not a Twenty issue. |

**Summary:** 4 real Twenty behaviors (1, 2, 4, 5), 2 real quirks (5, 7), 2 operator errors (6, 8). Nothing we "invented" turned out to be wrong.

---

## Divergences Worth Fixing

### Fix 1: Add `sourceConnectionOptions` to back-edges

**Why:** Canonical schema has a dedicated field for Iterator back-edges. Our edges work without it but may miss visual/validation semantics.

**Change:**
```python
def edge(vid, src, tgt, back_to_iterator=False):
    inp = {"workflowVersionId": vid, "source": src, "target": tgt}
    if back_to_iterator:
        inp["sourceConnectionOptions"] = {
            "connectedStepType": "ITERATOR",
            "settings": {"isConnectedToLoop": True}
        }
    d = gql(..., {"i": inp})
```

### Fix 2: Add post-Phase-3 graph verification

**Why:** Would have caught Bug 6 (missing edges) at build time instead of at runtime.

**Change:** After Phase 3, read back the graph and assert:
- Every step (except IF_ELSE and terminal) has `len(nextStepIds) >= 1`
- Every IF_ELSE has both branches populated
- Iterator has `initialLoopStepIds` and at least one back-edge

### Fix 3: Update build script header comment

**Why:** Replace "cfg wipes nextStepIds" with accurate model: "edges are separate — use createWorkflowVersionEdge."

---

## Strategic Question: Should We Rewrite to MCP?

**Current state:** We call GraphQL mutations directly with user JWT tokens.
**MCP alternative:** Call `POST /mcp` with API key, use `execute_tool` to run `create_workflow_version_step` etc.

**Pros of MCP:**
- API key auth (no token refresh dance)
- Twenty's tool wrapper handles some validation
- Same interface as Twenty's own AI

**Cons of MCP:**
- Extra indirection (MCP → tool registry → GQL resolver → same mutation)
- JSON-RPC framing adds overhead
- We already have working code
- No additional capability — MCP tools wrap the same mutations we already call

**Verdict:** **Keep GraphQL direct for now.** Consider MCP migration only if:
1. We need to support multiple Twenty workspaces (MCP's auth model is simpler)
2. Twenty breaks the direct GraphQL API in a future version
3. We want to share the build script across non-dev-access Twenty instances

---

## Action Items

1. ✅ Document canonical patterns (this file)
2. [ ] Apply Fix 1: sourceConnectionOptions on back-edges
3. [ ] Apply Fix 2: post-Phase-3 graph verification
4. [ ] Apply Fix 3: update header comment
5. [ ] Verify no regression: run LIMIT=2 smoke test
