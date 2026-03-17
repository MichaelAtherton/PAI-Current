# PDF Report Generation Workflow

**Trigger:** "pdf report", "generate pdf", "report pdf", "geo pdf"

## Purpose

Transform GEO audit data into a professionally formatted PDF report with charts, score gauges, and visual dashboards. Uses the `GeneratePdfReport.py` tool to produce a print-ready deliverable.

**Output:** `GEO-REPORT.pdf` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

## When to Use

- After a full GEO audit is complete and a client-ready PDF is needed
- When the client needs a branded, printable report (not just markdown)
- For formal presentations or stakeholder packages
- As the final step in the audit pipeline: audit -> markdown report -> PDF report

## Prerequisites

- **Prior audit data required** — run `/geo audit [url]` first
- **Python dependency:** `pip install reportlab`
- **Tool:** `${PAI_DIR}/skills/GeoSeo/Tools/GeneratePdfReport.py`

---

## Workflow Steps

### Step 1: Verify Audit Data Exists

Check for existing audit output files that contain the data needed for the PDF:

Resolve the output directory *(see SKILL.md → Output Directory)*:
```bash
GEO_OUTPUT="${PAI_DIR}/output/GeoSeo/{domain-slug}/latest"

# Check for audit outputs in the domain's output directory
echo "=== Checking for audit data in $GEO_OUTPUT ==="

for file in \
  GEO-AUDIT-REPORT.md \
  GEO-CONTENT-ANALYSIS.md \
  GEO-CITABILITY-SCORE.md \
  GEO-CRAWLER-ACCESS.md \
  GEO-BRAND-MENTIONS.md \
  GEO-SCHEMA-REPORT.md \
  GEO-TECHNICAL-AUDIT.md \
  GEO-PLATFORM-OPTIMIZATION.md \
  GEO-LLMSTXT-ANALYSIS.md \
  GEO-CLIENT-REPORT.md; do
  if [ -f "$GEO_OUTPUT/$file" ]; then
    echo "FOUND: $file ($(wc -l < "$GEO_OUTPUT/$file") lines)"
  else
    echo "MISSING: $file"
  fi
done
```

**If no audit files are found:**
Stop and inform the user:
> "No audit data found. Please run `/geo audit [url]` first to generate the data needed for the PDF report."

**If partial data is found:**
Proceed with available data. The PDF will include sections for available data and mark missing sections as "Not Assessed."

**Minimum required:** At least `GEO-AUDIT-REPORT.md` or `GEO-CLIENT-REPORT.md` must exist. Without either, the PDF cannot be generated.

### Step 2: Extract Scores, Findings, and Recommendations

Parse each audit file to extract structured data. Build a complete data picture:

**From GEO-AUDIT-REPORT.md or GEO-CLIENT-REPORT.md:**
- Overall GEO Readiness Score (0-100)
- Category scores (6 categories)
- Executive summary text
- Key findings by severity
- Recommendations by timeline tier

**From GEO-CONTENT-ANALYSIS.md:**
- E-E-A-T scores (Experience, Expertise, Authoritativeness, Trustworthiness)
- Content metrics (word count, readability, structure)
- AI content assessment score
- Topical authority score

**From GEO-CRAWLER-ACCESS.md:**
- Crawler access status for each AI platform bot
- robots.txt configuration details
- Specific blocked/allowed crawlers

**From GEO-PLATFORM-OPTIMIZATION.md:**
- Platform-by-platform visibility status
- Citation quality per platform
- Platform-specific recommendations

**From GEO-BRAND-MENTIONS.md:**
- Brand mention count and sentiment
- Citation readiness score
- Authority signals

**From GEO-SCHEMA-REPORT.md:**
- Schema types present and valid
- Missing schema opportunities
- Validation errors

**From GEO-TECHNICAL-AUDIT.md:**
- Core Web Vitals metrics
- Technical issue count by severity
- Mobile responsiveness, HTTPS, sitemap status

**From GEO-CITABILITY-SCORE.md:**
- Top citable pages with scores
- Bottom pages needing improvement
- Content pattern analysis

**From GEO-LLMSTXT-ANALYSIS.md:**
- llms.txt presence and quality
- Configuration details

