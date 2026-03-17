# Constraint Specification Format

Business constraints are the rules that must always be true across the entire system. Unlike feature specs (which describe what happens when things go right), constraint specs describe invariants — rules the system must never violate.

**Location:** `docs/specs/constraints/` — organized by domain (business-rules.md, security.md, access-control.md, etc.)

---

## Template

```markdown
# Constraints: [Domain Name]

> [One sentence: what category of rules this file covers]

**Last updated:** [date]
**Enforced by:** [mechanical enforcement: middleware / lint rule / test suite / all three]

---

## [Constraint Name]

CONSTRAINT: [Constraint name — short, descriptive, searchable]
RULE: [The exact rule in one sentence. No hedging. "Free accounts cannot..." not "Free accounts should not..."]
EXAMPLE VIOLATION: [Concrete scenario — specific user, specific action, specific threshold crossed]
ENFORCEMENT: [What the system does — HTTP status, error message, log event, alert]
TESTS: [Test file and test name that verifies this constraint]

---

## [Next Constraint Name]

CONSTRAINT: [Name]
RULE: [Rule]
EXAMPLE VIOLATION: [Scenario]
ENFORCEMENT: [Response]
TESTS: [Reference]
```

---

## Example: Business Rules

```markdown
# Constraints: Business Rules

> Entitlement, rate limiting, and access rules that govern product behavior.

**Last updated:** 2026-02-19
**Enforced by:** Middleware (rate limits), test suite (all)

---

## Free Tier API Limits

CONSTRAINT: Free tier daily API limit
RULE: Free accounts cannot make more than 100 API calls per 24-hour rolling window
EXAMPLE VIOLATION: Free user makes their 101st API call at 11:45pm
ENFORCEMENT: Return HTTP 429. Body: {"error": "daily_limit_reached", "limit": 100, "reset_at": "[timestamp]", "upgrade_url": "/billing"}. Log event: rate_limit_hit with user_id and timestamp.
TESTS: tests/middleware/rate-limit.test.ts → "should return 429 on 101st request for free tier"

---

## Trial Period Expiry

CONSTRAINT: Trial account feature access
RULE: Trial accounts lose access to paid features exactly at trial expiry timestamp, not at end of day
EXAMPLE VIOLATION: Trial expired at 14:32 but user can still access export feature at 14:45
ENFORCEMENT: Every request to a paid feature checks trial_expires_at against current timestamp. Return HTTP 402 if expired. Body: {"error": "trial_expired", "expired_at": "[timestamp]", "upgrade_url": "/billing"}
TESTS: tests/middleware/auth.test.ts → "should deny paid feature access after trial expiry"
```

---

## Example: Security Constraints

```markdown
# Constraints: Security

> Authentication, authorization, and data protection rules.

---

## Cross-Account Data Access

CONSTRAINT: User data isolation
RULE: No user can read, modify, or delete data owned by another user, even if they know the resource ID
EXAMPLE VIOLATION: User A calls GET /api/documents/123 where document 123 belongs to User B
ENFORCEMENT: Every data access query includes WHERE user_id = [authenticated_user_id]. Return HTTP 404 (not 403) to avoid confirming resource existence.
TESTS: tests/api/documents.test.ts → "should return 404 for document owned by different user"

---

## Session Token Expiry

CONSTRAINT: Session token lifetime
RULE: Session tokens expire after 24 hours of inactivity, not 24 hours from issuance
EXAMPLE VIOLATION: User token issued at 9am is rejected at 9:01am the next day even though user was active at 8:55am
ENFORCEMENT: Sliding expiry — reset expiry timestamp on every authenticated request. Last-active stored in token or session store.
TESTS: tests/auth/session.test.ts → "should extend session on active use"
```

---

## Constraint Quality Checklist

Before a constraint is considered complete:

- [ ] RULE is a single declarative sentence with no ambiguity ("cannot" not "should not")
- [ ] EXAMPLE VIOLATION is specific — names the user type, action, and threshold
- [ ] ENFORCEMENT names the HTTP status, error body format, and any logging/alerting
- [ ] TESTS references the specific test file and test name (not "add tests")
- [ ] ENFORCED BY notes whether mechanical enforcement exists (middleware, lint) or only test coverage

**Constraints without mechanical enforcement are aspirational, not actual.** If a constraint is worth having, it's worth enforcing automatically, not just testing.
