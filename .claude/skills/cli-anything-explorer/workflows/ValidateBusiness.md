# Workflow: Validate a Business Idea

Use this workflow when the user wants to stress-test, red-team, or validate a CLI-Anything business concept before committing resources.

## Prerequisites

Load the relevant idea from `references/ActionableRoadmap.md` or `references/IdeationLandscape.md`, plus `references/FirstPrinciples.md` for grounding.

## Process

### 1. Define the Hypothesis

Every business idea is a stack of hypotheses. Break it down:

- **Market hypothesis**: "There are X potential customers willing to pay $Y for Z"
- **Production hypothesis**: "CLI-Anything can produce Z at quality level Q in time T"
- **Unit economics hypothesis**: "Cost per unit is $C, price is $P, margin is viable"
- **Moat hypothesis**: "Competitors can't easily replicate because of [reason]"
- **Compounding hypothesis**: "This gets better over time because of [flywheel]"

### 2. Red Team the Idea

Invoke **Thinking/RedTeam** with the full context. Seed the red team with:
- The specific idea and its pipeline
- The claimed unit economics
- The target market
- The assumed competitive advantage

The red team should attack from these angles:
- **Technical risk**: Can CLI-Anything actually produce this at the claimed quality?
- **Market risk**: Does the demand exist? Is the price point realistic?
- **Competitive risk**: What stops someone from copying this in 2 weeks?
- **Operational risk**: What breaks at scale?
- **Regulatory risk**: Any legal/compliance issues?

### 3. World/Threat Model

Invoke **Thinking/WorldThreatModelHarness** to test the idea across time horizons:
- **6 months**: What's the realistic state?
- **18 months**: How has the market changed?
- **3 years**: Is this still viable or has it been commoditized?

### 4. Market Research

Invoke **Research** (Standard or Extensive) to answer:
- How big is the actual market? (Not TAM hand-waving — real addressable customers)
- Who are the current players? What do they charge?
- What are customers complaining about with existing solutions?
- Are there regulatory tailwinds or headwinds?

### 5. Feasibility Test

Design the smallest possible test to validate the core hypothesis:
- **What's the MVP?** The simplest version that proves the concept works.
- **How long to build?** Using `workflows/BuildPipeline.md` as the implementation guide.
- **What constitutes success?** Define before building. "Success = 3 paying customers in 30 days" or "Success = pipeline produces deliverable in <2 hours that a human rates 7+/10."

### 6. Decision Framework

After all inputs, score the idea:

| Dimension | Score (1-10) | Evidence |
|---|---|---|
| Market demand | | Research findings |
| Technical feasibility | | Red team + prototype |
| Unit economics | | Cost analysis |
| Defensibility | | Moat analysis |
| Compounding potential | | Flywheel assessment |
| Time to first revenue | | Implementation estimate |

**Go threshold**: Average score >= 7 AND no dimension below 5.
**Pivot threshold**: Average 5-7, investigate what needs to change.
**Kill threshold**: Average < 5 OR any dimension at 1-2.

## Routing to Other Skills

| Need | Skill |
|---|---|
| Deep adversarial critique | **Thinking/RedTeam** |
| Multi-horizon threat modeling | **Thinking/WorldThreatModelHarness** |
| Market/competitor research | **Research** (Standard or Extensive) |
| 4-perspective debate on viability | **Thinking/Council** |
| Scientific hypothesis testing on feasibility | **Thinking/Science** |
