# Assess Workflow

Diagnose the user's current prompting capabilities across all 4 disciplines and produce a gap analysis with actionable next steps.

## Step 1: Load Framework

Read `Framework.md` from the skill root for the full reference.

## Step 2: Diagnostic Interview

Walk through each discipline with targeted questions. Ask 2-3 questions per layer, adapting based on answers.

### Layer 1: Prompt Craft
- "When you write a prompt, do you routinely include examples, counter-examples, and explicit output format?"
- "Do you have a library of reusable prompt templates for recurring tasks?"
- "When output is wrong, can you quickly identify whether the issue was unclear instructions, missing context, or wrong framing?"

### Layer 2: Context Engineering
- "Do you use claude.md files, system prompts, or other persistent context documents?"
- "Have you built or configured RAG pipelines, memory systems, or MCP connections for your work?"
- "When starting a new AI session, what context do you load? Is it automated or manual?"

### Layer 3: Intent Engineering
- "Have you documented your decision frameworks — what 'good enough' looks like for different categories of work?"
- "Do your AI systems know when to escalate vs. decide autonomously?"
- "Have you encoded organizational goals, trade-off hierarchies, or values into agent infrastructure?"

### Layer 4: Specification Engineering
- "Have you written a complete specification that an agent executed autonomously for hours/days?"
- "Do your organizational documents function as agent-readable specifications?"
- "Can you decompose a week-long project into independently executable, verifiable 2-hour subtasks?"

## Step 3: Score Each Layer

Rate each layer on a 4-point scale:

| Level | Description |
|-------|-------------|
| **0 — Unaware** | Doesn't know this discipline exists |
| **1 — Aware** | Understands the concept but hasn't practiced it |
| **2 — Practicing** | Has done it a few times, building the skill |
| **3 — Proficient** | Does this consistently and well |

## Step 4: Gap Analysis

Produce a structured output:

```markdown
## Prompting Stack Assessment

### Scores
| Discipline | Score | Status |
|------------|-------|--------|
| Prompt Craft | X/3 | [status] |
| Context Engineering | X/3 | [status] |
| Intent Engineering | X/3 | [status] |
| Specification Engineering | X/3 | [status] |

### Primary Gap
[The lowest-scoring or most impactful gap]

### Recommended Next Steps
1. [Specific action for the primary gap]
2. [Second priority action]
3. [Third priority action]

### Your Biggest Leverage Point
[Which improvement would produce the largest 10x-style gap closure based on their current work]
```

## Step 5: Recommend Workflow

Based on the assessment, recommend which PromptingStack workflow to run next. Map directly:
- Low Prompt Craft → **PromptCraft** workflow
- Low Context Engineering → **ContextEngineering** workflow
- Low Intent Engineering → **IntentEngineering** workflow
- Low Specification Engineering → **SpecificationEngineering** workflow
- Practical application needed → **Skillify** workflow
