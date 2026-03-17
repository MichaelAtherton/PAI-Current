# GEO Audit Workflow

**Mode:** Full orchestrated audit with 5 parallel subagents | **Quick mode available**

## When to Use

- User says "geo audit", "full audit", "geo score", "audit [url]"
- User says "quick audit", "quick geo", "60-second", "snapshot" → triggers Quick Mode
- Default workflow when a URL is provided without a specific sub-command

---

## Output Directory Setup

**Before any analysis, resolve the output directory** *(see SKILL.md → Output Directory for full convention)*:

1. Extract domain slug from the target URL: strip protocol + `www.`, hostname only, dots→hyphens, lowercase, 63-char cap
2. Set today's date as `YYYY-MM-DD`
3. Create the output directory:
   ```bash
   GEO_OUTPUT="${PAI_DIR}/output/GeoSeo/{domain-slug}/{YYYY-MM-DD}"
   mkdir -p "$GEO_OUTPUT"
   ```
4. If the directory already exists (same-day re-audit), append `-2`, `-3`, etc.
5. All output files in this workflow are written to `$GEO_OUTPUT/`
6. Pass `$GEO_OUTPUT` to all subagents so they write to the same directory

---

## Quality Gates (Apply to ALL Modes)

| Gate | Limit | Action on Breach |
|------|-------|------------------|
| Max pages crawled | 50 | Stop crawling, note in report |
| Fetch timeout | 30 seconds per request | Skip page, log as unreachable |
| Rate limiting | 1 second delay between requests | Enforced via sleep between fetches |
| robots.txt | Must respect directives | Check FIRST before any crawling |
| Total audit timeout | 10 minutes | Produce partial report with disclaimer |

---

## Quick Mode

**Trigger:** User includes "quick", "snapshot", "60-second", or "fast" in request.

**Skip all subagents.** Do an inline 60-second snapshot:

### Quick Step 1: Fetch Homepage (5s)

```
WebFetch(url)
→ Extract: title, meta description, H1, H2s, word count
→ Note: Does the homepage have clear, citable answer blocks?
```

### Quick Step 2: Citability Spot Check (15s)

Score the homepage content only:
- Find the 3 most prominent content blocks (first H2 section, hero text, about section)
- For each block, evaluate:
  - Is it self-contained? (Can an AI quote it without needing surrounding context?)
  - Does it contain specific facts, numbers, or claims?
  - Is it 50-200 words? (optimal citation range)
- Quick citability score: count of blocks scoring YES on all 3 / total blocks × 100

### Quick Step 3: Crawler Access Check (15s)

```bash
# Fetch robots.txt
WebFetch("{domain}/robots.txt")
```

Check for blocks on these critical crawlers:
- GPTBot → ChatGPT/OpenAI
- ClaudeBot → Claude/Anthropic
- PerplexityBot → Perplexity

Score: 3/3 allowed = GREEN, 1-2 blocked = YELLOW, all blocked = RED

### Quick Step 4: Schema Spot Check (10s)

From the homepage HTML already fetched:
- Search for `application/ld+json` script blocks
- Check for: Organization, WebSite, FAQPage, HowTo, Article
- Score: 3+ types = GREEN, 1-2 = YELLOW, 0 = RED

### Quick Step 5: llms.txt Check (10s)

```
WebFetch("{domain}/llms.txt")
```

- Exists and valid → GREEN
- Exists but malformed → YELLOW
- Missing → RED

### Quick Output

```markdown
# ⚡ GEO Quick Snapshot: {domain}

**Date:** {YYYY-MM-DD}
**Mode:** 60-Second Snapshot

| Check | Status | Notes |
|-------|--------|-------|
| Citability | 🟢/🟡/🔴 | [X/3 blocks citable] |
| AI Crawlers | 🟢/🟡/🔴 | [X/3 critical crawlers allowed] |
| Schema Markup | 🟢/🟡/🔴 | [X types found] |
| llms.txt | 🟢/🟡/🔴 | [exists/missing/malformed] |

**Estimated GEO Readiness:** [High/Medium/Low/Critical]

## Top 3 Quick Wins
1. [Most impactful finding]
2. [Second finding]
3. [Third finding]

---
*Quick snapshot only. Run a full GEO audit for comprehensive scoring and recommendations.*
```

