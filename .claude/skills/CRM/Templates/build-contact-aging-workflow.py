#!/usr/bin/env python3
"""
Twenty CRM Workflow Builder — Contact Aging Analysis
=====================================================
Reference implementation for building workflows via API.

BUG INVESTIGATION PROTOCOL:
  If this script fails or produces unexpected results, DO NOT debug inline
  for more than 15 minutes. Instead:
  1. Capture the exact error message
  2. Write 2-3 targeted API test hypotheses (curl to REST/GraphQL)
  3. Run tests via parallel agents
  4. Document findings in References/BugFindings-{date}.md
  5. Search Twenty GitHub issues for known bugs
  No public workflow API docs exist — all behavior must be verified empirically.

BUILD ORDER (critical):
  Phase 1: Create ALL steps (parentStepId sets initial edges)
  Phase 2: Configure ALL steps (updateWorkflowVersionStep — wipes edges, OK)
  Phase 3: Add ALL edges LAST (createWorkflowVersionEdge — these persist)
  Phase 4: Delete EMPTY orphans, set trigger, activate

KEY LEARNINGS:
- API key works for REST + /metadata. User token required for /graphql mutations.
- Fresh token before every gql() call (30-min expiry).
- updateWorkflowVersionStep WIPES nextStepIds — never include nextStepIds in step config.
- createWorkflowVersionEdge adds edges that persist IF called after all configs.
- First step in empty version returns CHANGE diff (not CREATE) — parse both.
- Iterator items: {{findId.all}}, currentItem: {{iteratorId.currentItem.id}}
- AI_AGENT uses 'prompt' field, NOT 'agentInput'.
- IF_ELSE boolean filter: type="boolean", operand="IS".
- IF_ELSE branches: include correct nextStepIds in the branches array during config.
- EMPTY placeholders auto-created by IF_ELSE/ITERATOR — delete as last step.
- Iterator REQUIRES back-edges from every terminal loop step back to the Iterator.
  Without these, the executor completes 1 iteration then hangs (no re-entry).
- cfg() (updateWorkflowVersionStep) WIPES ALL nextStepIds. Every forward edge that was
  set by parentStepId in Phase 1 must be re-added as an explicit edge in Phase 3.
  Missing edges cause getAllStepIdsInLoop to return incomplete loop set, which causes
  back-edge parents to appear as non-loop parents → shouldExecuteChildStep fails.
"""

import json, subprocess, os, time, sys

BASE = "http://localhost:3030"
API_KEY = os.environ.get("TWENTY_API_KEY", "")
AGENT_ID = "5cea09b4-3875-4d14-b9a4-7b4265faa5dc"  # Email Relationship Analyzer
LIMIT = 2  # Smoke test. Set to 500 for production (requires Iterator history patch on worker).


# ── Helpers ──────────────────────────────────────────

def _curl(args):
    r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(r.stdout)
    except:
        print(f"  CURL PARSE ERROR: {r.stdout[:100]}", file=sys.stderr)
        return {"errors": [{"message": "parse error"}]}

def fresh_token():
    """Get a fresh workspace ACCESS token. Call before every gql()."""
    r1 = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
        "-d", '{"query":"mutation{getLoginTokenFromCredentials(email:\\"michael@pai.local\\",password:\\"pai2026!\\",origin:\\"http://localhost:3030\\"){loginToken{token}}}"}'])
    lt = r1["data"]["getLoginTokenFromCredentials"]["loginToken"]["token"]
    r2 = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
        "-d", f'{{"query":"mutation{{getAuthTokensFromLoginToken(loginToken:\\"{lt}\\",origin:\\"http://localhost:3030\\"){{tokens{{accessOrWorkspaceAgnosticToken{{token}}}}}}}}"}}'])
    return r2["data"]["getAuthTokensFromLoginToken"]["tokens"]["accessOrWorkspaceAgnosticToken"]["token"]

def gql(query, variables=None):
    """Execute GraphQL on /graphql with fresh user token."""
    t = fresh_token()
    d = {"query": query}
    if variables:
        d["variables"] = variables
    r = _curl(["curl", "-s", "-X", "POST", f"{BASE}/graphql", "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {t}", "-d", json.dumps(d)])
    if r.get("errors"):
        print(f"  ⚠ GQL: {r['errors'][0]['message']}")
        return None
    return r.get("data")

