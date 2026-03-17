# ContextEngineering Workflow

Help the user build or audit their context infrastructure — the 99.98% of the context window that isn't their prompt.

## Step 1: Assess Current Context Infrastructure

Ask the user about their current setup:
- Do they use claude.md / system prompt files? Where?
- Do they have RAG or document retrieval pipelines?
- Do they use MCP connections?
- Do they have memory systems (persistent context across sessions)?
- What tools/tool definitions are configured?
- How do they load project context at session start?

## Step 2: Identify Context Gaps

Based on their answers, identify what's missing from their token environment:

| Context Layer | Status | Gap |
|---------------|--------|-----|
| **System prompts / claude.md** | [exists/missing/weak] | [specific gap] |
| **Project conventions** | [exists/missing/weak] | [specific gap] |
| **Tool definitions** | [exists/missing/weak] | [specific gap] |
| **Retrieved documents (RAG)** | [exists/missing/weak] | [specific gap] |
| **Message history management** | [exists/missing/weak] | [specific gap] |
| **Memory systems** | [exists/missing/weak] | [specific gap] |
| **MCP connections** | [exists/missing/weak] | [specific gap] |

## Step 3: Apply the Relevance Principle

Key insight from Anthropic: LLMs degrade as you give them MORE information. The goal is not maximum context — it's maximum RELEVANT context.

For each existing context source, evaluate:
- Is this information actually used by the agent?
- Does including it improve output quality measurably?
- Could this be loaded on-demand instead of always-on?
- Is there redundant or contradictory information?

## Step 4: Design the Context Architecture

Based on the assessment, produce a context engineering plan:

```markdown
## Context Engineering Plan

### Always-Loaded Context (system prompt / claude.md)
- [Item 1: why it earns its place]
- [Item 2: why it earns its place]

### On-Demand Context (loaded by workflows/tools)
- [Item 1: when to load, what triggers it]
- [Item 2: when to load, what triggers it]

### Context to Build
- [Gap 1: what to create, where to put it]
- [Gap 2: what to create, where to put it]

### Context to Remove/Compress
- [Bloat 1: what to cut, why]
- [Bloat 2: what to cut, why]
```

## Step 5: Build or Improve

If the user wants to proceed, help them:
1. Write or improve their claude.md / system prompt
2. Set up project convention files
3. Configure tool definitions
4. Design memory/retrieval architecture
5. Set up MCP connections if applicable

Focus on the highest-impact gap first. Each context document should follow the principle: **every line must earn its place.**

## Output Format

```markdown
## Context Engineering Audit

### Current State
[Summary of what exists]

### Key Gaps
1. [Most impactful gap]
2. [Second gap]
3. [Third gap]

### Recommended Architecture
[The plan from Step 4]

### First Action
[The single most impactful thing to do right now]
```
