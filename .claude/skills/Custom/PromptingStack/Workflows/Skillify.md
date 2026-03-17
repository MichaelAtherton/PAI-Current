# Skillify Workflow

Take any arbitrary task and run it through the 5 specification primitives to produce an agent-executable specification. This is the practical application workflow — turn a vague request into a tight spec.

## Step 1: Get the Task

Ask the user: "What task do you want to specify?"

Accept any format — a vague idea, a one-liner, a detailed brief. The whole point is transforming whatever they give into a complete spec.

## Step 2: Quick Assessment

Before diving in, assess what's missing. Compare their input against the 5 primitives:

| Primitive | Present? | Gap |
|-----------|----------|-----|
| Self-contained problem statement | Y/N | [what's missing] |
| Acceptance criteria | Y/N | [what's missing] |
| Constraint architecture | Y/N | [what's missing] |
| Decomposition | Y/N | [what's missing] |
| Evaluation design | Y/N | [what's missing] |

Show the user: "Here's what your task description is missing."

## Step 3: Interview for Gaps

For each missing primitive, ask targeted questions. Keep it efficient — don't ask what's already clear.

**Self-contained problem statement gaps:**
- "What background would a new team member need to understand this?"
- "What systems or tools are involved?"
- "What does [ambiguous term] mean in your context?"

**Acceptance criteria gaps:**
- "How would someone verify this is done correctly?"
- "What's the difference between 80% done and 100% done?"

**Constraint architecture gaps:**
- "What would technically satisfy this request but be wrong?"
- "What should definitely NOT happen?"
- "If there are multiple valid approaches, which do you prefer?"

**Decomposition gaps:**
- "Can this be broken into phases?"
- "What can be done in parallel vs. what's sequential?"

**Evaluation design gaps:**
- "Can you give me an example of a good output?"
- "What would a subtle failure look like?"

## Step 4: Generate the Specification

Produce the complete spec using the template from `Workflows/SpecificationEngineering.md` Step 3.

Keep it concise — only include what's relevant to the task scope. A 2-hour task doesn't need the same spec depth as a 2-week project.

### Scaling Guide

| Task Size | Spec Depth |
|-----------|------------|
| < 1 hour | Problem statement + acceptance criteria + key constraints (1 page) |
| 1-4 hours | All 5 primitives, light decomposition (1-2 pages) |
| 1-3 days | Full spec with decomposition and eval design (2-4 pages) |
| 1+ weeks | Full spec with break patterns for planner agents (4+ pages) |

## Step 5: Present and Iterate

Show the spec to the user. Ask:
- "Does this capture what you need?"
- "Is anything missing or wrong?"
- "Would you hand this to an agent as-is?"

Iterate until the user is satisfied.

## Step 6: Output

Deliver the final specification in a format the user can use:
- If for claude.md or agent config → markdown optimized for context windows
- If for a team document → structured with headers and tables
- If for a task tracker → decomposed into actionable items

Also offer: "Want me to execute this spec now, or save it for later?"
