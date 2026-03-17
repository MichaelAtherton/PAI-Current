# IntentEngineering Workflow

Help the user encode organizational purpose, goals, values, trade-off hierarchies, and decision boundaries into agent-readable infrastructure.

Context engineering tells agents what to KNOW. Intent engineering tells agents what to WANT.

## Step 1: Identify the Scope

Ask the user what level they're working at:

| Scope | Example |
|-------|---------|
| **Personal** | Individual contributor encoding their own decision frameworks |
| **Team** | Team lead encoding team values and priorities |
| **Organizational** | Encoding company strategy, OKRs, trade-offs |
| **Product/Agent** | Encoding intent for a specific AI agent or product |

## Step 2: Extract Intent Components

Interview the user to surface these five components:

### 2a. Goals
- What is this agent/team/org trying to achieve?
- What does success look like in 30 days? 90 days? A year?
- What metrics matter most?

### 2b. Values & Trade-off Hierarchies
- When two good things conflict, which wins? (Speed vs quality? Cost vs coverage? Thoroughness vs simplicity?)
- What does "good enough" look like for different work categories?
- What is NEVER acceptable regardless of trade-offs?

### 2c. Decision Boundaries
- What can the agent/team decide autonomously?
- What requires human approval?
- What is the escalation threshold? (Dollar amount? Risk level? Novelty?)

### 2d. Optimization Targets
- What should be MAXIMIZED?
- What should be MINIMIZED?
- What should be MAINTAINED at a specific level?

**Klarna warning:** Optimizing for the wrong target with perfect execution is worse than mediocre execution toward the right target.

### 2e. Anti-Patterns
- What has gone wrong before when intent was unclear?
- What "technically correct but wrong" outcomes have you seen?
- What would a smart, well-intentioned agent do wrong without this intent guidance?

## Step 3: Draft Intent Document

Produce a structured intent document:

```markdown
# Intent: [Scope Name]

## Mission
[1-2 sentence purpose statement]

## Goals (Prioritized)
1. [Primary goal — this wins when goals conflict]
2. [Secondary goal]
3. [Tertiary goal]

## Trade-off Hierarchy
When in conflict, prefer (in order):
1. [First priority] over [second priority]
2. [Second priority] over [third priority]
3. [Specific trade-off relevant to this scope]

## Quality Definitions
| Work Category | "Good Enough" | "Excellent" | "Unacceptable" |
|---------------|---------------|-------------|-----------------|
| [Category 1] | [definition] | [definition] | [definition] |
| [Category 2] | [definition] | [definition] | [definition] |

## Decision Boundaries
### Autonomous (agent decides)
- [Decision type 1]
- [Decision type 2]

### Requires Approval
- [Decision type 1: why]
- [Decision type 2: why]

### Escalation Triggers
- [Trigger 1: condition → escalate to whom]
- [Trigger 2: condition → escalate to whom]

## Anti-Patterns (Must Avoid)
- [Anti-pattern 1: what it looks like, why it's wrong]
- [Anti-pattern 2: what it looks like, why it's wrong]
```

## Step 4: Integration

Help the user integrate the intent document into their infrastructure:
- For personal scope: embed in claude.md or personal context files
- For team scope: create shared intent document accessible to all team agents
- For org scope: encode in organizational specification documents
- For agent scope: embed in system prompt or agent configuration

## Step 5: Validation

Test the intent document by presenting 3-5 hypothetical scenarios and checking whether the intent document would produce the RIGHT decision:

1. Present scenario
2. Apply intent document rules
3. Check: does the outcome match what the user actually wants?
4. If not, refine the intent document
