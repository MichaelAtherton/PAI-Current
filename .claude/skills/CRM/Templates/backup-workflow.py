#!/usr/bin/env python3
"""
Twenty Workflow Backup Utility
==============================
Dumps a workflow + its current version + all steps + trigger to a JSON file.

Usage:
  python3 backup-workflow.py <workflowId>
  python3 backup-workflow.py 90f1d148-cd10-419a-895c-d8edaa86e9c4

Output: .claude/skills/CRM/Templates/backups/workflow-<wfId>-<timestamp>.json

The backup captures:
- Workflow metadata (name, statuses)
- All workflow versions (id, status, createdAt)
- For each version: steps (full settings), trigger, nextStepIds, edges
- Logic function IDs + source code for any CODE steps

Restoration is manual — use the build script pattern to recreate from the JSON.
"""
import json, subprocess, os, sys, time
from pathlib import Path

BASE = "http://localhost:3030"
API_KEY = os.environ.get("TWENTY_API_KEY", "")
BACKUP_DIR = Path(__file__).parent / "backups"

def _curl(args):
    r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(r.stdout)
    except:
        return {"raw": r.stdout[:500], "err": r.stderr[:200]}

def fresh_token():
    r1 = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
        "-d", '{"query":"mutation{getLoginTokenFromCredentials(email:\\"michael@pai.local\\",password:\\"pai2026!\\",origin:\\"http://localhost:3030\\"){loginToken{token}}}"}'])
    lt = r1["data"]["getLoginTokenFromCredentials"]["loginToken"]["token"]
    r2 = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
        "-d", f'{{"query":"mutation{{getAuthTokensFromLoginToken(loginToken:\\"{lt}\\",origin:\\"http://localhost:3030\\"){{tokens{{accessOrWorkspaceAgnosticToken{{token}}}}}}}}"}}'
    ])
    return r2["data"]["getAuthTokensFromLoginToken"]["tokens"]["accessOrWorkspaceAgnosticToken"]["token"]

def gql(query):
    t = fresh_token()
    r = _curl(["curl", "-s", "-X", "POST", f"{BASE}/graphql", "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {t}", "-d", json.dumps({"query": query})])
    return r.get("data")

def metadata_gql(query):
    """Query metadata schema (for logic functions)."""
    r = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {API_KEY}", "-d", json.dumps({"query": query})])
    return r.get("data")

def backup_workflow(wf_id):
    print(f"Backing up workflow {wf_id}")

    # 1. Workflow metadata
    wf_data = gql(f'{{workflows(filter:{{id:{{eq:"{wf_id}"}}}}){{edges{{node{{id name statuses createdAt updatedAt}}}}}}}}')
    if not wf_data or not wf_data["workflows"]["edges"]:
        print(f"  ERROR: Workflow {wf_id} not found")
        return None
    wf = wf_data["workflows"]["edges"][0]["node"]
    print(f"  Workflow: {wf['name']} ({wf['statuses']})")

    # 2. All workflow versions
    versions_data = gql(f'{{workflowVersions(filter:{{workflowId:{{eq:"{wf_id}"}}}}){{edges{{node{{id status createdAt updatedAt steps trigger}}}}}}}}')
    versions = [e["node"] for e in versions_data["workflowVersions"]["edges"]]
    print(f"  Versions: {len(versions)}")

    # 3. For each CODE step, fetch the logic function source
    logic_fn_ids = set()
    for v in versions:
        steps = v.get("steps") or []
        if isinstance(steps, str):
            steps = json.loads(steps)
        for s in steps:
            if s.get("type") == "CODE":
                lfn_id = s.get("settings", {}).get("input", {}).get("logicFunctionId")
                if lfn_id:
                    logic_fn_ids.add(lfn_id)

    logic_fns = {}
    if logic_fn_ids:
        print(f"  Fetching {len(logic_fn_ids)} logic functions...")
        for lfn_id in logic_fn_ids:
            # getLogicFunctionSourceCode returns the source; findOneLogicFunction returns metadata
            src_q = 'query($input: LogicFunctionIdInput!) { getLogicFunctionSourceCode(input: $input) }'
            r = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
                "-H", f"Authorization: Bearer {API_KEY}",
                "-d", json.dumps({"query": src_q, "variables": {"input": {"id": lfn_id}}})])
            src = (r.get("data") or {}).get("getLogicFunctionSourceCode")
            meta_q = 'query($input: LogicFunctionIdInput!) { findOneLogicFunction(input: $input) { id name description } }'
            r2 = _curl(["curl", "-s", "-X", "POST", f"{BASE}/metadata", "-H", "Content-Type: application/json",
                "-H", f"Authorization: Bearer {API_KEY}",
                "-d", json.dumps({"query": meta_q, "variables": {"input": {"id": lfn_id}}})])
            meta = (r2.get("data") or {}).get("findOneLogicFunction") or {}
            if src or meta:
                logic_fns[lfn_id] = {**meta, "sourceCode": src}

    # 4. Write backup
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow-{wf_id[:8]}-{timestamp}.json"

    backup = {
        "backup_metadata": {
            "backup_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "twenty_base": BASE,
            "backup_script_version": "1.0",
        },
        "workflow": wf,
        "versions": versions,
        "logic_functions": logic_fns,
    }
    backup_path.write_text(json.dumps(backup, indent=2))
    print(f"\n✓ Backup written: {backup_path}")
    print(f"  Size: {backup_path.stat().st_size:,} bytes")
    print(f"  Steps: {sum(len(v.get('steps') or []) for v in versions)}")
    print(f"  Logic functions: {len(logic_fns)}")
    return backup_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 backup-workflow.py <workflowId>")
        sys.exit(1)
    backup_workflow(sys.argv[1])
