---
name: 2PassExtraction
description: Two-pass stakeholder transcript extraction and use case discovery — broad extraction in Pass 1, sharpened recommendations and pre-design synthesis in Pass 2, outputs a structured discovery doc. USE WHEN 2 pass extraction, extract from transcript, discovery pass, document use case, stakeholder extraction, transcript to spec, use case from transcript, extract use case, discovery doc, pass 1, pass 2, sharpen extraction.
---

# 2PassExtraction

Extracts use case intelligence from large stakeholder transcripts using a disciplined two-pass methodology. Produces a structured discovery document ready for user flow design.

---

## When To Use This Skill

- You have a large stakeholder transcript (recorded conversation, interview, demo walkthrough)
- You need to extract a **specific use case or feature area** — not summarize the whole transcript
- You have contextual notes from the user that frame what to look for
- The output needs to be design-ready, not just a summary

---

## Inputs Required

Before starting, confirm you have:

1. **The transcript** — pasted inline or referenced by file path
2. **Focus notes** — user's handwritten or typed notes that frame the use case focus
3. **Output path** — where to write the discovery doc (default: project's `new-coach-profile-specs/` or equivalent)
4. **Use case name** — used for the filename: `{use-case-name}-discovery.md`

---

## Execution

### Pass 1 — Broad Extraction

Read the transcript through the lens of the focus notes. Extract in named categories — don't over-refine yet. Goal: surface everything relevant without losing anything.

Standard categories to populate (skip any that don't apply):

- **What this feature/flow actually is** — the mental model behind it
- **The real-world workflow** — what the user does today, step by step
- **People involved** — roles, relationships, handoffs
- **Information types** — what data exists, where it lives, who owns it
- **Privacy / access concerns** — who sees what
- **Entry points and triggers** — what kicks off the flow
- **Exit conditions** — when is it done
- **Ingestion / capture methods** — how data gets into the system
- **Naming and language** — exact words the stakeholder used
- **What they reacted positively to** — validated elements of existing design
- **What's missing** — gaps they named or implied
- **Future vision (parked)** — things explicitly flagged as not now

Present Pass 1 output inline to the user. Then **stop and ask**: *"Ready for Pass 2?"*

---

### Pass 2 — Sharpening

Re-read Pass 1 with a critical lens. The standard for Pass 2: **recommendations, not just observations**. For every open question, either resolve it with a recommendation or confirm it is genuinely unresolvable from the transcript alone.

Pass 2 checklist — apply to every section:

- [ ] **Make the call** — every "candidate" list needs a winner with rationale. Don't leave naming decisions, placement decisions, or interaction decisions as open lists.
- [ ] **Resolve open questions** — if the transcript contains enough signal to answer a question, answer it. Only leave questions open if they genuinely require a future conversation with the stakeholder.
- [ ] **Reject weak options explicitly** — don't just list alternatives. Say which ones are wrong and why.
- [ ] **Separate ongoing from onboarding** — if a feature persists beyond the initial flow, note where it lives after the setup phase ends.
- [ ] **Define placeholders** — if a category (e.g. "private to leader") is named but not elaborated, define the most likely use cases from context and make a phase 1 / phase 2 recommendation.
- [ ] **Write the pre-design synthesis** — end with a conceptual wireframe-level description of what the redesigned page/flow should look like. This is what bridges the doc to actual design work. ASCII wireframe preferred.

**Self-check before writing the doc:** Ask — *"Am I doing Pass 1 work labeled as Pass 2?"* Pass 2 must contain explicit recommendations, not just more observations. If a section still reads as "here are the options," it hasn't been sharpened.

---

## Output Document Structure

Write the discovery doc to the specified output path. Standard sections:

```
# {Use Case Name} — Stakeholder Discovery
> Source: {stakeholder name}, {date}
> Status: DRAFT — Pass 2 complete, ready for user flow design
> Next step: Design user flow + redesign spec for {target file}

1. What {Feature} Actually Is
2. The Real-World Flow (step-by-step)
3. Information Architecture / Privacy Model
4. Key Named Artifacts (specific fields or objects the stakeholder named)
5. Ongoing vs. Onboarding (what persists, where it lives after setup)
6. Ingestion / Capture Methods
7. What the Tab/Page Holds (content inventory table)
8. Naming Decisions (with recommendation)
9. Completion / Exit Signal (with recommendation)
10. Relationship to Adjacent Features
11. Stakeholder's Reaction to Existing Design
12. Pre-Design Synthesis (conceptual wireframe)
13. Remaining Open Questions (only genuinely unresolved ones)
14. Future Vision (parked)
15. Key Quotes
```

Omit sections that don't apply. Add sections specific to the use case as needed.

---

## Quality Standard

The discovery doc is done when:

- A designer could pick it up cold and know what to build
- Every section has a recommendation or a clear reason why one can't be made yet
- The pre-design synthesis (§12) gives a conceptual layout of the redesigned page
- Open questions (§13) are genuinely open — not lazy deferrals
- The future vision (§14) is captured but clearly parked

---

## Example Invocation

> *"Let's do a 2 pass extraction on the vault use case. Here are my notes: [notes]. Here's the transcript: [transcript]. Write the doc to docs/specs/new-coach-profile-specs/vault-discovery.md"*

The skill will run Pass 1, present it, confirm with the user, then run Pass 2 and write the file.
