# GEO llms.txt Analysis & Generation Workflow

**Mode:** Analysis of existing llms.txt OR generation of new one | **Single-domain**

## When to Use

- User says "llms.txt", "llms txt", "generate llms", "check llms.txt"
- Called as subcomponent of the full Audit workflow (within GeoTechnical subagent)
- User wants to create or improve their /llms.txt file for AI engine consumption

---

## Core Concept

**llms.txt** is an emerging standard (proposed by Jeremy Howard / Answer.AI) that provides LLMs with a structured overview of a website's content. It serves as a "table of contents for AI" — helping language models understand what a site offers, which pages are most important, and how to describe them accurately.

**Why it matters:**
- LLMs use llms.txt to build more accurate representations of a site
- It reduces hallucination about your brand (you define how you're described)
- It prioritizes which content AI should focus on
- It's the equivalent of a sitemap.xml but optimized for language models instead of search crawlers

**Two files:**
- `/llms.txt` — Concise overview with key pages and descriptions (typically 1-5KB)
- `/llms-full.txt` — Extended version with more detailed content and full page descriptions (optional, can be larger)

**Standard Format (llms.txt specification):**

```markdown
# {Site Name}

> {One-line description of the site/company}

## {Section Name}

- [{Page Title}]({URL}): {Brief description of what this page covers}
- [{Page Title}]({URL}): {Brief description}

## {Another Section}

- [{Page Title}]({URL}): {Brief description}
```

**Format rules:**
- H1 (`#`) — Site name (exactly one)
- Blockquote (`>`) — Site description (immediately after H1)
- H2 (`##`) — Section headings (group pages by topic)
- Bullet entries (`-`) — Individual pages with `[Title](URL): Description` format
- Optional: Additional markdown paragraphs within sections for context

---

## Workflow

### Step 1: Check for Existing llms.txt

```
WebFetch("{domain}/llms.txt")
```

**Result A: File exists** → Proceed to Step 2 (Validate & Score)

**Result B: File returns 404/empty** → Record "llms.txt not found"

Then check for llms-full.txt:

```
WebFetch("{domain}/llms-full.txt")
```

**Record status of both files.** If neither exists, skip to Step 4 (Generate).

---

### Step 2: Validate Existing llms.txt

If llms.txt exists, validate its format and content against the specification.

#### 2.1: Format Validation

Check each structural requirement:

| Check | Expected | Pass/Fail |
|-------|----------|-----------|
| H1 title present | Exactly one `# Title` line | ✓/✗ |
| H1 matches site name | Title reflects the actual brand/site name | ✓/✗ |
| Blockquote description | `> description` immediately after H1 | ✓/✗ |
| H2 sections present | At least 2 `## Section` headings | ✓/✗ |
| Bullet entries format | `- [Title](URL): Description` per line | ✓/✗ |
| URLs are absolute | All URLs start with https:// or http:// | ✓/✗ |
| No broken markdown | All links properly formatted, no orphaned brackets | ✓/✗ |
| Reasonable length | Between 500 bytes and 50KB | ✓/✗ |
| UTF-8 encoding | No encoding errors or garbled characters | ✓/✗ |

**Format score:** Count of passing checks / total checks × 100

#### 2.2: URL Validation

For each URL listed in llms.txt (up to 30):

```
WebFetch(url) or curl -s -o /dev/null -w "%{http_code}" -L "url"
```

**Record per URL:**
- HTTP status code (200 = valid, 301/302 = redirect, 404 = broken, other = issue)
- Whether the page title matches the link text in llms.txt
- Whether the page content matches the description in llms.txt

**URL health score:** Count of valid URLs (200 or working redirect) / total URLs × 100

#### 2.3: Content Analysis

Evaluate the llms.txt content quality:

**Completeness — Does it cover the site's key content?**

Fetch the site's sitemap or crawl the homepage to discover key pages:
```
WebFetch("{domain}/sitemap.xml")
```

Compare pages in llms.txt against discovered pages:
- Are the most important pages included? (Homepage, main product/service pages, key blog posts)
- Are obvious sections missing? (No blog section when site has a blog, no pricing when SaaS, etc.)
- Coverage ratio: pages in llms.txt / important pages discovered

**Accuracy — Do descriptions match reality?**

For the top 5 URLs in llms.txt, fetch the page and verify:
- Does the description in llms.txt accurately reflect the page content?
- Is the page title in the link text correct?
- Are there any outdated descriptions (referencing old products, wrong prices, etc.)?

**Usefulness — Would an LLM find this helpful?**

Evaluate descriptions for LLM utility:
- Are descriptions specific enough to differentiate pages? (Not just "Learn more about X")
- Do descriptions contain key facts an LLM would need? (What the page teaches, what questions it answers)
- Are sections logically organized? (By topic, not by URL structure)
- Is the site description in the blockquote accurate and specific?

---

### Step 3: Score Existing llms.txt

#### Completeness (40% of total score)

```
completeness_score based on:
- Key pages coverage: 0-50 points
  - Homepage referenced: 10 points
  - Main product/service pages: 15 points (proportional to coverage)
  - Blog/content section: 10 points (if site has blog)
  - About/company page: 5 points
  - Other important sections: 10 points (proportional)

- Section organization: 0-30 points
  - Logical grouping by topic: 15 points
  - No empty sections: 5 points
  - Sections match site's actual structure: 10 points

- No critical omissions: 0-20 points
  - Deduct 10 per missing critical section (e.g., no products section for e-commerce)
  - Minimum 0

completeness_raw = key_pages + section_org + no_omissions  # 0-100
completeness_score = completeness_raw
```

#### Accuracy (35% of total score)

```
accuracy_score based on:
- URL validity: 0-30 points
  - All URLs return 200: 30 points
  - Deduct (30 / total_urls) per broken URL
  - Redirects count as 50% valid

- Description accuracy: 0-40 points
  - For each verified page: does description match content?
  - Score each 0-10, average across verified pages, scale to 40

- Title accuracy: 0-20 points
  - For each verified page: does link text match page title?
  - Score each 0-10, average across verified pages, scale to 20

- Freshness: 0-10 points
  - No outdated references: 10 points
  - Some outdated content: 5 points
  - Clearly stale: 0 points

accuracy_raw = url_validity + desc_accuracy + title_accuracy + freshness  # 0-100
accuracy_score = accuracy_raw
```

#### Usefulness (25% of total score)

```
usefulness_score based on:
- Description specificity: 0-35 points
  - Generic ("Learn about X"): 0 per entry
  - Moderate ("Guide to implementing X for Y"): 5 per entry
  - Specific ("Step-by-step tutorial for implementing OAuth2 in Node.js with code examples"): 10 per entry
  - Average across entries, scale to 35

- LLM utility: 0-35 points
  - Would an LLM citing this file produce accurate summaries? 0-15
  - Does the file help an LLM understand what questions this site answers? 0-10
  - Does the blockquote description capture the site's unique value? 0-10

- Organization quality: 0-30 points
  - Sections are intuitive: 10 points
  - Pages are in logical order within sections: 10 points
  - No duplicate entries: 10 points

usefulness_raw = specificity + llm_utility + organization  # 0-100
usefulness_score = usefulness_raw
```

#### Composite Score

```
llmstxt_score = (
  completeness_score × 0.40 +
  accuracy_score     × 0.35 +
  usefulness_score   × 0.25
)
```

Round to nearest integer.

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Comprehensive, accurate, and highly useful for LLMs |
| 75-89 | Good | Solid coverage with minor gaps or stale entries |
| 60-74 | Fair | Exists but needs significant improvements |
| 40-59 | Poor | Major gaps in coverage, accuracy, or usefulness |
| 0-39 | Critical | Barely functional or severely outdated |

**If existing file scored, skip to Step 6 (Output Report) unless user also requests generation/improvement.**

---

### Step 4: Discover Site Content (For Generation)

If llms.txt doesn't exist, or user requests generation/improvement, discover the site's content:

#### 4.1: Crawl Site Structure

```
WebFetch("{domain}/sitemap.xml")    → Parse all URLs and last-modified dates
WebFetch("{domain}")                → Extract navigation, internal links
WebFetch("{domain}/robots.txt")     → Check for disallowed paths
```

**Build page inventory:**

For each discovered page, record:
- URL
- Page title (from sitemap or link text)
- Estimated type: Product, Blog, Docs, About, Pricing, FAQ, Landing, API, Legal
- Last modified date (if available)
- Priority (from sitemap priority tag, or inferred from site structure)

#### 4.2: Prioritize Pages for Inclusion

**Include (always, if they exist):**
- Homepage
- Main product/service pages (up to 5)
- Pricing page
- About page
- Documentation landing page
- API reference landing page
- Blog index page

**Include (top selections):**
- Top 5 blog posts (most recent or highest priority)
- Top 3 documentation pages (getting started, key concepts, tutorials)
- FAQ page
- Contact page
- Case studies (top 3)

**Exclude:**
- Legal pages (privacy policy, terms of service) — unless legal site
- Login/signup pages
- Admin or internal pages
- Pagination pages (/page/2, /page/3)
- Tag/category archive pages (include parent only)
- Duplicate content pages
- Pages blocked in robots.txt

**Target:** 15-40 page entries total. Quality over quantity.

#### 4.3: Fetch Key Pages for Description Writing

For the top 20 priority pages, fetch content to write accurate descriptions:

```
WebFetch(page_url)
→ Extract: title, meta description, H1, first 2 paragraphs, key topics
```

Respect rate limiting: 1 second delay between fetches.

---

### Step 5: Generate llms.txt

#### 5.1: Determine Sections

Group pages into logical sections based on content type and site structure:

**Common section patterns by business type:**

**SaaS:**
```
## Product
## Features
## Documentation
## Blog
## Company
```

**E-commerce:**
```
## Products
## Buying Guides
## Support
## Blog
## About
```

**Publisher:**
```
## Featured Content
## Topics
## Authors
## About
```

**Agency:**
```
## Services
## Case Studies
## Resources
## Company
```

**Local Business:**
```
## Services
## Service Areas
## Reviews
## About
```

#### 5.2: Write Descriptions

For each page entry, write a description that:

1. **Starts with what the page IS** (not "This page is about...")
   - GOOD: "Step-by-step guide to implementing SSO with SAML 2.0, including code examples for Python and Node.js"
   - BAD: "Learn more about our SSO feature"

2. **Includes key facts an LLM would need:**
   - What questions does this page answer?
   - What unique information does it contain?
   - What topics does it cover in depth?

3. **Is 10-30 words** (concise but specific)

4. **Uses natural language** (not keyword-stuffed marketing copy)

#### 5.3: Compose the File

```markdown
# {Site Name}

> {Company/site description: what they do, who they serve, what makes them distinctive. 1-2 sentences, 20-40 words.}

## {Section 1}

- [{Page Title}]({absolute_url}): {Description. 10-30 words, specific and factual.}
- [{Page Title}]({absolute_url}): {Description.}

## {Section 2}

- [{Page Title}]({absolute_url}): {Description.}
- [{Page Title}]({absolute_url}): {Description.}

{Continue for all sections}
```

#### 5.4: Generate llms-full.txt (Optional)

If user requests or if site has rich content, also generate llms-full.txt:

- Same structure as llms.txt
- Extended descriptions (30-80 words per entry)
- Additional context paragraphs within sections
- More pages included (up to 60)
- Include key facts, statistics, or methodology descriptions inline

---

### Step 6: Output Report

Generate `GEO-LLMSTXT-ANALYSIS.md` in the output directory *(see SKILL.md → Output Directory for path convention: `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`)*:

```markdown
# GEO llms.txt Analysis: {domain}

**Date:** {YYYY-MM-DD}
**llms.txt Status:** {Exists - Scored / Missing - Generated / Missing - Not Generated}
**llms-full.txt Status:** {Exists / Missing}

---

## Executive Summary

{2-3 sentences about the current state and recommendations}

---

{IF EXISTING FILE WAS ANALYZED:}

## Current llms.txt Score: {score}/100 ({rating})

### Score Breakdown

| Category | Weight | Score | Notes |
|----------|--------|-------|-------|
| Completeness | 40% | {score}/100 | {X pages covered / Y important pages} |
| Accuracy | 35% | {score}/100 | {X/Y URLs valid, descriptions verified} |
| Usefulness | 25% | {score}/100 | {quality assessment} |
| **TOTAL** | **100%** | **{score}/100** | |

### Format Validation

| Check | Status |
|-------|--------|
| H1 title | {details} |
| Blockquote description | {details} |
| H2 sections | {count found} |
| Bullet entry format | {X/Y correctly formatted} |
| Absolute URLs | {details} |
| Reasonable length | {file size} |

### URL Health

| URL | Status | Title Match | Description Match |
|-----|--------|-------------|-------------------|
| {url} | 200 / 404 / 301 | yes/no | yes/no |
{...verified URLs}

**URL Health Rate:** {valid}/{total} ({percentage}%)

### Missing Pages

These important pages were discovered but not included in llms.txt:

| Page | Type | Why It Should Be Included |
|------|------|---------------------------|
| {url} | {type} | {reason} |
{...missing important pages}

### Description Quality Issues

| Entry | Issue | Suggested Improvement |
|-------|-------|-----------------------|
| {page title} | {issue: too vague / inaccurate / outdated} | {better description} |
{...issues found}

{END IF EXISTING FILE}

---

{IF FILE WAS GENERATED:}

## Generated llms.txt

**Pages discovered:** {total}
**Pages included:** {included}
**Sections created:** {count}

### Generation Process
1. Crawled sitemap: {X pages found}
2. Analyzed homepage navigation: {Y additional pages}
3. Fetched {Z} key pages for description writing
4. Grouped into {N} logical sections
5. Wrote descriptions for {M} page entries

### Generated File

The following llms.txt has been generated and saved to the output directory:

```
{Full generated llms.txt content}
```

{IF llms-full.txt also generated:}

### Generated llms-full.txt

```
{Full generated llms-full.txt content}
```

{END IF}

### Installation Instructions

1. Save the generated `llms.txt` file to your domain root (accessible at `{domain}/llms.txt`)
2. Ensure the file is served with `Content-Type: text/plain; charset=utf-8`
3. Do NOT block it in robots.txt
4. Optionally add a reference in your HTML:
   ```html
   <link rel="help" href="/llms.txt" type="text/plain" title="LLM Site Guide">
   ```
5. Update the file whenever you add, remove, or significantly change pages

{END IF GENERATED}

---

## Recommendations

### Immediate Actions
{numbered list of highest-priority improvements}

### Ongoing Maintenance
- Review llms.txt monthly for accuracy
- Add new pages when they're published
- Remove pages that are deleted or redirected
- Update descriptions when page content changes significantly
- Check URL health quarterly (broken links degrade AI trust)

### Advanced Optimizations
- Create llms-full.txt with extended descriptions for richer AI understanding
- Include key statistics and differentiators in descriptions
- Organize sections to match user intent patterns (what questions are people asking?)
- Cross-reference with sitemap.xml to ensure alignment

---

*Generated by PAI GeoSeo llms.txt Analyzer — {date}*
```

#### File Outputs

Depending on the workflow path, save the following files to the output directory (`${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`):

| Scenario | Files Output |
|----------|-------------|
| Existing llms.txt analyzed | `GEO-LLMSTXT-ANALYSIS.md` |
| llms.txt generated | `GEO-LLMSTXT-ANALYSIS.md` + `llms.txt` |
| llms.txt + llms-full.txt generated | `GEO-LLMSTXT-ANALYSIS.md` + `llms.txt` + `llms-full.txt` |
| Existing analyzed + improved version | `GEO-LLMSTXT-ANALYSIS.md` + `llms-txt-improved.txt` |

---

## Error Handling

| Error | Response |
|-------|----------|
| Domain unreachable | Abort with error |
| llms.txt exists but is binary/non-text | Flag as CRITICAL format error, score 0 |
| llms.txt is extremely large (>100KB) | Analyze first 50KB only, flag unusual size |
| No sitemap and few discoverable pages | Generate minimal llms.txt from homepage links only, note limitation |
| Page fetches fail during description writing | Use meta description or link text as fallback, note "unverified" |
| Site is entirely behind authentication | Cannot generate meaningful llms.txt, report limitation |

## Dependencies

- **Tools:** WebFetch (required)
- **Output:** `GEO-LLMSTXT-ANALYSIS.md` and optionally `llms.txt`, `llms-full.txt` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`