**STOP here for Quick Mode. Do not proceed to Full Audit.**

---

## Full Audit Workflow

### Phase 1: Discovery

#### Step 1.1: Fetch Homepage

```
WebFetch(url)
```

Capture and store:
- Full HTML content
- Page title and meta description
- All H1, H2, H3 headings
- Word count of main content area
- Internal links found on page
- External links found on page
- Any structured data (JSON-LD blocks)
- Open Graph and Twitter Card meta tags

#### Step 1.2: Detect Business Type

Analyze homepage content against detection signals. Score each type 0-10 based on signal density:

**SaaS Signals (score each 0-2):**
- Pricing page link (look for /pricing, "plans", "pricing" in nav)
- Sign up / free trial CTA (buttons, forms with "sign up", "start free", "get started")
- API documentation link (/docs, /api, "developers" in nav)
- Feature comparison tables
- Integration logos or partner mentions

**Local Business Signals (score each 0-2):**
- Physical address in header/footer (street address pattern matching)
- Phone number displayed prominently
- Google Maps embed or "directions" link
- Service area mentions ("serving [city]", "[city] [service]")
- Local schema markup (LocalBusiness, address, geo coordinates)

**E-commerce Signals (score each 0-2):**
- Product listing pages (/products, /shop, /store, /collections)
- Shopping cart icon or /cart link
- Price displays with currency symbols ($, €, £)
- "Add to cart" or "Buy now" buttons
- Product categories in navigation

**Publisher/Media Signals (score each 0-2):**
- Blog section (/blog, /articles, /news, /magazine)
- Article bylines (author names with dates)
- Category/tag navigation
- Comment sections or social share buttons
- RSS feed link or newsletter signup

**Agency/Services Signals (score each 0-2):**
- Portfolio or case studies section (/work, /portfolio, /case-studies)
- Client logos displayed
- "Contact us" or "Get a quote" as primary CTA
- Team page with individual bios
- Industry-specific service pages

**Classification:** Assign the type with the highest score. If tie, prefer: E-commerce > SaaS > Local > Publisher > Agency. Store as `business_type` for later use.

If score is below 3 for all types, classify as "General" and note that business type detection was inconclusive.

#### Step 1.3: Discover Site Structure

**Attempt sitemap discovery in order:**

```
1. WebFetch("{domain}/sitemap.xml")
2. WebFetch("{domain}/sitemap_index.xml")
3. Check robots.txt for Sitemap: directive
4. Fall back to link crawling from homepage (max 2 levels deep)
```

**From sitemap or crawl, build page inventory:**

For each page (max 50), record:
- URL
- Last modified date (from sitemap, if available)
- Estimated page type: Homepage, Product, Blog/Article, About, Contact, Pricing, Documentation, FAQ, Landing Page, Other
- Priority for analysis (based on page type and sitemap priority)

**Page priority for analysis:**
1. Homepage (always)
2. Pricing page (SaaS/E-commerce)
3. Top blog posts (Publisher) — pick 3 most recent
4. Product pages (E-commerce) — pick 3 top-level
5. Service pages (Agency) — pick 3 main services
6. About page
7. FAQ page
8. Documentation landing (SaaS)
9. Contact page
10. Remaining pages up to limit

**Store the page inventory as `site_pages` for subagent use.**

#### Step 1.4: Pre-Flight Checks

Before launching subagents, verify:

```
1. Homepage fetched successfully (non-empty, HTTP 200)
2. Business type detected (not "Unknown")
3. At least 5 pages discovered
4. robots.txt fetched and parsed
```

If homepage fetch fails entirely → ABORT with error message. Do not launch subagents against a site that cannot be reached.

If fewer than 5 pages found → proceed but note "Limited site structure detected" in report.

---

