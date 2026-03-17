# Workflow: MeasureSuccess

> Determine what tier of success has been achieved and what must be true before advancing to the next tier. Used at MVP Gate and at any point during a build to assess standing.

**Invoke when:** "measure success", "are we successful", "what tier are we at", "check MVP", combined with any build that has deployed code

---

## The Three-Tier Model

Success is a progression, not a menu. Tier 1 must be achieved before Tier 2 is meaningful. Tier 2 must be working before Tier 3 is possible.

```
Tier 1: Infrastructure Deployed (no crashes, no errors)
    ↓ (only attempt after Tier 1 passes)
Tier 2: User Can Complete Journey (end-to-end success)
    ↓ (only attempt after Tier 2 passes)
Tier 3: Autonomous Recovery (system learns from failure)
```

---

## Tier 1: Infrastructure Deployed

**Definition:** The application runs and responds without crashes, missing dependencies, or environment configuration failures.

**Checks:**

| Check | How to Verify | Pass Signal |
|-------|--------------|-------------|
| Application starts | Health check endpoint | `GET /health` returns 200 |
| All services connected | Test each dependency | DB query succeeds, auth check succeeds |
| No fatal errors at startup | Observability logs | Railway logs show no ERROR or FATAL on startup |
| CI is green | Build pipeline | GitHub Actions / CI shows ✓ on last commit |
| Environment variables set | Health check or env audit | No "undefined" or "missing key" errors |
| Deployment platform live | Railway dashboard | Service shows "Active" status |

**Tier 1 Score:**

```
Tier 1: [N/6 checks passing]

Pass: 6/6 — Infrastructure healthy. Proceed to Tier 2.
Warn: 4-5/6 — Infrastructure partially healthy. Fix failing checks before user testing.
Fail: <4/6 — Infrastructure broken. Do not attempt Tier 2 — it will give false results.
```

**Common Tier 1 Failures and Fixes:**

| Failure | Likely Cause | Fix |
|---------|-------------|-----|
| Health check 503 | Service still starting | Increase `healthcheckTimeout` in `railway.toml` |
| DB connection refused | Wrong `DATABASE_URL` | Verify Railway variable references the correct database |
| Auth check 401 | Missing or wrong API keys | Check Clerk keys in Railway environment variables |
| Build fails | Missing dependency | Run `bun install` locally, check `bun.lock` is committed |

---

## Tier 2: User Can Complete Journey

**Definition:** A real person (not the builder) can open the application and complete the core user journey described in Phase 0 without hitting an error page or dead end.

**Pre-condition:** Tier 1 must be 6/6 before running Tier 2 checks.

**Checks:**

| Check | How to Verify | Pass Signal |
|-------|--------------|-------------|
| Happy path completable | Browser: walk the path manually | User reaches the success state from Phase 0 |
| No 4xx/5xx on happy path | Browser → network tab or Sentry | Zero errors during the core journey |
| Error states handled gracefully | Trigger each failure mode from spec | Error message shown, not blank page or stack trace |
| Data persists correctly | Complete journey, reload, check data | Data from the journey is still present after refresh |
| Mobile-readable (if web) | Resize to 375px width | Core journey completable on mobile width |
| Onboarding works without context | Have someone unfamiliar try it | They complete the journey without asking you for help |

**Tier 2 Score:**

```
Tier 2: [N/6 checks passing]

Pass: 6/6 — Users can succeed. Proceed to Tier 3 if desired.
Warn: 4-5/6 — Users mostly succeed but hit friction. Note blockers for next build loop.
Fail: <4/6 — Users fail before completing the journey. Run BuildLoop before measuring again.
```

**The "Unfamiliar User" Test:**

> Give the URL to someone who has never seen the product. Tell them only what the product is supposed to do (not how to use it). Watch them use it. Do not explain anything. Note every point of confusion. Every confusion is a spec gap.

This is the most reliable Tier 2 verification. Screenshots and network tab audits are secondary.

---

## Tier 3: Autonomous Recovery

**Definition:** When the system encounters an error, it classifies the error, attempts a fix from the known fix library, and documents the outcome — without human intervention.

**Pre-condition:** Tier 2 must be 6/6 before Tier 3 is meaningful. Autonomous recovery on a broken user journey is not success.

**Checks:**

| Check | How to Verify | Pass Signal |
|-------|--------------|-------------|
| Error classification working | Trigger a known error type | Error correctly classified (infrastructure / logic / spec / environment) |
| Known fix library populated | Count entries in `docs/known-fixes/` | At least 3 documented fixes from past build sessions |
| 3-attempt budget enforced | Trigger an unresolvable error | System escalates after 3 attempts, does not loop infinitely |
| Escalation path working | Let 3 attempts fail | Human-readable escalation report generated |
| Fix documentation saved | Resolve an error autonomously | Resolution saved to `docs/known-fixes/` for next time |
| AGENTS.md updated after fix | Complete a recovery cycle | AGENTS.md reflects newly discovered environment knowledge |

**Tier 3 Score:**

```
Tier 3: [N/6 checks passing]

Pass: 6/6 — True autonomous recovery. The system learns from failure.
Warn: 3-5/6 — Partial autonomy. Some error types handled, others need human help.
Fail: <3/6 — No meaningful autonomy. Tier 3 is not yet achieved.
```

**Reality Check:**

Tier 3 is not built in a single session. It emerges from multiple build cycles where each manual recovery produces a documented fix. After 4-6 builds, the known fix library is large enough to handle most failures. The first build's Tier 3 score is expected to be 0-2/6.

---

## Maturity Score

Combine all tiers into a single score after each build:

```
AgentBuild Maturity Score
═════════════════════════

Tier 1 (Infrastructure):  [N/6] ████████░░  [N*100/6]%
Tier 2 (User Journey):    [N/6] ████░░░░░░  [N*100/6]%
Tier 3 (Autonomy):        [N/6] ██░░░░░░░░  [N*100/6]%

Overall: [T1+T2+T3]/18 = [score]%

Build #[N] | Date: [date] | Project: [project name]
```

Track this score across builds. The progression from Build 1 to Build 5 should show clear Tier 1 and Tier 2 improvement. Tier 3 grows slowly — that is expected.

---

## Output Format

After running MeasureSuccess, produce this report:

```markdown
## Build Success Report — [Project Name] — [Date]

### Tier 1: Infrastructure [N/6]
[Pass/Warn/Fail] — [1-sentence summary]
Failing checks: [list or "none"]

### Tier 2: User Journey [N/6]
[Pass/Warn/Fail] — [1-sentence summary]
Failing checks: [list or "none"]
Unfamiliar user test: [passed / not yet run / failed: describe blocker]

### Tier 3: Autonomous Recovery [N/6]
[Pass/Warn/Fail] — [1-sentence summary]
Known fixes documented: [count]
Failing checks: [list or "none"]

### Overall Maturity: [score]%

### Recommended Next Actions
1. [Most impactful next action to improve score]
2. [Second action]
3. [Third action]
```

---

## Integration

- **Invoked by:** `Workflows/MvpGate.md` (Gate 1: Core Value Demonstrable)
- **Feeds into:** `Workflows/ErrorRecovery.md` (when Tier 2 failures involve errors)
- **Feeds into:** `Workflows/BuildRetrospective.md` (at end of build cycle)
- **Updates:** `docs/known-fixes/` (Tier 3 documentation)
