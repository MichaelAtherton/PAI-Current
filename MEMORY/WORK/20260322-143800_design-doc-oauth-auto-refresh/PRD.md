---
task: Design doc for NanoClaw OAuth auto-refresh
slug: 20260322-143800_design-doc-oauth-auto-refresh
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-22T14:38:00-06:00
updated: 2026-03-22T14:45:00-06:00
---

## Context

Design doc for NanoClaw to auto-refresh OAuth tokens. Claude Max uses OAuth only — no standalone API keys. Written to `docs/design/AUTO_REFRESH_OAUTH.md` in NanoClaw repo.

## Criteria

- [x] ISC-1: Design doc follows DYNAMIC_OAUTH.md format exactly
- [x] ISC-2: Problem statement references specific overnight 401 failure
- [x] ISC-3: Current vs proposed flow diagrams included
- [x] ISC-4: Token refresh endpoint and parameters documented
- [x] ISC-5: Proactive refresh timer strategy specified with exact timing
- [x] ISC-6: Atomic file write pattern specified for credentials.json
- [x] ISC-7: Race condition analysis table included
- [x] ISC-8: Data safety guarantee table included
- [x] ISC-9: Acceptance criteria with verification steps (28 ACs across 6 steps)
- [x] ISC-10: Rollback plan included

## Decisions

- Proactive refresh at 75% of token lifetime (~6h for 8h tokens)
- Reactive fallback on 401 as safety net
- Atomic write via temp file + rename
- Mutex to prevent concurrent refresh attempts
- All changes isolated to credential-proxy.ts + tests

## Verification

All 10 criteria verified by reading the written document. 403 lines, 28 acceptance criteria, 7-row race condition table, 8-row data safety table.