### Phase 2: Parallel Analysis

Launch 5 subagents simultaneously in a single message. Each subagent receives the homepage content, business type, and page inventory.

**CRITICAL: All 5 Task calls must be in ONE message for true parallelism.**

#### Subagent 1: GeoAiVisibility

```
Task({
  description: "GEO AI Visibility Analysis for {domain}",
  prompt: "You are the GeoAiVisibility analyzer. Assess how visible {domain} is in AI-powered search engines.

CONTEXT:
- Domain: {domain}
- Business type: {business_type}
- Homepage content: {homepage_content_summary}
- Pages to analyze: {top_10_pages}

ANALYZE:
1. **Brand Query Simulation**: For the brand name, what would an AI likely say? Would it cite this site?
2. **Category Query Simulation**: For the main product/service category, would this site appear in AI responses?
3. **Content Citability**: Score top 5 pages for AI citation readiness:
   - Self-contained answer blocks (can be quoted without context)
   - Statistical density (numbers, percentages, specific claims)
   - Structural clarity (clear headings, logical flow)
   - Unique insights (not generic advice available everywhere)
4. **Competitive Differentiation**: What unique claims or data does this site have that competitors likely don't?

SCORE (0-100):
- 80-100: AI engines would confidently cite this site for relevant queries
- 60-79: Some content is citable but inconsistent
- 40-59: Generic content, rarely cited over competitors
- 0-39: Content is not structured for AI citation

OUTPUT FORMAT:
Return a structured report with: overall_score (0-100), top_findings (list), critical_issues (list), recommendations (list), page_scores (dict of url: score)"
})
```

#### Subagent 2: GeoPlatformAnalysis

```
Task({
  description: "GEO Platform Readiness Analysis for {domain}",
  prompt: "You are the GeoPlatformAnalysis analyzer. Assess {domain}'s readiness across AI search platforms.

CONTEXT:
- Domain: {domain}
- Business type: {business_type}
- robots.txt content: {robots_txt_content}
- Homepage content: {homepage_content_summary}

ANALYZE EACH PLATFORM:

1. **ChatGPT/OpenAI**: GPTBot access in robots.txt, content depth for conversational answers, structured data that OpenAI can parse
2. **Google AI Overviews**: Featured snippet optimization, FAQ schema, HowTo schema, clear definitions, list formatting
3. **Perplexity**: PerplexityBot access, citation-ready content with sources, factual density
4. **Claude/Anthropic**: ClaudeBot access, long-form content quality, technical accuracy signals
5. **Bing Copilot**: Bing crawler access, Microsoft integration signals, Edge optimization
6. **Apple Intelligence**: Applebot-Extended access, Maps data (for local), structured contact info

PER-PLATFORM SCORING (0-100):
- Crawler access: 30 points (allowed = 30, blocked = 0)
- Content optimization for platform's style: 40 points
- Structural readiness (schema, metadata): 30 points

OUTPUT FORMAT:
Return: overall_score (0-100, average of platform scores), platform_scores (dict), critical_blocks (which platforms are blocked), optimization_gaps (list), recommendations (list)"
})
```

#### Subagent 3: GeoTechnical