def rest_patch(path, data):
    return _curl(["curl", "-s", "-X", "PATCH", f"{BASE}{path}", "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {API_KEY}", "-d", json.dumps(data)])

def make_step(vid, stype, parent=None, conn=None):
    """Create a step. Returns new step ID."""
    inp = {"workflowVersionId": vid, "stepType": stype}
    if parent:
        inp["parentStepId"] = parent
    if conn:
        inp["parentStepConnectionOptions"] = {"type": conn}
    d = gql("mutation($i:CreateWorkflowVersionStepInput!){createWorkflowVersionStep(input:$i){stepsDiff}}", {"i": inp})
    if not d:
        return None
    for item in d["createWorkflowVersionStep"]["stepsDiff"]:
        if item.get("type") == "CREATE" and isinstance(item.get("value"), dict) and item["value"].get("type") == stype:
            return item["value"]["id"]
        if item.get("type") == "CHANGE" and isinstance(item.get("value"), list):
            for v in item["value"]:
                if isinstance(v, dict) and v.get("type") == stype:
                    return v["id"]
    return None

def cfg(vid, step):
    """Configure a step's settings. Do NOT include nextStepIds."""
    d = gql("mutation($i:UpdateWorkflowVersionStepInput!){updateWorkflowVersionStep(input:$i){id name type}}",
        {"i": {"workflowVersionId": vid, "step": step}})
    if d:
        print(f"  ✓ {d['updateWorkflowVersionStep']['name']}")
    return d is not None

def edge(vid, src, tgt, from_iterator_to_loop=False):
    """Connect two steps. Call AFTER all cfg() calls.

    When from_iterator_to_loop=True, passes sourceConnectionOptions per the
    canonical MCP schema — this field applies when SOURCE is an Iterator and
    the edge is entering its loop body (not for back-edges TO an iterator).

    Verified empirically: passing sourceConnectionOptions with a non-iterator
    source step fails with "Source step ... is not an iterator." Back-edges
    from UPDATE_RECORD → ITERATOR should NOT set this field.
    """
    inp = {"workflowVersionId": vid, "source": src, "target": tgt}
    if from_iterator_to_loop:
        inp["sourceConnectionOptions"] = {
            "connectedStepType": "ITERATOR",
            "settings": {"isConnectedToLoop": True}
        }
    d = gql("mutation($i:CreateWorkflowVersionEdgeInput!){createWorkflowVersionEdge(input:$i){stepsDiff}}",
        {"i": inp})
    return d is not None

def verify_graph(vid, iterator_ids=None):
    """Post-Phase-3 graph verification — catches missing edges before runtime.

    Asserts:
    - Every non-IF_ELSE, non-UPDATE/DELETE-terminal step has nextStepIds
    - Every IF_ELSE has both branches with nextStepIds populated
    - Every Iterator has initialLoopStepIds AND at least one back-edge

    Returns: (ok: bool, errors: list[str])
    """
    iterator_ids = iterator_ids or []
    node = get_node(vid)
    steps = node["steps"]
    by_id = {s["id"]: s for s in steps}
    errors = []

    # Steps that legitimately have no nextStepIds: loop terminal steps (back-edge targets)
    # and EMPTY placeholders. Everything else should have edges.
    for s in steps:
        sid = s["id"]
        name = s["name"]
        stype = s["type"]
        nxt = s.get("nextStepIds") or []

        if stype == "EMPTY":
            continue

        if stype == "IF_ELSE":
            branches = s.get("settings", {}).get("input", {}).get("branches", [])
            if len(branches) < 2:
                errors.append(f"IF_ELSE '{name}' has {len(branches)} branches, expected 2")
                continue
            for i, b in enumerate(branches):
                bname = "TRUE" if i == 0 else "FALSE"
                if not b.get("nextStepIds"):
                    errors.append(f"IF_ELSE '{name}' {bname} branch has empty nextStepIds")
            continue

        if stype == "ITERATOR":
            init = s.get("settings", {}).get("input", {}).get("initialLoopStepIds") or []
            if not init:
                errors.append(f"Iterator '{name}' has empty initialLoopStepIds")
            # Check at least one back-edge exists (some step points at this iterator)
            back_edges = [other for other in steps
                          if sid in (other.get("nextStepIds") or [])
                          and other["id"] != s.get("parentStepId", "")]
            if not back_edges:
                errors.append(f"Iterator '{name}' has no back-edges from loop body")
            continue

        # Regular step — must have nextStepIds unless it's terminal in a loop
        # (points back to its enclosing iterator)
        if not nxt:
            errors.append(f"Step '{name}' ({stype}) has empty nextStepIds — missing forward edge?")

    return (len(errors) == 0, errors)

