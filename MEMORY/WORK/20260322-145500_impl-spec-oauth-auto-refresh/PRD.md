---
task: Technical implementation spec for OAuth auto-refresh
slug: 20260322-145500_impl-spec-oauth-auto-refresh
effort: standard
phase: complete
progress: 8/8
mode: interactive
started: 2026-03-22T14:55:00-06:00
updated: 2026-03-22T15:10:00-06:00
---

## Context

Implementation spec for OAuth auto-refresh, translating AUTO_REFRESH_OAUTH.md design doc into exact code changes with line numbers and before/after diffs.

## Criteria

- [x] ISC-1: Follows DYNAMIC_OAUTH_IMPL.md format (before/after diffs, line numbers)
- [x] ISC-2: All 38 design doc ACs mapped to specific code changes
- [x] ISC-3: credential-proxy.ts changes specified with exact insert points
- [x] ISC-4: index.ts shutdown and alert wiring changes specified
- [x] ISC-5: Test code provided for all new functions
- [x] ISC-6: AC-to-Change mapping table included
- [x] ISC-7: Build and deploy sequence included
- [x] ISC-8: Files NOT modified list included

## Verification

- 1105 lines, 35 AC mappings, 3 files changed
- All 38 ACs from design doc mapped in AC↔Change table
- Caught and documented the scheduling race (scheduleTokenRefresh called from both proxy and index.ts) — revised to single call from index.ts
