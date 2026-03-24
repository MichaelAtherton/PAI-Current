---
name: NanoClaw Linux Deployment
description: NanoClaw deployed on Ubuntu 24.04 with RTX 3090. Key paths, service names, and gotchas from the deployment.
type: project
---

NanoClaw personal AI assistant orchestrator deployed on Ubuntu 24.04 + NVIDIA RTX 3090 (2026-03-21).

**Why:** Second instance alongside macOS deployment. Uses CUDA for faster embedding and transcription.

**How to apply:**
- Repo: `/home/abba/Documents/apps/nanoclaw-ubunto24`
- Telegram bot: `@linus_linux_bot` (token in .env)
- 4 systemd user services: `chromadb`, `embedding`, `transcription`, `nanoclaw`
- Manage with: `systemctl --user {status|restart|stop} {service}`
- GPU monitoring: `nvidia-smi` (~18.5GB of 24GB used)
- Embedding: Qwen3-VL-8B, float16, 4096 dimensions, port 8100
- Transcription: faster-whisper large-v3, int8, port 8200
- ChromaDB: port 8000
- NanoClaw orchestrator: port 3001 (credential proxy)
- systemd uses nvm node path (`/home/abba/.nvm/versions/node/v22.22.1/bin/node`), NOT `/usr/bin/node` (v18)
- Embedding server.py uses `dtype=torch.float16` (not float32) to fit in VRAM alongside transcription
