# AgentBuild — Build Loop Workflow

The operating rhythm of agentic development. Not sprints. Not tickets. A pull-based loop driven by specs.

**Invoke when:** A spec is ready in `docs/specs/` and the environment is healthy (CI passing).

---

## The 8-Step Loop

```
PICK → TASK → BUILD → GATE → REVIEW → MERGE → OBSERVE → REPEAT
```

---

### Step 1: PICK

**Lucy says:**
> "Which spec are we building next? Options from `docs/specs/features/`:
> [list available specs]
>
> Pick one, or I'll suggest the lowest-dependency feature to start."

**Dependency rule:** Build features in dependency order. A feature that other features depend on always goes first. If unsure, ask Lucy to map dependencies before picking.

---

### Step 2: TASK

**Before generating a build task, validate the spec exists and is complete:**

```
VALIDATION (mandatory — do NOT skip):
1. Verify file exists: docs/specs/features/[feature-name].md
2. Verify it contains ALL required sections:
   - Happy Path (with FEATURE/USER/ACTION/RESULT)
   - Edge Cases
   - Failure Behaviors
   - Business Constraints That Apply
   - Out of Scope (MVP)
   - Test Coverage Required (with granular checkboxes, not section references)
3. Verify Spec status is READY or HARDENED (not DRAFT)
4. Verify checkboxes describing visible browser behavior are tagged VERIFY: browser

If ANY validation fails → STOP. Do not issue a build task. Route to spec creation:
  - If file missing: Create spec using SpecFeature.md template format
  - If sections missing: Add missing sections to existing spec
  - If status is DRAFT: Harden the spec (edge cases, failure modes, test checkboxes)
  - If VERIFY: browser tags missing: Tag visual behavior checkboxes
```

**Lucy generates the build task from the validated spec:**

```
SPEC: docs/specs/features/[feature-name].md
SCOPE: [Specific sections to implement — section numbers or named items]
CONSTRAINTS:
  - Must satisfy all CONSTRAINT blocks in docs/specs/constraints/business-rules.md
  - Must follow all conventions in AGENTS.md
  - Edge cases listed in spec sections [N-M] must have test coverage
DONE WHEN:
  - All tests pass
  - CI is green
  - Happy path from spec is implemented and tested
  - Edge cases approved in spec are covered by tests
  - No behavior present that is NOT in the spec
```

**Lucy says:**
> "Build task issued. The agent has the spec, the constraints, and the done criteria. I'm not providing implementation guidance — the spec IS the guidance. If the agent asks a follow-up question, that's a spec gap we need to fix."

**If agent asks a follow-up question:**
> "Noted — this is a spec gap. Before answering, let's add this to the spec so it's covered permanently. [Add to spec]. Now the agent has what it needs."

---

### Step 3: BUILD

Agent executes. Lucy monitors but does not intervene in implementation decisions.

**What the agent does (no human involvement):**
- Reads the spec and AGENTS.md
- Implements the feature
- Writes tests covering happy path and all approved edge cases
- Runs tests locally
- Runs linter
- Creates a PR with a description referencing the spec

**What Lucy watches for:**
- Does the PR description reference the spec? (If not, ask the agent to add it)
- Are the commit messages meaningful?
- Did CI run on the PR?

---

### Step 4: GATE

**Non-negotiable. All three tiers must pass before proceeding.**

#### Tier 1: Mechanical (same as before)

**Lucy checks:**
```
[ ] Tests pass
[ ] CI is green
[ ] Linter passes
```

If Tier 1 fails, issue a fix task (same format as before) and loop back.

#### Tier 2: Test Quality

**After Tier 1 passes, Lucy reads the actual test files and checks four things:**

1. **NO TAUTOLOGIES** — No assertion where both expected and actual are literals. `expect(true).toBe(true)`, `expect(1).toBe(1)`, `expect("ok").toBe("ok")` — these prove nothing. Every assertion must reference a system-produced value (a response, a return value, a DB record, a side effect).

2. **NO MOCK-ONLY COVERAGE** — For every behavior in the spec's Test Coverage Required checkboxes, at least one test exercises real infrastructure (real DB, real HTTP handler, real file system). Mock-only tests verify assumptions about interfaces, not actual behavior. A feature "tested" entirely with mocks passes even if the real system is broken.

3. **NO UNTESTED HANDLERS** — Grep for handler registrations (route definitions, webhook endpoints, callback registrations). Every handler found must have at least one test that calls it. A handler with zero tests passes the gate by absence — the most dangerous kind of "passing."

4. **ASSERTIONS MATCH SPEC** — Each checkbox in the spec's Test Coverage Required section names a specific behavior. That behavior must appear as an assertion in a test. "Rate limiting returns 429 after 5 failed attempts" → there must be a test that makes 5+ requests and asserts status 429.

**If Tier 2 fails:**

Issue a **test-quality fix task** — not "tests are bad," but specific violations:

