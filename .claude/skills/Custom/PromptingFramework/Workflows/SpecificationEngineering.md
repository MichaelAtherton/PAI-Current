# SpecificationEngineering Workflow

**Layer 4 of 4** — Write agent-executable specifications using the 5 primitives. Top of the stack.

**Depends on all three layers:**
- **L1 PromptCraft** (`Artifacts/prompt-library.md`) — clear writing skills to produce clear specs
- **L2 ContextEngineering** (`Artifacts/context-architecture.md`) — spec references existing context, doesn't restate it
- **L3 IntentEngineering** (`Artifacts/intent-document.md`) — tie-breaking rules for ambiguous edges

**Artifact produced:** `Artifacts/{project-name}-spec.md` — complete agent-executable specification.

**Artifact path:** Read from `Artifacts/context-architecture.md` and `Artifacts/intent-document.md`, write to `Artifacts/{project-name}-spec.md`.

## Step 1: Scope the Spec

Ask three questions:
1. "What's the project or outcome?"
2. "How long should an agent work on this autonomously?" (hours / days / weeks)
3. "What agent architecture?" (single agent / planner-worker / team)

**Scale the spec depth to the scope:**

| Scope | Spec Depth | Primitives |
|-------|------------|------------|
| < 1 hour | Problem + criteria + constraints | 1-page spec |
| 1-4 hours | All 5 primitives, light decomposition | 1-2 pages |
| 1-3 days | Full spec with decomposition + eval | 2-4 pages |
| 1+ weeks | Full spec with break patterns for planner agents | 4+ pages |

## Step 2: Apply the 5 Primitives

### Primitive 1 — Self-Contained Problem Statement

Write it. Then apply the test: **hand it to someone with zero context. Can they start working?**

If not, what's missing? Add it. Common gaps:
- Domain terminology undefined
- Systems/tools/access not specified
- Implicit organizational knowledge not surfaced
- Input format assumptions unstated (what if the input has unexpected structure?)

**Pull from L2:** Open `Artifacts/context-architecture.md` and reference which context documents the agent needs loaded. Don't restate what's already in the context layer — point to it.

### Primitive 2 — Acceptance Criteria

Write 3-5 criteria. Each one must pass this test: **could an independent observer verify this without asking a single question?**

Bad: "The code should be clean." (Who decides what's clean?)
Good: "All functions have < 20 lines, no nested callbacks beyond 2 levels, and eslint passes with zero warnings."

**Pull from L3:** Open `Artifacts/intent-document.md` and reference its quality definitions. "Good enough" for this work category is defined there — don't reinvent it.

### Primitive 3 — Constraint Architecture

Four categories:

| Category | Source | Question |
|----------|--------|----------|
| **Musts** | Requirements | What absolutely must happen? |
| **Must-nots** | Anti-patterns from L3 | What would a smart executor do wrong? |
| **Preferences** | Trade-off hierarchy from L3 | When two valid approaches exist, which wins? |
| **Escalation triggers** | Decision boundaries from L3 | What should make the agent stop? |

**This is where the full stack integrates.** Must-nots come from the anti-patterns you identified in intent engineering. Preferences come from the trade-off hierarchy. Escalation triggers come from decision boundaries. The constraint architecture is L3 intent made specific to THIS project.

### Primitive 4 — Decomposition

Break into subtasks. Rules:
- Each < 2 hours of work
- Clear input → output per task
- Each independently verifiable
- Dependencies explicit

**Pre-scan before decomposition:** Before breaking work into subtasks, the spec should instruct the executor to scan the full input and detect its actual structure. Decomposition should adapt to what's there, not assume a fixed format. If a single input file contains multiple logical units (e.g., two meetings in one transcript, multiple data sources in one export), each unit gets its own extraction pass.

**For planner-worker architectures:** Define break patterns — not the subtasks themselves, but the RULES for how a planner should decompose:
- "Natural boundaries are [X]"
- "Never split [Y] across tasks"
- "Each task should produce [type of artifact]"
- "If the input contains multiple logical units, decompose per unit first, then per extraction type"

### Primitive 5 — Evaluation Design

For each acceptance criterion, build a test:

| Criterion | Test | Known-Good Output | Subtle Failure |
|-----------|------|-------------------|----------------|
| [criterion] | [how to verify] | [example of right] | [example of almost-right-but-wrong] |

The "subtle failure" column is the hard part. It's what separates specs that produce 80% outputs from specs that produce 100% outputs.

## Step 3: Assemble

```markdown
# Specification: [Project Name]
**Scope:** [hours/days/weeks] | **Architecture:** [single/planner-worker/team]
**Context required:** [list context docs from L2 that must be loaded]
**Intent reference:** [link to intent document from L3]

## Problem Statement
[Self-contained. Zero-context reader can start working.]

## Acceptance Criteria
1. [ ] [Verifiable by independent observer]
2. [ ] [Verifiable by independent observer]
3. [ ] [Verifiable by independent observer]

## Constraints
**Must:** [non-negotiable requirements]
**Must not:** [anti-patterns from L3, made specific to this project]
**Prefer:** [trade-offs from L3, applied here]
**Escalate if:** [boundaries from L3, applied here]

## Decomposition
### Phase 1: [Name]
- [ ] Task 1.1 — In: [X] → Out: [Y] — Verify: [how]
- [ ] Task 1.2 — In: [X] → Out: [Y] — Verify: [how]

### Phase 2: [Name] (depends on Phase 1)
- [ ] Task 2.1 — In: [output of 1.1] → Out: [Y]

### Break Patterns
- [Rule for planner agents to decompose further]
- [Natural boundaries to respect]

## Evaluation
| Criterion | Test | Good Output | Subtle Failure |
|-----------|------|-------------|----------------|
| [1] | [method] | [right] | [almost-right-but-wrong] |
| [2] | [method] | [right] | [almost-right-but-wrong] |
```

## Step 4: Validate the Full Stack Integration

Check that the spec actually uses the layers below it:

- [ ] **L1 check:** Is the writing clear? Could you hand any section to a stranger?
- [ ] **L2 check:** Does the spec reference context docs, not restate them?
- [ ] **L3 check:** Do constraints trace back to intent document entries?
- [ ] **L3 check:** Do preferences match the trade-off hierarchy?
- [ ] **L3 check:** Do escalation triggers match decision boundaries?
- [ ] **Completeness check:** Does the spec instruct a pre-scan of input before extraction? Does it require a second pass to catch items the template might miss? Does it favor exhaustive capture with tagging over selective extraction?

If any check fails, the spec is decoupled from the stack. Fix the connection.

## Step 5: Deliver

Present the spec. Ask: "Would you hand this to an agent and walk away for [scope duration]?"

If no — iterate. If yes — the stack is complete.

**This is the top of the stack.** The spec is the output. It encodes everything:
- Clear writing from L1
- Right information environment from L2
- Right priorities from L3
- Right blueprint from L4
