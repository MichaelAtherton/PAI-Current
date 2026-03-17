# PromptCraft Workflow

Improve the user's synchronous prompt writing skills. This is Layer 1 — table stakes, but foundational.

## Step 1: Get the Prompt

Ask the user for either:
- A specific prompt they want improved
- A recurring task they want a prompt template for
- A description of what they're trying to accomplish

## Step 2: Evaluate Against the 5 Elements

Score the prompt (or draft one) against the 5 core elements of prompt craft:

| Element | Present? | Quality |
|---------|----------|---------|
| **Clear instructions** | Y/N | Specific, unambiguous, actionable? |
| **Examples & counter-examples** | Y/N | Relevant, edge-case-covering? |
| **Guardrails** | Y/N | Prevent common failure modes? |
| **Explicit output format** | Y/N | Structured, parseable, useful? |
| **Ambiguity resolution** | Y/N | Conflicts addressed? Defaults stated? |

## Step 3: Identify Failure Modes

For each missing or weak element, describe the specific failure it causes:
- Missing instructions → model guesses intent → wrong output
- No examples → model picks wrong style/format → rework needed
- No guardrails → model does technically correct but useless things
- No output format → inconsistent, unparseable results
- No ambiguity resolution → model makes random choices in edge cases

## Step 4: Rewrite

Produce an improved prompt that addresses all gaps. Show before/after with annotations explaining each change.

## Step 5: Template (Optional)

If this is a recurring task, produce a reusable template with:
- Fixed structural elements
- Variable slots clearly marked with `{PLACEHOLDER}` syntax
- Usage notes for each variable
- Example of a filled-in version

## Output Format

```markdown
## Prompt Craft Analysis

### Original Prompt
> [user's prompt]

### Element Scores
| Element | Score | Issue |
|---------|-------|-------|
| Clear instructions | X/3 | [issue] |
| Examples | X/3 | [issue] |
| Guardrails | X/3 | [issue] |
| Output format | X/3 | [issue] |
| Ambiguity resolution | X/3 | [issue] |

### Improved Prompt
[The rewritten prompt]

### What Changed
- [Annotation 1]
- [Annotation 2]

### Template (if recurring)
[Reusable template version]
```
