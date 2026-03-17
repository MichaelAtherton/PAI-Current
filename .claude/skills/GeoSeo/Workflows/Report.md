# Client Report Generation Workflow

**Trigger:** "geo report", "client report", "generate report", "audit report"

## Purpose

Aggregate all GEO audit results into a single, client-ready markdown deliverable. This is the business-oriented report that stakeholders read — it translates technical findings into strategic priorities with clear business impact.

**Output:** `GEO-CLIENT-REPORT.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

## When to Use

- After completing a full GEO audit (or subset of audit workflows)
- When a client needs a self-contained deliverable summarizing their GEO readiness
- To compile findings from multiple individual workflow outputs into one report
- As the final step in the audit-to-report pipeline

## Prerequisites

This workflow aggregates data from prior audit runs. Resolve the output directory first *(see SKILL.md → Output Directory)*:

1. Determine `{domain-slug}` from the target URL (strip protocol + www, hostname only, dots→hyphens, lowercase)
2. Set the output directory:
   ```bash
   GEO_OUTPUT="${PAI_DIR}/output/GeoSeo/{domain-slug}/latest"
   ```
3. Check for existing audit data in that directory:

```bash
# Check for available audit data in the domain's latest output directory
for file in \
  GEO-AUDIT-REPORT.md GEO-CONTENT-ANALYSIS.md GEO-CITABILITY-SCORE.md \
  GEO-CRAWLER-ACCESS.md GEO-BRAND-MENTIONS.md GEO-SCHEMA-REPORT.md \
  GEO-TECHNICAL-AUDIT.md GEO-PLATFORM-OPTIMIZATION.md GEO-LLMSTXT-ANALYSIS.md; do
  ls -la "$GEO_OUTPUT/$file" 2>/dev/null
done
```

**If the `latest` symlink doesn't exist or no audit data is found:** Inform the user they need to run `/geo audit [url]` first. Do not generate a report from thin air.

**If partial data exists:** Generate the report with available data and clearly mark missing sections as "Not Assessed — run [workflow name] to populate."

---

## GEO Readiness Score Formula

The composite GEO Readiness Score aggregates all audit dimensions. **Canonical weights defined in `ScoringMethodology.md` — if weights change, update there first.**

| Category | Weight | Source Workflow |
|----------|--------|----------------|
| AI Citability & Visibility | 25% | Citability + Crawlers + LlmsTxt |
| Brand Authority Signals | 20% | BrandMentions |
| Content Quality (E-E-A-T) | 20% | Content |
| Technical Foundations | 15% | Technical |
| Structured Data | 10% | Schema |
| Platform Optimization | 10% | PlatformOptimizer |

**Calculation:**
```
GEO Readiness Score = (
  (citability_score / citability_max * 25) +
  (brand_score / brand_max * 20) +
  (content_score / content_max * 20) +
  (technical_score / technical_max * 15) +
  (schema_score / schema_max * 10) +
  (platform_score / platform_max * 10)
)
```

Round to nearest integer. Score is 0-100.

| Score | Rating | Business Meaning |
|-------|--------|------------------|
| 85-100 | Excellent | AI platforms are very likely citing this site; maintain and optimize |
| 70-84 | Good | Solid foundation; targeted improvements will yield strong ROI |
| 55-69 | Developing | Significant gaps; competitors are likely outperforming in AI search |
| 40-54 | Weak | Major investment needed; largely invisible to AI platforms |
| Below 40 | Critical | Fundamental GEO strategy required; near-zero AI visibility |

---

## Report Structure (12 Sections)

### Tone and Style Guidelines

- **Professional but accessible** — a CMO or founder should understand every section
- **Action-oriented** — every finding leads to a recommendation
- **Business-impact focused** — translate technical issues into revenue/visibility impact
- **No unexplained jargon** — define technical terms on first use
- **Quantified wherever possible** — "3 of 5 AI crawlers blocked" not "some crawlers blocked"
- **Confident but honest** — state clearly what's good, what's bad, what's unknown

**Target length:** 3,000-6,000 words. Self-contained and printable.

---

## Workflow Steps

### Step 1: Collect All Audit Data

Read each available audit output file and extract:

**From each file, extract:**
- Scores (numerical)
- Key findings (positive and negative)
- Specific recommendations
- Data points and metrics
- Risk levels and severity ratings

```bash
# Read all available audit files
# Parse scores, findings, and recommendations from each
```

Organize extracted data into these categories:
- **Scores:** All numerical scores by category
- **Findings:** All findings tagged by severity (Critical / High / Medium / Low / Info)
- **Recommendations:** All recommendations tagged by timeline (Quick Win / Medium-Term / Strategic)
- **Metrics:** All quantitative data points

### Step 2: Calculate Composite GEO Readiness Score

Using the formula above, calculate the weighted composite score.

**If a category has no data (workflow not run):**
- Exclude it from the calculation
- Redistribute its weight proportionally across available categories
- Note in the report: "Score based on X of 6 categories assessed"

**Example with missing data:**
```
Available: Citability (25%), Content (20%), Technical (15%), Schema (10%)
Missing: Brand (20%), Platform (10%)
Redistributed weights: Citability 35.7%, Content 28.6%, Technical 21.4%, Schema 14.3%
```

### Step 3: Write Section 1 — Executive Summary

**Length:** 300-500 words

```markdown
## Executive Summary

