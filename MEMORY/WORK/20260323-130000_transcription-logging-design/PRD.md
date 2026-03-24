---
task: Design doc for transcription service logging framework
slug: 20260323-130000_transcription-logging-design
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-23T13:00:00Z
updated: 2026-03-23T13:05:00Z
---

## Context

The transcription service at `services/transcription/server.py` uses bare `print()` for logging. When yt-dlp fails to download a URL, the stderr is captured in the RuntimeError but never logged to journalctl — it only appears in the HTTP 502 response body, which the Docker agent discards. This makes diagnosing the ~10% failure rate impossible without manual reproduction.

### Risks
- Over-engineering: rewriting all services when only transcription needs fixing
- Breaking existing journalctl log parsing if format changes

## Criteria

- [x] ISC-1: Design doc covers yt-dlp stderr logging on failure
- [x] ISC-2: Design doc specifies Python logging module (not print)
- [x] ISC-3: Design doc preserves journalctl compatibility
- [x] ISC-4: Design doc includes structured error context (URL, exit code, stderr)
- [x] ISC-5: Design doc specifies HTTP response includes error detail
- [x] ISC-6: Design doc scoped to transcription service only
- [x] ISC-7: Design doc includes acceptance criteria for each change
- [x] ISC-8: Design doc written to nanoclaw repo docs/design/
- [x] ISC-9: Design doc addresses the Linus agent visibility gap
- [x] ISC-10: Design doc does not propose changes to other services

## Decisions

- Use Python logging module (matches atlas-extract pattern)
- Preserve [transcription] prefix in format string for journalctl compatibility
- Fix SKILL.md to read HTTPError response body (the visibility gap)
- Add error_type field for future agent intelligence

## Verification

- ISC-1: Change 2 in design doc explicitly covers yt-dlp stderr logging
- ISC-2: Change 1 specifies logging.basicConfig with logger = logging.getLogger("transcription")
- ISC-3: Format string preserves [transcription] prefix
- ISC-4: logger.error includes url=, exit_code=, stderr= fields
- ISC-5: Change 4 adds error_type + url to JSON response
- ISC-6: "What This Does NOT Change" section explicitly excludes other services
- ISC-7: 8 acceptance criteria with verification steps
- ISC-8: Written to docs/design/TRANSCRIPTION_LOGGING.md
- ISC-9: Change 3 fixes urllib.error.HTTPError handling in SKILL.md
- ISC-10: "What This Does NOT Change" section lists 4 unmodified services
