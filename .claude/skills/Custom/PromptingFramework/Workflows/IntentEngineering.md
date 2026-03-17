# IntentEngineering Workflow

**Layer 3 of 4** — Encode what agents should WANT, not just what they should KNOW.

**Depends on:** Layer 2 artifact (`Artifacts/context-architecture.md`). Intent rides on context — you can't encode "prefer satisfaction over speed" if the agent has no access to satisfaction metrics. You'll embed intent directly into the context infrastructure you built.

**Artifact produced:** `Artifacts/intent-document.md` — goals, trade-off hierarchies, decision boundaries, and escalation triggers. This gets embedded into your context architecture AND becomes the tie-breaking ruleset that specifications depend on.

**Artifact path:** Read from `Artifacts/context-architecture.md`, write to `Artifacts/intent-document.md`.

## Step 1: Identify Where Intent Is Missing

Open `Artifacts/context-architecture.md` (Layer 2 artifact). For each context document listed, ask:

- Does this tell the agent what to DO but not WHAT MATTERS?
- If two valid approaches exist, does the agent know which to prefer?
- If something goes wrong, does the agent know when to stop vs. push through?

**The Klarna test:** Could your agent optimize perfectly for the WRONG metric? If yes, intent is missing.

## Step 2: Extract the Four Intent Components

Interview the user. Be direct — don't accept vague answers.

### Goals (ranked, not listed)
- "If you could only accomplish ONE thing with this agent/team/project, what is it?"
- "What's second? What's third?"
- "When goal 1 and goal 2 conflict, goal 1 wins — correct?"

Force a stack rank. Goals that aren't ranked aren't goals — they're wishes.

### Trade-off Hierarchies
Present concrete either/or scenarios from the user's actual work:
- "This report can be thorough OR fast. Which?"
- "This code can be clean OR shipped today. Which?"
- "This response can be comprehensive OR concise. Which?"
- "This extraction can capture everything loosely OR capture fewer items precisely. Which?"

Build the hierarchy from their answers, not from abstract values.

**Default trade-off when not specified:** Completeness over template compliance. A structured output that's missing real content is worse than a slightly messy output that captures everything. The template is an organizational tool, not a filter. Encode this unless the user explicitly prefers precision over recall.

### Decision Boundaries
Three categories — make them draw the lines:
- **Autonomous:** "What can the agent just DO without asking?"
- **Approval required:** "What must the agent get sign-off on? Why?"
- **Escalation triggers:** "What should make the agent STOP and flag a human?"

### Anti-Patterns
- "Tell me about a time AI did something technically correct but wrong."
- "What would a smart, well-intentioned junior employee get wrong here?"
- "What's the most expensive mistake an agent could make in your work?"
- "Has a tool ever given you a clean, well-structured output that was missing important content? What was lost?"

**Default anti-pattern:** Template-driven filtering — where the structure of the output determines what gets extracted from the input, instead of the input determining what the output contains. This manifests as clean-looking results with silent content loss. Always include this unless the user's use case genuinely prioritizes precision over recall.

## Step 3: Draft the Intent Document

```markdown
# Intent: [Scope]

## Primary Goal
[One sentence. This wins all conflicts.]

## Goal Stack (ranked)
1. [Primary — always wins]
2. [Secondary — wins against everything below]
3. [Tertiary]

## Trade-offs (when X conflicts with Y)
| Prefer | Over | Because |
|--------|------|---------|
| [X] | [Y] | [concrete reason from their work] |
| [A] | [B] | [concrete reason] |

## Decision Boundaries
| Autonomous | Needs Approval | Escalate Immediately |
|------------|---------------|---------------------|
| [action] | [action: why] | [condition: consequence] |

## Anti-Patterns
| Pattern | Why It's Wrong | How to Detect |
|---------|---------------|---------------|
| [behavior] | [consequence from real experience] | [signal] |
```

## Step 4: Embed Into Context Architecture

Open `Artifacts/context-architecture.md` (Layer 2 artifact). For each context document:

1. **System prompt / claude.md:** Add the goal stack and top 3 trade-offs. These are always-loaded.
2. **Project conventions:** Add relevant decision boundaries for that project scope.
3. **Tool definitions:** Add escalation triggers to tools that can cause damage.
4. **On-demand context:** Tag documents with which goals they serve — this helps agents prioritize retrieval.

**The output is NOT a separate intent file floating in space.** It's intent woven INTO the existing context infrastructure. The context architecture doc gets updated to reflect where intent lives.

## Step 5: Stress Test

Present 3 scenarios where priorities conflict. Apply the intent document. Check:

| Scenario | Intent Says | User Agrees? | Fix |
|----------|-------------|-------------|-----|
| [conflict scenario from their real work] | [decision per intent doc] | Y/N | [adjustment if N] |

If the intent document produces wrong answers, it's wrong. Fix it. Iterate until every scenario resolves correctly.

## → Next Layer

Your agents now know what to know and what to want. For bounded tasks, this is powerful. But when agents run for days — producing multi-phase outputs across sessions — intent alone can't hold. You need blueprints: complete, self-contained specifications with acceptance criteria, constraints, decomposition, and evaluation built in.

The intent document you just built becomes the tie-breaking ruleset that specifications rely on at ambiguous edges. Every spec has gray areas. Without intent, agents resolve them randomly. With intent, they resolve them according to your priorities.

**When ready:** → SpecificationEngineering workflow. Bring your intent document and context architecture.
