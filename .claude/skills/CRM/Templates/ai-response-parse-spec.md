# Spec: Parse AI_AGENT Response into Person Fields

**Date:** 2026-04-04
**Scope:** Insert 1 CODE step into the existing 12-step Contact Aging workflow
**Risk:** Low — no existing steps modified, only new step + edge rewiring

---

## Problem

AI_AGENT ("Analyze Relationship") returns:
```json
{"response": "{\"relationshipStatus\":\"AT_RISK\",\"aiSummary\":\"...\",\"confidence\":80}"}
```

UPD_AI references `{{ai_id.relationshipStatus}}` — resolves to empty because `relationshipStatus` is inside a JSON string, not a top-level field. Result: contactPriority and lastContactDays are saved, but relationshipStatus and aiSummary are silently dropped.

## Solution

Insert **CODE_PARSE_AI** between AI_AGENT and UPD_AI:

```
Before:  AI_AGENT → UPD_AI → ITER
After:   AI_AGENT → CODE_PARSE_AI → UPD_AI → ITER
```

### CODE_PARSE_AI logic function

```javascript
export const main = async (params) => {
  const raw = params.aiResponse || '';
  try {
    const parsed = JSON.parse(raw);
    return {
      relationshipStatus: parsed.relationshipStatus || 'UNKNOWN',
      aiSummary: parsed.aiSummary || '',
      confidence: parsed.confidence || 0
    };
  } catch (e) {
    return {
      relationshipStatus: 'UNKNOWN',
      aiSummary: 'AI response could not be parsed',
      confidence: 0
    };
  }
};
```

Input: `{"aiResponse": "{{ai_id.response}}"}`

Output schema:
| Field | Type | Example |
|-------|------|---------|
| relationshipStatus | TEXT | AT_RISK |
| aiSummary | TEXT | Contact declined a meeting... |
| confidence | NUMBER | 80 |

### UPD_AI changes

Update variable references from `{{ai_id.*}}` to `{{parseAiId.*}}`:
```python
"relationshipStatus": "{{parse_ai_id.relationshipStatus}}",
"aiSummary": "{{parse_ai_id.aiSummary}}"
```

## Build Script Changes

1. **Phase 1:** Add `make_step(vid, "CODE", ai_id)` after AI_AGENT — creates CODE_PARSE_AI as child of AI_AGENT
2. **Phase 1:** Change UPD_AI parent from `ai_id` to `parse_ai_id`
3. **Phase 2:** Add cfg() for CODE_PARSE_AI with logic function + output schema
4. **Phase 2:** Update UPD_AI cfg() to reference `parse_ai_id` instead of `ai_id` for relationshipStatus and aiSummary
5. **Phase 3:** Replace `AI→UPD_AI` edge with `AI→CODE_PARSE_AI` + `CODE_PARSE_AI→UPD_AI` edges

## What Does NOT Change

- All 12 existing steps — unchanged
- All other edges — unchanged
- Iterator, IF_ELSE guards, back-edges — unchanged
- CODE (computeContactPriority) — unchanged
- No-email path — unchanged (doesn't hit AI_AGENT)
- UPD_BASIC path — unchanged (doesn't use AI fields)

## Resulting Graph (13 steps)

```
FIND → ITER → FIND_MSG → IF_HAS_EMAIL?
                           ┌──────┴──────┐
                        (true)         (false)
                           │              │
                      FIND_DET      CODE_NOEMAIL
                           │              │
                         CODE        UPD_NOEMAIL → ITER
                           │
                      IF_PRIORITY?
                      ┌────┴────┐
                   (true)    (false)
                      │         │
                  AI_AGENT  UPD_BASIC → ITER
                      │
                 CODE_PARSE_AI    ← NEW
                      │
                   UPD_AI → ITER
```

## Verification

After deployment, run with LIMIT=3 and check:
1. Person with email + company: `relationshipStatus` is one of ACTIVE/COOLING/AT_RISK/COLD/DEAD (not null, not empty)
2. Person with email + company: `aiSummary` is a non-empty sentence referencing email content
3. Person without email: `relationshipStatus` stays null (no-email path doesn't hit AI)
4. Person with email + no company: `relationshipStatus` stays null (UPD_BASIC path, AI skipped)
