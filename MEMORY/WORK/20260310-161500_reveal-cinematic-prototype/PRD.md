---
task: Build /reveal-cinematic route using cinematic-animation skill
slug: 20260310-161500_reveal-cinematic-prototype
effort: standard
phase: complete
progress: 11/11
mode: interactive
started: 2026-03-10T16:15:00-06:00
updated: 2026-03-10T16:15:00-06:00
---

## Context

Michael wants a second reveal prototype at `/reveal-cinematic` that uses the cinematic-animation skill's component library (CinematicHeading, StreamingParagraph, GlowingSection, RevealInput, AssemblyTimeline) to create the same three-phase reveal experience. This lets him compare Option 1 (hand-coded RevealPage) vs Option 3 (skill-driven approach) side by side.

Key differences from Option 1:
- Word-by-word streaming (StreamingParagraph) vs character-by-character
- GlowingSection containers with pulsing amber borders
- AssemblyTimeline with timeline dots and track lines
- RevealInput with command-line-style prefix
- Blur-to-sharp per-word animation vs per-character

Uses same mockBriefing data. Same dark canvas aesthetic. Same three phases: input → generating → presenting.

### Risks
- Component library patterns may not compose cleanly into three-phase flow
- Word-by-word streaming may feel slower or less cinematic than character-by-character

## Criteria

- [x] ISC-1: RevealCinematicPage.tsx created in src/pages/reveal/ directory
- [x] ISC-2: Route /reveal-cinematic added to App.tsx outside AuthLayout
- [x] ISC-3: Uses CinematicHeading component from skill for title reveal
- [x] ISC-4: Uses StreamingParagraph component from skill for text streaming
- [x] ISC-5: Uses GlowingSection component from skill for section containers
- [x] ISC-6: Uses AssemblyTimeline pattern from skill for section orchestration
- [x] ISC-7: Three phases implemented: input → generating → presenting
- [x] ISC-8: Reuses mockBriefing data from existing reveal directory
- [x] ISC-9: Dark canvas background with amber/gold accent colors
- [x] ISC-10: Existing /reveal route unchanged
- [x] ISC-A1: No modification to RevealPage.tsx

## Decisions

## Verification

- All 11 criteria pass
- TypeScript compiles clean
- RevealPage.tsx untouched (git diff empty)
- New file: RevealCinematicPage.tsx (16.4KB)
- Route: /reveal-cinematic added outside AuthLayout