def get_node(vid):
    """Get version's steps and trigger."""
    d = gql(f'{{workflowVersions(filter:{{id:{{eq:"{vid}"}}}}){{edges{{node{{steps trigger}}}}}}}}')
    return d["workflowVersions"]["edges"][0]["node"] if d else None


# ── BUILD (12-step architecture per loop-restructure-implementation.md) ──

t0 = time.time()
print("=" * 60)
print("BUILDING: Contact Aging Analysis (13-step, IF_HAS_EMAIL + AI parse)")
print("  Phases: create → configure → edges → cleanup")
print("=" * 60)

# Create workflow shell (REST, API key)
r = _curl(["curl", "-s", "-X", "POST", f"{BASE}/rest/workflows", "-H", "Content-Type: application/json",
    "-H", f"Authorization: Bearer {API_KEY}", "-d", '{"name": "Contact Aging Analysis"}'])
wf_id = r["data"]["createWorkflow"]["id"]
vlist = _curl(["curl", "-s", f"{BASE}/rest/workflowVersions?limit=20", "-H", f"Authorization: Bearer {API_KEY}"])
vid = next(v["id"] for v in vlist["data"]["workflowVersions"] if v.get("workflowId") == wf_id)
rest_patch(f"/rest/workflowVersions/{vid}",
    {"trigger": {"type": "CRON", "settings": {"type": "CUSTOM", "pattern": "0 8 * * 1"}}})
print(f"WF: {wf_id}\nVER: {vid}\n")


# ═══ PHASE 1: CREATE ALL 12 STEPS ═══
print("── Phase 1: Create steps (12) ──")
find_id         = make_step(vid, "FIND_RECORDS");                              print(f"  1  FIND:         {find_id[:12]}")
iter_id         = make_step(vid, "ITERATOR", find_id);                         print(f"  2  ITER:         {iter_id[:12]}")
find_msg_id     = make_step(vid, "FIND_RECORDS", iter_id, "loop");             print(f"  3  FIND_MSG:     {find_msg_id[:12]}")
if_email_id     = make_step(vid, "IF_ELSE", find_msg_id);                      print(f"  4  IF_EMAIL:     {if_email_id[:12]}")
# TRUE branch (has email):
find_det_id     = make_step(vid, "FIND_RECORDS", if_email_id, "true");         print(f"  5  FIND_DET:     {find_det_id[:12]}")
code_id         = make_step(vid, "CODE", find_det_id);                         print(f"  6  CODE:         {code_id[:12]}")
if_prio_id      = make_step(vid, "IF_ELSE", code_id);                         print(f"  7  IF_PRIO:      {if_prio_id[:12]}")
ai_id           = make_step(vid, "AI_AGENT", if_prio_id, "true");             print(f"  8  AI_AGENT:     {ai_id[:12]}")
parse_ai_id     = make_step(vid, "CODE", ai_id);                             print(f"  9  PARSE_AI:     {parse_ai_id[:12]}")
upd_ai_id       = make_step(vid, "UPDATE_RECORD", parse_ai_id);              print(f"  10 UPD_AI:       {upd_ai_id[:12]}")
upd_basic_id    = make_step(vid, "UPDATE_RECORD", if_prio_id, "false");       print(f"  11 UPD_BASIC:    {upd_basic_id[:12]}")
# FALSE branch (no email):
code_noemail_id = make_step(vid, "CODE", if_email_id, "false");               print(f"  12 CODE_NOEMAIL: {code_noemail_id[:12]}")
upd_noemail_id  = make_step(vid, "UPDATE_RECORD", code_noemail_id);           print(f"  13 UPD_NOEMAIL:  {upd_noemail_id[:12]}")

all_steps = [find_id, iter_id, find_msg_id, if_email_id, find_det_id, code_id,
             if_prio_id, ai_id, parse_ai_id, upd_ai_id, upd_basic_id, code_noemail_id, upd_noemail_id]
if not all(all_steps):
    print("\n⚠ Step creation failed. Aborting.")
    sys.exit(1)