```
SPEC: [same spec]
ISSUE: Test quality violations:
  - TAUTOLOGY: `auth.test.ts:42` → `expect(true).toBe(true)` — replace with assertion against actual auth response
  - MOCK-ONLY: Rate limiting behavior tested only via mocked middleware — add integration test with real DB
  - UNTESTED HANDLER: `POST /api/webhooks/stripe` registered at `routes/webhook.ts:15` has zero tests
  - SPEC MISMATCH: Checkbox "expired session returns 401" has no matching assertion in any test file
SCOPE: Fix only the listed test quality violations. Do not change feature behavior.
DONE WHEN: All four Tier 2 checks pass. All Tier 1 checks still pass.
```

#### Tier 3: Browser Verification (Spec-Driven)

**After Tier 2 passes, verify every `VERIFY: browser` checkbox from the spec in a real browser.**

Lucy uses the Playwright skill (`/playwright-skill`) or Playwright MCP tools (`mcp__plugin_playwright_playwright__*`) to execute this 5-step protocol:

**T3-1: Classify checkboxes.** Read the spec's `Test Coverage Required` section. Only checkboxes tagged `VERIFY: browser` are in scope. Zero tagged = Tier 3 auto-passes.

**T3-2: Start the application.** Dev server must be running (e.g., `npm run dev` or `bun run dev`).

**T3-3: For each `VERIFY: browser` checkbox, run the verification protocol:**

| Checkbox Type | Protocol | Playwright Tools Used |
|---|---|---|
| **Renders X** (element presence) | Navigate → snapshot → confirm element → screenshot | `browser_navigate`, `browser_snapshot`, `browser_take_screenshot` |
| **Responsive N→M→K** (layout at breakpoints) | For each breakpoint: resize → snapshot → confirm layout → screenshot | `browser_resize`, `browser_snapshot`, `browser_take_screenshot` |
| **Interaction produces change** (filter, sort, click) | Navigate → BEFORE snapshot → perform action → AFTER snapshot → confirm DOM change → screenshot | `browser_click`/`browser_select_option`/`browser_fill_form`, `browser_snapshot` |
| **Animation/transition exists** | Navigate → `browser_evaluate` computed style → confirm not `none` | `browser_evaluate`, `browser_take_screenshot` |

**T3-4: Write BROWSER evidence lines.** For each verified checkbox, append a `BROWSER` line below the existing `EVIDENCE` line in the spec:

```
- [x] Roster page renders bento card grid with client name, role, company, industry pill, status badge
  - EVIDENCE: ClientRosterPage.test.tsx "renders bento card grid..." | TYPE: component
  - BROWSER: screenshot `docs/browser-verification/client-roster--bento-grid.png` → navigated to /clients, confirmed 8 cards with name, role, company, industry pill, status badge in DOM snapshot
  - VERIFY: browser
```

**T3-5: Pass/fail.** Passes when ALL `VERIFY: browser` checkboxes have a BROWSER line. Fails with specific violations:

```
SPEC: [same spec]
ISSUE: Browser verification failures:
  - MISSING: Checkbox "Cards display client name" — element not found in DOM snapshot
  - LAYOUT: Checkbox "Grid reflows to 1 column at 375px" — shows 2 columns not 1
  - INTERACTION: Checkbox "Status filter updates cards" — card count unchanged after click
SCOPE: Fix only the listed visual/rendering issues. Do not change test files or feature behavior.
DONE WHEN: All three tiers pass. Screenshots saved to docs/browser-verification/.
```

**Screenshot naming convention:**
```
[feature-name]--[checkbox-slug].png                   # Standard
[feature-name]--[checkbox-slug]--[width]px.png        # Responsive
[feature-name]--[checkbox-slug]--after.png             # Post-interaction
```

**Do not proceed to Step 5 until all three tiers are green.**

---

### Step 5: REVIEW

**This is the only human step in the loop. Three questions only — answer takes 5-15 minutes.**

**Lucy presents the PR and asks:**

> "Review checklist — three questions:
>
> **Q1: Does this match the spec?**
> Read the spec. Read the PR description. Does the implemented behavior match what you specified? (Not the code — the behavior.)
>
> **Q2: Are the edge cases from Phase 2 covered in the tests?**
> Check the test file. Do you see tests for the edge cases you approved in Phase 2b? Name any that are missing.
>
> **Q3: Is there any behavior present that wasn't in the spec?**
> Scope creep check. Did the agent add anything you didn't ask for? (Not necessarily bad — but you should know about it and decide if it stays.)
>
> Answer all three. If Q1 or Q2 fail, this goes back to the agent. If Q3 has additions you want to keep, update the spec to include them."

**Review passes when:** Q1 = yes, Q2 = yes, Q3 = yes (or reviewed additions accepted and spec updated).

---

### Step 6: MERGE

**Lucy says:**
> "Merging PR #[N] — [feature name]. Merge commit created. Watching for any CI failures on main..."

**If merge causes CI failure on main:**
> "Merge broke CI on main. Immediate fix task — this takes priority over all new features."

---

### Step 6b: VERIFY SPEC (Mandatory — cannot skip)

