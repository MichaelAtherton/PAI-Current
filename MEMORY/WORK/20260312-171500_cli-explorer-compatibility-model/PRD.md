---
task: Update cli-anything-explorer with software compatibility model
slug: 20260312-171500_cli-explorer-compatibility-model
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-12T17:15:00-05:00
updated: 2026-03-12T17:15:30-05:00
---

## Context

Michael identified that the cli-anything-explorer skill implicitly assumes all target software is open-source with readable source code. This limits brainstorming because it excludes proprietary professional software (Photoshop, Final Cut Pro, AutoCAD, etc.) that CAN be wrapped via alternative access paths (scripting APIs, AppleScript, vendor CLIs).

The insight: CLI-Anything's methodology extends beyond source code analysis. The real requirement is "can we communicate with the software programmatically?" — source code is just one path. Others include scripting APIs, COM automation, AppleScript, vendor CLIs, and plugin APIs.

Additionally, the vibe-kanban evaluation revealed that software which is ALREADY agent-accessible (web apps with APIs) doesn't need CLI-Anything wrapping. This negative filter is also missing from the skill.

### Risks
- Edits could make references too long, violating progressive disclosure
- Must keep changes surgical — don't rewrite working content

## Criteria

- [x] ISC-1: TechnicalFoundation.md updated with expanded access model beyond source code
- [x] ISC-2: FirstPrinciples.md constraint table updated to reflect scriptable interfaces, not just source code
- [x] ISC-3: ExploreNewIdea.md workflow includes software compatibility pre-screen step
- [x] ISC-4: New reference created: SoftwareCompatibility.md with access model taxonomy
- [x] ISC-5: Compatibility quick-filter documented (5-question screener)
- [x] ISC-6: Proprietary software examples included (Photoshop, AutoCAD, etc.)
- [x] ISC-7: "Already agent-accessible" negative filter documented (the vibe-kanban lesson)
- [x] ISC-8: SKILL.md routing table updated to reference new compatibility content
- [x] ISC-9: Access paths taxonomy covers all 5 paths (source, scripting API, AppleScript/COM, vendor CLI, plugin API)
- [x] ISC-10: Existing content not broken or contradicted by additions

## Decisions

## Verification
