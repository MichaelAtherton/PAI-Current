---
task: Implement Phase 4 deployment per implementation spec
slug: 20260323-000000_phase4-deployment-nightly-system
effort: advanced
phase: execute
progress: 33/33
mode: interactive
started: 2026-03-23T00:00:00Z
updated: 2026-03-23T00:01:00Z
---

## Context

Implement Phase 3-4 deployment from `/home/abba/Documents/apps/nanoclaw-ubunto24/docs/design/PHASE3_4_DEPLOYMENT_IMPL.md`. This covers Checkpoints 9-14b: deploying atlas-extract as a persistent systemd service, building the batch extraction script, GPU swap orchestration for nightly runs, and the timer system.

The spec is fully defined with Michael's decisions: sequential retains, continue on failure, Telegram + log file, `--count-only` for nightly skip, `ExecStopPost` safety net. 6 files to create, ~300 lines total.

Current state: orphan python process on port 8300 from testing, 5 systemd services running, vLLM venv and model present on disk, .env has Telegram credentials.

### Risks
- R1: vLLM fails to start → EXIT trap restores daytime services
- R3: Hindsight crashes during batch → continue on failure, retry next night
- R7: Embedding/transcription don't restart → ExecStopPost safety net
- R10: Orphan process on :8300 → kill before deploying service
- chromadb Python package not installed → use REST API with requests instead
- No MAIN_CHAT_ID in .env → Michael needs to add this for Telegram alerts

## Criteria

### CP9: atlas-extract.service
- [x] ISC-1: Orphan process on port 8300 killed before service creation
- [x] ISC-2: atlas-extract.service file written to ~/.config/systemd/user/
- [x] ISC-3: Service has After=hindsight.service dependency
- [x] ISC-4: Service has Restart=always with RestartSec=5
- [x] ISC-5: Service environment sets EXTRACT_PORT, HINDSIGHT_URL, BANK_ID
- [x] ISC-6: systemctl --user enable atlas-extract succeeds
- [x] ISC-7: systemctl --user start atlas-extract succeeds
- [x] ISC-8: curl localhost:8300/health returns status ok

### CP9b: vllm-extraction.service
- [x] ISC-9: vllm-extraction.service file written to ~/.config/systemd/user/
- [x] ISC-10: Service ExecStart uses /home/abba/vllm-venv/bin/vllm with correct model path
- [x] ISC-11: Service has --max-model-len=16384 and --max-num-seqs=8
- [x] ISC-12: Service has NO [Install] section (not enabled, manual start only)

### CP10-11b: atlas-extract-batch.py
- [x] ISC-13: Script accepts --chromadb-url, --extract-url, --hindsight-url, --collection, --bank-id args
- [x] ISC-14: --count-only prints unprocessed URL count and exits
- [x] ISC-15: --dry-run shows what would be processed without POSTing
- [x] ISC-16: --limit N processes at most N URLs then stops
- [x] ISC-17: Chunk reassembly groups by URL, sorts by chunk_index, joins with spaces
- [x] ISC-18: Each URL POSTed to service's POST /extract endpoint
- [x] ISC-19: Continue on failure — failed URL logged, next URL attempted
- [x] ISC-20: After all retains: POST consolidate to Hindsight, POST reflect to service
- [x] ISC-21: Summary printed to stdout (Telegram-ready format)
- [x] ISC-22: --log-file writes detailed per-URL results

### CP12-12b: atlas-nightly-extract.sh
- [x] ISC-23: Phase 0 runs --count-only, exits 0 if nothing new
- [x] ISC-24: Phase 1 stops embedding and transcription services
- [x] ISC-25: Phase 2 starts vllm-extraction and polls health with 120s timeout
- [x] ISC-26: EXIT trap always restores daytime services (embedding + transcription)
- [x] ISC-27: Script is executable (chmod +x)

### CP13-14b: Nightly service + timer
- [x] ISC-28: atlas-nightly.service has ExecStopPost restoring daytime services
- [x] ISC-29: atlas-nightly.service has TimeoutStartSec=14400
- [x] ISC-30: atlas-nightly.timer fires at 23:00 daily with Persistent=true
- [x] ISC-31: Timer enabled via systemctl --user enable

### Anti-criteria
- [x] ISC-A1: Existing Phase 1-2 service code NOT modified
- [x] ISC-A2: Existing 5 running services NOT disrupted (except brief atlas-extract restart)

## Decisions

## Verification
