# Summarize Workflow

Analyze existing transcripts and generate organized markdown summaries grouped by topic.

Invoke this directly if transcripts already exist, or it will be called automatically at the end of ProcessProfile.

## Step 1: Read All Transcripts

Read every `.txt` file in the `transcripts/` directory. Each file has this header format:

```
Video ID: {id}
Title: {title}
URL: {url}
Duration: {duration}s

--- TRANSCRIPT ---

{transcript text}
```

Parse out the `Video ID`, `Title`, `URL`, and transcript body from each file.

## Step 2: Analyze Each Transcript

For each transcript, extract:

- **Topic** — A descriptive 2-4 word kebab-case category name (e.g., `agentic-engineering`, `context-management`, `productivity-tips`)
- **Summary** — One sentence capturing the main point
- **Key Tips** — 3-5 actionable bullet points
- **Details** — Any additional context worth preserving

Group videos with the same topic together.

## Step 3: Slugify Titles

Convert each video title to a kebab-case filename:
- Lowercase all characters
- Replace spaces with dashes
- Remove special characters (`!`, `?`, `&`, `#`, etc.)
- Collapse multiple dashes

Examples:
- `"How to Use Context Windows"` → `how-to-use-context-windows.md`
- `"Claude Code Tips & Tricks!"` → `claude-code-tips-tricks.md`
- `"5 AI Tools I Use Daily"` → `5-ai-tools-i-use-daily.md`

## Step 4: Write Summary Files

Create `summaries/` directory and one subdirectory per topic.

**File format** (`summaries/{topic-name}/{slugified-title}.md`):

```markdown
---
video_id: {id}
title: {title}
url: {url}
topic: {topic}
---

# {Title}

## Summary
{one-sentence summary}

## Key Tips
- {tip 1}
- {tip 2}
- {tip 3}

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

## {Topic Name}
- [{Video Title}](./{topic-name}/{slugified-title}.md)
- [{Video Title}](./{topic-name}/{slugified-title}.md)

## {Another Topic}
- [{Video Title}](./{topic-name}/{slugified-title}.md)
```

## Step 6: Report

After completion, report:
- Total transcripts processed
- Topics identified (list them)
- Total summary files created
- Location: `summaries/INDEX.md`