[Company/Brand Name] was assessed for Generative Engine Optimization (GEO) readiness
on [date]. GEO measures how well a website is positioned to appear in AI-generated
search results from platforms like ChatGPT, Claude, Perplexity, Gemini, and Google
AI Overviews.

### Overall GEO Readiness: [SCORE]/100 — [RATING]

[2-3 sentences translating the score into business meaning. What does this mean
for the client's visibility in AI search? How does it compare to typical sites
in their industry?]

### Key Strengths
- [Top positive finding with business impact]
- [Second positive finding]
- [Third positive finding]

### Critical Gaps
- [Most urgent issue with business impact]
- [Second critical issue]
- [Third critical issue]

### Bottom Line
[1-2 sentences: What should the client do first? What's the expected impact
of addressing the recommendations?]
```

### Step 4: Write Section 2 — Score Breakdown

```markdown
## GEO Score Breakdown

| Category | Score | Weight | Weighted | Rating |
|----------|-------|--------|----------|--------|
| AI Citability & Visibility | X/100 | 25% | X | [emoji + label] |
| Brand Authority Signals | X/100 | 20% | X | [emoji + label] |
| Content Quality (E-E-A-T) | X/100 | 20% | X | [emoji + label] |
| Technical Foundations | X/100 | 15% | X | [emoji + label] |
| Structured Data | X/100 | 10% | X | [emoji + label] |
| Platform Optimization | X/100 | 10% | X | [emoji + label] |
| **GEO Readiness Score** | | **100%** | **X/100** | **[rating]** |

### Score Context
[Brief paragraph explaining what each category measures and why it matters
for AI search visibility. Avoid jargon — explain for a non-technical reader.]
```

### Step 5: Write Section 3 — AI Visibility Dashboard

```markdown
## AI Visibility Dashboard

