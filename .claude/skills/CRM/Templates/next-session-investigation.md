# Next Session: IS_EMPTY on SELECT Field (Bug 8)

**Date:** 2026-04-04
**Priority:** BLOCKING — 151 of 235 people can't be reprocessed
**Estimated time:** 30 minutes with investigation protocol

---

## Current State

- **Workflow:** f00b3b54 (13-step, with AI parse, LIMIT=500, ACTIVE)
- **Version:** 1ff7592b
- **84 people** processed (contactPriority + relationshipStatus set)
- **151 people** stuck: contactPriority=NULL via GQL+REST, but FIND_RECORDS IS_EMPTY finds 0

### Relationship Status Breakdown (48 with AI analysis)
| Status | Count |
|--------|-------|
| DEAD | 31 |
| COLD | 7 |
| AT_RISK | 7 |
| ACTIVE | 2 |
| COOLING | 1 |
| null (no AI path) | 187 |

## Symptom

FIND_RECORDS step with `IS_EMPTY` operand on contactPriority field (fieldMetadataId: `6babc91f-791a-4897-9105-d9c00afd9edc`) finds 0 results for the 151 people that GQL confirms have NULL contactPriority.

## What Works

- GQL `{people(filter:{contactPriority:{is:NULL}})}` → 151 (correct)
- REST `/rest/people/{id}` → `contactPriority: null` (correct)
- GQL `updatePerson(data:{contactPriority:null})` → returns None (appears to work)
- FIND_RECORDS IS_EMPTY on DATE_TIME fields → works correctly (Bug 3 confirmed)

## What Doesn't Work

- FIND_RECORDS IS_EMPTY on contactPriority (SELECT type) → finds 0 of the 151 NULL records
- REST PATCH `{contactPriority: null}` → may not actually write SQL NULL for SELECT fields

## Investigation Plan

### Step 1: Check the database directly
```sql
docker exec twenty-local-db-1 psql -U postgres -d default \
  -c "SELECT \"contactPriority\", COUNT(*) FROM core.\"person\" GROUP BY \"contactPriority\" ORDER BY COUNT(*) DESC;"
```
This tells us what the actual column values are. If we see `''` (empty string) instead of NULL, that's the root cause.

### Step 2: Check the fieldMetadataId
```sql
docker exec twenty-local-db-1 psql -U postgres -d default \
  -c "SELECT id, name, type FROM core.\"fieldMetadata\" WHERE id = '6babc91f-791a-4897-9105-d9c00afd9edc';"
```
Verify it points to the correct field.

### Step 3: Check FIND_RECORDS IS_EMPTY SQL translation
Instrument `find-records.workflow-action.js` to log the generated SQL WHERE clause when IS_EMPTY is used on a SELECT field.

### Step 4: Test alternative reset approach
```sql
-- Try direct SQL NULL update
docker exec twenty-local-db-1 psql -U postgres -d default \
  -c "UPDATE core.\"person\" SET \"contactPriority\" = NULL WHERE \"contactPriority\" IS NOT NULL LIMIT 5;"
-- Then run workflow and see if IS_EMPTY finds them
```

## Files

- Build script: `.claude/skills/CRM/Templates/build-contact-aging-workflow.py`
- Debugging guide: `.claude/skills/CRM/References/WorkflowDebugging.md`
- Bug findings: `.claude/skills/CRM/References/BugFindings-2026-04-04.md`
- AI parse spec: `.claude/skills/CRM/Templates/ai-response-parse-spec.md`

## Prerequisites

- Twenty CRM running on localhost:3030
- OPENAI_API_KEY env var set on server + worker containers
- Iterator history patch applied on worker (`history: []`)
