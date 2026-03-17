# Content Quality & E-E-A-T Assessment Workflow

**Trigger:** "content quality", "e-e-a-t", "eeat", "content audit", "content assessment"

## Purpose

Evaluate a URL or set of pages for content quality through the lens of Google's E-E-A-T framework (Experience, Expertise, Authoritativeness, Trustworthiness), extended with GEO-specific modifiers for AI citability. Produces a scored assessment with actionable recommendations.

**Output:** `GEO-CONTENT-ANALYSIS.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

## When to Use

- Assessing whether content is strong enough to be cited by AI platforms
- Auditing content quality before a full GEO audit
- Evaluating a blog, landing page, or content hub for E-E-A-T signals
- Diagnosing why a site is not appearing in AI-generated answers
- Comparing content quality across competitor pages

## Input

- **Required:** URL of page or site to assess
- **Optional:** Target keywords, competitor URLs, industry/niche context

---

## Scoring Framework

### Base E-E-A-T Score (0-100)

| Dimension | Points | Weight Rationale |
|-----------|--------|------------------|
| Experience | 0-25 | First-hand, lived experience signals |
| Expertise | 0-25 | Demonstrated subject-matter depth |
| Authoritativeness | 0-25 | Recognition by peers, citations, credentials |
| Trustworthiness | 0-25 | Accuracy, transparency, reliability — **MOST CRITICAL** |

**Google's own guidelines state Trustworthiness is the most important dimension.** When in doubt, weight Trustworthiness scoring more conservatively.

### GEO Modifier Bonuses (0-40)

| Modifier | Points | Purpose |
|----------|--------|---------|
| Content Metrics | 0-15 | Word count, readability, structure quality |
| AI Content Assessment | 0-10 | Detection of AI-generated vs human-authored signals |
| Topical Authority | 0-10 | Breadth and depth of topic coverage across site |
| Content Freshness | 0-5 | Recency, update frequency, timeliness |

**Maximum possible score: 140** (base 100 + modifiers 40)
**Effective reporting scale: 0-140**, but thresholds below are calibrated to the base 100.

**IMPORTANT — Normalization for GEO composite:** When this score feeds into the GEO Readiness composite (as the "Content Quality" 20% category — see `ScoringMethodology.md` for canonical weights), normalize to 0-100 by capping at 100. Scores above 100 indicate exceptional content but are reported as 100 in the composite to maintain consistent weighting.

---

## Workflow Steps

### Step 1: Fetch and Parse Content

```bash
# Fetch the target URL
WebFetch(url, "Extract all visible text content, headings, meta tags, author info, dates, schema markup, internal links, and images with alt text")
```

**Extract and record:**
- Page title and meta description
- H1, H2, H3 heading hierarchy
- Full body text content
- Author name, bio, credentials (if present)
- Publication date and last-modified date
- Internal and external link count
- Image count and alt text presence
- Schema markup (Article, FAQ, HowTo, Person, Organization)
- Comments or user-generated content sections

### Step 2: Crawl Supporting Pages

```bash
# Fetch sitemap or crawl internal links to assess topical authority
WebFetch(sitemap_url, "Extract all URLs from sitemap, count total pages, identify content clusters and topic coverage")
```

**If no sitemap:**
- Extract internal links from the target page
- Follow up to 10 internal links to assess site depth
- Note navigation structure and content organization

**Record:**
- Total indexed pages (estimate)
- Number of pages on the same topic/cluster
- Presence of author pages, about pages, contact pages
- Blog post count and publishing frequency

### Step 3: Score Experience (0-25)

Evaluate first-hand, lived experience signals in the content.

| Signal | Points | How to Detect |
|--------|--------|---------------|
| First-person accounts ("I tested", "We implemented") | 0-5 | Scan for first-person narrative with specific details |
| Original photos, screenshots, or data | 0-5 | Check for non-stock images, original charts, proprietary data |
| Specific details only a practitioner would know | 0-5 | Look for nuanced insights, edge cases, practical tips |
| Case studies with real outcomes | 0-5 | Named clients, specific metrics, before/after comparisons |
| User-generated content (reviews, comments, community) | 0-5 | Check for active discussion, real user feedback |

**Scoring guide:**
- **20-25:** Rich first-hand experience throughout; original research/data; specific named examples
- **15-19:** Clear practitioner perspective with some original content
- **10-14:** General experience signals but lacks specificity
- **5-9:** Minimal experience signals; reads like secondary research
- **0-4:** No discernible first-hand experience; purely aggregated information

### Step 4: Score Expertise (0-25)

Evaluate demonstrated subject-matter knowledge.

| Signal | Points | How to Detect |
|--------|--------|---------------|
| Technical depth and accuracy | 0-5 | Correct terminology, nuanced explanations, no factual errors |
| Author credentials visible | 0-5 | Degree, certifications, job title, years of experience stated |
| Comprehensive coverage of subtopics | 0-5 | Addresses edge cases, alternatives, limitations, prerequisites |
| Citations to primary sources | 0-5 | Links to studies, official documentation, authoritative references |
| Structured methodology or framework | 0-5 | Step-by-step processes, decision trees, scoring systems |

**Scoring guide:**
- **20-25:** Deep expertise evident; correct technical detail; comprehensive coverage; strong citations
- **15-19:** Solid expertise; mostly accurate; good depth on core topic
- **10-14:** Adequate knowledge; surface-level treatment of complex subtopics
- **5-9:** Shallow expertise; generic advice; missing key nuances
- **0-4:** Inaccurate or misleading content; no demonstrated knowledge

### Step 5: Score Authoritativeness (0-25)

Evaluate external recognition and authority signals.

| Signal | Points | How to Detect |
|--------|--------|---------------|
| Author is a recognized figure in the field | 0-5 | Search for author name + topic; check LinkedIn, conference appearances |
| Site is a known authority in the niche | 0-5 | Domain age, backlink profile indicators, brand recognition |
| Content is referenced or cited by others | 0-5 | Search for URL or quoted passages in other sources |
| Professional affiliations and partnerships | 0-5 | Industry associations, certifications, notable client logos |
| Awards, press mentions, media coverage | 0-5 | Check for press page, "as seen in", award badges |

**To assess external authority:**
```bash
# Search for the brand/author reputation
WebSearch("[brand name] + [topic] reviews")
WebSearch("[author name] + [field] expertise")
```

**Scoring guide:**
- **20-25:** Widely recognized authority; frequently cited; strong brand in niche
- **15-19:** Established player; some external recognition; growing authority
- **10-14:** Moderate authority; limited external validation
- **5-9:** Little external recognition; new or unknown in the space
- **0-4:** No authority signals; anonymous or unverifiable authorship

### Step 6: Score Trustworthiness (0-25) — MOST CRITICAL

Evaluate accuracy, transparency, and reliability signals.

| Signal | Points | How to Detect |
|--------|--------|---------------|
| Factual accuracy (spot-check claims) | 0-5 | Verify 3-5 specific claims against known sources |
| Transparency: author, company, contact info | 0-5 | About page, physical address, contact form, privacy policy |
| Editorial standards: corrections, updates, disclosures | 0-5 | Correction notices, affiliate disclosures, conflict of interest statements |
| Security and privacy: HTTPS, cookie consent, privacy policy | 0-5 | Check for HTTPS, privacy policy link, GDPR compliance signals |
| Consistency: no contradictions, no misleading claims | 0-5 | Cross-reference claims within the page and across the site |

**Red flags that reduce Trustworthiness:**
- Missing contact information or physical address: **-5**
- No author attribution: **-3**
- Factual errors found during spot-check: **-5 per error**
- Deceptive practices (hidden affiliate links, fake reviews): **-10**
- No HTTPS: **-3**
- Excessive popup/interstitial ads: **-2**

**Scoring guide:**
- **20-25:** Highly transparent; factually accurate; clear editorial standards; full contact info
- **15-19:** Good transparency; minor gaps; mostly accurate
- **10-14:** Adequate but missing key trust signals (no author, limited contact info)
- **5-9:** Significant trust gaps; unverifiable claims; minimal transparency
- **0-4:** Major trust issues; deceptive practices; factual errors; anonymous

### Step 7: Calculate Content Metrics Modifier (0-15)

| Metric | Target | Points | Scoring |
|--------|--------|--------|---------|
| Word count | Varies by page type | 0-5 | See targets below |
| Readability (Flesch) | 60-70 | 0-5 | 60-70 = 5; 50-59 or 71-80 = 3; <50 or >80 = 1 |
| Structure quality | Well-organized | 0-5 | See criteria below |

**Word count targets:**
| Page Type | Minimum | Ideal | Maximum Before Penalty |
|-----------|---------|-------|----------------------|
| Homepage | 500 | 800-1200 | 2000 |
| Service/Product page | 800 | 1200-2000 | 3000 |
| Blog post | 1500 | 2000-3000 | 5000 |
| Pillar/Guide page | 3000 | 4000-6000 | 10000 |
| FAQ page | 500 | 1000-2000 | 3000 |

**Word count scoring:**
- Meets ideal range: **5 points**
- Meets minimum but below ideal: **3 points**
- Below minimum: **1 point**
- Significantly above maximum (padding): **2 points** (penalty for fluff)

**Readability assessment (approximate Flesch score):**
- Count average sentence length (words per sentence)
- Count average syllables per word
- Flesch = 206.835 - 1.015(words/sentence) - 84.6(syllables/word)
- Target: 60-70 (easily understood by 13-15 year olds)

**Paragraph quality:**
- Target: 40-80 words per paragraph
- Single-sentence paragraphs are acceptable for emphasis but should not dominate
- Wall-of-text paragraphs (150+ words): **-2 points**

**Structure quality scoring:**
- Clear H1 with keyword: **+1**
- Logical H2/H3 hierarchy: **+1**
- Bullet/numbered lists present: **+1**
- Table of contents for long content: **+1**
- Summary/TL;DR section: **+1**

### Step 8: AI Content Assessment Modifier (0-10)

Evaluate whether content appears AI-generated vs. human-authored. AI-generated content is not inherently penalized by Google, but generic AI content lacks the specificity that drives AI citations.

**AI content indicators (each reduces score):**

| Indicator | Penalty | Detection Method |
|-----------|---------|------------------|
| Generic phrasing ("In today's digital landscape") | -2 | Pattern matching common AI openings |
| Hedging overload ("It's important to note that") | -2 | Count hedge phrases per 500 words; >3 = flag |
| Lack of specificity (no names, numbers, dates) | -2 | Check for concrete examples, specific data points |
| Uniform sentence structure | -1 | Assess sentence length variation |
| Missing personal voice or opinion | -1 | Look for "I think", "In my experience", strong positions |
| Perfect grammar with no style personality | -1 | Overly formal, no colloquialisms, no humor |
| Repetitive transition phrases | -1 | "Furthermore", "Moreover", "Additionally" density |

**Common AI-generated openings to flag:**
- "In today's [adjective] landscape/world..."
- "When it comes to [topic]..."
- "In the ever-evolving world of..."
- "[Topic] has become increasingly important..."
- "Whether you're a [persona] or [persona]..."

**Scoring:**
- **8-10:** Clearly human-authored; strong voice; specific and opinionated
- **5-7:** Mostly human; some generic sections; adequate specificity
- **3-4:** Mixed signals; significant generic passages; may be AI-assisted
- **0-2:** Strongly appears AI-generated; generic throughout; no unique voice

### Step 9: Topical Authority Modifier (0-10)

Assess the site's depth of coverage on the topic.

**Page count assessment:**
```bash
# Count pages on the same topic cluster
# Use sitemap data from Step 2
```

| Coverage Level | Page Count | Score |
|----------------|------------|-------|
| Comprehensive authority | 20+ pages on topic | +10 |
| Strong coverage | 15-19 pages | +7 |
| Moderate coverage | 10-14 pages | +5 |
| Basic coverage | 5-9 pages | +2 |
| Minimal coverage | <5 pages | -5 (penalty) |

**Additional topical authority signals:**
- Content hub or pillar page structure: **+2 bonus** (max 10)
- Internal linking between topic pages: **+1 bonus**
- Regular publishing cadence on topic: **+1 bonus**
- Glossary or resource pages: **+1 bonus**

### Step 10: Content Freshness Modifier (0-5)

| Freshness Signal | Points |
|------------------|--------|
| Updated within 3 months | 5 |
| Updated within 6 months | 4 |
| Updated within 12 months | 3 |
| Updated within 24 months | 2 |
| Older than 24 months | 1 |
| No date visible at all | 0 |

**Freshness bonuses:**
- "Last updated" date visible on page: **+1** (max 5)
- Regular update cadence across site: **+1** (max 5)

**Freshness penalties (for time-sensitive topics):**
- Outdated statistics or references: **-2**
- Broken links to cited sources: **-1**
- References to deprecated tools/methods: **-1**

### Step 11: Calculate Final Score

```
Base E-E-A-T Score:
  Experience:        [0-25]
  Expertise:         [0-25]
  Authoritativeness: [0-25]
  Trustworthiness:   [0-25]
  ─────────────────────────
  Base Total:        [0-100]

