---
task: Analyze transcript to define magical landing experience
slug: 20260310-143000_magical-landing-experience-design
effort: extended
phase: complete
progress: 20/20
mode: interactive
started: 2026-03-10T14:30:00-06:00
updated: 2026-03-10T14:32:00-06:00
---

## Context

Michael and Steve Jacobs are building BriefingPro — a platform where executive coaches create hyper-personalized briefings for leaders. Steve has an upcoming May presentation to Mayo Clinic coaches where he needs to demonstrate BriefingPro's vision.

Steve's core problem: he's building a presentation arc that creates "magic in the room" — walking coaches through the limitations of pre-AI coaching, building to an "until now" moment, then revealing what's possible. The landing page/experience is the reveal moment. It CANNOT look like "just another website" or Steve says he "just wouldn't show it."

The task is NOT to build the landing page. It's to deeply analyze Steve's transcript, extract the design requirements for a "magical" experience, assess how the claude-code-design-stack skill can help, and produce a design strategy.

### What the app already is
BriefingPro: React SPA with Clerk auth, client roster, profile, briefing generator (topic + context + personalization → AI-generated white papers), briefing review, delivery, learning journey, and planned podcast generation. Swiss Modernism 2.0 + Bento Box design system. Navy/slate/gold color scheme.

### What Steve needs for the May meeting
Not a marketing landing page. An EXPERIENCE that:
1. Serves as the "reveal" moment after building tension about coaching limitations
2. Makes coaches feel "magic is being created in the room"
3. Shows the platform vision without being a product demo
4. Doesn't overwhelm with features — focused, not a feature dump
5. Could incorporate a live demo moment (type in a topic, generate a briefing in real-time)

### Risks
- Generic SaaS aesthetic would kill the presentation moment
- Too many features shown = coaches tune out
- The experience must work in a PRESENTATION context (projector, audience), not just a browser
- Steve's audience are coaches, not tech people — they need emotional resonance, not feature lists

## Criteria

- [x] ISC-1: Transcript key quotes extracted identifying Steve's emotional bar
- [x] ISC-2: Transcript key quotes extracted identifying what Steve explicitly rejects
- [x] ISC-3: Steve's presentation arc mapped phase by phase
- [x] ISC-4: The "magic moment" requirements defined from Steve's own words
- [x] ISC-5: Anti-patterns identified (what would make Steve skip showing it)
- [x] ISC-6: Audience profile synthesized (Mayo Clinic coaches, not tech users)
- [x] ISC-7: Live demo moment requirements extracted from transcript
- [x] ISC-8: Feature prioritization for the experience (what to show vs hide)
- [x] ISC-9: Design stack tool-to-requirement mapping complete
- [x] ISC-10: UI/UX Pro Max applicability assessed with specific queries
- [x] ISC-11: Google Stitch applicability assessed for mockup generation
- [x] ISC-12: 21st.dev Magic applicability assessed for component generation
- [x] ISC-13: Gap analysis — what the design stack cannot do for this experience
- [x] ISC-14: Presentation-context constraints documented (projector, audience, pacing)
- [x] ISC-15: Emotional design principles identified for "magical" feel
- [x] ISC-16: Recommended design direction synthesized from all analysis
- [x] ISC-17: Comparison to existing BriefingPro aesthetic — what stays vs changes
- [x] ISC-18: Actionable next steps documented with tool-specific instructions
- [x] ISC-A1: No generic SaaS landing page patterns recommended
- [x] ISC-A2: No feature-dump approach recommended

## Decisions

## Verification
