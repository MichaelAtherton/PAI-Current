# ProcessSource Workflow

Full pipeline: scrape a YouTube channel or playlist → download audio → transcribe → summarize by topic.

## Step 1: Verify Environment

The project is symlinked from TikTokBulk:

```
${PAI_DIR}/skills/Scraping/YouTubeBulk/short-form-video-transcriber/
```

Verify the environment is set up:

```bash
cd "${PAI_DIR}/skills/Scraping/YouTubeBulk/short-form-video-transcriber"
source .venv/bin/activate
which yt-dlp
```

If `yt-dlp` is not found or the symlink is missing:
```bash
# Create symlink if missing
[ ! -d "${PAI_DIR}/skills/Scraping/YouTubeBulk/short-form-video-transcriber" ] && \
  ln -s "${PAI_DIR}/skills/Scraping/TikTokBulk/short-form-video-transcriber" \
        "${PAI_DIR}/skills/Scraping/YouTubeBulk/short-form-video-transcriber"

# Set up venv if missing
cd "${PAI_DIR}/skills/Scraping/YouTubeBulk/short-form-video-transcriber"
if [ ! -d .venv ]; then
  python -m venv .venv && source .venv/bin/activate
  pip install -e ".[dev]"
else
  source .venv/bin/activate
fi
```

**Recommended `.env` for YouTube** (create in project root):
```
WHISPER_MODEL=small       # small recommended for long-form YouTube (vs base for TikTok)
SKIP_EXISTING=true        # skip already-transcribed videos on re-run
OUTPUT_DIR=transcripts    # transcript output directory
STATE_DIR=state           # audio temp files
SUB_LANGS=en,en.*         # subtitle languages (default: English; e.g., es,es.* for Spanish)
```

## Step 2: Get Inputs

Ask the user:

> What YouTube channel or playlist URL do you want to process?
> Examples:
> - Channel: `https://www.youtube.com/@example_creator`
> - Playlist: `https://www.youtube.com/playlist?list=PLxxxxxxx`

> How many videos? (Leave blank for all, or enter a number like `10`)
>
> **Note:** Videos are returned in the order yt-dlp discovers them (typically newest-first for channels, playlist order for playlists). Entering `10` gives you the first 10 in that order.

Store as:
- `SOURCE_URL` — the full YouTube URL
- `LIMIT` — integer or `None`

### Handle Edge Cases

After getting the URL, detect the source type:

```python
from short_form_scraper.scraper.youtube import detect_youtube_source_type
source_type = detect_youtube_source_type(SOURCE_URL)
```