GEO Modifiers:
  Content Metrics:   [0-15]
  AI Content:        [0-10]
  Topical Authority: [0-10] (can be negative)
  Content Freshness: [0-5]
  ─────────────────────────
  Modifier Total:    [-5 to 40]

FINAL SCORE:         [Base + Modifiers]
```

### Step 12: Interpret Score and Generate Recommendations

| Score Range | Rating | Interpretation | AI Citation Likelihood |
|-------------|--------|----------------|----------------------|
| 115-140 | Exceptional | Elite content; best-in-class authority | Very high — strong citation candidate |
| 85-114 | Strong | High-quality content with clear authority | High — likely to be cited by AI platforms |
| 70-84 | Solid | Good content with room for improvement | Moderate — may be cited for specific queries |
| 55-69 | Developing | Adequate but significant gaps exist | Low — rarely cited without improvements |
| 40-54 | Weak | Major quality or trust issues | Very low — needs substantial overhaul |
| Below 40 | Critical | Fundamental content strategy needed | Negligible — complete rebuild recommended |

### Step 13: Generate Output Report

Write `GEO-CONTENT-ANALYSIS.md` to the output directory (`${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`) with the following structure:

```markdown
# GEO Content Quality & E-E-A-T Analysis

**URL:** [target URL]
**Date:** [analysis date]
**Analyst:** GeoSeo Content Workflow

---

## Score Summary

| Dimension | Score | Max | Rating |
|-----------|-------|-----|--------|
| Experience | X | 25 | [rating] |
| Expertise | X | 25 | [rating] |
| Authoritativeness | X | 25 | [rating] |
| Trustworthiness | X | 25 | [rating] |
| **Base E-E-A-T** | **X** | **100** | **[rating]** |
| Content Metrics | X | 15 | [rating] |
| AI Content Assessment | X | 10 | [rating] |
| Topical Authority | X | 10 | [rating] |
| Content Freshness | X | 5 | [rating] |
| **FINAL SCORE** | **X** | **140** | **[rating]** |

## Experience Assessment
[Detailed findings with specific examples from the content]

## Expertise Assessment
[Detailed findings with specific examples from the content]

## Authoritativeness Assessment
[Detailed findings with specific examples from the content]

## Trustworthiness Assessment
[Detailed findings with specific examples from the content]

## Content Metrics
- **Word Count:** X words ([meets/below/exceeds] target of Y for [page type])
- **Readability:** Flesch ~X ([assessment])
- **Structure:** [assessment of heading hierarchy, lists, formatting]

## AI Content Signals
[Flags found, specific examples of generic/AI phrasing if detected]

## Topical Authority
- **Pages on topic:** X pages
- **Content hub structure:** [yes/no, description]
- **Internal linking:** [assessment]

## Content Freshness
- **Last updated:** [date or "not visible"]
- **Publishing cadence:** [assessment]

## Priority Recommendations

### Quick Wins (implement within 1 week)
1. [specific, actionable recommendation]
2. [specific, actionable recommendation]
3. [specific, actionable recommendation]

### Medium-Term (implement within 1-3 months)
1. [specific, actionable recommendation]
2. [specific, actionable recommendation]

### Strategic (3-6 months)
1. [specific, actionable recommendation]
2. [specific, actionable recommendation]

## Competitor Comparison (if competitor URLs provided)
| Metric | Target Site | Competitor 1 | Competitor 2 |
|--------|-------------|--------------|--------------|
| E-E-A-T Base | X | X | X |
| Final Score | X | X | X |
| Word Count | X | X | X |
| Topical Authority | X pages | X pages | X pages |
```

---

## Quality Checks Before Delivery

1. **Every score has a justification** — no score without a specific content example
2. **Recommendations are actionable** — "Add author bio with credentials" not "Improve expertise"
3. **Trustworthiness is weighted most heavily** — if Trust score is low, flag it prominently regardless of other scores
4. **AI citation likelihood is clearly stated** — the client needs to know if their content will be picked up
5. **No false positives on AI content detection** — technical writing can appear AI-like; consider context
6. **Word count is assessed against page type** — do not penalize a homepage for being under 1500 words

---

## Key Principle

Content quality is the foundation of GEO performance. AI platforms cite content that demonstrates genuine expertise and trustworthiness. A page with a perfect technical SEO setup but thin, generic content will never be cited. Score honestly and recommend specifically.
