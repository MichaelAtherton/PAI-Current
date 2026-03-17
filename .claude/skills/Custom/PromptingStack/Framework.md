# PromptingStack Framework Reference

Complete reference for the 4-discipline prompting stack and 5 specification primitives.

Source: Nate Hager — "'Prompting' Just Split Into 4 Skills" (Feb 2026)
Video: https://www.youtube.com/watch?v=BpibZSMGtdY

---

## The Core Insight

"Prompting" now hides four completely different skill sets. Most people practice only one (Prompt Craft). The gap between people who see all four and those who don't is 10x and widening.

These disciplines are **cumulative** — each layer makes the layers above it possible. You cannot write good specs if you can't write good prompts. You can't build effective agent systems without understanding context engineering. You can't align agent behavior with organizational goals without intent engineering.

---

## The 4 Disciplines

### Layer 1: Prompt Craft
**Altitude:** Individual | **Time Horizon:** Synchronous session | **Status:** Table stakes

The original skill. Synchronous, session-based, individual.

**Core competencies:**
- Clear instructions
- Relevant examples and counter-examples
- Appropriate guardrails
- Explicit output format
- Ambiguity and conflict resolution

**Analogy:** Knowing how to type was once a differentiator. Now it's assumed. Prompt craft is the same — necessary but not differentiating.

**Ceiling:** This skill breaks the moment agents run for hours without checking in. In synchronous prompting, YOU are the intent layer, context layer, and quality layer. With autonomous agents, all of that must be encoded before the agent starts.

---

### Layer 2: Context Engineering
**Altitude:** Project/Team | **Time Horizon:** Session setup | **Status:** Where industry attention is focused

The shift from crafting a single instruction to curating the entire information environment an agent operates within.

**Scope:** System prompts, tool definitions, retrieved documents, message history, memory systems, MCP connections, claude.md files, RAG pipeline design, memory architectures.

**Key insight (Anthropic):** LLMs degrade as you give them more information. Include RELEVANT tokens — retrieval quality drops as context grows.

**The math:** Your 200-token prompt is 0.02% of what the model sees in a million-token context window. The other 99.98% is context engineering.

**What 10x practitioners do differently:** They don't write 10x better prompts. They build 10x better context infrastructure. Their agents start each session with the right project files, conventions, and constraints already loaded.

---

### Layer 3: Intent Engineering
**Altitude:** Organization | **Time Horizon:** Persistent infrastructure | **Status:** Emerging discipline

Encoding organizational purpose, goals, values, trade-off hierarchies, and decision boundaries into infrastructure that agents can act against.

**Relationship to context:** Context engineering tells agents what to KNOW. Intent engineering tells agents what to WANT.

**Proof case — Klarna:** AI agent resolved 2.3M customer conversations in month one. Optimized for resolution time, not customer satisfaction. Had to rehire human agents. Perfect context, terrible intent alignment.

**Critical property:** You can have perfect context and terrible intent alignment. You CANNOT have good intent alignment without good context.

**Stakes escalation:** Screwing up a prompt wastes your morning. Screwing up intent engineering screws up your entire team/org/company.

---

### Layer 4: Specification Engineering
**Altitude:** Enterprise | **Time Horizon:** Days to weeks of autonomous execution | **Status:** Emerging, best practitioners already doing it

Writing documents across your organization that autonomous agents can execute against over extended time horizons without human intervention.

**Key shift:** Not about an individual agent's context window. Not about the intent you've given agents. It's about thinking of your entire informational corpus as agent-fungible, agent-readable.

**Proof case — Anthropic + Opus 4.5:** "Build a clone of claude.ai" → agent tried too much at once, ran out of context, left next session guessing. Fix was NOT a better model — it was specification engineering: a laser agent sets up environment, a progress log documents what's been done, a coding agent makes incremental progress against a structured plan.

**The analogy:** When building small → verbal instructions work. When building large → you need blueprints. Specifications ARE blueprints for autonomous agents.

**Fractal nature:** Applies at individual agent task level AND at org document corpus level. Your corporate strategy is a specification. Your OKRs are specifications. Everything becomes a specification agents can use.

---

## The 5 Specification Primitives

### Primitive 1: Self-Contained Problem Statements
Can you state a problem with enough context that the task is plausibly solvable without the agent going out for more information?

**Training exercise:** Take a conversational request like "update the dashboard to show Q3 numbers" and rewrite it as if the recipient has never seen your dashboard, doesn't know what Q3 means in your org, doesn't know which database to query, and has no access to any information other than what you include.

**Why it matters:** AI doesn't fill gaps reliably. It fills them with statistical plausibility — a polite way of saying it guesses in ways that are often subtly wrong.

---

### Primitive 2: Acceptance Criteria
If you can't describe what "done" looks like, an agent can't know when to stop.

**The 80% problem:** "Build a login page" vs "Build a login page that handles email/password, social OAuth via Google and GitHub, progressive disclosure of 2FA, session persistence for 30 days, and rate limiting after 5 failed attempts."

**Training exercise:** For every task you delegate, write three sentences that an independent observer could use to verify the output without asking you any questions. If you can't write those sentences, you don't understand the task well enough to delegate it.

---

### Primitive 3: Constraint Architecture
Four categories that turn a loose specification into a reliable one:

| Category | Description |
|----------|-------------|
| **Musts** | What the agent has to do |
| **Must-nots** | What the agent cannot do |
| **Preferences** | What the agent should prefer when multiple valid approaches exist |
| **Escalation triggers** | What the agent should escalate rather than decide autonomously |

**Training exercise:** Before delegating a task, write down what a smart, well-intentioned person might do that would technically satisfy the request but produce the wrong outcome. Those failure modes become your constraint architecture.

**Real-world example:** The claude.md pattern — concise, high-signal constraint documents. "Use these build commands. Follow these conventions. Run these tests. Never modify these files." Every line must earn its place.

---

### Primitive 4: Decomposition
Large tasks broken into components that can be executed independently, tested independently, and integrated predictably.

**The granularity rule:** Decompose into subtasks that each take less than 2 hours, have clear input/output boundaries, and can be verified independently.

**2026 evolution:** You don't manually write all subtasks. You provide the BREAK PATTERNS that a planner agent can use to decompose larger work reliably. Your job is describing what done looks like and what decomposable pieces look like so the planner can break work into 50-60 subtasks.

---

### Primitive 5: Evaluation Design
How do you KNOW the output is good? Not "does it look reasonable" but "can you prove measurably, consistently, that this is good?"

**Training exercise:** For every recurring AI task, build 3-5 test cases with known good outputs and run them periodically (especially after model updates).

**What it catches:** Regressions, builds intuition for model failure modes, creates institutional knowledge about what "good" looks like for your specific use cases.

---

## The Human Dimension

The best human managers already operate with this clarity: complete context when delegating, specified acceptance criteria, articulated constraints. AI is enforcing a communication discipline that the best leaders practiced intuitively.

Toby Lutke (Shopify CEO) insight: "A lot of what people in big companies call politics is actually bad context engineering for humans." Specification engineering surfaces implicit assumptions that play out as politics and grudges.

---

## Progression Path

1. **Close the prompt craft gap** — reread documentation, do interactive tutorials, build a folder of recurring tasks with baseline prompts
2. **Build your personal context layer** — write a claude.md equivalent for your work (goals, constraints, communication preferences, quality standards, institutional context)
3. **Get into specification engineering** — take a real project, write a full spec before touching AI
4. **Build intent infrastructure** — encode decision frameworks, define "good enough" for each category of work, write down what gets escalated vs decided by AI
