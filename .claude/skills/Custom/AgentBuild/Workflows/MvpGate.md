# AgentBuild — MVP Gate Workflow

MVP is not "all features built." MVP is "the core value is demonstrable and the feedback loop is working."

**Invoke when:** All planned MVP features have completed the build loop, or you want to assess readiness.

---

## The Gate (6 Items — All Must Pass)

**Lucy walks through each item:**

### Gate 1: Core Value Demonstrable

> "Can you show this to a real user right now and have them experience the value proposition from Phase 0?
>
> Phase 0 said: '[restate the two locked sentences]'
>
> Can someone do that thing, and does the result match what you said? Not a demo — a real user, live."

**Pass:** Yes, a real user can experience the core value proposition.
**Fail:** No, it's not ready for a real user yet. (Return to build loop for the blocking feature.)

---

### Gate 2: CI Is Green

> "Is CI passing on main right now? Not on a branch — on main."

**Lucy checks:** Run or inspect the current CI status on the main branch.

**Pass:** All CI checks green on main.
**Fail:** CI is failing on main. Fix before evaluating other gates.

---

### Gate 3: Observability Is Live

> "Can you see what's happening in production? Check:
> - Error tracking (Sentry or equivalent): are errors flowing in?
> - Request logs: are you seeing request data?
> - Business metrics: are the 3-5 events from Phase 6 firing?
> - Health check: does /health return 200?"

**Invoke Browser** to verify dashboards are active.

**Pass:** All four observability checks confirmed live.
**Fail:** Setup is incomplete. Return to Phase 6.

---

### Gate 4: At Least One Real User Has Confirmed Value

> "Has at least one real human — not you, not a teammate who built it — used this and confirmed the value proposition?
>
> This is the non-negotiable MVP gate. 'It works on my machine' is not MVP. A real user saying 'this solves my problem' is MVP."

**Pass:** Real user has confirmed value proposition.
**Fail:** Not yet. The next step is getting the first real user, not building more features.

---

### Gate 5: Environment Diagnosis Has Run At Least Once

> "Have we run the Environment Diagnosis workflow at least once on this project?
>
> The purpose isn't to find failures — it's to verify the environment is set up for sustainable iteration. If we haven't diagnosed the environment, we don't know what breaks next will look like."

**Pass:** `Workflows/EnvironmentDiagnosis.md` has been run and the report exists.
**Fail:** Run it now before calling MVP. (Takes ~30 minutes.)

---

### Gate 6: AGENTS.md Reflects Current State

> "Is AGENTS.md current? Does it reflect the repo as it exists right now — directory structure, conventions, how tests run, what 'done' means?
>
> AGENTS.md is the next agent's onboarding document. If it's outdated, the next build cycle starts with a broken environment."

**Lucy reads AGENTS.md and the current repo structure, flags discrepancies.**

**Pass:** AGENTS.md matches current repo state.
**Fail:** Update AGENTS.md before declaring MVP. (This is a build task for the agent.)

---

## Gate Results

**Lucy summarizes:**

```
MVP GATE RESULTS

Gate 1 — Core Value Demonstrable: [PASS / FAIL]
Gate 2 — CI Green on Main: [PASS / FAIL]
Gate 3 — Observability Live: [PASS / FAIL]
Gate 4 — Real User Confirmed: [PASS / FAIL]
Gate 5 — Environment Diagnosed: [PASS / FAIL]
Gate 6 — AGENTS.md Current: [PASS / FAIL]

Result: [MVP READY / NOT READY — N gates failing]
```

**If all pass:**
> "MVP confirmed. You have:
> - Working software delivering real value to a real user
> - A green CI pipeline
> - Observability into what's happening
> - A diagnosed environment ready for the next build cycle
>
> The loop continues. Every new feature starts at Phase 2 (edge case generation). Every production incident is a spec update. The factory keeps running."

**If any fail:**
> "Not MVP yet — [N] gates failing. Here's what blocks you: [list failing gates with specific next actions for each]."