### Step 3: Structure Data into JSON Schema

Build the JSON payload required by `GeneratePdfReport.py`. Every field must be populated from audit data or marked as null if unavailable.

**Required JSON Schema:**

```json
{
  "url": "https://example.com",
  "brand_name": "Example Brand",
  "date": "2026-03-10",
  "geo_score": 72,
  "scores": {
    "ai_platform": {
      "score": 65,
      "max": 100,
      "label": "AI Platform Readiness",
      "rating": "Developing"
    },
    "content": {
      "score": 78,
      "max": 100,
      "label": "Content Quality (E-E-A-T)",
      "rating": "Good"
    },
    "technical": {
      "score": 82,
      "max": 100,
      "label": "Technical Health",
      "rating": "Good"
    },
    "schema": {
      "score": 55,
      "max": 100,
      "label": "Schema & Structured Data",
      "rating": "Developing"
    },
    "brand": {
      "score": 70,
      "max": 100,
      "label": "Brand Authority & Citability",
      "rating": "Good"
    },
    "crawlers": {
      "score": 80,
      "max": 100,
      "label": "AI Crawler Access",
      "rating": "Good"
    }
  },
  "platforms": {
    "chatgpt": {
      "name": "ChatGPT",
      "visibility": "partial",
      "citation_quality": "paraphrase",
      "notes": "Brand mentioned but not directly cited with URL"
    },
    "claude": {
      "name": "Claude",
      "visibility": "not_found",
      "citation_quality": "none",
      "notes": "No brand presence detected"
    },
    "perplexity": {
      "name": "Perplexity",
      "visibility": "found",
      "citation_quality": "direct_cite",
      "notes": "Direct URL citation in search results"
    },
    "gemini": {
      "name": "Gemini",
      "visibility": "partial",
      "citation_quality": "paraphrase",
      "notes": "Referenced in related content suggestions"
    },
    "google_aio": {
      "name": "Google AI Overviews",
      "visibility": "not_found",
      "citation_quality": "none",
      "notes": "Not appearing in AI overview panels"
    }
  },
  "crawler_access": {
    "GPTBot": {"status": "allowed", "platform": "ChatGPT/OpenAI"},
    "ClaudeBot": {"status": "blocked", "platform": "Claude/Anthropic"},
    "PerplexityBot": {"status": "allowed", "platform": "Perplexity"},
    "Google-Extended": {"status": "not_configured", "platform": "Gemini/AI Overviews"},
    "Bytespider": {"status": "blocked", "platform": "TikTok/Doubao"}
  },
  "findings": [
    {
      "severity": "critical",
      "title": "ClaudeBot blocked in robots.txt",
      "description": "The robots.txt file explicitly blocks ClaudeBot, preventing Anthropic's Claude from indexing site content. This removes the site from one of the top 3 AI platforms."
    },
    {
      "severity": "high",
      "title": "No FAQPage schema on service pages",
      "description": "Service pages answer common questions in body text but lack FAQPage structured data, reducing the likelihood of AI platforms extracting and citing Q&A content."
    },
    {
      "severity": "medium",
      "title": "Author bios missing on blog posts",
      "description": "12 of 15 blog posts lack author attribution with credentials, weakening E-E-A-T expertise signals."
    },
    {
      "severity": "low",
      "title": "Image alt text incomplete",
      "description": "23% of images lack descriptive alt text, a minor accessibility and SEO signal."
    }
  ],
  "quick_wins": [
    {
      "action": "Unblock ClaudeBot in robots.txt",
      "impact": "Restores visibility on Claude platform",
      "effort": "15 minutes"
    },
    {
      "action": "Add llms.txt file to root domain",
      "impact": "Provides AI platforms structured site overview",
      "effort": "1 hour"
    },
    {
      "action": "Add FAQPage schema to top 5 service pages",
      "impact": "Improves AI extraction of Q&A content",
      "effort": "2-3 hours"
    }
  ],
  "medium_term": [
    {
      "action": "Add author bios with credentials to all blog posts",
      "impact": "Strengthens E-E-A-T expertise signals across content",
      "effort": "1-2 weeks"
    },
    {
      "action": "Build topic cluster hub pages for core services",
      "impact": "Establishes topical authority for AI citation",
      "effort": "2-4 weeks"
    }
  ],
  "strategic": [
    {
      "action": "Launch original research program with annual industry reports",
      "impact": "Creates unique citable assets that AI platforms prioritize",
      "effort": "2-3 months"
    },
    {
      "action": "Build digital PR campaign targeting industry publications",
      "impact": "Increases brand mentions and authority signals",
      "effort": "3-6 months ongoing"
    }
  ],
  "executive_summary": "Example Brand scores 72/100 on GEO readiness — a solid foundation with clear gaps in AI platform visibility and structured data. The site has strong content quality (78/100) and good technical health (82/100), but is underperforming on schema implementation (55/100) and AI platform readiness (65/100). Most critically, ClaudeBot is blocked and no llms.txt file exists. Implementing the quick wins alone would raise the score to an estimated 80+. The three-month strategic plan targets 85+ by building topical authority and original research assets."
}
```

