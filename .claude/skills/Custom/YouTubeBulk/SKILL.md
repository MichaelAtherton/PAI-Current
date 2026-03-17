---
name: YouTubeBulk
description: Bulk-transcribe an entire YouTube channel or playlist — scrapes all video URLs, downloads audio, transcribes with Whisper, and generates organized summaries grouped by topic. USE WHEN user wants to process a YouTube channel, transcribe all videos from a YouTuber, bulk download YouTube content, build a knowledge base from YouTube, process a YouTube playlist, OR bulk transcribe YouTube videos.
---

# YouTubeBulk

Batch-process an entire YouTube channel or playlist: scrape every video URL, pull existing YouTube subtitles (near-instant) with Whisper fallback, and produce organized markdown summaries grouped by topic with a master index.

## Workflow Routing

**When executing a workflow, call the notification script via Bash:**

```bash
${PAI_DIR}/tools/skill-workflow-notification WorkflowName YouTubeBulk
```

| Workflow | Trigger | File |
|----------|---------|------|
| **ProcessSource** | "process this YouTube channel", "bulk transcribe", "transcribe all videos", "process playlist" | `workflows/ProcessSource.md` |
| **Summarize** | "summarize transcripts", "transcripts already downloaded", "just summarize" | `workflows/Summarize.md` |
| **Skillify** | "skillify", "turn summary into a skill", "create skill from summary" | `workflows/Skillify.md` |

## Examples

**Example 1: Full pipeline from channel URL**
```
User: "Transcribe all videos from https://www.youtube.com/@somecreator"
→ Invokes ProcessSource workflow
→ Scrapes all video URLs from the channel
→ Downloads audio and transcribes each video
→ Claude analyzes and summarizes each transcript
→ Produces summaries/ directory grouped by topic + INDEX.md
```

**Example 2: Process a playlist**
```
User: "Process this playlist https://www.youtube.com/playlist?list=PLxyz123"
→ Invokes ProcessSource workflow with playlist URL
→ Scrapes all videos in the playlist
→ Downloads, transcribes, and summarizes
```

**Example 3: Limit to first N videos**
```
User: "Process the first 5 videos from https://www.youtube.com/@somecreator"
→ Invokes ProcessSource workflow with limit=5
→ Scrapes, downloads, transcribes 5 videos
→ Generates summaries and index
```

**Example 4: Summarize already-downloaded transcripts**
```
User: "I already have the transcripts — just summarize them"
→ Invokes Summarize workflow
→ Reads all .txt files from transcripts/ directory
→ Generates summaries/ and INDEX.md without re-downloading
```

## Dependencies

This skill shares the `short-form-video-transcriber` project (symlinked from TikTokBulk):

**GitHub:** https://github.com/grandamenium/short-form-video-transcriber

**Setup:** The symlink points to TikTokBulk's installed copy. Verify:
```bash
cd "${PAI_DIR}/skills/YouTubeBulk/short-form-video-transcriber"
source .venv/bin/activate
which yt-dlp
```

If the symlink or venv doesn't exist, set it up:
```bash
# Create symlink (if missing)
ln -s "${PAI_DIR}/skills/TikTokBulk/short-form-video-transcriber" \
      "${PAI_DIR}/skills/YouTubeBulk/short-form-video-transcriber"

# Install (if venv missing — run from TikTokBulk's copy)
cd "${PAI_DIR}/skills/TikTokBulk/short-form-video-transcriber"
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

**Configure** (optional `.env` overrides):
- `WHISPER_MODEL` — Model size: tiny, base, small, medium, large (**recommended: `small`** for long-form YouTube content; only used as fallback)
- `OUTPUT_DIR` — Where transcripts are stored
- `STATE_DIR` — App state/resume persistence
- `SKIP_EXISTING` — Skip already-processed videos (set to `true`)

**Transcription Strategy:** Subtitles first, Whisper fallback. Most YouTube videos have auto-generated or creator-uploaded captions. The skill pulls those via yt-dlp (~1-2 sec/video) and only loads Whisper if no subtitles are available. Each transcript is tagged with `Source: subtitles` or `Source: whisper`.

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
