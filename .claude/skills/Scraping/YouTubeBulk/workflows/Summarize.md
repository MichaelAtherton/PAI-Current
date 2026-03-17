# Summarize Workflow

Analyze existing transcripts and generate organized markdown summaries grouped by topic. Adapted for long-form YouTube content with richer extraction than short-form video summaries.

Invoke this directly if transcripts already exist, or it will be called automatically at the end of ProcessSource.

## Step 1: Read All Transcripts

Read every `.txt` file in the `transcripts/` directory. Each file has this header format:

```
Video ID: {id}
Title: {title}
URL: {url}
Duration: {duration}s
Source: {subtitles (manual)|subtitles (auto)|whisper}

--- TRANSCRIPT ---

{transcript text}
```

Parse out the `Video ID`, `Title`, `URL`, `Duration`, `Source`, and transcript body from each file.

## Step 2: Analyze Each Transcript

For each transcript, extract:

- **Topic** — A descriptive 2-4 word kebab-case category name (e.g., `machine-learning`, `system-design`, `productivity-tips`)
- **Content Type** — Classify as one of: `tutorial`, `lecture`, `interview`, `conference-talk`, `vlog`, `review`, `walkthrough`, `discussion`, `other`
- **Summary** — 2-3 sentences capturing the main points (long-form content warrants more context than a single sentence)
- **Key Insights** — 5-8 actionable bullet points
- **Chapters/Structure** — If the video has clear sections or topic shifts, list them with approximate timestamps (e.g., `0:00 - Intro`, `5:30 - Main concept`, `15:00 - Demo`)
- **Details** — Any additional context worth preserving

Group videos with the same topic together.

## Step 3: Slugify Titles

Convert each video title to a kebab-case filename:
- Lowercase all characters
- Replace spaces with dashes
- Remove special characters (`!`, `?`, `&`, `#`, `|`, etc.)
- Collapse multiple dashes

Examples:
- `"How to Build a RAG Pipeline"` → `how-to-build-a-rag-pipeline.md`
- `"React Server Components Explained!"` → `react-server-components-explained.md`
- `"10 Tips for Better Code Reviews"` → `10-tips-for-better-code-reviews.md`

## Step 4: Write Summary Files

Create `summaries/` directory and one subdirectory per topic.

**File format** (`summaries/{topic-name}/{slugified-title}.md`):

```markdown
---
video_id: {id}
title: {title}
url: {url}
topic: {topic}
content_type: {content_type}
duration: {duration}s
source: {source}
---

# {Title}

## Summary
{2-3 sentence summary}

## Key Insights
- {insight 1}
- {insight 2}
- {insight 3}
- {insight 4}
- {insight 5}

## Chapters/Structure
- 0:00 - {section description}
- {timestamp} - {section description}
- {timestamp} - {section description}

## Details
{additional context}

## Full Transcript
{original transcript}
```

## Step 5: Write INDEX.md

Create `summaries/INDEX.md` listing all summaries grouped by topic:

```markdown
# Video Summaries Index

Generated: {date}
Total videos: {count}
Total runtime: {hours}h {minutes}m

## {Topic Name}
- [{Video Title}](./{topic-name}/{slugified-title}.md) — {content_type}, {duration_min} min
- [{Video Title}](./{topic-name}/{slugified-title}.md) — {content_type}, {duration_min} min

## {Another Topic}
- [{Video Title}](./{topic-name}/{slugified-title}.md) — {content_type}, {duration_min} min
```

## Step 6: Report

After completion, report:
- Total transcripts processed
- Total runtime across all videos
- Topics identified (list them)
- Content type breakdown (e.g., "5 tutorials, 3 interviews, 2 lectures")
- Total summary files created
- Location: `summaries/INDEX.md`
