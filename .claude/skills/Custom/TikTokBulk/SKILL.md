---
name: TikTokBulk
description: Bulk-transcribe an entire TikTok profile — scrapes all video URLs, downloads audio, transcribes with Whisper, and generates organized summaries grouped by topic. USE WHEN user wants to process an entire TikTok profile, transcribe all videos from a creator, bulk download TikTok content, build a knowledge base from a TikTok account, OR process multiple TikTok videos at once.
---

# TikTokBulk

Batch-process an entire TikTok creator's profile: scrape every video URL, download audio, transcribe with Whisper, and produce organized markdown summaries grouped by topic with a master index.

## Workflow Routing

**When executing a workflow, call the notification script via Bash:**

```bash
${PAI_DIR}/tools/skill-workflow-notification WorkflowName TikTokBulk
```

| Workflow | Trigger | File |
|----------|---------|------|
| **ProcessProfile** | "process this TikTok profile", "bulk transcribe", "transcribe all videos" | `workflows/ProcessProfile.md` |
| **Summarize** | "summarize transcripts", "transcripts already downloaded", "just summarize" | `workflows/Summarize.md` |
| **Skillify** | "skillify", "turn summary into a skill", "create skill from summary" | `workflows/Skillify.md` |

## Examples

**Example 1: Full pipeline from profile URL**
```
User: "Transcribe all videos from https://www.tiktok.com/@somecreator"
→ Invokes ProcessProfile workflow
→ Scrapes all video URLs from the profile
→ Downloads audio and transcribes each video
→ Claude analyzes and summarizes each transcript
→ Produces summaries/ directory grouped by topic + INDEX.md
```

**Example 2: Limit to first N videos**
```
User: "Process the first 10 videos from https://www.tiktok.com/@somecreator"
→ Invokes ProcessProfile workflow with limit=10
→ Scrapes, downloads, transcribes 10 videos
→ Generates summaries and index
```

**Example 3: Summarize already-downloaded transcripts**
```
User: "I already have the transcripts — just summarize them"
→ Invokes Summarize workflow
→ Reads all .txt files from transcripts/ directory
→ Generates summaries/ and INDEX.md without re-downloading
```

## Dependencies

This skill requires the `short-form-video-transcriber` project by [@agentic.james](https://www.tiktok.com/@agentic.james):

**GitHub:** https://github.com/grandamenium/short-form-video-transcriber

**Install:**
```bash
git clone https://github.com/grandamenium/short-form-video-transcriber.git
cd short-form-video-transcriber
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

**Configure** (optional `.env` overrides):
- `WHISPER_MODEL` — Model size: tiny, base, small, medium, large (default: base)
- `OUTPUT_DIR` — Where transcripts are stored
- `STATE_DIR` — App state/resume persistence
- `SKIP_EXISTING` — Skip already-processed videos (set to `true`)

**Setup check:** Run `/start` from inside the project, or verify manually:
```bash
source .venv/bin/activate && which yt-dlp
```

See `ProcessProfile.md` for full setup verification steps.

## Output Structure

```
{project_root}/
├── transcripts/          # Raw transcripts with metadata headers
│   └── {video_id}.txt
└── summaries/            # Organized, analyzed output
    ├── INDEX.md          # Master index grouped by topic
    └── {topic-name}/
        └── {slugified-title}.md
```