```
Task({
  description: "GEO Technical SEO Analysis for {domain}",
  prompt: "You are the GeoTechnical analyzer. Assess {domain}'s technical foundation for AI search optimization.

CONTEXT:
- Domain: {domain}
- Business type: {business_type}
- Site pages: {site_pages}
- Homepage HTML: {homepage_html}

ANALYZE:

1. **Crawlability for AI**:
   - robots.txt completeness and AI crawler directives
   - Sitemap.xml presence, validity, and completeness
   - URL structure clarity (semantic, hierarchical)
   - Internal linking depth (can AI crawlers reach all content in ≤3 hops?)
   - Crawl budget signals (duplicate content, parameter URLs, thin pages)

2. **Rendering & Accessibility**:
   - JavaScript dependency (is core content in initial HTML or requires JS rendering?)
   - Server-side rendering detection (check for pre-rendered content)
   - Mobile responsiveness meta tag
   - Page load signals (large images, excessive scripts)

3. **Structured Data Foundation**:
   - JSON-LD blocks present (count and types)
   - Schema.org types implemented
   - Missing critical schemas for business type:
     - SaaS: Organization, SoftwareApplication, FAQPage, HowTo
     - Local: LocalBusiness, address, openingHours, geo
     - E-commerce: Product, Offer, AggregateRating, BreadcrumbList
     - Publisher: Article, NewsArticle, Person (author), BlogPosting
     - Agency: Organization, Service, Review, ProfessionalService

4. **AI-Specific Technical Signals**:
   - /llms.txt presence and quality
   - Canonical tags (preventing duplicate citation)
   - Hreflang (for multi-language AI responses)
   - Open Graph completeness (AI platforms use OG data for context)
   - Meta robots directives (noai, noimageai tags)

SCORING (0-100):
- Crawlability: 30 points
- Rendering: 20 points
- Structured Data: 30 points
- AI-Specific: 20 points

OUTPUT FORMAT:
Return: overall_score (0-100), category_scores (dict), critical_issues (list sorted by severity), warnings (list), recommendations (list with effort estimate: quick/medium/large)"
})
```

#### Subagent 4: GeoContent

```
Task({
  description: "GEO Content Quality Analysis for {domain}",
  prompt: "You are the GeoContent analyzer. Assess {domain}'s content quality through the lens of AI citation and E-E-A-T.

CONTEXT:
- Domain: {domain}
- Business type: {business_type}
- Pages to analyze: {priority_pages}

FOR EACH PRIORITY PAGE, FETCH AND ANALYZE:

1. **E-E-A-T Signals (Experience, Expertise, Authoritativeness, Trustworthiness)**:
   - Author attribution: Are articles bylined? Do authors have bio pages?
   - Credentials displayed: Qualifications, certifications, years of experience
   - Original research: First-party data, case studies, proprietary statistics
   - External citations: Does content reference and link to authoritative sources?
   - Publication dates: Are dates shown? Is content recent?
   - Review/editorial process signals

2. **Content Structure for AI**:
   - Answer-first format: Does content lead with the answer, not build up to it?
   - Definition blocks: Clear, quotable definitions for key terms?
   - Fact density: Specific numbers, percentages, dates per paragraph
   - Self-containment: Can paragraphs be understood in isolation?
   - List and table formatting: Structured data within content
   - Content freshness: Last updated dates, up-to-date statistics

3. **Topic Authority**:
   - Content depth: Word count vs topic complexity (thin = under 300w for complex topics)
   - Topic clustering: Are related topics covered comprehensively with internal links?
   - Unique value: What does this content offer that ChatGPT couldn't generate itself?
   - Proprietary data: Original statistics, surveys, benchmarks
   - Expert quotes or interviews

4. **Content Gaps for Business Type**:
   - SaaS: Missing comparison pages, missing 'vs' content, no integration guides
   - Local: Missing service area pages, no neighborhood content, thin service descriptions
   - E-commerce: Missing buying guides, no product comparisons, thin product descriptions
   - Publisher: Missing evergreen content, no pillar pages, weak topic clusters
   - Agency: Missing methodology pages, no process documentation, weak case studies

SCORING (0-100):
- E-E-A-T signals: 30 points
- AI-optimized structure: 30 points
- Topic authority: 25 points
- Content completeness: 15 points

OUTPUT FORMAT:
Return: overall_score (0-100), page_scores (dict of url: {score, strengths, weaknesses}), eeat_score, structure_score, authority_score, completeness_score, critical_gaps (list), rewrite_priorities (top 3 pages that need immediate attention with specific suggestions)"
})
```

#### Subagent 5: GeoSchema