- **`"video"`** — The user pasted a single video URL. Ask: "That's a single video, not a channel/playlist. Want me to transcribe just this one video, or did you mean to paste a channel URL?"
  - If the URL also contains `&list=`, ask: "This URL contains both a video and a playlist. Do you want to process the **full playlist** or just this **single video**?"
  - For a single video, use `get_single_video_metadata()` and process it directly (skip Step 3's scrape loop).
- **`"unknown"`** — Warn the user: "I couldn't identify this as a YouTube channel, playlist, or video. Please check the URL."
- **`"channel"` or `"playlist"`** — Proceed normally to Step 3.

## Step 3: Scrape Video List and Confirm

Scrape the video list once and serialize it to a temp file so Step 4 can reuse it without hitting YouTube again:

```bash
source .venv/bin/activate && python -c "
import json
from pathlib import Path
from short_form_scraper.scraper.youtube import YouTubeScraper, detect_youtube_source_type

source_url = 'SOURCE_URL'
source_type = detect_youtube_source_type(source_url)
print(f'Detected source type: {source_type}')

scraper = YouTubeScraper(source_url)
videos = list(scraper.get_video_urls(limit=LIMIT_OR_NONE))

# Cache scraped metadata so Step 4 doesn't re-scrape
cache = [{'id': v.id, 'url': v.url, 'title': v.title, 'description': v.description,
          'duration': v.duration, 'view_count': v.view_count, 'like_count': v.like_count}
         for v in videos]
Path('state').mkdir(exist_ok=True)
Path('state/video_list.json').write_text(json.dumps(cache, indent=2))

total_seconds = sum(v.duration for v in videos)
total_hours = total_seconds // 3600
total_minutes = (total_seconds % 3600) // 60

print(f'\nFound {len(videos)} videos ({total_hours}h {total_minutes}m total):\n')
for i, v in enumerate(videos, 1):
    title = v.title[:60] + '...' if len(v.title) > 60 else v.title
    duration_min = round(v.duration / 60, 1) if v.duration else 0
    print(f'{i}. {title} ({duration_min} min)')
    print(f'   URL: {v.url}')
    print()
"
```

**Show the list to the user with the total duration estimate and confirm before proceeding.**

A large channel may have hundreds of hours of content. If the total is very high, suggest using a limit or processing a specific playlist instead.

## Step 4: Extract Subtitles or Transcribe Each Video

**Subtitle-first approach:** YouTube videos usually have captions (auto-generated or creator-uploaded). Pulling subtitles via yt-dlp is near-instant vs. minutes of Whisper processing. This step tries subtitles first, falls back to Whisper only when needed.

**Language:** Defaults to English (`en`). Set `SUB_LANGS` in `.env` to override (e.g., `SUB_LANGS=es,es.*` for Spanish).

Read from the cached video list (no re-scrape), then process each video:

```bash
source .venv/bin/activate && python -c "
import json, os, re, subprocess, glob
from pathlib import Path
from short_form_scraper.downloader.video import VideoDownloader
from short_form_scraper.transcriber.whisper import WhisperTranscriber
from short_form_scraper.config import Settings

settings = Settings()
yt_dlp_path = settings.yt_dlp_path or 'yt-dlp'
sub_langs = os.environ.get('SUB_LANGS', 'en,en.*')

Path('transcripts').mkdir(exist_ok=True)
Path('state').mkdir(exist_ok=True)

# Read cached video list from Step 3
cache = json.loads(Path('state/video_list.json').read_text())

# Lazy-load Whisper only if needed
_downloader = None
_transcriber = None

def get_downloader():
    global _downloader
    if _downloader is None:
        _downloader = VideoDownloader()
    return _downloader

def get_transcriber():
    global _transcriber
    if _transcriber is None:
        print('  Loading Whisper model (first fallback)...')
        _transcriber = WhisperTranscriber()
    return _transcriber

def parse_vtt(vtt_text):
    \"\"\"Parse VTT into clean paragraphed text.

    YouTube auto-generated VTT uses overlapping cues where consecutive cues
    repeat prior text with new words appended. We deduplicate exact-match lines
    and insert paragraph breaks roughly every 4 sentences for readability.
    \"\"\"
    lines = vtt_text.split('\n')
    text_lines = []
    seen = set()
    for line in lines:
        line = line.strip()
        # Skip VTT header, metadata, timestamps, cue numbers, empty lines
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:') or line.startswith('NOTE'):
            continue
        if re.match(r'^\d+$', line):
            continue
        if re.match(r'[\d:.]+\s*-->\s*[\d:.]+', line):
            continue
        # Strip inline timestamp tags (<00:00:01.234>), HTML tags (<c>, </c>, <b>)
        line = re.sub(r'<[\d:.]+>', '', line)
        line = re.sub(r'<[^>]+>', '', line)
        # Strip VTT position/alignment metadata ({position:0%} etc.)
        line = re.sub(r'\{[^}]+\}', '', line)
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            text_lines.append(line)

    # Join and insert paragraph breaks every ~4 sentences for readability
    raw = ' '.join(text_lines)
    sentences = re.split(r'(?<=[.!?])\s+', raw)
    paragraphs = []
    for i in range(0, len(sentences), 4):
        paragraphs.append(' '.join(sentences[i:i+4]))
    return '\n\n'.join(paragraphs)

def try_subtitles(video_id, url):
    \"\"\"Try to pull YouTube subtitles. Returns (transcript_text, sub_type) or (None, None).
    sub_type is 'manual' or 'auto' based on yt-dlp output.
    \"\"\"
    sub_prefix = f'state/subs_{video_id}'
    # Clean up any previous subtitle files for this video
    for old in glob.glob(f'{sub_prefix}*'):
        Path(old).unlink()

    cmd = [
        yt_dlp_path,
        '--write-subs', '--write-auto-subs',
        '--sub-langs', sub_langs,
        '--sub-format', 'vtt',
        '--skip-download',
        '--no-playlist',
        '-o', sub_prefix,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    # Look for any subtitle file that was written
    sub_files = sorted(glob.glob(f'{sub_prefix}*.vtt'))
    if not sub_files:
        if result.stderr:
            print(f'  yt-dlp stderr: {result.stderr.strip()[:200]}')
        return None, None

    # Determine sub type from yt-dlp stdout and pick best file
    stdout = result.stdout.lower() if result.stdout else ''
    has_manual = 'writing video subtitles' in stdout
    sub_type = 'manual' if has_manual else 'auto'

    # If multiple files, prefer the one without 'auto' in the filename
    chosen = sub_files[0]
    if len(sub_files) > 1:
        for f in sub_files:
            fname = Path(f).name.lower()
            if 'auto' not in fname and 'generated' not in fname:
                chosen = f
                break

    vtt_text = Path(chosen).read_text(encoding='utf-8', errors='replace')
    transcript = parse_vtt(vtt_text)

    # Clean up subtitle files
    for f in glob.glob(f'{sub_prefix}*'):
        Path(f).unlink()

    if len(transcript.strip()) < 20:
        if result.stderr:
            print(f'  yt-dlp stderr: {result.stderr.strip()[:200]}')
        return None, None

    return transcript, sub_type

stats = {'subtitles_manual': 0, 'subtitles_auto': 0, 'whisper': 0, 'skipped': 0, 'failed': 0}

for i, entry in enumerate(cache, 1):
    video_id = entry['id']
    transcript_file = Path('transcripts') / f'{video_id}.txt'

    # Skip if already transcribed (resume support)
    if transcript_file.exists():
        print(f'[{i}/{len(cache)}] Skipping (already done): {entry[\"title\"][:50]}')
        stats['skipped'] += 1
        continue

    duration_min = round(entry['duration'] / 60, 1) if entry.get('duration') else 0
    print(f'[{i}/{len(cache)}] Processing: {entry[\"title\"][:50]}... ({duration_min} min)')

    try:
        # Phase 1: Try YouTube subtitles first (near-instant)
        print(f'  Trying subtitles...')
        transcript, sub_type = try_subtitles(video_id, entry['url'])

        if transcript:
            source = f'subtitles ({sub_type})'
            print(f'  Got {sub_type} subtitles: {len(transcript)} chars')
            stats[f'subtitles_{sub_type}'] += 1
        else:
            # Phase 2: Fall back to Whisper
            source = 'whisper'
            print(f'  No subtitles available, falling back to Whisper...')
            audio_path = get_downloader().download(entry['url'], Path(f'state/audio_{video_id}'))
            print(f'  Downloaded: {audio_path}')
            transcript = get_transcriber().transcribe(audio_path)
            print(f'  Transcribed: {len(transcript)} chars')
            audio_path.unlink()
            stats['whisper'] += 1

        content = f'''Video ID: {video_id}
Title: {entry['title']}
URL: {entry['url']}
Duration: {entry['duration']}s
Source: {source}

--- TRANSCRIPT ---

{transcript}
'''
        transcript_file.write_text(content)
        print(f'  Saved: {transcript_file} (via {source})')

    except Exception as e:
        print(f'  ERROR: {e}')
        stats['failed'] += 1

    print()

print(f'Done! Transcripts saved to transcripts/')
print(f'  Manual subs: {stats[\"subtitles_manual\"]} | Auto subs: {stats[\"subtitles_auto\"]} | Whisper: {stats[\"whisper\"]} | Skipped: {stats[\"skipped\"]} | Failed: {stats[\"failed\"]}')
"
```

**Notes:**
- Already-transcribed videos are skipped automatically (safe to re-run after failures)
- Whisper model is only loaded if at least one video lacks subtitles
- Subtitle extraction takes ~1-2 seconds per video vs. minutes for Whisper
- Prefers manual (creator-uploaded) subtitles over auto-generated when both exist
- Detects subtitle type from yt-dlp's stdout (not filename guessing)
- Logs yt-dlp stderr when subtitle extraction fails (debugging visibility)
- Language defaults to English; set `SUB_LANGS` in `.env` to override
- Transcripts are paragraphed (~4 sentences each) for readability

## Step 5: Summarize Transcripts

Invoke the **Summarize** workflow now that all transcripts exist.

→ See `workflows/Summarize.md`

## Step 6: Report Results

After completion, report:
- Total videos found
- Total runtime across all videos (sum of durations)
- Successfully transcribed (new + previously skipped)
- Failed (list titles and errors)
- Topics identified
- Output locations: `transcripts/` and `summaries/`
