---
task: Implement /reset command per approved design spec
slug: 20260321-170000_implement-reset-command
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-21T17:00:00-05:00
updated: 2026-03-21T17:00:00-05:00
---

## Context

Implement the `/reset` Telegram command for NanoClaw per the approved design doc (RESET_COMMAND.md) and implementation spec (RESET_COMMAND_IMPL.md). 5 production file changes, 3 test file changes.

## Criteria

- [x] ISC-1: deleteSession function added to src/db.ts
- [x] ISC-2: deleteSession tests pass in db.test.ts (27/27)
- [x] ISC-3: killProcess method added to src/group-queue.ts
- [x] ISC-4: killProcess tests pass in group-queue.test.ts (16/16)
- [x] ISC-5: /reset command handler added to telegram.ts
- [x] ISC-6: onReset added to TelegramChannelOpts and ChannelOpts interfaces
- [x] ISC-7: /reset tests pass in telegram.test.ts (53/53)
- [x] ISC-8: onReset wired in index.ts with deleteSession import
- [x] ISC-9: npm run build succeeds with zero errors
- [x] ISC-10: All existing + new tests pass (321/321 across 20 files)

## Decisions

## Verification
