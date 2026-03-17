# AgentBuild — Edge Case Generation Workflow

Systematic method for generating edge cases and failure modes that PMs and founders don't know they don't know.

**Invoke when:** A happy path spec exists and needs to be hardened before build.

---

## The Knowledge Gap Problem

The fundamental challenge: you can only specify what you can imagine. But real users will do things you didn't imagine, and real systems will fail in ways you didn't anticipate.

This workflow generates those cases *before* they become production incidents.

---

## The Synthetic User Protocol

Five agent personas, each probing your spec for gaps from a different angle.

**Lucy invokes Council with this prompt:**

```
You are five different agents, each playing a distinct user persona interacting with this feature specification. I will give you the spec. For each persona, generate 3-5 edge cases this spec does not handle.

SPEC:
[paste full feature spec here]

PERSONA 1 — The Ideal User
Profile: Uses the product exactly as intended. Reads documentation. Does everything right.
Question: Even ideal usage can hit edge cases at scale or in sequence. What would surprise even this user?
Output format: [Triggering condition] → [What happens with current spec] → [What should happen]

PERSONA 2 — The Confused First-Timer
Profile: Never seen this type of product before. No domain knowledge. Will misread every label.
Question: What will they try that seems logical to them but breaks the spec?
Output format: [Triggering condition] → [What happens with current spec] → [What should happen]

PERSONA 3 — The Power User
Profile: Expert. Will push every limit, find every shortcut, use every parameter to its boundary.
Question: What boundary does this spec fail to define? What happens at the edges of allowed behavior?
Output format: [Triggering condition] → [What happens with current spec] → [What should happen]

PERSONA 4 — The Adversarial User
Profile: Actively trying to break, abuse, or exploit the system. Assumes good-faith behavior is optional.
Question: What can they do that the spec permits but shouldn't? What can they exploit?
Output format: [Triggering condition] → [What happens with current spec] → [What should happen]

PERSONA 5 — The System Administrator
Profile: Responsible for this at 3am when it breaks. Needs to diagnose quickly with incomplete information.
Question: When this fails, what information does the admin NOT have? What does the system not log, not report, not surface?
Output format: [Triggering condition] → [What happens with current spec] → [What should happen]
```

**Lucy presents results:**

> "Council generated [N] edge cases across 5 personas. For each, decide:
> - **Include** → add to spec, will be covered in tests
> - **Exclude** → out of scope for MVP (state why)
> - **Defer** → post-MVP (add to backlog, not spec)
>
> [List edge cases by persona with Include/Exclude/Defer prompt for each]"

---

## Domain Failure Mode Research

**Lucy invokes Research skill:**

> "Research: What are the most common failure modes in [domain/feature type] applications? Include: API failures, data consistency issues, race conditions, timeout scenarios, and user-state corruption. Return the top 10 with descriptions and recommended handling."

**Lucy presents and asks:**
> "Research found [N] domain failure modes. For each, does your current spec define the correct behavior? If not, we add it."

---

## System Failure Specification

**Lucy generates directly (no skill needed — standard prompts):**

For each feature, Lucy runs through this failure matrix:

```
SYSTEM FAILURES — for [feature name]:

1. Database unavailable at request time
   → What should happen? [user-facing message? retry? fail silently?]

2. Upstream service returns 500
   → What should happen? [degrade gracefully? surface error? queue for retry?]

3. Request timeout (>30s)
   → What should happen? [cancel? queue? inform user?]

4. Partial write failure (wrote to A, failed writing to B)
   → What should happen? [rollback? compensate? alert?]

5. Session expiry mid-action
   → What should happen? [save state? lose state? prompt re-auth?]

6. Concurrent access (two users modifying same resource simultaneously)
   → What should happen? [last write wins? first write wins? conflict error?]

7. Input technically valid but semantically wrong
   → What should happen? [accept? reject? warn?]

8. Rate limit hit mid-flow
   → What should happen? [queue? fail? inform with retry-after?]
```

**Lucy asks for each:** "What is the correct behavior?" Each answer becomes a CONSTRAINT block in the spec.

---

## Constraint Mining Session

For founders and PMs who have tacit knowledge not yet in the spec.

**Lucy says:**

> "Let's surface the rules that live in your head. I'll ask questions — your answers become business constraints in the spec.
>
> **Q1:** What would make this product feel broken even if technically it worked? (User expectation constraints)
>
> **Q2:** What can users never do, no matter what? (Hard prohibitions — legal, business, ethical)
>
> **Q3:** What are you charging for? What are you giving away free? (Entitlement and tier constraints)
>
> **Q4:** Who is NOT allowed to use this at all? (Access constraints)
>
> **Q5:** What's the worst thing a user could do that the system currently wouldn't prevent? (Gap in prohibitions)"

**Lucy formats each answer as a CONSTRAINT block:**

```
CONSTRAINT: [name derived from the rule]
RULE: [exact rule as stated]
EXAMPLE VIOLATION: [concrete scenario that breaks this rule]
ENFORCEMENT: [what the system does when violated — error, block, log, alert]
```

---

## Output: Hardened Spec

After this workflow completes, the feature spec contains:

1. **Happy path** (from user)
2. **Approved edge cases** (from Synthetic User Protocol, with Include decisions)
3. **System failure behaviors** (from failure matrix)
4. **Domain failure modes** (from Research, with user decisions)
5. **Business constraints** (from Constraint Mining Session)

**Lucy says:**
> "Spec is hardened. Invoking IterativeDepth for final completeness review before we build..."

**Invoke IterativeDepth:**
> "Review this complete spec from 4 angles: QA engineer (what's missing from tests?), security engineer (what's unspecified that creates vulnerability?), new engineer (what's ambiguous that would cause them to implement incorrectly?), customer success rep (what doesn't match how users actually behave?). Flag all gaps."

**Address any gaps, then:**
> "Specification complete. Saving to `docs/specs/features/[feature-name].md`. Ready for the build loop."
