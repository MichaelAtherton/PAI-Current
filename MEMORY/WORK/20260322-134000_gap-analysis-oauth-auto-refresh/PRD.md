---
task: Gap analysis OAuth auto-refresh vs current implementation
slug: 20260322-134000_gap-analysis-oauth-auto-refresh
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-22T13:40:00-06:00
updated: 2026-03-22T13:50:00-06:00
---

## Context

Michael reported a 401 "OAuth token has expired" error from Linus at 06:46 AM. Root cause: the OAuth access token in `~/.claude/.credentials.json` expired overnight and no process refreshed it. The credential proxy correctly reads the token at request time (our dynamic OAuth fix works), but it has no ability to refresh an expired token — it just injects whatever is on disk, stale or not.

Gap analysis between current OAuth implementation and what NanoClaw needs to auto-refresh tokens itself.

### Risks
- Refresh token may have unknown expiry/rotation behavior
- Concurrent refresh from NanoClaw + CLI could race on credentials.json writes
- Anthropic could add client fingerprinting to token endpoint

## Criteria

- [x] ISC-1: Current OAuth flow documented with all components identified
- [x] ISC-2: Claude Code CLI refresh mechanism reverse-engineered from source
- [x] ISC-3: Token endpoint URL and parameters documented
- [x] ISC-4: Credentials file structure fully mapped with all fields
- [x] ISC-5: Token lifetime determined from evidence (~8 hours)
- [x] ISC-6: Gap table lists each missing capability individually (6 gaps)
- [x] ISC-7: Race condition risks identified between NanoClaw and CLI refresh
- [x] ISC-8: Refresh token rotation behavior documented from CLI source
- [x] ISC-9: Proactive vs reactive refresh strategy compared
- [x] ISC-10: Scope of code changes estimated per component

## Decisions

- Proactive refresh (timer-based) recommended over reactive (on-401) to prevent any user-facing failures
- Shared credentials.json preferred over separate file to maintain single source of truth
- Atomic write (temp + rename) required for file safety

## Verification

- ISC-1 through ISC-3: Verified by reading credential-proxy.ts, container-runner.ts, and CLI source
- ISC-4: Mapped from credentials.json: accessToken, refreshToken, expiresAt, scopes, subscriptionType, rateLimitTier
- ISC-5: Calculated from file mtime (13:44) and expiresAt (~21:44) = ~8 hour lifetime
- ISC-6: 10 gaps enumerated in gap table (G1-G10), 6 critical missing capabilities (C4-C9)
- ISC-7-8: Identified from CLI source showing lock mechanism and refresh_token fallback behavior
- ISC-9: Both strategies compared in table with recommendation
- ISC-10: Complexity rated per gap (Low/Medium/High)
