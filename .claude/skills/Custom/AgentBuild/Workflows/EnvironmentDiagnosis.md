# AgentBuild — Environment Diagnosis Workflow

When agents fail repeatedly, the fix is almost never "prompt harder." The fix is: what capability is missing in the environment?

**Invoke when:** Agent output is consistently wrong, CI is failing inexplicably, the build loop keeps cycling on the same type of failure, or a production incident reveals a systematic gap.

---

## The Core Principle (From the OpenAI Experiment)

> "When something failed, the fix usually wasn't 'prompt harder.' The fix was — what capability is missing in the environment? Better structure, better constraints, better feedback loop, so the agent can reliably do the work next time."

The engineer stops being the person who writes the solution and becomes the person who designs the system that produces solutions.

---

## Diagnosis Checklist

**Lucy runs through all five categories. For each: identify if this is the failure mode, then apply the fix.**

---

### Category 1: Feedback Signal Quality

**Diagnosis question:** Can the agent tell if it succeeded? Is the failure signal specific enough to act on?

**Signs this is the problem:**
- Tests pass but behavior is wrong
- Agent "fixes" something and breaks something else
- Error messages say "something went wrong" not "X failed because Y"
- The agent can't distinguish a partial success from a full failure

**Lucy checks:**
```
[ ] Are test assertions specific? (not just "returns 200" but "returns 200 with body containing X")
[ ] Do failing tests name WHY they failed, not just that they failed?
[ ] Are error messages in the code specific enough for the agent to understand what happened?
[ ] Is there logging at key decision points (not just request/response — intermediate state too)?
[ ] Does the CI output give the agent enough information to fix the failure without a human explaining it?
```

**Fix actions:**
- Add more specific test assertions: "Expected X, got Y" not "test failed"
- Improve error messages in application code: include the condition that caused the error
- Add structured logging at decision boundaries
- Update AGENTS.md: "When a test fails, the error message will tell you [X]. This means [Y]."

---

### Category 2: Constraint Enforcement

**Diagnosis question:** Are business rules enforced mechanically, or just stated in a document the agent might not read?

**Signs this is the problem:**
- Agent correctly understands a rule but produces code that violates it
- The same rule violation appears in multiple PRs
- Agent adds features that technically work but violate business logic

**Lucy checks:**
```
[ ] Is every business constraint in docs/specs/constraints/business-rules.md?
[ ] Are linting rules or pre-commit hooks enforcing any of these mechanically?
[ ] Are there test cases that specifically verify constraint compliance (not just happy path)?
[ ] Does AGENTS.md reference the constraint spec explicitly?
[ ] Are constraints stated as code-checkable rules, not as prose?
```

**Fix actions:**
- Add ESLint/custom lint rules for patterns that keep appearing incorrectly
- Add pre-commit hooks that check specific constraint patterns
- Add test cases: "this input should return 403, not 200" for access constraints
- Update AGENTS.md: "CONSTRAINT: Always check docs/specs/constraints/business-rules.md before implementing any access control."
- For pricing/entitlement: add middleware-level enforcement, not just application-level

---

### Category 3: Context Completeness

**Diagnosis question:** Does the agent have enough context to make the right decision without asking?

**Signs this is the problem:**
- Agent asks follow-up questions (every follow-up = a spec gap)
- Agent makes reasonable-sounding choices that are wrong for your specific domain
- Agent implements something generic when you needed something specific to your business
- Different agents produce different implementations of the same feature

**Lucy checks:**
```
[ ] Does AGENTS.md describe the project's domain context, not just conventions?
[ ] Is the architecture decision record (docs/specs/architecture/decisions.md) up to date?
[ ] Do spec files include "why" for non-obvious decisions?
[ ] Are there any domain-specific terms used in specs that aren't defined anywhere?
[ ] Does AGENTS.md explain what makes this project different from a generic [type] project?
```

**Fix actions:**
- Update AGENTS.md with domain context: "This is a [domain] application. Unlike generic [type] apps, we [specific constraint/pattern/rule]."
- Add an Architecture Decision Record for every non-obvious decision
- Add a Glossary section to AGENTS.md for domain-specific terms
- Review recent agent follow-up questions — each is a AGENTS.md or spec update

---

### Category 4: Scope Clarity

**Diagnosis question:** Is the boundary of each task unambiguous? Can the agent wander into adjacent behavior?

**Signs this is the problem:**
- Agent implements the right feature but also changes adjacent code
- PR includes changes not related to the spec
- Agent "improves" things that weren't broken
- Agent's interpretation of "implement X" includes things that belong in a different feature

**Lucy checks:**
```
[ ] Does every build task have an explicit SCOPE line?
[ ] Do spec files have "OUT OF SCOPE" sections for MVP?
[ ] Is it clear where one feature ends and the next begins?
[ ] Does the build task reference specific sections of the spec (not the whole spec)?
[ ] Are there shared utilities the agent might modify? Are they protected?
```

**Fix actions:**
- Add OUT OF SCOPE sections to every spec: "Do NOT implement [adjacent thing] — that is a separate feature."
- Tighten build task SCOPE lines: reference specific sections, not the entire spec
- Add "do not modify" comments to shared/foundational code
- Update AGENTS.md: "When in doubt about scope, implement less. Submit a PR and ask in the PR description."

---

### Category 5: Recovery Path

**Diagnosis question:** When the agent fails, does it know what to do next?

**Signs this is the problem:**
- Agent attempts to fix a failure by doing something completely different from the spec
- Agent gets stuck in a loop of making and breaking things
- CI failure leads to a large unrelated change in the next commit
- Agent "solves" a test failure by deleting the test

**Lucy checks:**
```
[ ] Does AGENTS.md have a "When tests fail" section with specific guidance?
[ ] Does AGENTS.md have a "When uncertain" section?
[ ] Are there common failure patterns documented with their correct resolutions?
[ ] Is there guidance against deleting tests to make CI pass?
[ ] Is there guidance about when to stop and flag for human review?
```

**Fix actions:**
- Update AGENTS.md with explicit recovery guidance:
  - "When a test fails: read the test, understand what it's asserting, fix the code (not the test) unless the test is wrong"
  - "When uncertain about correct behavior: check docs/specs/ first. If not there, stop and flag with a PR comment."
  - "Never delete a test to make CI pass. If a test is wrong, add a comment explaining why and flag for human review."
- Document the most common failure patterns with their resolutions

---

## The Diagnosis Output

After running all 5 categories, Lucy summarizes:

```
ENVIRONMENT DIAGNOSIS REPORT

Category 1 — Feedback Signal Quality: [PASS / FIX NEEDED]
  → [Actions taken or recommended]

Category 2 — Constraint Enforcement: [PASS / FIX NEEDED]
  → [Actions taken or recommended]

Category 3 — Context Completeness: [PASS / FIX NEEDED]
  → [Actions taken or recommended]

Category 4 — Scope Clarity: [PASS / FIX NEEDED]
  → [Actions taken or recommended]

Category 5 — Recovery Path: [PASS / FIX NEEDED]
  → [Actions taken or recommended]

Root cause: [Primary category that caused the failure]
Changes made: [List of files updated]
AGENTS.md updated: [Yes/No — what was added]
Expected outcome: [What should be different in the next build cycle]
```

**Lucy says:**
> "Environment updated. Resume the build loop — the same failure type should not recur. If it does, we have a more fundamental issue in Category [N] and need to dig deeper."
