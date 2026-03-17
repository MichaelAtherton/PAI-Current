# ContextEngineering Workflow

**Layer 2 of 4** — Curate the full token environment. The 99.98% that isn't your prompt.

**Depends on:** Layer 1 artifact (`Artifacts/prompt-library.md`). Your best prompts and templates become the raw material for persistent context documents. Every context doc IS a prompt — if you can't write clear instructions (L1), your context docs will be unclear too.

**Artifact produced:** `Artifacts/context-architecture.md` — a map of what loads when, what earns its place, and what needs to be built. This becomes the structure that intent gets encoded into.

**Artifact path:** Read from `Artifacts/prompt-library.md`, write to `Artifacts/context-architecture.md`.

## Step 1: Inventory What Exists

Don't ask abstract questions. Look at what's actually there:

1. **Read their claude.md** (or equivalent) — does it exist? How many lines? When was it last updated?
2. **Check for system prompts** — any persistent instruction files?
3. **Check for tool definitions** — what tools are configured? Are descriptions accurate?
4. **Check for memory/RAG** — any document retrieval or persistent memory?
5. **Check for MCP connections** — any external integrations?

Produce a raw inventory:

| Layer | Exists? | Size | Last Updated | Quality |
|-------|---------|------|-------------|---------|
| claude.md / system prompt | Y/N | [lines] | [date] | [1-3] |
| Project conventions | Y/N | [lines] | [date] | [1-3] |
| Tool definitions | Y/N | [count] | [date] | [1-3] |
| Document retrieval | Y/N | [docs] | [date] | [1-3] |
| Memory system | Y/N | [type] | [date] | [1-3] |
| MCP connections | Y/N | [count] | [date] | [1-3] |

## Step 2: Audit for Relevance

For every existing context item, apply the test: **"If I removed this line, would the agent make worse decisions?"**

- **Yes → keep.** It earns its place.
- **No → cut.** It's diluting retrieval quality.
- **Maybe → flag.** Move it to on-demand loading.

LLMs degrade with more tokens. Inclusion has a cost. The audit should produce a kill list and a keep list.

## Step 3: Pull From the Prompt Library

Open `Artifacts/prompt-library.md` (Layer 1 artifact). Identify:

- **Recurring instructions** that appear across multiple prompts → these should be in the system prompt, not repeated every time
- **Quality standards** that you enforce manually every session → encode as persistent context
- **Guardrails** you always include → move to always-loaded context
- **Output formats** you reuse → standardize as context-level defaults

This is the concrete connection: Layer 1 patterns graduate into Layer 2 infrastructure.

## Step 4: Design the Architecture

```markdown
# Context Architecture

## Always-Loaded (system prompt / claude.md)
Every line here was tested: removing it causes measurably worse output.
- [Item: WHY it earns its place — what breaks without it]
- [Item: WHY it earns its place]

## On-Demand (loaded by workflows/triggers)
- [Item: WHEN it loads, WHAT triggers it, WHY not always-on]
- [Item: WHEN it loads, WHAT triggers it]

## To Build (gaps identified in audit)
- [Gap: what to create, where it lives, what problem it solves]
- [Gap: what to create, where it lives]

## To Cut (bloat identified in audit)
- [Item: WHY it's being removed — what cost does it impose?]

## Graduated from Prompt Library
- [Pattern from L1 → now persistent in context as: X]
```

## Step 5: Build the Highest-Impact Gap

Don't try to build everything. Pick the single highest-impact gap and build it now:

1. Write or rewrite the document
2. Apply every line of the prompt craft discipline from Layer 1 — clear instructions, examples, guardrails, format, ambiguity handling
3. Place it in the right location (always-loaded vs on-demand)
4. Test: start a new session, run a task, compare output quality before/after

## → Next Layer

Your agent now has the right information. But information doesn't tell it what to prioritize. When speed conflicts with quality, which wins? When cost conflicts with coverage, what's the trade-off? That's not in your context — and your agent is guessing.

The next layer encodes intent INTO the context architecture you just built. You'll open `context-architecture.md` and add a layer of purpose to it.

**When ready:** → IntentEngineering workflow. Bring your context architecture.
