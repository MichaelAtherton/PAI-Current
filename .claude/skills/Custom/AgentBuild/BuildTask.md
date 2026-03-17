# Build Task Format

The build task is the complete human-to-agent handoff. It must contain everything the agent needs to implement and verify a feature without asking a follow-up question.

**Format:** Used in Phase 4 (Build Loop) Step 2 (TASK). Issued by Lucy on behalf of Michael.

---

## Template

```
SPEC: docs/specs/features/[feature-name].md
SCOPE: [Specific sections or items to implement — reference by section name or item number]
CONSTRAINTS:
  - Must satisfy all CONSTRAINT blocks in docs/specs/constraints/[relevant-file].md
  - Must follow all conventions in AGENTS.md
  - [Any task-specific constraints beyond the spec]
DONE WHEN:
  - All tests pass
  - CI is green (tests + lint)
  - Happy path from spec is implemented and tested
  - Edge cases marked Include in spec are covered by tests
  - Failure behaviors in spec are implemented and tested where automatable
  - No behavior is present that is NOT in the spec
  - PR description references this spec file
  - Every `- [ ]` in the spec's "Test Coverage Required" section can be verified as satisfied
  - TEST QUALITY (all must be true):
    - No tautological assertions (both sides literals — e.g. expect(true).toBe(true))
    - Every route/webhook/callback handler has at least one test
    - No behavior covered exclusively by mocks (mock-only = companion integration test required)
    - Every assertion references a system-produced value (response, DB record, return value)
```

---

## Examples

### Example 1: Full Feature

```
SPEC: docs/specs/features/user-auth.md
SCOPE: Full spec — implement all sections
CONSTRAINTS:
  - Must satisfy all CONSTRAINT blocks in docs/specs/constraints/security.md
  - Must satisfy all CONSTRAINT blocks in docs/specs/constraints/business-rules.md
  - Must follow all conventions in AGENTS.md
DONE WHEN:
  - All tests pass
  - CI is green
  - Happy path (login, logout, session persistence) implemented and tested
  - All 8 edge cases marked Include are covered by tests
  - All 6 failure behaviors (DB unavailable, session expiry, etc.) are implemented
  - No behavior outside the spec
  - PR description references docs/specs/features/user-auth.md
```

### Example 2: Partial Feature (Sections Only)

```
SPEC: docs/specs/features/billing.md
SCOPE: Sections 1-3 only (Free tier and Pro tier entitlements). Do NOT implement Sections 4-6 (Enterprise tier) — those are a separate task.
CONSTRAINTS:
  - Must satisfy CONSTRAINT "Free Tier API Limits" in docs/specs/constraints/business-rules.md
  - Must satisfy CONSTRAINT "Trial Period Expiry" in docs/specs/constraints/business-rules.md
  - Must follow conventions in AGENTS.md
DONE WHEN:
  - Free tier rate limiting works per spec section 1
  - Pro tier unlimited access works per spec section 2
  - Trial expiry behavior works per spec section 3
  - CI is green
  - Nothing from sections 4-6 is implemented
```

### Example 3: Fix Task (After Gate Failure)

```
SPEC: docs/specs/features/user-auth.md
SCOPE: Fix only — CI is failing on this specific test: "should return 429 when session is expired mid-request"
ISSUE: [paste exact error output from CI]
CONSTRAINTS:
  - Fix only the failing test. Do not change behavior unrelated to this failure.
  - Session expiry behavior is defined in spec section 3.2
DONE WHEN:
  - The specific failing test now passes
  - All previously-passing tests still pass
  - CI is green
  - No other behavior changed
```

---

## What Makes a Build Task Complete

The build task must answer these questions for the agent without the agent needing to ask:

| Question | Where Answered |
|----------|---------------|
| What am I building? | SPEC line |
| How much of it? | SCOPE line |
| What rules must I follow? | CONSTRAINTS |
| How do I know I'm done? | DONE WHEN |
| What should I NOT build? | SCOPE (exclusions) |

**If the agent asks a follow-up question, the build task is incomplete.** Add the answer to the spec or AGENTS.md, then reissue the task. Do not answer verbally — answers that exist only in a conversation are lost to the next agent.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| `SPEC: general requirements` | Agent has no source of truth |
| `SCOPE: everything` | Too broad — agent wanders |
| `DONE WHEN: it works` | Not testable — agent can't verify |
| `CONSTRAINTS: be careful` | Meaningless — not actionable |
| Answering agent questions in chat | Answer dies with the session; next agent doesn't have it |
| Writing implementation hints | Agent owns implementation — your hints conflict with its judgment |
| `expect(true).toBe(true)` | Tautology — proves nothing, passes even if the feature is deleted |
| All tests use mocks with zero integration tests | Mocks verify assumptions about interfaces, not actual behavior |
| Handler exists with zero tests | Untested handlers pass the gate by absence — the most dangerous kind of "passing" |
| Assertions that don't reference system output | `expect("ok").toBe("ok")` tests the test, not the system |
