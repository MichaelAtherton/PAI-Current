# PromptingFramework Reference

Complete reference for the 4-discipline cumulative prompting stack.

Source: Nate Hager — "'Prompting' Just Split Into 4 Skills" (Feb 2026)
Video: https://www.youtube.com/watch?v=BpibZSMGtdY

---

## The Core Insight

"Prompting" now hides four completely different skill sets. Most people practice only one (Prompt Craft). The gap between people who see all four and those who don't is 10x and widening.

These disciplines are **cumulative** — each layer is a prerequisite for the layers above it:
- You cannot write good context documents if you can't write good prompts
- You cannot encode intent without context infrastructure to carry it
- You cannot write agent-executable specs without intent to resolve ambiguity at the edges

---

## Layer 1: Prompt Craft

**Altitude:** Individual | **Time Horizon:** Synchronous session | **Status:** Table stakes

The original skill. Synchronous, session-based, individual.

**Core competencies:**
- Clear instructions
- Relevant examples and counter-examples
- Appropriate guardrails
- Explicit output format
- Ambiguity and conflict resolution

**Ceiling:** This skill breaks the moment agents run for hours without checking in. In synchronous prompting, YOU are the intent layer, context layer, and quality layer. With autonomous agents, all of that must be encoded before the agent starts.

**Why the next layer needs this one:** Every context document IS a prompt — system prompts, claude.md files, tool definitions, memory schemas. Bad prompt craft = bad context documents = bad context engineering.

---

## Layer 2: Context Engineering

**Altitude:** Project/Team | **Time Horizon:** Session setup | **Status:** Where industry attention is focused

The shift from crafting a single instruction to curating the entire information environment an agent operates within.

**Scope:** System prompts, tool definitions, retrieved documents, message history, memory systems, MCP connections, claude.md files, RAG pipeline design, memory architectures.

**Key insight (Anthropic):** LLMs degrade as you give them more information. Include RELEVANT tokens — retrieval quality drops as context grows.

**The math:** Your 200-token prompt is 0.02% of what the model sees in a million-token context window. The other 99.98% is context engineering.

**10x practitioners:** Don't write 10x better prompts. They build 10x better context infrastructure. Their agents start each session with the right project files, conventions, and constraints already loaded.

**Ceiling:** You can have a perfectly informed agent that optimizes for the wrong thing. Klarna had perfect context — knew everything about customers and processes — but optimized for resolution speed instead of satisfaction. Context tells agents what to KNOW. It doesn't tell them what to WANT.

**Why the next layer needs this one:** Intent without context is useless. You can't encode "prefer customer satisfaction over resolution speed" if the agent has no access to satisfaction metrics, escalation paths, or customer history. Intent rides ON context.

---

## Layer 3: Intent Engineering

**Altitude:** Organization | **Time Horizon:** Persistent infrastructure | **Status:** Emerging discipline

Encoding organizational purpose, goals, values, trade-off hierarchies, and decision boundaries into infrastructure that agents can act against.

**Relationship:** Context engineering tells agents what to KNOW. Intent engineering tells agents what to WANT.

**Proof case — Klarna:** AI agent resolved 2.3M customer conversations in month one. Optimized for resolution time, not customer satisfaction. Had to rehire human agents. Perfect context, terrible intent alignment.

**Stakes escalation:** Screwing up a prompt wastes your morning. Screwing up intent engineering screws up your entire team/org/company.

**Ceiling:** Intent engineering works for bounded tasks and monitored sessions. But when agents run for days/weeks producing complex multi-phase outputs, intent alone isn't enough. The entire problem domain must be specified so completely that an autonomous system can execute without checking in.

**Why the next layer needs this one:** A specification without encoded intent produces the Anthropic Opus 4.5 problem — technically correct but architecturally incoherent output. Intent provides the tie-breaking rules that specs rely on at ambiguous edges.

---

## Layer 4: Specification Engineering

**Altitude:** Enterprise | **Time Horizon:** Days to weeks of autonomous execution | **Status:** Emerging

Writing documents across your organization that autonomous agents can execute against over extended time horizons without human intervention.

**Key shift:** Not about a single agent's context window. Not about intent alone. It's about thinking of your entire informational corpus as agent-fungible, agent-readable.

**Proof case — Anthropic + Opus 4.5:** "Build a clone of claude.ai" → agent tried too much at once, ran out of context, left next session guessing. Fix was specification engineering: laser agent sets up environment, progress log documents what's been done, coding agent makes incremental progress against a structured plan.

**Fractal nature:** Applies at individual agent task level AND org document corpus level. Corporate strategy, OKRs, product specs — everything becomes a specification agents can use.

**No ceiling — this is the top of the stack.**

---

## The 5 Specification Primitives

### 1. Self-Contained Problem Statements
Can you state a problem with enough context that the task is plausibly solvable without the agent going out for more information?

**Training:** Rewrite "update the dashboard to show Q3 numbers" as if the recipient has never seen your dashboard, doesn't know what Q3 means in your org, and has zero access beyond what you include.

### 2. Acceptance Criteria
If you can't describe what "done" looks like, an agent can't know when to stop.

**Training:** For every delegated task, write three sentences an independent observer could use to verify the output without asking you any questions.

### 3. Constraint Architecture
Four categories: **Musts** (non-negotiable), **Must-nots** (forbidden), **Preferences** (tie-breakers), **Escalation triggers** (stop and ask).

**Training:** Write down what a smart, well-intentioned person might do that technically satisfies the request but produces the wrong outcome. Those failure modes become your constraints.

### 4. Decomposition
Subtasks that each take < 2 hours, have clear I/O boundaries, and can be verified independently.

**2026 evolution:** You don't write all subtasks — you provide BREAK PATTERNS that a planner agent uses to decompose work reliably.

### 5. Evaluation Design
How do you KNOW the output is good? Not "looks reasonable" but "provably, measurably, consistently good."

**Training:** For every recurring AI task, build 3-5 test cases with known-good outputs. Run them after model updates.

---

## The Human Dimension

The best human managers already operate with this clarity. AI is enforcing a communication discipline that the best leaders practiced intuitively.

Toby Lutke (Shopify CEO): "A lot of what people in big companies call politics is actually bad context engineering for humans." Specification engineering surfaces implicit assumptions that play out as politics.

Getting better at this stack makes you better at communicating with humans too. Your emails get tighter, your memos get better, your decision frameworks get stronger.
