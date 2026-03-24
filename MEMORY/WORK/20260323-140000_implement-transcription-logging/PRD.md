---
task: Implement transcription logging per implementation spec
slug: 20260323-140000_implement-transcription-logging
effort: standard
phase: complete
progress: 9/9
mode: interactive
started: 2026-03-23T14:00:00Z
updated: 2026-03-23T14:15:00Z
---

## Context

Implement the transcription logging framework per `docs/design/TRANSCRIPTION_LOGGING_IMPL.md`. 6 checkpoints, 2 files, ~40 lines changed. Adds Python logging module, yt-dlp stderr logging, error_type in responses, timeout handling, and Linus error body parsing.

## Criteria

- [x] ISC-1: Zero print() calls remain in server.py
- [x] ISC-2: journalctl shows [transcription] INFO/ERROR prefix after restart
- [x] ISC-3: yt-dlp stderr appears in journalctl on failure (url + exit_code + stderr)
- [x] ISC-4: URL appears in both success and failure log lines
- [x] ISC-5: error_type field in all error HTTP responses
- [x] ISC-6: subprocess.TimeoutExpired caught separately, returns 504
- [x] ISC-7: Linus SKILL.md reads error response body via urllib.error.HTTPError
- [x] ISC-8: YT_DLP_VERBOSE=1 env var enables --verbose flag
- [x] ISC-9: Service healthy after restart, existing transcription flow unbroken

## Decisions

- Used full rewrite of server.py for clarity (all changes in one pass)
- Added instruction to SKILL.md telling Linus not to guess at cause (e.g., "private video")

## Verification

- ISC-1: `grep -c 'print(' server.py` = 0
- ISC-2: journalctl shows `[transcription] INFO Loading...`, `[transcription] INFO Model loaded...`
- ISC-3: journalctl shows `[transcription] ERROR yt-dlp failed | url=https://example.com/... | exit_code=1 | stderr=ERROR: [generic] Unable to download...`
- ISC-4: Success: `Done in Xs (N chars) url=...`. Failure: `yt-dlp failed | url=...`
- ISC-5: curl bad URL returns `{"error": "...", "error_type": "download_failed", "url": "..."}`
- ISC-6: `grep 'TimeoutExpired' server.py` confirms catch present
- ISC-7: SKILL.md has `except urllib.error.HTTPError as e:` with `e.read()` body parsing
- ISC-8: `grep 'YT_DLP_VERBOSE' server.py` confirms env var check
- ISC-9: Health endpoint returns `{"status": "ok"}`, service active (running)
