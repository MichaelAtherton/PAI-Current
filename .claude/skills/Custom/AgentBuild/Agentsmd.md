 # AGENTS.md Template and Protocol

AGENTS.md is the most important file in any agentic repository. It is the agent's operating manual — the single source of truth for how to work in this specific repo. Every agent that ever touches this repo reads this first.

**Location:** Always at the repo root: `/AGENTS.md`

---

## Template

Copy this into the generated AGENTS.md. Replace all `[bracketed]` values.

```markdown
# AGENTS.md — [Project Name]

> [One sentence from Phase 0: what this does for whom]

**MVP Done When:** [One sentence from Phase 0: what done looks like]

---

## Project Context

### What This Is
[2-3 sentences of domain context. What makes this different from a generic [type] project. Include the domain-specific constraints that an agent wouldn't know by default.]

### What This Is NOT
[1-2 sentences on what's explicitly out of scope. Prevents agents from wandering into adjacent features.]

---

## Repository Structure

```
/
├── AGENTS.md              ← This file. Read first. Always.
├── README.md              ← User-facing description
├── src/                   ← Application source code
│   └── [structure here]
├── tests/                 ← All tests live here, mirroring src/ structure
├── docs/
│   └── specs/
│       ├── MASTER.md      ← Index of all specs — start here for context
│       ├── features/      ← Feature specs — what to build
│       ├── constraints/   ← Business rules — what must always be true
│       └── architecture/  ← Decisions — why things are the way they are
├── .github/
│   └── workflows/
│       ├── ci.yml         ← Runs on every PR: tests + lint
│       └── deploy.yml     ← Runs on merge to main
└── [other files]
```

**Where things go:**
- New features: `src/[feature-name]/`
- Tests for new features: `tests/[feature-name]/` (mirror the src structure)
- New specs: `docs/specs/features/[feature-name].md`
- New constraints: `docs/specs/constraints/[domain].md`

**Critical:** `docs/` is committed to the GitHub repository alongside the code. It is not local-only, not a scratch folder, not optional. Specs are the source of truth agents build from — they must be version-controlled so any agent in any session can read them cold.

---

## Coding Conventions

### Naming
- Files: `kebab-case.ts`
- Functions: `camelCase`
- Types/Classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- [Add any project-specific naming rules]

### Error Handling
- Never silently swallow errors
- Always include the original error in re-thrown errors
- Error messages must state: what happened, where, what the caller can do about it
- Use structured error types, not string errors
- [Add any project-specific error patterns]

### Logging
- Log at entry and exit of significant operations
- Include correlation IDs on all log lines
- Never log: passwords, tokens, PII, full request bodies with credentials
- Log levels: DEBUG (dev only), INFO (normal operation), WARN (degraded state), ERROR (failure)

### Testing
- Every public function has at least one test
- Every edge case approved in specs has a test
- Tests must be readable — the test name is the documentation
- Test names: `it("should [behavior] when [condition]")`
- Never skip tests. Never delete tests to make CI pass.
- If a test is wrong: add a comment explaining why, create a PR comment flagging it for human review

---

## How to Run Tests

```bash
# Run all tests
[test command]

# Run tests for a specific file
[test command for file]

# Run tests in watch mode
[watch command]
```

---

## How to Run Linter

```bash
# Check lint
[lint command]

# Auto-fix lint issues
[lint fix command]
```

---

## CI Requirements

Every PR must pass before merge:
- [ ] All tests pass
- [ ] Linter passes with zero errors
- [ ] [Any other CI checks]

CI runs automatically on PR creation and every push to the PR branch.

---

## What "Done" Means for Any Task

A task is done when ALL of the following are true:
1. The behavior described in the referenced spec is implemented
2. Tests cover the happy path from the spec
3. Tests cover all edge cases marked "Include" in the spec
4. CI is green (tests + lint)
5. No behavior is present that is NOT in the spec
6. PR description references the spec file

---

## When Tests Fail

1. Read the test output carefully — it tells you what was expected and what was received
2. Find the test that's failing and understand what it's asserting
3. Fix the **code**, not the test (unless the test has a bug — see below)
4. If fixing the code breaks other tests, those other tests are telling you something about your change
5. Never comment out or delete a test to make CI pass
6. If a test is genuinely wrong: add `// FIXME: This test is wrong because [reason]` and flag in your PR description

---

## When Uncertain About Behavior

1. Check `docs/specs/features/` first — look for the relevant spec
2. Check `docs/specs/constraints/` for business rules that apply
3. Check `docs/specs/architecture/decisions.md` for why things are structured the way they are
4. If the spec is silent: do NOT guess. Add a comment in the code explaining the uncertainty and flag in the PR description for human review
5. DO NOT implement behavior not in the spec, even if you think it's a good idea

---

## Domain-Specific Notes

[Add domain context here. Things an agent wouldn't know by default:]
- [Domain term]: [Definition]
- [Key business rule in plain language]
- [Why something counterintuitive is the way it is]
- [Gotcha that caused problems before]

---

## Architecture Decisions

See `docs/specs/architecture/decisions.md` for decisions and their rationale.

**Critical decisions:**
- [Decision 1]: [Why — one sentence]
- [Decision 2]: [Why — one sentence]

---

*Last updated: [date] — always keep this current*
```

---

## AGENTS.md Update Protocol

AGENTS.md is a **living document**. It must be updated whenever:

1. **Directory structure changes** — add new directories, restructure existing ones
2. **Conventions change** — new naming rules, new error handling patterns
3. **Environment diagnosis finds a gap** (Category 3 or 5 most commonly)
4. **An agent asks a follow-up question** — the answer goes here so the next agent doesn't need to ask
5. **A production incident reveals a spec gap** — add domain context explaining the root cause

**Update as a build task:**
```
SPEC: AGENTS.md Update
SCOPE: Update AGENTS.md to reflect [specific change].
TASK: [Specific section to update and what it should say]
DONE WHEN: AGENTS.md reflects current repo state, no stale information remains.
```

**Never let AGENTS.md go stale.** A stale AGENTS.md means the next agent starts with wrong assumptions. It is the most expensive technical debt in an agentic repository.
