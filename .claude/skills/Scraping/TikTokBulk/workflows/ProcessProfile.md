# ProcessProfile Workflow

Full pipeline: scrape a TikTok profile → download audio → transcribe → summarize by topic.

## Step 1: Verify Environment

The repo is already cloned at:

```
${PAI_DIR}/skills/Scraping/TikTokBulk/short-form-video-transcriber/
```

Verify the environment is set up:

```bash
cd "${PAI_DIR}/skills/Scraping/TikTokBulk/short-form-video-transcriber"
source .venv/bin/activate
which yt-dlp
```

If `yt-dlp` is not found, set up the environment:
```bash
cd "${PAI_DIR}/skills/Scraping/TikTokBulk/short-form-video-transcriber"
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

**Optional `.env` config** (create in project root):
```
WHISPER_MODEL=base        # tiny/base/small/medium/large
SKIP_EXISTING=true        # skip already-transcribed videos on re-run
OUTPUT_DIR=transcripts    # transcript output directory
STATE_DIR=state           # audio temp files
```

## Step 2: Get Inputs

Ask the user:

> What TikTok profile URL do you want to process?
> Example: `https://www.tiktok.com/@example_creator`

> How many videos? (Leave blank for all, or enter a number like `10`)
>
> **Note:** Videos are returned newest-first. Entering `10` gives you the 10 most recent videos. There is no built-in way to start from the oldest — if you need that, process all videos and work backwards from the results.

Store as:
- `PROFILE_URL` — the full TikTok profile URL
- `LIMIT` — integer or `None`

## Step 3: Scrape Video URLs

```bash
source .venv/bin/activate && python -c "
from short_form_scraper.scraper.tiktok import TikTokScraper

scraper = TikTokScraper('PROFILE_URL')
videos = list(scraper.get_video_urls(limit=LIMIT_OR_NONE))

print(f'Found {len(videos)} videos:')
for i, v in enumerate(videos, 1):
    title = v.title[:60] + '...' if len(v.title) > 60 else v.title
    print(f'{i}. {title}')
    print(f'   URL: {v.url}')
    print()
"
```

Show the list to the user and confirm before proceeding.

## Step 4: Download and Transcribe Each Video

Create output directories, then process each video:

```bash
source .venv/bin/activate && python -c "
from short_form_scraper.scraper.tiktok import TikTokScraper
from short_form_scraper.downloader.video import VideoDownloader
from short_form_scraper.transcriber.whisper import WhisperTranscriber
from pathlib import Path

scraper = TikTokScraper('PROFILE_URL')
downloader = VideoDownloader()
transcriber = WhisperTranscriber()

Path('transcripts').mkdir(exist_ok=True)
Path('state').mkdir(exist_ok=True)

videos = list(scraper.get_video_urls(limit=LIMIT_OR_NONE))

for i, metadata in enumerate(videos, 1):
    transcript_file = Path('transcripts') / f'{metadata.id}.txt'

    # Skip if already transcribed (resume support)
    if transcript_file.exists():
        print(f'[{i}/{len(videos)}] Skipping (already done): {metadata.title[:50]}')
        continue

    print(f'[{i}/{len(videos)}] Processing: {metadata.title[:50]}...')

    try:
        audio_path = downloader.download(metadata.url, Path(f'state/audio_{metadata.id}'))
        print(f'  Downloaded: {audio_path}')

        transcript = transcriber.transcribe(audio_path)
        print(f'  Transcribed: {len(transcript)} chars')

        content = f'''Video ID: {metadata.id}
Title: {metadata.title}
URL: {metadata.url}
Duration: {metadata.duration}s

--- TRANSCRIPT ---

{transcript}
'''
        transcript_file.write_text(content)
        print(f'  Saved: {transcript_file}')

        audio_path.unlink()

    except Exception as e:
        print(f'  ERROR: {e}')

    print()

print('Done! Transcripts saved to transcripts/')
"
```

**Note:** Already-transcribed videos are skipped automatically, so this is safe to re-run after failures.

## Step 5: Summarize Transcripts

Invoke the **Summarize** workflow now that all transcripts exist.

→ See `workflows/Summarize.md`

## Step 6: Report Results

After completion, report:
- Total videos found
- Successfully transcribed (new + previously skipped)
- Failed (list titles and errors)
- Topics identified
- Output locations: `transcripts/` and `summaries/`
