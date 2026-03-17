# Feature Specification Format

Every feature built by AgentBuild gets a spec file in `docs/specs/features/[feature-name].md`. This format is what the agent reads to implement. Complete = no follow-up questions.

---

## Template

```markdown
# Feature: [Feature Name]

> [One sentence: what this feature does and why it matters]

**Spec status:** [DRAFT / READY / HARDENED / COMPLETE]
**Build status:** [Not started / In progress / Built]
**Last updated:** [date]

---

## Happy Path

FEATURE: [Feature name]
USER: [Specific user — not "the user" — be precise about who]
ACTION: [What they want to accomplish — specific, behavioral]
RESULT: [What they see/receive when it works perfectly — specific, observable]

**Example:**
FEATURE: Login
USER: Returning user who has previously created an account
ACTION: Submits email and password on the login form
RESULT: Redirected to dashboard, session cookie set, username shown in navigation bar

---

## Edge Cases

[List all approved edge cases from Phase 2b. Format: condition → correct behavior]

### Input Edge Cases
- **[Condition]:** [Correct behavior — specific, not "handle gracefully"]
- **[Condition]:** [Correct behavior]

### State Edge Cases
- **[Condition]:** [Correct behavior]

### Boundary Edge Cases
- **[Condition]:** [Correct behavior]

---

## Failure Behaviors

[From Phase 2c — what the system does when things go wrong]

| Failure Condition | Correct Behavior | User Message |
|-------------------|-----------------|--------------|
| [Database unavailable] | [Return 503, log error] | "[User-facing message]" |
| [Session expired] | [Redirect to login] | "[User-facing message]" |
| [Upstream 500] | [Return 502, include retry-after] | "[User-facing message]" |
| [Input valid but unexpected] | [Behavior] | "[User-facing message]" |

---

## Business Constraints That Apply

[Reference or list constraints from docs/specs/constraints/ that apply to this feature]

- **[Constraint name]:** [One-sentence rule statement]
- See: `docs/specs/constraints/[relevant-file].md` for full details

---

## Out of Scope (MVP)

[Explicitly state what is NOT included in this implementation]

- [Thing that seems related but isn't this feature]
- [Enhancement to defer post-MVP]
- [Adjacent behavior that belongs in a different spec]

---

## Test Coverage Required

**These checkboxes are the source of truth for build completion.** A feature is not "Built" until every checkbox here is `[x]`. MASTER.md's Build Status is derived from this section — never the other way around. The Build Loop's Step 6b (VERIFY SPEC) checks each item with evidence before marking it complete.

The agent must have tests for:
- [ ] Happy path (Section: Happy Path)
- [ ] All edge cases in Section: Edge Cases
- [ ] All failure behaviors in Section: Failure Behaviors where testable
- [ ] Each constraint listed in Section: Business Constraints

### Rules

- **Every route, webhook, and callback handler in scope must have a dedicated test checkbox.** No handler goes untested by omission.
- **Each checkbox gets a TYPE tag:** `unit-real | unit-mock | integration | e2e`
- **Mock-only is insufficient.** If a checkbox's TYPE is `unit-mock`, a companion `integration` or `unit-real` test must also exist for that behavior. Mocks verify assumptions, not behavior.
- **No tautologies.** `expect(true).toBe(true)` or any literal-to-literal assertion is a **test theater violation** and fails the checkbox. Every assertion must reference a system-produced value.
- **Checkboxes describing visible browser behavior get a `VERIFY: browser` tag.** This tells the Build Loop's Tier 3 to verify this checkbox in a real browser using Playwright. Tag checkboxes about: rendered UI elements, user interactions, responsive layout, loading states, animations. Do NOT tag checkboxes about server behavior, data layer, or business logic.
- **Each checkbox names a single specific behavior** — not a section reference, not a vague category.

### Evidence Format

When a checkbox is checked, it MUST include an evidence block. This is what makes the checkbox valid:

```
- [x] Rate limiting returns 429 after 5 failed attempts
  - EVIDENCE: `rate-limit.test.ts` → `should return 429 on 6th failed login` → asserts res.status === 429 after 6 calls against real DB
  - TYPE: integration
```

```
- [x] Webhook signature verification rejects tampered payloads
  - EVIDENCE: `webhook.test.ts` → `rejects invalid signature` → asserts 401 response with modified HMAC against real handler
  - TYPE: unit-real
```

A checkbox without an evidence block is not checked — it's wishful thinking.

**Browser verification evidence** (written during Build Loop Tier 3, not during BUILD):

```
- [x] Grid reflows from 4 columns (desktop) to 1 column (mobile)
  - EVIDENCE: `Page.test.tsx` → `responsive grid columns` → asserts grid class changes
  - TYPE: component
  - BROWSER: screenshots `docs/browser-verification/feature--grid-reflow--1280px.png`, `--768px.png`, `--375px.png` → confirmed 4-col at 1280, 2-col at 768, 1-col at 375
  - VERIFY: browser
```

The BROWSER line is written by Lucy during Tier 3 gate verification. A checkbox tagged `VERIFY: browser` requires BOTH an EVIDENCE line (from Step 6b) AND a BROWSER line (from Tier 3) to be fully verified.

### When Hardening Specs (Specify Phase)

Replace the generic checkboxes above with feature-specific granular items. Each checkbox should name a specific testable behavior, not a section reference. Example:
```
- [ ] Sign-up creates coach record
- [ ] Login returns valid session
- [ ] Expired session redirects to login
- [ ] POST /api/webhooks/stripe validates signature before processing
```
Not:
```
- [ ] Happy path (Section: Happy Path)
```

---

## Acceptance Criteria

This feature is done when:
1. Happy path produces exactly the described RESULT for the described USER and ACTION
2. All edge cases produce their described correct behaviors
3. All failure behaviors produce their described behaviors
4. All listed constraints are enforced
5. CI is green
6. Nothing in "Out of Scope" was implemented
7. Every checkbox in "Test Coverage Required" is `[x]` with evidence
8. Spec status is set to COMPLETE and Build status is set to Built
```

---

## Spec Quality Checklist

Before issuing a build task against a spec, verify:

- [ ] USER is specific (not "the user" or "users")
- [ ] RESULT is observable (something you can see, not "works correctly")
- [ ] Every edge case has a specific correct behavior (not "handle gracefully")
- [ ] Every failure behavior has a specific user message (not "show an error")
- [ ] Out of Scope section exists and is populated
- [ ] Business constraints are referenced
- [ ] Test coverage section is complete
- [ ] Every route/webhook/callback handler in scope has a dedicated test checkbox
- [ ] No checkbox is satisfiable with mock-only tests (each has a path to `unit-real`, `integration`, or `e2e`)
- [ ] Each checkbox names a single specific behavior (not "auth works" or "edge cases covered")
- [ ] Checkboxes describing visible browser behavior are tagged `VERIFY: browser`
- [ ] Checkboxes about server/data behavior are NOT tagged `VERIFY: browser`

**A spec without specific behaviors is not a spec — it's a wish. The agent will guess. The guess will be wrong.**

**A spec with vague test checkboxes is permission to write fake tests.** If the checkbox says "auth works," the agent will write `expect(true).toBe(true)` and check the box. Make the checkbox specific enough that only a real test can satisfy it.
