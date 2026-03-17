# PromptCraft Workflow

**Layer 1 of 4** — Write clear, structured instructions. Foundation for everything above.

**Artifact produced:** `Artifacts/prompt-library.md` — a collection of the user's refined prompts and templates that becomes raw material for their context layer.

**Artifact path:** Write to `Artifacts/prompt-library.md` relative to the skill directory. If it already exists, append new entries rather than overwriting.

## Step 1: Identify the Work

Ask: "What's one task you do repeatedly with AI where the output isn't consistently good?"

Don't accept abstract answers. Get a specific, concrete task. If they say "writing emails" — which emails? To whom? What goes wrong?

## Step 2: Draft or Collect

Either:
- Have them paste an existing prompt they use
- Write a first-draft prompt together from their description

## Step 3: Score Ruthlessly

Evaluate against 6 elements. Be blunt — score 0-3, no inflation:

| Element | Score | Verdict |
|---------|-------|---------|
| **Instructions** | 0-3 | Could a stranger follow these without asking a single question? |
| **Examples** | 0-3 | Does the model see what "right" and "wrong" look like? |
| **Guardrails** | 0-3 | What's the dumbest correct-but-useless thing the model could do? Is that blocked? |
| **Output format** | 0-3 | Could you parse this output programmatically? |
| **Ambiguity handling** | 0-3 | When two instructions conflict, does the prompt say which wins? |
| **Adaptiveness** | 0-3 | If the input doesn't match expectations (unusual format, multiple items in one file, unexpected structure), does the prompt handle that or break? |

**Scoring key:** 0 = absent, 1 = present but weak, 2 = solid, 3 = bulletproof.

## Step 4: Rewrite

Fix every element scoring below 2. Show the diff — what changed and WHY each change prevents a specific failure mode. No generic "improved clarity" annotations. Name the failure: "Without this guardrail, the model will [specific bad outcome]."

**Completeness over compliance.** The rewritten prompt must produce output that captures everything relevant in the input, not just what fits neatly into a template. Two principles:

1. **Pre-scan before extraction.** The prompt should instruct the model to scan the input first and adapt its approach — detecting unexpected structure (multiple items in one file, mixed formats, section breaks that indicate separate contexts). A rigid template applied blindly to unexpected input loses information.

2. **Exhaustive-then-tagged.** When extracting items from a source (action items, decisions, entities), the prompt should instruct: capture ALL candidates first, then tag/classify/rank them. This prevents the template from filtering out valid items that don't fit a narrow definition. It's better to surface 14 items with certainty tags than to present 4 "clean" items and silently drop 10.

The goal is structured completeness — use the template's structure as an organizational tool, not a filter.

3. **Preserve required sub-fields.** Completeness applies to content capture, not to template relaxation. When the template specifies sub-fields for an item (e.g., open questions must include "Why it matters" and "Who should answer"), those sub-fields are required — they're what make the output actionable. Broadening capture scope must not loosen structural requirements on the items captured.

## Step 5: Templatize

Convert the improved prompt into a reusable template:
- Fixed structure stays fixed
- Variables marked as `{{VARIABLE_NAME}}` with a one-line description each
- One filled-in example showing the template in use

## Step 6: Completeness Check

Before finalizing, apply the **second-pass test**: re-read the source material (or a representative sample) with the rewritten prompt in mind. Ask:

- Are there items in the source that the prompt would miss because they don't fit the template's categories?
- If the input had an unexpected format (two meetings in one file, mixed content types, speaker changes mid-stream), would the prompt handle it or silently drop content?
- Does the prompt instruct exhaustive capture before filtering, or does it filter during capture?

If the prompt would miss valid content, add a **pre-scan instruction** ("Before extracting, scan the full input and note any structural surprises — multiple documents, format changes, or section breaks that suggest separate contexts. Adapt your extraction accordingly.") and a **completeness guardrail** ("After extraction, re-scan the source for any items not yet captured. Surface anything missed, even if it doesn't fit neatly into the template categories.").

## Step 7: Produce the Artifact

Save the output to `Artifacts/prompt-library.md`. If the file already exists, append the new entry. This is the **prompt library**:

```markdown
# Prompt Library

## [Task Name]
**Use when:** [one-line trigger description]
**Last updated:** [date]
**Element scores:** Instructions [X] | Examples [X] | Guardrails [X] | Format [X] | Ambiguity [X]

### Template
[The template with {{VARIABLES}}]

### Example (filled)
[One complete example]

### Known failure modes
- [What goes wrong if you skip X]
- [Edge case to watch for]

### Adaptiveness notes
- [What happens if the input format is unexpected]
- [What the prompt does with multiple items in one file]
```

Repeat for additional tasks if the user wants to keep going.

## → Next Layer

This prompt library is good for synchronous work. But it's 0.02% of what the model sees. The next layer takes your best prompts and templates and uses them as building blocks for the persistent context documents — system prompts, claude.md files, tool definitions — that shape the other 99.98%.

**When ready:** → ContextEngineering workflow. Bring your prompt library.