**The feature spec is the source of truth for build completion.** After merge, verify every checkbox in the feature spec's `Test Coverage Required` section, then update the spec file and MASTER.md.

**Lucy does (not the agent — this is Lucy's responsibility):**

1. **Read** `docs/specs/features/[feature-name].md`

2. **For each `- [ ]` checkbox in `Test Coverage Required`, execute this 6-step checklist:**

   **Step A: Find the test.** Grep test files for the behavior named in the checkbox. If no test file mentions it, the checkbox fails immediately.

   **Step B: Read the test assertions.** Open the test file and read the actual `expect()`/`assert` calls. Do not trust test names — read the body.

   **Step C: Verify no tautologies.** Every assertion must reference a system-produced value. If both sides of an assertion are literals (`expect(true).toBe(true)`, `expect("ok").toEqual("ok")`), the checkbox fails.

   **Step D: Verify test type matches requirement.** Check if the test uses real infrastructure (DB, HTTP, file system) or mocks. If mock-only, proceed to Step F.

   **Step E: Write the evidence line into the spec.** Format:
   ```
   - [x] [Behavior description]
     - EVIDENCE: `[test-file]` → `[test name]` → [what it actually asserts]
     - TYPE: [unit-real | unit-mock | integration | e2e]
   ```

   **Step F: If mock-only, verify companion test exists.** A `unit-mock` test alone is insufficient. There must be a companion `integration`, `unit-real`, or `e2e` test for the same behavior. If none exists, the checkbox fails.

3. **If any checkbox fails:** The feature is NOT complete. Issue a fix task (Step 2 format) targeting the failed checkboxes with specific reasons:
   ```
   ISSUE: Spec verification failures:
     - "Rate limiting returns 429" — FAILED: test uses expect(true).toBe(true) (tautology)
     - "Webhook validates signature" — FAILED: no test found for POST /api/webhooks handler
     - "Session expiry redirects" — FAILED: mock-only, no integration companion
   ```
   Do NOT proceed to Step 7.

4. **When ALL checkboxes pass with evidence written:**
   - Edit the feature spec: set `**Spec status:** COMPLETE`
   - Edit `docs/specs/MASTER.md`: set the feature's Build Status to `Built`
   - Commit both file changes: `"docs: mark [feature-name] spec complete (PID-xxx)"`

**Why this step exists:** Without it, build completion is determined by vibes — "tests pass" and "CI green" don't guarantee the spec's specific test coverage requirements are met. The feature spec checkboxes are the granular, per-feature source of truth. MASTER.md's Build Status is derived from the feature spec status, never the other way around.

**Anti-pattern:** Marking MASTER.md as "Built" without all feature spec checkboxes checked. This is the equivalent of marking a task done without running the tests.

---

### Step 7: OBSERVE

**After merge, watch for 24-48 hours (or until next feature is ready):**

**Lucy monitors (via observability from Phase 6):**
- Error rate on the new feature's endpoints
- Any business metric events that aren't firing
- User behavior that suggests spec misunderstanding

**If production issue found:**
> "Production issue detected: [error/metric]. This becomes a spec update, not a patch. Adding to `docs/specs/features/[feature-name].md` as a new edge case. Issuing fix task with updated spec."

**The production → spec feedback loop:**
```
Production error →
Identify which spec section didn't cover this →
Update spec (add as edge case or failure mode) →
Issue fix task referencing updated spec →
Gate → Review → Merge
```

---

### Step 8: REPEAT

**Lucy says:**
> "Feature shipped. Back to Step 1 — what's next?"

Return to Step 1 (PICK) for the next feature.

**When all features are shipped:** Route to `Workflows/MvpGate.md`.

---

## Build Loop Anti-Patterns

**Never do these:**

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Reviewing code quality (how it's written) | Agent owns code quality. You own behavioral correctness. |
| Patching production without a spec update | The spec will generate the same bug again next build |
| Skipping the gate because "it looks fine" | Non-negotiable. Gate fails → goes back to agent. Always. |
| Writing any implementation code yourself | You've broken the factory model. The agent can't learn from your intervention. |
| Answering agent follow-up questions without fixing the spec | You've answered for this session but not for the next agent. |
| Passing Tier 1 and skipping Tier 2 | "Tests pass" means nothing if tests don't test anything. The BriefingPro auth build proved this. |
| Accepting `expect(true).toBe(true)` as a passing test | Tautology — passes even if the feature is deleted. Test theater. |
| Accepting mock-only coverage as complete | Mocks verify your assumptions about interfaces. Integration tests verify the system actually works. |
| Marking spec checkbox without writing evidence | Evidence-free checkboxes are vibes. Write the test file, test name, and what it asserts. |
| Running Tier 3 as ad-hoc screenshots without checking spec checkboxes | You verify what looks interesting, not what the spec requires. Spec gaps hide. |
| Skipping Tier 3 because "all tests pass" | A component can pass all unit tests and render blank in the browser. |
| Building from a PRD or task doc instead of a feature spec | PRDs define product vision. Feature specs define testable behavior. Without a spec, test checkboxes are invented during build — the fox designs the henhouse. |