**Field population rules:**
- `url`: From audit target URL
- `brand_name`: Extracted from site title, Organization schema, or user input
- `date`: Current date in YYYY-MM-DD format
- `geo_score`: From composite GEO Readiness Score calculation
- `scores`: From individual workflow outputs; use null for unassessed categories
- `platforms`: From PlatformOptimizer output; use "not_assessed" visibility if not run
- `crawler_access`: From Crawlers workflow output
- `findings`: Aggregated from all workflows, sorted by severity (critical first)
- `quick_wins`, `medium_term`, `strategic`: From Action Plan in client report or aggregated from individual workflow recommendations
- `executive_summary`: From client report Executive Summary or synthesized from available data

**Severity levels for findings:**
- `critical`: Blocks AI visibility entirely (e.g., all crawlers blocked, site not indexed)
- `high`: Significantly reduces AI citation likelihood (e.g., no schema, major content gaps)
- `medium`: Reduces effectiveness but not blocking (e.g., missing author bios, partial schema)
- `low`: Minor improvements with incremental benefit (e.g., alt text, meta description length)

### Step 4: Write JSON to Temporary File

```bash
# Write the structured JSON data to a temp file
cat > /tmp/geo-report-data.json << 'JSONEOF'
{
  ... [populated JSON from Step 3] ...
}
JSONEOF

# Verify JSON is valid
python3 -c "import json; json.load(open('/tmp/geo-report-data.json')); print('JSON valid')"
```

**If JSON validation fails:** Fix the malformed JSON before proceeding. Common issues:
- Unescaped quotes in description fields
- Trailing commas in arrays/objects
- Missing closing brackets

### Step 5: Verify reportlab Dependency

```bash
# Check if reportlab is installed
python3 -c "import reportlab; print(f'reportlab {reportlab.Version}')" 2>/dev/null

# If not installed:
pip install reportlab
```

**If pip install fails:** Try `pip3 install reportlab` or `python3 -m pip install reportlab`. If still failing, inform the user they need to install the dependency manually.

### Step 6: Execute PDF Generation Script

```bash
# Run the PDF generator
python3 ${PAI_DIR}/skills/GeoSeo/Tools/GeneratePdfReport.py \
  /tmp/geo-report-data.json \
  "$GEO_OUTPUT/GEO-REPORT.pdf"
```

**Expected execution time:** 2-10 seconds depending on data volume.

**If the script fails:**
1. Check error output for missing fields in JSON
2. Verify all required JSON fields are present (see schema above)
3. Check that reportlab is properly installed
4. Ensure write permissions in the output directory

### Step 7: Verify PDF Output

```bash
# Verify the PDF was created and has reasonable size
ls -la "$GEO_OUTPUT/GEO-REPORT.pdf"

# Check file size (should be 100KB-2MB for a typical report)
FILE_SIZE=$(stat -f%z "$GEO_OUTPUT/GEO-REPORT.pdf" 2>/dev/null || stat -c%s "$GEO_OUTPUT/GEO-REPORT.pdf" 2>/dev/null)
echo "PDF size: ${FILE_SIZE} bytes"

# Verify it's a valid PDF
file "$GEO_OUTPUT/GEO-REPORT.pdf"
# Expected: "GEO-REPORT.pdf: PDF document, version 1.4"

# Count pages (approximate from metadata)
python3 -c "
import os
size = os.path.getsize('$GEO_OUTPUT/GEO-REPORT.pdf')
print(f'File size: {size:,} bytes ({size/1024:.0f} KB)')
print('PDF generated successfully')
"
```