# Capture auto-generated IDs before configs wipe them
node = get_node(vid)
# Three CODE steps = three logic functions
code_step = next(s for s in node["steps"] if s["id"] == code_id)
lfn_id = code_step["settings"]["input"].get("logicFunctionId", "")
parse_ai_step = next(s for s in node["steps"] if s["id"] == parse_ai_id)
lfn_parse_ai_id = parse_ai_step["settings"]["input"].get("logicFunctionId", "")
code_noemail_step = next(s for s in node["steps"] if s["id"] == code_noemail_id)
lfn_noemail_id = code_noemail_step["settings"]["input"].get("logicFunctionId", "")
iter_step = next(s for s in node["steps"] if s["id"] == iter_id)
# Two IF_ELSE steps = two sets of branches
if_email_step = next(s for s in node["steps"] if s["id"] == if_email_id)
if_email_branches = if_email_step["settings"]["input"]["branches"]
fg_email = if_email_branches[0].get("filterGroupId", "fg-email")
if_prio_step = next(s for s in node["steps"] if s["id"] == if_prio_id)
if_prio_branches = if_prio_step["settings"]["input"]["branches"]
fg_prio = if_prio_branches[0].get("filterGroupId", "fg-prio")

# Update BOTH logic functions (metadata API, API key)
# Logic function 1: computeContactPriority (has email — uses message.receivedAt)
code_email_str = ('export const main = async (params) => { '
    'const p = params.person || {}; '
    'const msg = params.latestMessage; '
    'const hasCo = !!p.companyId; '
    'let days = 999; let lastContactDate = null; '
    'if (msg && msg.receivedAt) { lastContactDate = msg.receivedAt; '
    '  days = Math.floor((new Date() - new Date(msg.receivedAt)) / 86400000); } '
    'let priority = "LOW"; '
    'if (hasCo && days <= 30) priority = "HIGH"; '
    'else if (hasCo) priority = "MEDIUM"; '
    'else if (days <= 30) priority = "MEDIUM"; '
    'const emailSubject = msg && msg.subject ? msg.subject : "No email found"; '
    'const emailBody = msg && msg.text ? msg.text.slice(0, 1500) : "No email content available"; '
    'const emailDirection = msg && msg.direction ? msg.direction : "UNKNOWN"; '
    'return { contactPriority: priority, lastContactDays: days, lastContactDate: lastContactDate, '
    'shouldAnalyze: hasCo, dealInfo: hasCo ? "Has company" : "No company", '
    'emailSubject, emailBody, emailDirection }; };')
_curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
    "-H", f"Authorization: Bearer {API_KEY}", "-d",
    json.dumps({"query": "mutation U($i:UpdateLogicFunctionFromSourceInput!){updateOneLogicFunction(input:$i)}",
        "variables": {"i": {"id": lfn_id, "update": {"name": "computeContactPriority", "sourceHandlerCode": code_email_str}}}})])

# Logic function 2: computeContactPriorityNoEmail (no email — uses person.createdAt)
code_noemail_str = ('export const main = async (params) => { '
    'const p = params.person || {}; '
    'const hasCo = !!p.companyId; '
    'let days = 999; '
    'if (p.createdAt) { days = Math.floor((new Date() - new Date(p.createdAt)) / 86400000); } '
    'return { contactPriority: hasCo ? "MEDIUM" : "LOW", lastContactDays: days, lastContactDate: null, '
    'shouldAnalyze: false, dealInfo: hasCo ? "Has company, no email" : "No company, no email", '
    'emailSubject: "No email found", emailBody: "No email content available", emailDirection: "UNKNOWN" }; };')
_curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
    "-H", f"Authorization: Bearer {API_KEY}", "-d",
    json.dumps({"query": "mutation U($i:UpdateLogicFunctionFromSourceInput!){updateOneLogicFunction(input:$i)}",
        "variables": {"i": {"id": lfn_noemail_id, "update": {"name": "computeContactPriorityNoEmail", "sourceHandlerCode": code_noemail_str}}}})])

# Logic function 3: parseAiResponse (parses JSON string from AI_AGENT response)
code_parse_ai_str = ('export const main = async (params) => { '
    'const raw = params.aiResponse || ""; '
    'try { '
    '  const parsed = JSON.parse(raw); '
    '  return { '
    '    relationshipStatus: parsed.relationshipStatus || "UNKNOWN", '
    '    aiSummary: parsed.aiSummary || "", '
    '    confidence: parsed.confidence || 0 '
    '  }; '
    '} catch (e) { '
    '  return { '
    '    relationshipStatus: "UNKNOWN", '
    '    aiSummary: "AI response could not be parsed: " + raw.slice(0, 100), '
    '    confidence: 0 '
    '  }; '
    '} };')
_curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
    "-H", f"Authorization: Bearer {API_KEY}", "-d",
    json.dumps({"query": "mutation U($i:UpdateLogicFunctionFromSourceInput!){updateOneLogicFunction(input:$i)}",
        "variables": {"i": {"id": lfn_parse_ai_id, "update": {"name": "parseAiResponse", "sourceHandlerCode": code_parse_ai_str}}}})])

PARSE_AI_OUTPUT_SCHEMA = {
    "relationshipStatus": {"type": "TEXT", "label": "relationshipStatus", "value": "UNKNOWN", "isLeaf": True},
    "aiSummary": {"type": "TEXT", "label": "aiSummary", "value": "", "isLeaf": True},
    "confidence": {"type": "NUMBER", "label": "confidence", "value": 0, "isLeaf": True}}

# Output schema shared by both priority CODE steps
OUTPUT_SCHEMA = {
    "contactPriority": {"type": "TEXT", "label": "contactPriority", "value": "HIGH", "isLeaf": True},
    "lastContactDays": {"type": "NUMBER", "label": "lastContactDays", "value": 0, "isLeaf": True},
    "shouldAnalyze": {"type": "BOOLEAN", "label": "shouldAnalyze", "value": True, "isLeaf": True},
    "dealInfo": {"type": "TEXT", "label": "dealInfo", "value": "", "isLeaf": True},
    "lastContactDate": {"type": "DATE_TIME", "label": "lastContactDate", "value": "2025-01-01T00:00:00.000Z", "isLeaf": True},
    "emailSubject": {"type": "TEXT", "label": "emailSubject", "value": "", "isLeaf": True},
    "emailBody": {"type": "TEXT", "label": "emailBody", "value": "", "isLeaf": True},
    "emailDirection": {"type": "TEXT", "label": "emailDirection", "value": "", "isLeaf": True}}
ERR_OPTS = {"retryOnFailure": {"value": False}, "continueOnFailure": {"value": True}}
ERR_STRICT = {"retryOnFailure": {"value": False}, "continueOnFailure": {"value": False}}


# ═══ PHASE 2: CONFIGURE ALL 12 STEPS ═══
print("\n── Phase 2: Configure steps (13) ──")

# Step 1: Find Unprocessed People
fg_find = "fg-find-1"
find_input = {"objectName": "person", "limit": LIMIT,
    "filter": {"recordFilterGroups": [{"id": fg_find, "logicalOperator": "AND"}],
        "recordFilters": [{"id": "f-find-1", "fieldMetadataId": "897f05a3-ae48-4ae9-ba32-b89515a929d5",
            "operand": "IS_EMPTY", "value": "", "recordFilterGroupId": fg_find}]}}
cfg(vid, {"id": find_id, "name": "Find Unprocessed People", "type": "FIND_RECORDS", "valid": True,
    "settings": {"input": {k: v for k, v in find_input.items() if v is not None},
        "outputSchema": {}, "errorHandlingOptions": ERR_STRICT}})

# Step 2: Iterator
cfg(vid, {"id": iter_id, "name": "For Each Person", "type": "ITERATOR", "valid": True,
    "settings": {"input": {"items": "{{" + find_id + ".all}}", "initialLoopStepIds": [find_msg_id],
        "shouldContinueOnIterationFailure": True},
        "outputSchema": iter_step["settings"].get("outputSchema", {}), "errorHandlingOptions": ERR_OPTS}})