```
Task({
  description: "GEO Schema Markup Analysis for {domain}",
  prompt: "You are the GeoSchema analyzer. Audit {domain}'s structured data implementation for AI search optimization.

CONTEXT:
- Domain: {domain}
- Business type: {business_type}
- Pages to analyze: {priority_pages}
- Homepage HTML: {homepage_html}

ANALYZE:

1. **Existing Schema Inventory**:
   For each page, extract all JSON-LD blocks and catalog:
   - Schema type (@type)
   - Completeness: How many recommended properties are filled vs available
   - Accuracy: Do values match visible page content?
   - Nesting: Are related schemas properly connected (e.g., Organization → ContactPoint)?

2. **Required Schemas by Business Type**:

   **ALL types need:**
   - Organization (name, url, logo, description, sameAs for social profiles)
   - WebSite (with SearchAction if applicable)
   - BreadcrumbList (on all inner pages)

   **SaaS additionally needs:**
   - SoftwareApplication (applicationCategory, operatingSystem, offers)
   - FAQPage (on FAQ and feature pages)
   - HowTo (on documentation/tutorial pages)
   - Review/AggregateRating (testimonials)

   **Local Business additionally needs:**
   - LocalBusiness (full address, phone, hours, geo coordinates)
   - Service (for each service offered)
   - Review/AggregateRating
   - Event (if applicable)

   **E-commerce additionally needs:**
   - Product (name, description, image, sku, offers with price/currency/availability)
   - AggregateRating and Review
   - Offer (price, priceCurrency, availability, itemCondition)
   - CollectionPage (for category pages)

   **Publisher additionally needs:**
   - Article/NewsArticle/BlogPosting (headline, author, datePublished, dateModified, image)
   - Person (for authors — name, url, sameAs, jobTitle)
   - ImageObject (for featured images)

   **Agency additionally needs:**
   - ProfessionalService or Organization
   - Service (for each service line)
   - Review/AggregateRating
   - Person (team members)

3. **Schema Quality Audit**:
   - Validate against Schema.org specifications
   - Check for deprecated properties
   - Verify URLs in schema resolve correctly
   - Check image URLs are valid
   - Ensure no conflicting schemas on same page
   - Test for Google Rich Results eligibility

4. **AI-Specific Schema Opportunities**:
   - FAQPage schema (powers direct AI answers)
   - HowTo schema (powers step-by-step AI responses)
   - SpecialAnnouncement (for timely content)
   - Dataset (for data-heavy pages)
   - ClaimReview (for fact-checking sites)

SCORING (0-100):
- Required schemas present: 40 points
- Schema completeness (properties filled): 25 points
- Schema accuracy (matches page content): 20 points
- Advanced/AI-specific schemas: 15 points

OUTPUT FORMAT:
Return: overall_score (0-100), schemas_found (list of {type, page, completeness_pct}), missing_required (list), missing_recommended (list), errors (list), recommendations (list with priority and code snippets for top 3 missing schemas)"
})
```

---

### Phase 3: Synthesis

#### Step 3.1: Collect Results

Wait for all 5 subagents to return. For each subagent, extract:
- `overall_score` (0-100)
- `critical_issues` (list)
- `recommendations` (list)

If any subagent fails or times out:
- Log the failure
- Use a score of 0 for that category
- Note "Analysis incomplete" in the report for that section

#### Step 3.2: Calculate Composite GEO Score

**Canonical weights defined in `ScoringMethodology.md` — if weights change, update there first.**

```
GEO Score = (
  AI_Visibility_Score × 0.25 +       # Citability: 25%
  Brand_Content_Score  × 0.20 +       # Brand/Content from GeoContent: 20%
  Content_Quality_Score × 0.20 +      # Content from GeoContent: 20%
  Technical_Score       × 0.15 +      # Technical: 15%
  Schema_Score          × 0.10 +      # Schema: 10%
  Platform_Score        × 0.10        # Platform: 10%
)
```

**Mapping subagent scores to categories:**
- Citability (25%) → GeoAiVisibility `overall_score`
- Brand (20%) → GeoContent `eeat_score` (E-E-A-T is brand authority)
- Content (20%) → GeoContent `overall_score`
- Technical (15%) → GeoTechnical `overall_score`
- Schema (10%) → GeoSchema `overall_score`
- Platform (10%) → GeoPlatformAnalysis `overall_score`

