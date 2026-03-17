# Gastown Analysis: Architecture, Connections, and Divergences from PAI
*Analysis date: 2026-03-13 | Gastown version: main branch (last push 2026-03-14)*

---

## Who is Steve Yegge?

Steve Yegge is a legendary software engineer and blogger — Amazon (early 2000s, where he witnessed Bezos's famous SOA mandate), Google (10+ years), Sourcegraph (Head of Engineering working on Cody AI assistant), Grab. He is best known not for shipping products but for writing extraordinarily long, opinionated essays that shape how the industry thinks.

**Famous essays:** "Execution in the Kingdom of Nouns" (2006, Java satire), "The Google Platforms Rant" (2011, accidentally published publicly — argued Google builds great products but fails catastrophically at platforms because it never internalized the lesson of Bezos's SOA mandate at Amazon, which is what eventually produced AWS). He also wrote "Rich Programmer Food" (you need to understand compilers), "Universal Design Pattern" (properties pattern as first-class design), and co-authored the "Vibe Coding" book with Gene Kim (2025).

He built **Wyvern**, an MMORPG he worked on for ~20 years, launched on iOS in 2016.

His recent work is a trilogy of AI infrastructure tools, built bottom-up:
- **Efrit** — Native elisp coding agent running inside Emacs (146 HN points)
- **Beads** — Distributed git-backed issue tracker optimized for AI agents (~19,000 GitHub stars)
- **Gastown** — Multi-agent workspace orchestration layer (12,040 GitHub stars, "Welcome to Gas Town" essay: 354 HN points / 224 comments)

**His "Eight Levels of AI Coder Evolution" framework** (O'Reilly Radar, March 2026): Level 1-4 = using AI inside existing IDEs. Level 5 = the threshold where you stop opening your IDE entirely and manage agents. Levels 6-8 = managing increasingly large agent fleets. His famous line: *"Code is a liquid. You spray it through hoses. You don't freaking look at it."* Gastown is the infrastructure for people at Level 5+.

**The "AI Vampire" warning** (108 HN points): He acknowledges intensive multi-agent work creates profound psychological exhaustion ("Dracula effect") — he naps daily and has expressed regret about setting unrealistic standards for engineers without his 40 years of experience and unlimited token budget.

**The Wasteland vision** (March 2026, 68 HN points): Long-term, thousands of Gas Towns federated via DoltHub — a distributed reputation and work-claiming ecosystem. Your rig identity and work history are portable across wastelands. This is the explicit philosophical opposite of centralized SaaS AI tools.

**"Gooey Blob" note:** No essay by this title found in any archive. Likely a misremembered title — closest thematic match is "Kingdom of Nouns" (2006) or possibly an unpublished/private piece.

He is building bottom-up: memory/issue tracking → workspace coordination → orchestration. **These are the same layers PAI addresses**, built by someone arriving from the infrastructure side rather than the prompt/configuration side.

---

## Part 1: What Is Gastown?

### The Problem It Solves

Gastown's founding insight is blunt and correct: **AI agents lose context when they restart, and 4-10 parallel agents become chaos without a coordination layer.** The larger truth underneath: current AI coding tools (Claude Code, Codex, Cursor) are designed as single-agent tools. Running them at scale requires infrastructure that doesn't exist natively.

| Challenge | Gastown's Solution |
|---|---|
| Agents lose context on restart | Work persists in git-backed hooks (worktrees) |
| Manual agent coordination | Built-in mailboxes, identities, handoffs |
| 4-10 agents become chaotic | Scale comfortably to 20-30 agents |
| Work state lost in agent memory | Work state stored in Beads ledger (Dolt DB) |

### Three Core Operating Principles

The Gastown glossary (contributed by Clay Shirky) names three foundational operating principles that govern everything:

**GUPP (Gas Town Universal Propulsion Principle):** *"If there is work on your Hook, YOU MUST RUN IT."* No confirmation, no waiting, no announcements. The hook having work IS the assignment. This is physics, not politeness. "Gas Town is a steam engine — you are a piston." The failure mode GUPP prevents: an agent restarts, finds work on its hook, announces itself and waits for human confirmation, human is AFK trusting the engine to run, work sits idle, the whole system stalls.

**MEOW (Molecular Expression of Work / Mayor-Enhanced Orchestration Workflow):** Used in two senses — (1) in the glossary, MEOW = breaking large goals into detailed instructions for agents, supported by Beads/Epics/Formulas/Molecules; (2) in the README, MEOW = the recommended 7-step top-level workflow pattern (tell Mayor → Mayor analyzes → convoy creation → agent spawning → work distribution → progress monitoring → completion). Both senses are consistent: MEOW is the principle that work must be decomposed into trackable, atomic units before agents touch it.

**NDI (Nondeterministic Idempotence):** The overarching goal — ensuring useful outcomes through orchestration of potentially unreliable processes. The key insight: individual AI agent operations *will* fail or produce varying results. NDI says the system must be designed so eventual workflow completion is guaranteed anyway, through persistence (Beads), oversight (Witness, Deacon), and retryability. You don't fix non-determinism by making AI more deterministic; you make the infrastructure idempotent so failures are recoverable.

These three principles together form Gastown's operating philosophy: decompose work atomically (MEOW), execute immediately without ceremony (GUPP), design for failure recovery not for perfection (NDI).

### Core Architecture: The Vocabulary

Gastown introduces a rich domain vocabulary. Each term is load-bearing:

**Town** — the workspace directory (`~/gt/`). The root of everything. Analogous to PAI's `~/.claude/` as the root config directory — except Gastown's Town is much more explicit as a named concept with its own lifecycle.

**Rig** — a project container. Each rig wraps a git repository and its associated agents. You can have multiple rigs in a Town. A rig is roughly "one codebase being worked on by multiple agents." There's no PAI equivalent at this granularity.

**Mayor** — the primary AI coordinator. A special Claude Code instance with full workspace context. You talk to the Mayor, and it orchestrates everything else. The Mayor is *not* a human — it's an AI with a special elevated role. Closest PAI analog: the main Claude Code session running the Algorithm, but the Mayor is explicitly designed to *stay running* and coordinate across multiple sub-sessions.

**Crew Member** — your personal workspace within a rig. Where the human (you) does hands-on work. Explicit role distinction between you-the-human and the agents.

**Polecats** — worker agents with **persistent identity but ephemeral sessions**. This is the key design tension: a polecat has a name, history, and accumulated work context, but its actual session ends when work completes. The identity persists; the process doesn't. This is how Gastown solves the context-loss problem — not by keeping sessions alive, but by making *identity* and *work state* independent from *sessions*.

**Hooks** (Gastown definition) — git worktree-based persistent storage. **Critical naming collision:** Gastown's "hooks" are NOT the same as Claude Code's hooks (event callbacks). Gastown hooks are git worktrees attached to an agent's working context. They store work state, survive crashes/restarts, and are tracked via version control. They are the persistence mechanism, not an event system.

**Convoys** — work tracking units. A convoy bundles multiple Beads (issues/tasks) assigned to agents. When all issues in a convoy close, the convoy "lands" and notifies you. Convoys are how you track "is this batch of work done?" across multiple agents on multiple rigs.

**Beads** — the underlying work items. Git-backed, stored in a Dolt database (version-controlled SQL with cell-level merging). Each bead has a collision-resistant hash-based ID (e.g., `gt-abc12`). Beads are the atomic unit of assignable work. The term "bead" and "issue" are used interchangeably.

**MEOW (Mayor-Enhanced Orchestration Workflow)** — the recommended top-level pattern:
1. Tell the Mayor what you want
2. Mayor analyzes and breaks it into tasks
3. Mayor creates a convoy with beads
4. Mayor spawns polecats
5. Beads get slung to polecats
6. Progress tracked through convoy status
7. Mayor summarizes results when convoy lands

This is explicitly Gastown's version of a structured task execution workflow. More on this comparison below.

### The Hook Lifecycle (Gastown's Persistence Model)

```
[*] → Created (agent spawned)
    → Active (work assigned via git worktree)
    → Suspended (agent paused)
    → Active (resumed)
    → Completed (work done)
    → Archived
```

When an agent session crashes or ends, the work state is already committed to the git worktree. The *next* agent that picks up the work reads from that worktree — no state lost. This is the "propulsion principle": hooks act as engines that drive forward even through interruption.

### The Hooks Management System

Gastown has a sophisticated hooks management CLI (`gt hooks`) that:
- Maintains a **base config** (shared across all targets)
- Maintains **per-role overrides** (crew vs. polecat vs. witness)
- Syncs hooks across all workspace targets automatically
- Has a **registry** of installable hooks (catalog vs. source-of-truth separation)
- Validates sync status via `gt doctor`

Key registry hooks:
| Hook | Event | Roles |
|---|---|---|
| pr-workflow-guard | PreToolUse | crew, polecat |
| session-prime | SessionStart | all |
| pre-compact-prime | PreCompact | all |
| mail-check | UserPromptSubmit | all |
| costs-record | Stop | crew, polecat |

The `session-prime` hook runs `gt prime` on every session start — reloading the agent's role context, identity, and pending work. The `pre-compact-prime` hook does the same before context compaction. **This is Gastown's solution to the "lost context" problem at the Claude Code level.**

### Formula System (Beads Recipes)

Beads includes a formula system: TOML-defined workflows for repeatable processes. Example:
```toml
[[steps]]
id = "bump-version"
title = "Bump version"
description = "Run ./scripts/bump-version.sh {{version}}"

[[steps]]
id = "run-tests"
needs = ["bump-version"]  # dependency graph
```

Formulas support:
- Variable injection (`{{version}}`)
- Step dependencies (DAG execution)
- Trackable molecule instances (`bd mol pour release --var version=1.2.0`)

This is analogous to PAI's pipeline/flow system.

### Identity and Mail System

Each polecat has:
- A persistent identity (name, role, rig assignment)
- A mailbox (persists across session restarts)
- Context recovery via `gt prime` on session start

Communication patterns:
- **`gt mail send`** — sends message to agent mailbox (persists across restarts)
- **`gt nudge`** — immediate notification to wake a sleeping agent
- **`gt handoff`** — structured context transfer when agents change assignment

This solves a real problem: how do you give a new agent session the context accumulated by a previous agent session? Gastown answers: via structured mailbox + identity system, not by keeping the same session alive.

### The Wasteland: Federated Gas Towns

The most ambitious — and least-known — part of Gastown's vision. The Wasteland (`gt wl` commands) is a federated work-coordination network linking independent Gas Towns via DoltHub. Each Gas Town is a "rig" in the Wasteland. Rigs post work to a shared "wanted board," claim tasks, submit completions with evidence URLs, and earn multi-dimensional reputation stamps.

Key design principles:
- **Portable identity:** Your rig handle, work history, and reputation stamps are yours — not owned by any platform
- **Yearbook rule:** You cannot stamp your own work (enforced at the DB schema level)
- **Trust levels (planned, not yet enforced):** Registered → Participant → Contributor → Maintainer
- **Phase 1 is "wild-west mode":** All claims write locally only; conflict resolution happens when DoltHub forks are reconciled

The Wasteland is currently early-stage (Phase 1, `gt wl join`, `gt wl browse`, `gt wl claim`, `gt wl done`), but represents Yegge's long-term vision: *"A Thousand Gas Towns"* — thousands of independently operated personal AI infrastructures linked into a reputation network where work is the only input and reputation is the only output.

**This is philosophically significant for the PAI comparison:** Yegge's vision of personal ownership + federated reputation is the exact opposite of SaaS AI tools. It's closer to the original internet ethos of distributed ownership, where your infrastructure is yours and interoperability is via protocols, not platforms.

### HN Community Reception: Critical Signals

The major HN thread (354 points, 224 comments) surfaced consistent critiques worth noting:

- **Naming complexity:** The Mad Max vocabulary (Mayor, Deacon, Witness, Refinery, Polecat) was widely criticized for obfuscating rather than clarifying. One developer had Claude rename everything to "idiomatic distributed systems naming."
- **Cost barrier:** Multiple commenters questioned the economics of running 20-30 simultaneous agents. Yegge is assumed to have FAANG-tenure "FU money."
- **The "human review bottleneck":** A Stage 7 developer argued the real constraint isn't agent throughput but human review speed and accountability. More agents don't help if review becomes the bottleneck.
- **Self-referential concern:** *"AFAICT it has eaten its own tail"* — questioning whether Gastown has produced anything beyond itself.
- **Beads complexity:** Described as "225k lines of Go for basic task tracking."
- **Comparison to J2EE:** "The complexity of J2EE combined with AI-fueled solipsism."
- **Kent Beck contrast:** His view that LLMs excel in early exploration but lose value after initial concept validation — contrasting with Yegge's "let it rip" philosophy.

These are fair critiques. Gastown is high-complexity, high-cost, and optimized for a user profile (Level 5+ engineer with unlimited compute budget) that represents a small fraction of developers.

---

## Part 2: Connections Between Gastown and PAI

These are **convergent independent discoveries** — two people (Yegge from infrastructure-up, Michael from prompt-layer-down) independently arriving at the same categories of solution to the same underlying problem.

### Connection 1: Hooks as the Central Injection Mechanism

**PAI** uses Claude Code's hook system (SessionStart, UserPromptSubmit, Stop, PreToolUse) to inject context, run validation, capture state, and notify. Hooks fire automatically at lifecycle events and are the backbone of PAI's "always loaded" context.

**Gastown** uses hooks in two senses: (a) Claude Code's native hooks (same event system), and (b) its own "hooks" concept (git worktrees for state persistence). But critically, Gastown's *approach* to the Claude Code hooks is identical to PAI's: `session-prime` on SessionStart loads all context; `mail-check` on UserPromptSubmit injects pending work; `costs-record` on Stop captures usage data.

Both independently concluded: **hooks are the right injection point for making AI agents contextually aware without polluting the conversation with setup boilerplate.**

### Connection 2: Memory/Persistence as a First-Class Concern

**PAI** has an entire MEMORY/ system — RAW/ (event logs), WORK/ (PRDs, criteria), LEARNING/ (algorithm reflections, ratings), STATE/ (current session state, work registry). PAI treats memory as infrastructure, not an afterthought.

**Gastown** treats persistence identically, but at the infrastructure layer: Beads (git-backed Dolt DB) stores all work items with full history; git worktrees preserve agent work state across restarts; convoy tracking preserves cross-agent work relationships; mail system preserves communication across session boundaries.

Both share the same founding insight: **without persistent memory, AI agents are goldfish — capable but amnesiac. Memory is what makes intelligence compound.**

### Connection 3: Structured Workflow as Quality Gate

**PAI** has The Algorithm (Observe → Think → Plan → Build → Execute → Verify → Learn) — a mandatory structured workflow that turns capable AI into reliable output. The Algorithm is PAI's central quality mechanism. ISC criteria make success verifiable, not subjective.

**Gastown** has MEOW (Mayor-Enhanced Orchestration Workflow) and the formula/recipe system in Beads. MEOW is a 7-step structured pattern for multi-agent work. Formulas define repeatable processes as DAGs. Both impose structure because Yegge clearly believes (as PAI does) that **unstructured AI produces inconsistent results.**

The abstraction layer differs: PAI's Algorithm governs a single agent's *cognitive process*; Gastown's MEOW governs a *team of agents' coordination process*. Same insight, different scope.

### Connection 4: Multi-Agent Parallelism with Coordination

**PAI** supports parallel agents via the Algorithm's capability selection (Background Agents, Agent Teams, Worktree Isolation). The Agent System provides three agent types: task tool subagents, named agents (persistent identities), and custom dynamic agents (ComposeAgent).

**Gastown** is built entirely around parallel agent coordination. The Mayor spawns polecats, slings beads, monitors via convoys. `gt feed` provides real-time multi-agent monitoring. The problems view detects stuck/zombie agents.

Key difference: PAI's parallelism is *session-scoped* (launched within one Algorithm run, cleaned up when done); Gastown's parallelism is *persistent* (polecats have identities that outlast any single session).

### Connection 5: CLI as the Universal Interface

**PAI** Principle #10 explicitly: "Every operation should be accessible via command line." PAI tools are all CLIs (TypeScript via bun). The CLI provides discoverability, scriptability, testability, transparency.

**Gastown** is *built as* a CLI (`gt` command). Everything is a `gt` subcommand: `gt mayor attach`, `gt convoy create`, `gt sling`, `gt feed`, `gt hooks`, `gt config`. The CLI is not incidental — it's the entire user interface.

Both arrived at: **CLIs are the agent-native interface.** AI can invoke CLI commands reliably; GUI requires visual interpretation. For an agent-operated system, CLI is the only sensible choice.

### Connection 6: Context Recovery After Compaction/Restart

**PAI** Algorithm v3.7.0 has explicit context recovery instructions: "If after compaction you don't know your current phase or criteria status: 1. Read the most recent PRD from MEMORY/WORK/..." The `pre-compact-prime` hook (just added to Gastown's registry) addresses the same problem.

**Gastown** has `gt prime` — runs on SessionStart and PreCompact to reload full role context. The explicit instruction in AGENTS.md: "After compaction or new session, run `gt prime` to reload your full role context, identity, and any pending work."

This is not a coincidence. **Context compaction is an AI-native problem unique to LLMs** — unlike human workers, AI agents lose their "short-term memory" when contexts compress. Both systems independently built dedicated recovery mechanisms for this.

### Connection 7: Nondeterministic Idempotence as Design Philosophy

**Gastown's NDI principle** — design for failure recovery rather than trying to eliminate non-determinism — is explicitly stated and built into the architecture. The Witness detects stalled agents. The Deacon monitors zombie sessions. Beads' Dolt backend allows retrying any step. Formulas are idempotent. Polecats don't need to succeed on the first try; the system is designed to recover.

**PAI's Algorithm** encodes the same philosophy implicitly: the Verify phase exists because earlier phases may have produced wrong outputs. The ISC gate requires measurable success criteria before proceeding. Context recovery instructions exist for compaction events. The LEARN phase captures failures as learning for future iterations. Permission to say "I don't know" (Principle 16) is a direct acknowledgment that fabricating certainty is worse than admitting failure.

Both systems accept that AI is non-deterministic and design around recovery rather than elimination of failures.

---

## Part 3: Differences Between Gastown and PAI

### Difference 1: Abstraction Layer — Infrastructure vs. Prompt Layer

This is the fundamental divergence.

**Gastown** operates at the **infrastructure layer**:
- Go binary (`gt`) — compiled, typed, fast
- Git worktrees for state persistence
- Dolt (version-controlled SQL) for work tracking
- tmux for terminal session management
- External services (Dolt, sqlite3) as dependencies

**PAI** operates at the **prompt/cognitive layer**:
- CLAUDE.md files — loaded as system context
- settings.json hooks — TypeScript/shell scripts
- Markdown files in MEMORY/ — flat-file state
- Skills — markdown prompt files that self-activate
- The Algorithm — a behavioral specification, not code

Gastown requires Go, Dolt, git, tmux to be installed. PAI requires only Claude Code and a text editor. Gastown is infrastructure you deploy; PAI is configuration you write. **They are not competing — they are complementary layers.** Gastown could host PAI (the Mayor could be a PAI-configured Claude Code instance).

### Difference 2: Team/Project vs. Personal/Individual

**Gastown** is designed for **project-scale, team-oriented work**:
- Multiple rigs (projects)
- Multiple humans (crew members) per rig
- 20-30 worker agents per workspace
- Explicit roles: Mayor, Witness, Refinery, Polecat, Deacon
- Cross-rig convoy tracking
- Docker Compose for team deployment

**PAI** is designed for **individual-scale, personal work**:
- Single user (Michael)
- Personal goals and context (TELOS)
- Memory tied to individual preferences and history
- Skills personalized to one person's domain and style
- PRIVATE/PUBLIC separation protects personal data

This is a fundamental design philosophy difference. Gastown is building a **multi-agent workforce manager**. PAI is building a **personal cognitive infrastructure**. One scales horizontally (more agents, more projects); the other scales vertically (deeper personalization, richer context).

### Difference 3: Work Tracking — External DB vs. Flat Files

**Gastown/Beads** uses a **Dolt database** (version-controlled SQL with cell-level merge conflict resolution):
- Structured schema for issues, dependencies, labels, comments
- Hash-based collision-resistant IDs for multi-agent writes
- Full dependency graph between beads
- Compaction to preserve context window
- Native branching (git semantics applied to data)

**PAI** uses **flat markdown files** in MEMORY/:
- PRD.md with YAML frontmatter
- Criteria as markdown checkboxes
- work.json as a registry (populated by hooks, not hand-written)
- JSONL for raw event logs

Trade-offs: Beads scales better (concurrent writes, conflict resolution, rich queries). PAI's flat files are simpler (readable, no infrastructure dependency, LLM-native). Beads is better for 20+ agents writing simultaneously; PAI's MEMORY/ is better for a single agent's cognitive state.

### Difference 4: Agent Persistence Model

**Gastown** polecats have **persistent identity, ephemeral sessions**:
- Named agents with work history
- Session ends when work completes
- Identity and history survive the session ending
- New session picks up via `gt prime` + git worktree

**PAI** agents are **ephemeral identity, scoped to session**:
- Named agents (Serena, Marcus, Rook) have backstories but are invoked per-task
- Custom agents composed on-the-fly from traits
- No cross-session agent identity by default
- Memory is at the *system* level (MEMORY/), not at the *agent* level

Gastown's model is more like hiring contractors who know their job history. PAI's model is more like spinning up specialists with the right skill set for each task.

### Difference 5: Multi-Runtime vs. Claude-Native

**Gastown** supports **multiple AI runtimes**:
- Claude Code (primary)
- Codex CLI
- Cursor
- Augment (auggie)
- Amp
- OpenCode
- GitHub Copilot
- And more via `gt config agent set`

Runtime configuration is per-rig. Different projects can use different AI tools.

**PAI** is **Claude Code-native**:
- Built entirely around Claude Code's hook system, skills, CLAUDE.md
- Would require significant rethinking to port to Codex/Cursor
- The Algorithm and skill system are Claude Code-specific constructs

This is not a flaw in PAI — it's a design choice to go deep rather than broad. Gastown's multi-runtime support is a strength for teams using different tools.

### Difference 6: Self-Improvement vs. Static Infrastructure

**PAI** is designed to **continuously improve itself**:
- Algorithm reflections feed back into Algorithm upgrades
- Sentiment analysis captures implicit quality signals
- Rating system captures explicit feedback
- System can update its own skills, documentation, workflows
- The whole LEARNING/ directory feeds MineReflections → AlgorithmUpgrade

**Gastown** is **infrastructure that you improve**:
- You update the Go code to add features
- Registry is a catalog, not self-modifying
- No feedback loop from agent work quality back into the system's behavior
- Version-controlled, but by humans pushing to GitHub

PAI treats self-improvement as a core principle. Gastown treats the infrastructure as something humans maintain. This reflects the different user models: PAI wants to get smarter *for you*; Gastown wants to be reliable *for your agents*.

---

## Part 4: Synthesis — What Each Can Learn

### What PAI Could Learn From Gastown

**1. Polecat-style persistent agent identities**
PAI's named agents (Serena, Marcus, Rook) have backstories and voices but no cross-session state. A polecat model would let PAI agents accumulate work history: "Serena has reviewed 47 architecture decisions; here's her reasoning pattern." This would make agent output richer over time.

**2. Convoy-style batch work tracking**
PAI's current MEMORY/WORK/ is single-session PRDs. Gastown's convoy model tracks multi-session, multi-issue batches. For long-running PAI projects (building a feature over days), a convoy-style tracker would show "across 8 sessions, these 12 issues have been addressed, 3 remain."

**3. The Problems View (`gt feed --problems`)**
Gastown's GUPP violation / Stalled / Zombie detection is an excellent pattern. PAI has no equivalent mechanism for detecting when an Algorithm run is stuck or producing diminishing returns. A "problems view" equivalent could detect Algorithm phase stalls.

**4. Formula/Recipe System**
PAI has skills and pipelines, but Beads' formula system with explicit step dependencies (DAG), variable injection, and trackable molecule instances is more structured. PAI's pipelines could benefit from explicit dependency graphs rather than linear sequences.

**5. `gt doctor` — Workspace Health Checks**
Gastown's `gt doctor` validates that all settings files are in sync with what the hook system would generate. PAI has system integrity audits but they're manual (invoke the System skill). An automated health-check that validates PAI hook configurations, memory system integrity, and skill file validity would be valuable.

### What Gastown Lacks That PAI Has

**1. Cognitive Algorithm / Quality Assurance Layer**
Gastown coordinates *what work gets done* but has no mechanism for ensuring *quality of the work itself*. There's no equivalent to PAI's Algorithm — no ISC criteria, no verification phase, no euphoric surprise targeting. Gastown is a great manager; it doesn't make the workers smarter.

**2. Personal Context Layer**
Gastown has no TELOS equivalent — no sense of your goals, preferences, values, history. The Mayor knows about your workspace, but not about *you*. PAI's deepest value is that it knows who you are. Gastown is a workforce manager; PAI is a cognitive partner.

**3. Self-Improvement Feedback Loop**
Gastown has no mechanism for learning from past agent performance. PAI's reflections system, rating capture, sentiment analysis, and AlgorithmUpgrade workflow create a flywheel where the system gets measurably better. This is PAI's most unique long-term advantage.

**4. Skill System**
Gastown has no equivalent to PAI's skills — self-activating domain expertise packages that extend what the AI does well. The Mayor can be given instructions, but there's no modular "add Research expertise" or "add Security expertise" architecture.

**5. Multi-Model Research Routing**
PAI routes different research tasks to different AI models (Claude for academic, Gemini for multi-perspective, Grok for contrarian). Gastown supports multiple runtimes but for code work, not for specialized research capabilities.

---

## Framing: The Convergence Story

The most interesting insight about Gastown and PAI is not a specific feature overlap — it's that they are **independent proofs of the same theorem**:

> **Theorem:** AI agents need scaffolding that addresses (1) context persistence, (2) work state durability, (3) structured execution patterns, (4) multi-agent coordination, and (5) identity continuity to be reliably productive.

Steve Yegge built Gastown from the infrastructure layer up — starting with git worktrees, building persistence, then coordination, then the Mayor as coordinator.

PAI was built from the prompt layer down — starting with CLAUDE.md configuration, building the Algorithm for structured cognition, then the skill system for domain expertise, then the memory system for persistence.

They met in the middle. They share the same insight (scaffolding > model, structure enables reliability) but express it in different materials (Go binary vs. markdown configuration) at different altitudes (infrastructure vs. cognitive).

**They are not alternatives. They are layers of the same system.**

A fully-realized personal AI infrastructure might look like: Gastown at the workspace orchestration layer, PAI at the cognitive quality layer, running inside each of Gastown's agents. The Mayor would be a PAI-configured Claude Code instance. Each Polecat would run the Algorithm for its assigned task. Convoy tracking would replace (or complement) PAI's MEMORY/WORK/ PRDs. Beads would become the cross-session work registry.

That's the synthesis. Yegge and Michael are independently building complementary components of the same future.

---

### The "Platforms Rant" Lens Applied to Gastown and PAI

Yegge's most famous insight: platforms beat products because platforms expose APIs that allow others to build on top. Amazon beat Google at cloud because Bezos forced internal teams to build APIs. A product that doesn't expose its internals gets replaced by a platform-ized equivalent.

Applied to AI infrastructure, this insight is self-referential in an interesting way: **Gastown and PAI are both arguing that commodity AI tools (GitHub Copilot, Cursor, Claude.ai) will be beaten by personal infrastructure that exposes AI capabilities as composable, owned primitives.**

But there's a second-order application: **Gastown is more "platformy" than PAI.** Gastown exposes clean CLIs (`gt`, `bd`) that other tools can build on. The Wasteland is explicitly a federated protocol. Community spin-offs (BeadHub, nvim-beads, gastown-control-plane) are already building on it. PAI is currently less platform-like — it's personal configuration, not an exposed API. If Yegge's own thesis is right, PAI would benefit from more CLI surface area and more explicit interfaces that allow other tools to compose with it.

---

*Sources: github.com/steveyegge/gastown (README, AGENTS.md, docs/HOOKS.md, docs/concepts/*), github.com/steveyegge/beads, PAI/PAISYSTEMARCHITECTURE.md, PAI/PAIAGENTSYSTEM.md, PAI/Algorithm/v3.7.0.md*
