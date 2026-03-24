---
task: Deploy NanoClaw on Ubuntu 24.04 with CUDA GPU services
slug: 20260321-000000_deploy-nanoclaw-ubuntu-cuda
effort: advanced
phase: complete
progress: 26/26
mode: interactive
started: 2026-03-21T14:37:00-05:00
updated: 2026-03-21T16:33:00-05:00
---

## Context

Michael needs NanoClaw (personal AI assistant orchestrator) deployed on Ubuntu 24.04 with NVIDIA RTX 3090 (24GB VRAM). Architecture: 4 host services (NanoClaw orchestrator, ChromaDB, Embedding with Qwen3-VL-8B, Transcription with faster-whisper large-v3) + ephemeral Docker containers as ultra-lightweight HTTP clients. This is a second instance alongside the macOS deployment — requires a NEW Telegram bot token.

The macOS PAI instance (Lucy) produced a 17-step deployment guide after a 48-ISC evaluation. We follow that guide step-by-step. Driver and Node.js are already installed. ffmpeg, deno, AppArmor fix, and all NanoClaw-specific setup remain.

### Risks
- Docker socket permission denied despite user being in docker group (session may need refresh) — RESOLVED: required logout/login
- CUDA 13.0 / Driver 580 is newer than guide expected (550/12.4) — RESOLVED: backward compatible
- Qwen3-VL-8B download is ~16GB, will take significant time — RESOLVED: 39 min download
- faster-whisper large-v3 model ~3GB additional download — RESOLVED
- Combined GPU VRAM ~19-21GB of 24GB — RESOLVED: 18.5GB actual, OOM fixed by using float16 instead of float32
- AppArmor restriction could block container operations — RESOLVED

## Criteria

- [x] ISC-1: nvidia-smi shows RTX 3090 with CUDA driver loaded
- [x] ISC-2: ffmpeg installed and accessible from PATH
- [x] ISC-3: deno installed and accessible from PATH
- [x] ISC-4: Docker runs containers without permission errors
- [x] ISC-5: AppArmor userns restriction disabled for Docker
- [x] ISC-6: NanoClaw repo cloned to ~/Documents/apps/nanoclaw-ubunto24
- [x] ISC-7: npm ci and npm run build succeed in nanoclaw-ubunto24
- [x] ISC-8: nanoclaw-agent Docker image built successfully
- [x] ISC-9: .env file created with valid credentials
- [x] ISC-10: ChromaDB venv created via setup.sh
- [x] ISC-11: ChromaDB systemd service running and healthy
- [x] ISC-12: ChromaDB heartbeat endpoint returns JSON
- [x] ISC-13: Embedding server.py patched for CUDA + 8B model
- [x] ISC-14: Embedding setup.sh patched for CUDA smoke test
- [x] ISC-15: Embedding venv created and model downloaded
- [x] ISC-16: Embedding systemd service running on CUDA
- [x] ISC-17: Embedding /health returns device:cuda
- [x] ISC-18: Embedding /embed returns correct dimensions and norm ~1.0
- [x] ISC-19: Transcription files replaced (server.py, setup.sh, requirements.txt)
- [x] ISC-20: Transcription venv created and model downloaded
- [x] ISC-21: Transcription systemd service running on CUDA
- [x] ISC-22: Transcription /health returns device:cuda
- [x] ISC-23: NanoClaw orchestrator systemd service running
- [x] ISC-24: UFW firewall rules restrict services to Docker subnet
- [x] ISC-25: loginctl linger enabled for user
- [x] ISC-26: nvidia-smi shows ~19-21GB VRAM used by both model services

## Decisions

- Embedding loads in float16 on CUDA (not float32) — float32 caused OOM (22.3GB allocation vs 20.5GB free after transcription)
- systemd ExecStart uses nvm Node.js path (/home/abba/.nvm/versions/node/v22.22.1/bin/node) not /usr/bin/node (v18) — native modules compiled against v22
- NanoClaw repo at /home/abba/Documents/apps/nanoclaw-ubunto24 (not ~/nanoclaw as guide assumed)
- Embedding dimensions are 4096 (not 2048 as memory doc estimated — 8B model uses larger embedding space)

## Verification
