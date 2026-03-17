# SpecificationEngineering Workflow

Write a complete, agent-executable specification for a project using all 5 specification primitives.

This is the highest-altitude discipline: documents that autonomous agents can execute against over extended time horizons without human intervention.

## Step 1: Get the Project

Ask the user:
- What project or outcome do they want to specify?
- What is the scope? (Single task? Multi-day project? Ongoing process?)
- Who/what will execute against this spec? (Autonomous agent? Team of agents? Planner-worker architecture?)

## Step 2: Apply the 5 Primitives

Work through each primitive sequentially. For each one, interview the user, then draft that section.

### Primitive 1: Self-Contained Problem Statement

Draft a problem statement that includes ALL context needed. Test it with: "Could someone with zero prior context execute this?"

**Interview questions:**
- What is the desired outcome?
- What background does the executor need?
- What domain knowledge is assumed?
- What systems/tools/access is required?
- What terminology needs definition?

### Primitive 2: Acceptance Criteria

Write 3-5 verifiable acceptance criteria. Test: "Could an independent observer verify these without asking questions?"

**Interview questions:**
- What does "done" look like?
- What are the measurable indicators of success?
- What quality thresholds must be met?
- How would you test each criterion?

### Primitive 3: Constraint Architecture

Define all four constraint categories:

| Category | Questions |
|----------|-----------|
| **Musts** | What absolutely must happen? Non-negotiable requirements? |
| **Must-nots** | What must NOT happen? What would be dangerous/wrong? |
| **Preferences** | When multiple valid approaches exist, which should be preferred? |
| **Escalation triggers** | What conditions should cause the agent to stop and ask? |

**Test:** "What would a smart, well-intentioned executor do that technically satisfies the request but produces the wrong outcome?" Those failure modes become must-nots or constraints.

### Primitive 4: Decomposition

Break the project into independently executable subtasks.

**Rules:**
- Each subtask < 2 hours of work
- Clear input/output boundaries per subtask
- Each subtask independently verifiable
- Dependencies between subtasks explicitly stated

**For planner-worker architectures:** Also define the BREAK PATTERNS — the rules a planner agent should use to decompose this work. What defines a natural boundary? What should NOT be split?

### Primitive 5: Evaluation Design

Design the quality verification system.

**For each acceptance criterion:**
- What test would prove it's met?
- What does a known-good output look like?
- What does a subtle failure look like?
- How would you catch regressions?

**Build 3-5 eval test cases** with known-good outputs.

## Step 3: Assemble the Specification

Combine all primitives into a single document:

```markdown
# Specification: [Project Name]

## Problem Statement
[Self-contained description with all necessary context]

## Acceptance Criteria
1. [ ] [Criterion 1 — verifiable statement]
2. [ ] [Criterion 2 — verifiable statement]
3. [ ] [Criterion 3 — verifiable statement]

## Constraints

### Must
- [Requirement 1]
- [Requirement 2]

### Must Not
- [Anti-requirement 1]
- [Anti-requirement 2]

### Preferences
- Prefer [A] over [B] when [condition]
- Prefer [X] over [Y] when [condition]

### Escalation Triggers
- If [condition], stop and ask before proceeding
- If [condition], escalate to [person/process]

## Task Decomposition

### Phase 1: [Phase Name]
- [ ] Task 1.1: [description] — Input: [X] → Output: [Y]
- [ ] Task 1.2: [description] — Input: [X] → Output: [Y]

### Phase 2: [Phase Name]
- [ ] Task 2.1: [description] — Depends on: 1.1, 1.2
- [ ] Task 2.2: [description] — Input: [X] → Output: [Y]

### Break Patterns (for planner agents)
- [Rule for how to decompose further if needed]
- [Natural boundaries to respect]

## Evaluation

### Test Cases
| # | Input | Expected Output | Verification Method |
|---|-------|-----------------|---------------------|
| 1 | [input] | [expected] | [how to check] |
| 2 | [input] | [expected] | [how to check] |
| 3 | [input] | [expected] | [how to check] |

### Quality Checklist
- [ ] [Quality check 1]
- [ ] [Quality check 2]
- [ ] [Quality check 3]
```

## Step 4: Validate the Specification

Review the completed spec against these quality checks:
- **Self-containment:** Could someone with zero context execute this?
- **Completeness:** Are all acceptance criteria verifiable?
- **Constraint coverage:** Would a smart executor avoid common pitfalls?
- **Decomposition quality:** Are all tasks < 2 hours with clear boundaries?
- **Eval coverage:** Can every acceptance criterion be tested?

Flag any gaps and iterate with the user.