Round final score to nearest integer.

#### Step 3.3: Score Interpretation

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | AI-optimized leader. Fine-tune and maintain. |
| 75-89 | Good | Strong foundation with specific gaps to close. |
| 60-74 | Fair | Significant optimization opportunities. Quick wins available. |
| 40-59 | Poor | Major gaps in AI readiness. Structured intervention needed. |
| 0-39 | Critical | Not optimized for AI search at all. Full overhaul recommended. |

#### Step 3.4: Severity Classification

Classify all findings from all subagents:

**CRITICAL (fix immediately):**
- All Tier 1 AI crawlers blocked (GPTBot, ClaudeBot, PerplexityBot)
- No structured data at all
- Homepage returns error or is JS-only with no SSR
- Content is entirely AI-generated thin content
- No robots.txt exists

**HIGH (fix within 1 week):**
- One or more Tier 1 crawlers blocked
- Missing Organization schema
- No author attribution on any content
- Content below 300 words on key pages
- No sitemap.xml

**MEDIUM (fix within 30 days):**
- Missing business-type-specific schemas
- No llms.txt file
- Weak internal linking
- Content lacks specific statistics
- Missing FAQ structured data

**LOW (optimize when possible):**
- Missing Tier 3 crawler access
- OG tags incomplete
- Minor schema property gaps
- Content freshness signals missing

#### Step 3.5: Generate Quick Wins

Identify the top 5 actions that will produce the largest score improvement with the least effort:

**Quick Win Criteria:**
- Implementation time: under 1 hour
- No development resources needed (content or configuration changes)
- Expected score impact: 3+ points on composite score

**Typical quick wins (prioritize whichever apply):**
1. Unblock AI crawlers in robots.txt (+5-15 points)
2. Add Organization JSON-LD to homepage (+3-5 points)
3. Create llms.txt file (+2-4 points)
4. Add FAQ schema to existing FAQ content (+2-4 points)
5. Rewrite hero section as self-contained citable block (+2-3 points)
6. Add author bios to blog posts (+2-3 points)
7. Add publication dates to all content (+1-2 points)

#### Step 3.6: Build 30-Day Action Plan

Organize all recommendations into a phased plan:

**Week 1 — Critical Fixes & Quick Wins:**
- All CRITICAL severity items
- Top 5 quick wins
- Expected score improvement: [estimate]

**Week 2 — Technical Foundation:**
- All HIGH severity technical items
- Schema implementation for business type
- Sitemap and crawlability fixes
- Expected score improvement: [estimate]

**Week 3 — Content Optimization:**
- Rewrite top 3 priority pages for citability
- Add E-E-A-T signals (author bios, credentials, dates)
- Create missing content for business type gaps
- Expected score improvement: [estimate]

**Week 4 — Platform Optimization & Monitoring:**
- Platform-specific optimizations
- llms.txt creation/refinement
- Set up monitoring for AI citations
- LOW severity items
- Expected score improvement: [estimate]

---

### Phase 4: Report Output

Generate `GEO-AUDIT-REPORT.md` in the output directory (`$GEO_OUTPUT/`):