How [brand] currently appears (or doesn't) across major AI platforms:

| Platform | Visibility | Citation Quality | Action Needed |
|----------|-----------|-----------------|---------------|
| ChatGPT (GPT-4o) | [Found/Not Found/Partial] | [Direct cite/Paraphrase/None] | [action] |
| Claude (Anthropic) | [Found/Not Found/Partial] | [Direct cite/Paraphrase/None] | [action] |
| Perplexity | [Found/Not Found/Partial] | [Direct cite/Paraphrase/None] | [action] |
| Google AI Overviews | [Found/Not Found/Partial] | [Direct cite/Paraphrase/None] | [action] |
| Gemini | [Found/Not Found/Partial] | [Direct cite/Paraphrase/None] | [action] |

### What This Means
[2-3 sentences explaining the practical impact. "When potential customers ask
ChatGPT about [service], [brand] is/isn't being recommended..."]
```

**Note:** If platform visibility data was not collected (PlatformOptimizer not run), state: "Platform visibility was not assessed in this audit. Run a platform optimization analysis to populate this section."

### Step 6: Write Section 4 — Crawler Access

```markdown
## AI Crawler Access

AI platforms use specialized crawlers to index content for their models. Blocking
these crawlers means your content cannot appear in AI-generated answers.

| Crawler | Platform | Status | Impact |
|---------|----------|--------|--------|
| GPTBot | ChatGPT/OpenAI | [Allowed/Blocked/Not Configured] | [impact] |
| ClaudeBot | Claude/Anthropic | [Allowed/Blocked/Not Configured] | [impact] |
| PerplexityBot | Perplexity | [Allowed/Blocked/Not Configured] | [impact] |
| Google-Extended | Gemini/AI Overviews | [Allowed/Blocked/Not Configured] | [impact] |
| Bytespider | TikTok/Doubao | [Allowed/Blocked/Not Configured] | [impact] |

### robots.txt Assessment
[Summary of current robots.txt configuration and its impact on AI visibility]

### llms.txt Status
- **Present:** [Yes/No]
- **Quality:** [assessment if present]
- **Recommendation:** [specific action]
```

### Step 7: Write Section 5 — Brand Authority

```markdown
## Brand Authority & Recognition

AI platforms prefer citing brands they recognize as authoritative. This section
assesses [brand]'s digital authority footprint.

### Brand Mention Analysis
- **Total brand mentions found:** [count]
- **Sentiment breakdown:** [positive/neutral/negative %]
- **Mention sources:** [list key sources — industry publications, review sites, social media]
- **Competitor comparison:** [how brand mention volume compares to competitors]

### Citation Readiness
- **Citability Score:** [X/100]
- **Most citable content:** [list top 3 pages with scores]
- **Least citable content:** [list bottom 3 pages with scores]

### Authority Signals
[Assessment of backlink quality indicators, domain authority, industry recognition,
press coverage, professional associations]
```

### Step 8: Write Section 6 — Citability Analysis

```markdown
## Citability Analysis

Citability measures how likely AI platforms are to directly quote or reference
your content when answering user queries.

### Top Citable Pages
| Page | Score | Strengths |
|------|-------|-----------|
| [URL] | X/100 | [why it's citable] |
| [URL] | X/100 | [why it's citable] |
| [URL] | X/100 | [why it's citable] |

### Pages Needing Improvement
| Page | Score | Issues |
|------|-------|--------|
| [URL] | X/100 | [why it's not citable] |
| [URL] | X/100 | [why it's not citable] |

### Content Patterns That Drive AI Citations
[Summary of what makes the client's best content citable and how to replicate
that pattern across other pages]
```

### Step 9: Write Section 7 — Technical Health

```markdown
## Technical Health

Technical factors that affect both traditional search and AI platform indexing.

### Core Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Page Load Speed (LCP) | Xs | <2.5s | [status] |
| Mobile Responsiveness | [Y/N] | Yes | [status] |
| HTTPS | [Y/N] | Yes | [status] |
| Canonical Tags | [Present/Missing] | Present | [status] |
| Sitemap | [Present/Missing/Errors] | Valid | [status] |
| Structured Data Errors | [count] | 0 | [status] |
| Broken Links | [count] | 0 | [status] |
| Redirect Chains | [count] | 0 | [status] |

### Critical Technical Issues
[List any issues that directly prevent AI crawling or indexing]

### Technical Recommendations
[Prioritized list of technical fixes]
```

### Step 10: Write Section 8 — Schema & Structured Data

```markdown
## Schema & Structured Data

Structured data helps AI platforms understand your content's meaning, relationships,
and authority signals. It is the machine-readable layer that makes content parseable.

### Current Schema Implementation
| Schema Type | Present | Valid | Pages |
|-------------|---------|-------|-------|
| Organization | [Y/N] | [Y/N] | [count] |
| LocalBusiness | [Y/N] | [Y/N] | [count] |
| Article | [Y/N] | [Y/N] | [count] |
| FAQPage | [Y/N] | [Y/N] | [count] |
| HowTo | [Y/N] | [Y/N] | [count] |
| Person (author) | [Y/N] | [Y/N] | [count] |
| Product | [Y/N] | [Y/N] | [count] |
| BreadcrumbList | [Y/N] | [Y/N] | [count] |
| WebSite (sitelinks search) | [Y/N] | [Y/N] | [count] |

### Missing Schema Opportunities
[List schema types that should be implemented based on the business type and content]

### Validation Errors
[List any schema validation errors found]
```

### Step 11: Write Section 9 — llms.txt Status

```markdown
## llms.txt Configuration

llms.txt is a standardized file (similar to robots.txt) that helps AI platforms
understand your site's structure, key content, and preferred citation format.

### Current Status
- **File exists:** [Yes/No]
- **Location:** [URL or "Not found"]
- **Completeness:** [assessment]

### Recommended llms.txt Content
[If missing, provide a recommended llms.txt configuration. If present but
incomplete, suggest improvements.]
```

### Step 12: Write Section 10 — Prioritized Action Plan

This is the most important section for the client. Organize all recommendations into three tiers:

```markdown
## Prioritized Action Plan

### Quick Wins (1-2 Weeks)
High impact, low effort. Implement these immediately.

| # | Action | Category | Expected Impact | Effort |
|---|--------|----------|-----------------|--------|
| 1 | [specific action] | [category] | [what improves] | [hours/days] |
| 2 | [specific action] | [category] | [what improves] | [hours/days] |
| 3 | [specific action] | [category] | [what improves] | [hours/days] |
| 4 | [specific action] | [category] | [what improves] | [hours/days] |
| 5 | [specific action] | [category] | [what improves] | [hours/days] |

### Medium-Term Improvements (1-3 Months)
Moderate effort, significant cumulative impact.

| # | Action | Category | Expected Impact | Effort |
|---|--------|----------|-----------------|--------|
| 1 | [specific action] | [category] | [what improves] | [estimate] |
| 2 | [specific action] | [category] | [what improves] | [estimate] |
| 3 | [specific action] | [category] | [what improves] | [estimate] |
| 4 | [specific action] | [category] | [what improves] | [estimate] |
| 5 | [specific action] | [category] | [what improves] | [estimate] |

### Strategic Initiatives (3-6 Months)
High effort, transformative impact on AI visibility.

| # | Action | Category | Expected Impact | Effort |
|---|--------|----------|-----------------|--------|
| 1 | [specific action] | [category] | [what improves] | [estimate] |
| 2 | [specific action] | [category] | [what improves] | [estimate] |
| 3 | [specific action] | [category] | [what improves] | [estimate] |
```

**Action Plan Rules:**
- Every action must be specific and implementable ("Add FAQPage schema to /services page" not "Improve schema")
- Include effort estimate so client can plan resources
- Quick Wins should be genuinely achievable in 1-2 weeks by a single person
- Strategic items should explain why the longer timeline is justified
- Maximum 5-7 items per tier — prioritize ruthlessly
- Each action traces back to a specific finding in the report

### Step 13: Write Section 11 — Competitor Comparison (Optional)

Include only if competitor data was collected during the audit.

```markdown
## Competitor Comparison

How [brand] compares to key competitors in GEO readiness:

| Metric | [Brand] | [Competitor 1] | [Competitor 2] | [Competitor 3] |
|--------|---------|----------------|----------------|----------------|
| GEO Readiness Score | X/100 | X/100 | X/100 | X/100 |
| AI Platform Visibility | X/5 platforms | X/5 | X/5 | X/5 |
| Content E-E-A-T | X/100 | X/100 | X/100 | X/100 |
| Schema Implementation | X types | X types | X types | X types |
| AI Crawler Access | X/5 allowed | X/5 | X/5 | X/5 |
| llms.txt | [Y/N] | [Y/N] | [Y/N] | [Y/N] |

### Competitive Gaps
[Where the client is behind and what to prioritize]

### Competitive Advantages
[Where the client is ahead and how to maintain it]
```

If no competitor data exists, omit this section entirely — do not include it with placeholder text.

### Step 14: Write Section 12 — Appendix

```markdown
## Appendix

### Methodology
This report was generated using the GeoSeo audit framework, which evaluates
websites across six dimensions of AI search readiness. Scoring methodology
details are available in the GeoSeo Scoring Methodology reference.

### Scoring Weights
| Category | Weight | Rationale |
|----------|--------|-----------|
| AI Citability & Visibility | 25% | How likely AI engines are to quote this site's content |
| Brand Authority Signals | 20% | Mentions on Reddit, YouTube, Wikipedia, LinkedIn |
| Content Quality (E-E-A-T) | 20% | Expertise signals, original data, author credentials |
| Technical Foundations | 15% | SSR, crawlability, Core Web Vitals, security |
| Structured Data | 10% | Schema completeness, JSON-LD validation |
| Platform Optimization | 10% | Per-platform readiness across 5 AI search engines |

### GEO vs Traditional SEO
GEO (Generative Engine Optimization) focuses on optimizing for AI-powered search
platforms, which generate synthesized answers rather than lists of links. While
traditional SEO remains important, GEO addresses the rapidly growing share of
search that bypasses traditional results entirely.

### AI Search Market Context
- AI-referred sessions have grown 527% year-over-year
- AI-sourced traffic converts at 4.4x the rate of traditional organic
- The GEO services market is projected to reach $7.3B by 2031
- Only 23% of marketers are currently investing in GEO

### Audit Date and Scope
- **Date:** [date]
- **URL:** [primary URL audited]
- **Scope:** [full audit / partial — list what was assessed]
- **Workflows executed:** [list of workflows that were run]

### Disclaimer
Scores and recommendations are based on publicly available data and automated
analysis at the time of the audit. AI platform algorithms change frequently.
Regular re-assessment (quarterly recommended) ensures continued optimization.
```

### Step 15: Assemble Final Report

Combine all sections into `GEO-CLIENT-REPORT.md` with:

1. Report title with brand name and date
2. Table of contents with section links
3. All 12 sections in order (omit Competitor Comparison if no data)
4. Consistent formatting throughout
5. No orphaned placeholders or template brackets

**Final quality checks:**
- [ ] GEO Readiness Score is calculated and prominently displayed
- [ ] Executive Summary can stand alone as a 1-page brief
- [ ] Every finding links to a recommendation in the Action Plan
- [ ] Action Plan items are specific, actionable, and effort-estimated
- [ ] No unexplained jargon — all technical terms defined on first use
- [ ] Report is 3,000-6,000 words
- [ ] Report is self-contained — no external dependencies to understand it
- [ ] All scores have context (what's good, what's bad, what's average)
- [ ] Missing data sections are clearly marked, not silently omitted
- [ ] Tone is professional, confident, and action-oriented throughout

---

## Key Principle

This report is the deliverable the client pays for. It must be clear enough for a non-technical founder to act on and detailed enough for a marketing team to execute against. Every paragraph should answer the question: "What should I do about this?"
