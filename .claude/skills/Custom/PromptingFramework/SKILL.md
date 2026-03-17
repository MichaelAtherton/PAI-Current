---
name: PromptingFramework
description: Artifact-based 4-layer prompting stack — each workflow produces a concrete output that the next layer builds on. Prompt craft → context engineering → intent engineering → specification engineering. USE WHEN prompting framework, four layers, build prompting stack, layered prompting, artifact-based prompting, cumulative prompting disciplines.
---

# PromptingFramework

Build your prompting capability as a cumulative stack. Each workflow produces a **named artifact** that the next workflow opens and builds on.

```
L1 PromptCraft        → Artifacts/prompt-library.md
    ↓ feeds into
L2 ContextEngineering → Artifacts/context-architecture.md  (graduates L1 patterns)
    ↓ feeds into
L3 IntentEngineering  → Artifacts/intent-document.md       (embeds into L2 architecture)
    ↓ feeds into
L4 SpecEngineering    → Artifacts/{project-name}-spec.md   (references L2 + L3)
```

**Artifacts live in `Artifacts/`** inside this skill directory. This makes the skill self-contained and transferable — artifacts travel with the skill across users and machines.

**How this differs from PromptingStack:** PromptingStack teaches each discipline independently. PromptingFramework chains them — each layer's output is the next layer's input. Skip a layer and the artifacts don't connect.

**Design principle: Structured completeness.** The framework uses templates as organizational tools, not filters. Every workflow instructs: scan the input first, adapt to its actual structure, capture exhaustively, then tag and classify. A well-structured output that's missing content is worse than a comprehensive output with rough edges.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running WORKFLOWNAME in PromptingFramework"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **PromptingFramework** skill to ACTION...
   ```

## Workflow Routing

| Workflow | Trigger | Artifact | File |
|----------|---------|----------|------|
| **PromptCraft** | "improve my prompt", "prompt craft", "fix this prompt" | `Artifacts/prompt-library.md` | `Workflows/PromptCraft.md` |
| **ContextEngineering** | "build my context", "context engineering", "audit context" | `Artifacts/context-architecture.md` | `Workflows/ContextEngineering.md` |
| **IntentEngineering** | "encode intent", "intent engineering", "trade-offs" | `Artifacts/intent-document.md` | `Workflows/IntentEngineering.md` |
| **SpecificationEngineering** | "write a spec", "specification engineering", "specify this" | `Artifacts/{project}-spec.md` | `Workflows/SpecificationEngineering.md` |

## Examples

**Example 1: Start from scratch**
```
User: "Help me build my prompting stack"
→ Start at PromptCraft (L1)
→ User picks a recurring task, we score and rewrite the prompt
→ Produces prompt-library.md with templates and failure modes
→ Bridge: "These patterns should be persistent context, not repeated every session"
→ Proceed to ContextEngineering when ready
```

**Example 2: Mid-stack entry**
```
User: "I already have good prompts, help me build context"
→ Start at ContextEngineering (L2)
→ Inventory existing context docs, audit for relevance
→ Graduate prompt library patterns into persistent context
→ Produces context-architecture.md
→ Bridge: "Your agent knows what to know. Now encode what to want."
```

**Example 3: Full spec from stack**
```
User: "Write a spec for redesigning our onboarding"
→ Start at SpecificationEngineering (L4)
→ Applies 5 primitives, pulling constraints from intent doc (L3),
   referencing context architecture (L2), using clear writing (L1)
→ Validates full-stack integration before delivering
```

## Quick Reference

**The Artifact Chain** (all stored in `Artifacts/`):
1. **L1 → `Artifacts/prompt-library.md`** — refined prompts, templates, known failure modes
2. **L2 → `Artifacts/context-architecture.md`** — what loads when, what earns its place (built from L1 patterns)
3. **L3 → `Artifacts/intent-document.md`** — goals, trade-offs, boundaries (embedded into L2 architecture)
4. **L4 → `Artifacts/{project}-spec.md`** — agent-executable blueprint (references L2 context + L3 intent)

**Full Framework:** See `Framework.md` for the complete conceptual reference.