```markdown
# GEO Audit Report: {domain}

**Date:** {YYYY-MM-DD}
**Business Type:** {detected_type}
**Pages Analyzed:** {count}
**Audit Duration:** {time_taken}

---

## Executive Summary

{domain} scores **{score}/100** ({rating}) for AI search optimization readiness.

{2-3 sentence summary of the most important findings. Lead with the biggest opportunity or biggest risk.}

---

## GEO Score Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| AI Citability | 25% | {score}/100 | {weighted} |
| Brand Authority | 20% | {score}/100 | {weighted} |
| Content Quality | 20% | {score}/100 | {weighted} |
| Technical Foundation | 15% | {score}/100 | {weighted} |
| Schema Markup | 10% | {score}/100 | {weighted} |
| Platform Readiness | 10% | {score}/100 | {weighted} |
| **TOTAL** | **100%** | | **{total}/100** |

### Score Interpretation
{Rating}: {one-line meaning from interpretation table}

---

## Critical Findings

{List all CRITICAL severity items with explanation and fix}

## High Priority Findings

{List all HIGH severity items}

## Medium Priority Findings

{List all MEDIUM severity items}

## Low Priority Findings

{List all LOW severity items}

---

## Quick Wins (Under 1 Hour Each)

| # | Action | Expected Impact | Effort |
|---|--------|-----------------|--------|
| 1 | {action} | +{X} points | {time} |
| 2 | {action} | +{X} points | {time} |
| 3 | {action} | +{X} points | {time} |
| 4 | {action} | +{X} points | {time} |
| 5 | {action} | +{X} points | {time} |

---

## 30-Day Action Plan

### Week 1: Critical Fixes & Quick Wins
- [ ] {task}
- [ ] {task}
**Expected score after Week 1: {estimate}/100**

### Week 2: Technical Foundation
- [ ] {task}
- [ ] {task}
**Expected score after Week 2: {estimate}/100**

### Week 3: Content Optimization
- [ ] {task}
- [ ] {task}
**Expected score after Week 3: {estimate}/100**

### Week 4: Platform Optimization
- [ ] {task}
- [ ] {task}
**Expected score after Week 4: {estimate}/100**

---

## Detailed Analysis

### AI Citability Analysis
{Full output from GeoAiVisibility subagent, formatted}

### Platform Readiness
{Full output from GeoPlatformAnalysis subagent, formatted}

### Technical Foundation
{Full output from GeoTechnical subagent, formatted}

### Content Quality
{Full output from GeoContent subagent, formatted}

### Schema Markup
{Full output from GeoSchema subagent, formatted}

---

## Methodology

This audit was performed using PAI's GEO analysis framework. Scoring methodology:
- **Citability (25%)**: How likely AI engines are to quote this site's content in responses
- **Brand Authority (20%)**: E-E-A-T signals and brand differentiation
- **Content Quality (20%)**: Depth, structure, freshness, and unique value of content
- **Technical Foundation (15%)**: Crawlability, rendering, URL structure, and technical signals
- **Schema Markup (10%)**: Structured data completeness, accuracy, and AI-relevance
- **Platform Readiness (10%)**: Per-platform optimization across ChatGPT, Gemini, Perplexity, Claude, Bing Copilot

Pages analyzed: {count}/{total_discovered} (capped at 50 for audit efficiency)

---

*Generated by PAI GeoSeo Skill — {date}*
```

#### Post-Report Actions

1. **Save report** to `$GEO_OUTPUT/GEO-AUDIT-REPORT.md`
2. **Update `latest` symlink:**
   ```bash
   cd ${PAI_DIR}/output/GeoSeo/{domain-slug}
   ln -sfn {YYYY-MM-DD} latest
   ```
3. **Announce completion** with summary:
   ```
   GEO Audit complete for {domain}
   Score: {score}/100 ({rating})
   Top issue: {critical_finding_1}
   Top quick win: {quick_win_1}
   Full report: $GEO_OUTPUT/GEO-AUDIT-REPORT.md
   ```
4. **Suggest next steps**: "Run `geo report` to generate a client-ready PDF" or "Run `citability {url}` to deep-dive on specific pages"

---

## Error Handling

| Error | Response |
|-------|----------|
| Domain unreachable | Abort with clear error. Suggest checking URL. |
| robots.txt blocks all crawlers | Proceed with homepage only. Note limitation. |
| Subagent timeout (>3 min) | Use partial results. Note incomplete analysis. |
| Subagent returns invalid data | Score that category as 0. Note in report. |
| Fewer than 5 pages found | Proceed but flag "Limited site structure" |
| Non-HTML content type | Skip page, note in crawl log |

## Dependencies

- **Tools:** WebFetch (required), Task (for subagents)
- **Python tools:** `Tools/CitabilityScorer.py` (optional, used by Citability subagent)
- **Output:** `GEO-AUDIT-REPORT.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`