**Validation checks:**
- [ ] File exists and is non-empty
- [ ] File is valid PDF format (starts with `%PDF`)
- [ ] File size is 100KB-2MB (under 100KB suggests missing content; over 2MB suggests issues)
- [ ] File is readable (not corrupted)

---

## PDF Contents Reference

The `GeneratePdfReport.py` script generates a PDF with the following sections:

### Cover Page
- Brand name prominently displayed
- "GEO Readiness Assessment" title
- Date of assessment
- GEO Readiness Score displayed as a visual gauge (0-100)
- Color-coded: Red (<40), Orange (40-69), Yellow (70-84), Green (85+)

### Score Breakdown Page
- Horizontal bar chart showing all 6 category scores
- Each bar color-coded by rating (red/orange/yellow/green)
- Score labels with numerical values and ratings
- Weighted contribution to overall score shown

### AI Platform Readiness Dashboard
- 5-platform grid (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews)
- Each platform shows: visibility status icon, citation quality, action needed
- Color-coded status: Green (found), Yellow (partial), Red (not found)

### Crawler Access Status Table
- Table of 5 AI crawler bots
- Status column: Allowed (green), Blocked (red), Not Configured (gray)
- Platform mapping column
- Impact description for blocked crawlers

### Findings by Severity
- Findings grouped under severity headers
- Critical findings in red-bordered boxes
- High findings in orange-bordered boxes
- Medium findings in yellow-bordered boxes
- Low findings in blue-bordered boxes
- Each finding has title and description

### Action Plan
- Three-tier layout: Quick Wins, Medium-Term, Strategic
- Each action in a table row with: action description, expected impact, effort estimate
- Quick Wins highlighted with green accent (do these first)
- Strategic items with blue accent (plan these)

### Methodology Appendix
- Scoring framework explanation
- Category weight rationale
- GEO vs SEO context
- Market statistics (AI search growth data)
- Disclaimer and re-assessment recommendation

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `FileNotFoundError: GeneratePdfReport.py` | Script not at expected path | Verify `${PAI_DIR}` is set; check `skills/GeoSeo/Tools/` directory |
| `ModuleNotFoundError: reportlab` | reportlab not installed | Run `pip install reportlab` |
| `KeyError` in JSON parsing | Missing required field in data JSON | Check JSON against required schema; add missing fields |
| `PermissionError` on output | No write access to output directory | Check directory permissions; try writing to `/tmp/` first |
| PDF is 0 bytes | Script crashed during generation | Check stderr output; common cause is malformed JSON data |
| PDF is very small (<50KB) | Missing data sections | Verify all JSON fields are populated; null fields produce empty sections |

---

## Cleanup

```bash
# Remove temporary JSON file after successful PDF generation
rm -f /tmp/geo-report-data.json
```

---

## Integration Notes

### Full Pipeline Order
```
1. /geo audit [url]           → GEO-AUDIT-REPORT.md + individual workflow outputs
2. /geo report                → GEO-CLIENT-REPORT.md (aggregated markdown)
3. /geo pdf                   → GEO-REPORT.pdf (visual PDF from audit data)
```

### Running Without Client Report
The PDF can be generated directly from individual audit files (skipping the markdown client report step). The JSON extraction in Step 2 will pull from whichever files are available. However, the executive summary will be stronger if `GEO-CLIENT-REPORT.md` exists, as it contains the synthesized narrative.

### Customization
- Brand colors can be adjusted in the JSON (future: add `brand_colors` field)
- Logo inclusion requires modifying `GeneratePdfReport.py` (future enhancement)
- Additional sections can be added by extending the JSON schema

---

## Key Principle

The PDF is the polished, client-facing artifact. It should look professional enough to present in a boardroom. If the data quality from the audit is poor, fix the data first — do not generate a PDF with placeholder content. A bad PDF is worse than no PDF.
