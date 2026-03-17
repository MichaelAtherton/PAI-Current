---
name: PromptingStack
description: Four-discipline prompting framework — prompt craft, context engineering, intent engineering, and specification engineering with assessment and practical application. USE WHEN prompting stack, assess my prompting, improve my prompt, prompt craft, context engineering, build my context, intent engineering, encode intent, specification engineering, write a spec, specify this task, prompting framework, prompting skills 2026, four disciplines, spec engineering.
---

# PromptingStack

The complete 4-layer prompting framework for the autonomous agent era. Based on the insight that "prompting" has diverged into four cumulative disciplines operating at different altitudes and time horizons.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running WORKFLOWNAME in PromptingStack"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **PromptingStack** skill to ACTION...
   ```

**Full documentation:** `.claude/PAI/THENOTIFICATIONSYSTEM.md`

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Assess** | "assess my prompting", "where am I", "prompting gaps" | `Workflows/Assess.md` |
| **PromptCraft** | "improve my prompt", "prompt craft", "better prompt" | `Workflows/PromptCraft.md` |
| **ContextEngineering** | "build my context", "context engineering", "context layer" | `Workflows/ContextEngineering.md` |
| **IntentEngineering** | "encode intent", "intent engineering", "decision frameworks" | `Workflows/IntentEngineering.md` |
| **SpecificationEngineering** | "write a spec", "specification engineering", "write specification" | `Workflows/SpecificationEngineering.md` |
| **Skillify** | "specify this task", "turn this into a spec", "make this agent-executable" | `Workflows/Skillify.md` |

## Examples

**Example 1: Assessment**
```
User: "Assess my prompting skills"
-> Invokes Assess workflow
-> Walks through diagnostic questions for each of the 4 layers
-> Produces gap analysis with recommended next steps
```

**Example 2: Write a specification**
```
User: "Write a spec for migrating our auth system to OAuth"
-> Invokes SpecificationEngineering workflow
-> Applies 5 primitives: self-contained problem statement, acceptance criteria,
   constraint architecture, decomposition, evaluation design
-> Produces agent-executable specification document
```

**Example 3: Specify a task**
```
User: "Specify this task: redesign our onboarding flow"
-> Invokes Skillify workflow
-> Interviews for context, then runs through all 5 primitives
-> Outputs a structured spec ready for autonomous agent execution
```

## Quick Reference

**The 4 Disciplines (cumulative stack):**
1. **Prompt Craft** — synchronous, session-based instruction writing (table stakes)
2. **Context Engineering** — curating the full token environment
3. **Intent Engineering** — encoding purpose, goals, trade-off hierarchies
4. **Specification Engineering** — agent-executable documents for long-running autonomous work

**The 5 Specification Primitives:**
1. Self-contained problem statements
2. Acceptance criteria
3. Constraint architecture (musts, must-nots, preferences, escalation triggers)
4. Decomposition
5. Evaluation design

**Full Framework:** See `Framework.md` for the complete reference.