# Step 3: Find Messages (messageParticipant by person)
fg_msg = "fg-msg-1"
cfg(vid, {"id": find_msg_id, "name": "Find Messages", "type": "FIND_RECORDS", "valid": True,
    "settings": {"input": {"objectName": "messageParticipant", "limit": 1,
        "orderBy": {"gqlOperationOrderBy": [{"createdAt": "DescNullsLast"}]},
        "filter": {"recordFilterGroups": [{"id": fg_msg, "logicalOperator": "AND"}],
            "recordFilters": [{"id": "f-msg-1", "fieldMetadataId": "d19518ca-854c-4160-9e03-fee564cea05b",
                "operand": "IS", "value": "{{" + iter_id + ".currentItem.id}}", "recordFilterGroupId": fg_msg}]}},
        "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})

# Step 4: Has Email? (IF_ELSE guard — checks totalCount >= 1)
fixed_email_branches = [
    {**if_email_branches[0], "nextStepIds": [find_det_id]},
    {**if_email_branches[1], "nextStepIds": [code_noemail_id]}]
cfg(vid, {"id": if_email_id, "name": "Has Email?", "type": "IF_ELSE", "valid": True,
    "settings": {"input": {"branches": fixed_email_branches,
        "stepFilterGroups": [{"id": fg_email, "logicalOperator": "AND"}],
        "stepFilters": [{"id": "f-email-1", "type": "number",
            "stepOutputKey": "{{" + find_msg_id + ".totalCount}}", "operand": "GREATER_THAN_OR_EQUAL", "value": "1",
            "stepFilterGroupId": fg_email, "positionInStepFilterGroup": 0}]},
        "outputSchema": {}, "errorHandlingOptions": ERR_STRICT}})

# Step 5: Get Message Detail (message by id — for receivedAt)
fg_det = "fg-det-1"
cfg(vid, {"id": find_det_id, "name": "Get Message Detail", "type": "FIND_RECORDS", "valid": True,
    "settings": {"input": {"objectName": "message", "limit": 1,
        "filter": {"recordFilterGroups": [{"id": fg_det, "logicalOperator": "AND"}],
            "recordFilters": [{"id": "f-det-1", "fieldMetadataId": "ae62024e-6bf1-4a05-b674-26ea1c39f06e",
                "operand": "IS", "value": "{{" + find_msg_id + ".first.messageId}}", "recordFilterGroupId": fg_det}]}},
        "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})

# Step 6: Compute Priority (with email)
cfg(vid, {"id": code_id, "name": "Compute Priority", "type": "CODE", "valid": True,
    "settings": {"input": {"logicFunctionId": lfn_id, "logicFunctionInput": {
        "person": "{{" + iter_id + ".currentItem}}",
        "latestMessage": "{{" + find_det_id + ".first}}"}},
        "outputSchema": OUTPUT_SCHEMA, "errorHandlingOptions": ERR_OPTS}})

# Step 7: Is HIGH or MEDIUM? (IF_ELSE — checks shouldAnalyze)
fixed_prio_branches = [
    {**if_prio_branches[0], "nextStepIds": [ai_id]},
    {**if_prio_branches[1], "nextStepIds": [upd_basic_id]}]
cfg(vid, {"id": if_prio_id, "name": "Is HIGH or MEDIUM?", "type": "IF_ELSE", "valid": True,
    "settings": {"input": {"branches": fixed_prio_branches,
        "stepFilterGroups": [{"id": fg_prio, "logicalOperator": "AND"}],
        "stepFilters": [{"id": "f-prio-1", "type": "boolean",
            "stepOutputKey": "{{" + code_id + ".shouldAnalyze}}", "operand": "IS", "value": "true",
            "stepFilterGroupId": fg_prio, "positionInStepFilterGroup": 0}]},
        "outputSchema": {}, "errorHandlingOptions": ERR_STRICT}})

# Step 8: Analyze Relationship (AI_AGENT)
prompt = (f"You are a CRM relationship analyst. Analyze this contact's most recent email and determine their relationship status.\\n\\n"
    f"CONTACT: {{{{{iter_id}.currentItem.name.firstName}}}} {{{{{iter_id}.currentItem.name.lastName}}}}\\n"
    f"COMPANY: {{{{{iter_id}.currentItem.companyId}}}}\\n"
    f"DAYS SINCE LAST EMAIL: {{{{{code_id}.lastContactDays}}}}\\n"
    f"EMAIL DIRECTION: {{{{{code_id}.emailDirection}}}}\\n"
    f"EMAIL SUBJECT: {{{{{code_id}.emailSubject}}}}\\n"
    f"EMAIL BODY:\\n{{{{{code_id}.emailBody}}}}\\n\\n"
    f"CLASSIFICATION RULES:\\n"
    f"- ACTIVE: Engaged conversation within 30 days. Back-and-forth exchanges, meeting scheduling, project discussions, warm tone.\\n"
    f"- COOLING: Was active but slowing down. 30-90 days since contact, or last email was a brief reply with no follow-up.\\n"
    f"- AT_RISK: 90-180 days since contact, or last email shows disengagement (short replies, declined meetings, unsubscribe-like language).\\n"
    f"- COLD: 180-365 days since contact. No meaningful engagement in the email content.\\n"
    f"- DEAD: Over 365 days, OR email is automated/marketing/unsubscribe, OR no email found.\\n\\n"
    f"Respond with ONLY valid JSON, no other text:\\n"
    f'{{"relationshipStatus": "ACTIVE|COOLING|AT_RISK|COLD|DEAD", "aiSummary": "one sentence explaining your reasoning based on the email content", "confidence": 0-100}}')
cfg(vid, {"id": ai_id, "name": "Analyze Relationship", "type": "AI_AGENT", "valid": True,
    "settings": {"input": {"agentId": AGENT_ID, "prompt": prompt}, "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})

# Step 9: Parse AI Response (extracts JSON fields from AI_AGENT's response string)
cfg(vid, {"id": parse_ai_id, "name": "Parse AI Response", "type": "CODE", "valid": True,
    "settings": {"input": {"logicFunctionId": lfn_parse_ai_id, "logicFunctionInput": {
        "aiResponse": "{{" + ai_id + ".response}}"}},
        "outputSchema": PARSE_AI_OUTPUT_SCHEMA, "errorHandlingOptions": ERR_OPTS}})

# Step 10: Update Person (AI) — email path, has company, AI analyzed
cfg(vid, {"id": upd_ai_id, "name": "Update Person (AI)", "type": "UPDATE_RECORD", "valid": True,
    "settings": {"input": {"objectName": "person", "objectRecordId": "{{" + iter_id + ".currentItem.id}}",
        "objectRecord": {"contactPriority": "{{" + code_id + ".contactPriority}}",
            "lastContactDays": "{{" + code_id + ".lastContactDays}}",
            "lastContactDate": "{{" + code_id + ".lastContactDate}}",
            "relationshipStatus": "{{" + parse_ai_id + ".relationshipStatus}}",
            "aiSummary": "{{" + parse_ai_id + ".aiSummary}}"}},
        "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})

# Step 11: Update Person (Basic) — email path, no company
cfg(vid, {"id": upd_basic_id, "name": "Update Person (Basic)", "type": "UPDATE_RECORD", "valid": True,
    "settings": {"input": {"objectName": "person", "objectRecordId": "{{" + iter_id + ".currentItem.id}}",
        "objectRecord": {"contactPriority": "{{" + code_id + ".contactPriority}}",
            "lastContactDays": "{{" + code_id + ".lastContactDays}}",
            "lastContactDate": "{{" + code_id + ".lastContactDate}}"}},
        "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})

# Step 12: Compute Priority (no email) — uses person.createdAt as fallback
cfg(vid, {"id": code_noemail_id, "name": "Compute Priority (No Email)", "type": "CODE", "valid": True,
    "settings": {"input": {"logicFunctionId": lfn_noemail_id, "logicFunctionInput": {
        "person": "{{" + iter_id + ".currentItem}}"}},
        "outputSchema": OUTPUT_SCHEMA, "errorHandlingOptions": ERR_OPTS}})

# Step 13: Update Person (No Email)
cfg(vid, {"id": upd_noemail_id, "name": "Update Person (No Email)", "type": "UPDATE_RECORD", "valid": True,
    "settings": {"input": {"objectName": "person", "objectRecordId": "{{" + iter_id + ".currentItem.id}}",
        "objectRecord": {"contactPriority": "{{" + code_noemail_id + ".contactPriority}}",
            "lastContactDays": "{{" + code_noemail_id + ".lastContactDays}}"}},
        "outputSchema": {}, "errorHandlingOptions": ERR_OPTS}})


# ═══ PHASE 3: ADD EDGES LAST ═══
# NOTE: edges are a separate concern from step config. cfg() does not manage
# nextStepIds — use createWorkflowVersionEdge (via edge()) for every forward
# connection. See .claude/skills/CRM/References/CanonicalVsOurs.md.
print("\n── Phase 3: Add edges ──")
# Forward edges (src, tgt, label) — back_to_iterator defaults to False
forward_edges = [
    (find_id, iter_id, "FIND→ITER"),
    (find_msg_id, if_email_id, "FIND_MSG→IF_EMAIL"),
    (find_det_id, code_id, "FIND_DET→CODE"),
    (code_id, if_prio_id, "CODE→IF_PRIO"),
    (ai_id, parse_ai_id, "AI→PARSE_AI"),
    (parse_ai_id, upd_ai_id, "PARSE_AI→UPD_AI"),
    (code_noemail_id, upd_noemail_id, "CODE_NOEMAIL→UPD_NOEMAIL"),
]
# Back-edges: 3 terminal loop steps → Iterator. Canonical schema requires
# sourceConnectionOptions.isConnectedToLoop=true (set via back_to_iterator flag).
back_edges = [
    (upd_ai_id, iter_id, "UPD_AI→ITER (back-edge)"),
    (upd_basic_id, iter_id, "UPD_BASIC→ITER (back-edge)"),
    (upd_noemail_id, iter_id, "UPD_NOEMAIL→ITER (back-edge)"),
]
for src, tgt, label in forward_edges:
    ok = edge(vid, src, tgt)
    print(f"  {'✓' if ok else '⚠'} {label}")
for src, tgt, label in back_edges:
    # NOTE: sourceConnectionOptions is NOT for back-edges. The source of a
    # back-edge is UPDATE_RECORD, not ITERATOR, and Twenty rejects the payload
    # with "Source step ... is not an iterator." Back-edges work via plain
    # source+target — the Iterator's initialLoopStepIds drives re-entry.
    ok = edge(vid, src, tgt)
    print(f"  {'✓' if ok else '⚠'} {label}")

# Trigger → first step
rest_patch(f"/rest/workflowVersions/{vid}",
    {"trigger": {"type": "CRON", "settings": {"type": "CUSTOM", "pattern": "0 8 * * 1"}, "nextStepIds": [find_id]}})
print(f"  ✓ Trigger→FIND")


# ═══ PHASE 4: CLEANUP + ACTIVATE ═══
# ═══ PHASE 3.5: GRAPH VERIFICATION ═══
# Catches missing edges (Bug 6 class) BEFORE runtime. See CanonicalVsOurs.md.
print("\n── Phase 3.5: Graph verification ──")
ok, errors = verify_graph(vid)
if ok:
    print("  ✓ Graph structure valid")
else:
    print(f"  ⚠ {len(errors)} graph errors:")
    for e in errors:
        print(f"    - {e}")
    print("\n  ABORTING — fix errors above before activation. EMPTY steps will be cleaned up in Phase 4 so they are ignored here.")
    # Filter out errors that are just about EMPTY placeholders that will be cleaned up
    real_errors = [e for e in errors if "EMPTY" not in e]
    if real_errors:
        sys.exit(1)
    print("  (Above errors are EMPTY placeholders — Phase 4 will clean them up.)")


print("\n── Phase 4: Cleanup + Activate ──")
node = get_node(vid)
for s in node["steps"]:
    if s["type"] == "EMPTY":
        gql(f'mutation{{deleteWorkflowVersionStep(input:{{workflowVersionId:"{vid}",stepId:"{s["id"]}"}}){{stepsDiff}}}}')
        print(f"  Deleted EMPTY {s['id'][:12]}")

# Final verification
node = get_node(vid)
names = {s["id"]: s["name"] for s in node["steps"]}
print(f"\n  Trigger → {[names.get(n, n[:12]) for n in node['trigger'].get('nextStepIds', [])]}")
for s in node["steps"]:
    nxt = [names.get(n, n[:12]) for n in s.get("nextStepIds", [])]
    x = ""
    if s["type"] == "ITERATOR":
        x = f" loop→{[names.get(n, n[:12]) for n in s['settings']['input']['initialLoopStepIds']]}"
    if s["type"] == "IF_ELSE":
        for i, b in enumerate(s["settings"]["input"]["branches"]):
            label = "TRUE" if i == 0 else "FALSE"
            x += f" {label}→{[names.get(n, n[:12]) for n in b.get('nextStepIds', [])]}"
    print(f"  {s['type']:20s} {s['name']:30s} → {nxt}{x}")
print(f"  {len(node['steps'])} steps")

# Activate + Run
gql(f'mutation{{activateWorkflowVersion(workflowVersionId:"{vid}")}}')
gql(f'mutation{{runWorkflowVersion(input:{{workflowVersionId:"{vid}"}}){{__typename}}}}')
elapsed = time.time() - t0
print(f"\n✓ Running at {time.strftime('%H:%M:%S')} (built in {elapsed:.0f}s)")
print(f"\nWF: {wf_id}\nVER: {vid}\nLIMIT: {LIMIT}")
