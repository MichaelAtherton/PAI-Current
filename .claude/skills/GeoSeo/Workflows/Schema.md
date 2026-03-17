# Schema and Structured Data Audit Workflow

**8-step schema audit with GEO-critical structured data assessment and JSON-LD template generation**

## Purpose

Audit a website's structured data implementation for AI search engine optimization. Schema markup — especially `sameAs` properties — is the bridge between a website and its cross-platform entity identity. AI models use structured data to resolve entities, understand authority, and determine citation worthiness.

**Core Insight:** `sameAs` is the single most important schema property for GEO. It enables cross-platform entity resolution — telling AI models that your website, your LinkedIn, your YouTube, your Wikipedia page, and your Wikidata entry are all the same entity.

## When to Use

- Auditing existing schema markup quality
- Identifying missing GEO-critical schemas
- Generating ready-to-use JSON-LD templates
- Checking for deprecated schema types
- Verifying AI crawler compatibility of schema delivery

## Input

- **URL** (required): The domain to audit
- **Pages to check** (optional): Specific pages (default: homepage + 3-5 key pages)
- **Brand social profiles** (optional): URLs for sameAs generation

---

## Workflow Steps

### Step 1: Detect Existing Schema Markup

**Scan for all three schema formats across target pages.**

**Step 1.1: Fetch Pages**

Fetch the following pages (minimum):
- Homepage
- About page
- 2-3 blog/article pages
- Primary service/product page
- Contact page (if exists)

**Step 1.2: Extract Schema by Format**

For each page, detect and extract:

```
JSON-LD:
  - Look for <script type="application/ld+json"> tags
  - Parse JSON content
  - Record each @type found

Microdata:
  - Look for itemscope, itemtype, itemprop attributes
  - Record each itemtype found
  - Note: Microdata is harder for AI crawlers to parse

RDFa:
  - Look for typeof, property, vocab attributes
  - Record each typeof found
  - Note: RDFa is rarely used and poorly supported by AI crawlers
```

**Step 1.3: Format Assessment**

| Format | GEO Compatibility | Recommendation |
|--------|-------------------|----------------|
| **JSON-LD** | Excellent — preferred by Google, parseable by all AI crawlers | Use this exclusively |
| **Microdata** | Fair — parseable but harder to maintain, less consistent extraction | Migrate to JSON-LD |
| **RDFa** | Poor — rarely parsed by AI crawlers, complex syntax | Migrate to JSON-LD |

**Record:** Which format(s) are in use, which pages have schema, which pages are missing schema entirely.

---

### Step 2: Validate Existing Schema

**Step 2.1: Syntax Validation**

For each JSON-LD block found:

```
1. Parse as JSON — check for syntax errors (missing commas, unescaped quotes, etc.)
2. Verify @context is "https://schema.org" (not http, not missing)
3. Verify @type is a valid schema.org type
4. Check for required properties per type:
   - Organization: name, url (minimum)
   - Person: name (minimum)
   - Article: headline, author, datePublished (minimum)
   - WebSite: name, url (minimum)
   - BreadcrumbList: itemListElement (minimum)
5. Check for nested type errors (e.g., author should be Person type, not a plain string)
6. Flag any properties with empty or placeholder values
```

**Step 2.2: Content Accuracy Validation**

```
For each schema block, verify:
1. Organization name matches actual brand name on page
2. URLs point to valid, live pages
3. Dates are in ISO 8601 format and reasonable
4. Image URLs return valid images
5. Author names match actual author bylines
6. Phone/address match actual contact information
7. sameAs URLs are valid and point to correct profiles
```

**Step 2.3: Record Validation Issues**

| Issue Type | Severity | Example |
|-----------|----------|---------|
| Invalid JSON syntax | Critical | Missing closing bracket |
| Wrong @context | High | Using http instead of https |
| Missing required property | High | Article without headline |
| Property type mismatch | Medium | author as string instead of Person |
| Empty/placeholder value | Medium | `"description": ""` |
| Outdated information | Low | Old address, former employee name |

---

### Step 3: Check Google Rich Results Eligibility

**Step 3.1: Rich Result Types Assessment**

For each schema type found, check if it qualifies for Google rich results:

| Schema Type | Rich Result | Requirements Met? |
|-------------|------------|-------------------|
| Article | Article rich result | headline, image, author, publisher, datePublished |
| Product | Product rich result | name, image, offers (price, availability) |
| LocalBusiness | Local pack | name, address, telephone, openingHours |
| FAQPage | FAQ rich result | **RESTRICTED since Aug 2023** — only for government/health sites |
| HowTo | How-to rich result | **REMOVED since Sep 2023** — no longer generates rich results |
| Review | Review snippet | itemReviewed, reviewRating, author |
| Event | Event rich result | name, startDate, location |
| BreadcrumbList | Breadcrumb trail | itemListElement with position, name, item |
| WebSite + SearchAction | Sitelinks search box | potentialAction with target URL template |

**Step 3.2: Note Deprecated/Restricted Types**

```
DEPRECATED — Remove or repurpose:
  - HowTo: Rich results removed September 2023. Schema can remain for
    semantic purposes but generates no visual benefit.
  - FAQPage: Restricted to government and health authority sites since
    August 2023. Remove from commercial sites — it will be ignored.

STILL VALID but check implementation:
  - All other types remain eligible with correct implementation.
```

---

### Step 4: Evaluate GEO-Critical Schemas

**These are the schema types that directly impact AI search visibility.**

**Step 4.1: Organization Schema (20 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Brand Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Clear, comprehensive description of the organization",
  "foundingDate": "2020-01-15",
  "founders": [{"@type": "Person", "name": "Founder Name"}],
  "sameAs": [
    "https://www.linkedin.com/company/brand",
    "https://twitter.com/brand",
    "https://www.youtube.com/@brand",
    "https://github.com/brand",
    "https://www.wikidata.org/wiki/Q123456",
    "https://en.wikipedia.org/wiki/Brand_Name"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "support@example.com"
  }
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| Organization schema exists on homepage | 5 | Present? |
| Includes name, url, logo, description | 5 | All four present? |
| sameAs with 3+ platform URLs | 5 | Count sameAs entries |
| sameAs includes LinkedIn, YouTube, Wikipedia/Wikidata | 5 | Specific high-value platforms? |

**Step 4.2: Person/Author Schema (15 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Author Name",
  "url": "https://example.com/team/author-name",
  "jobTitle": "Chief Technology Officer",
  "worksFor": {"@type": "Organization", "name": "Brand Name"},
  "sameAs": [
    "https://www.linkedin.com/in/authorname",
    "https://twitter.com/authorname"
  ],
  "image": "https://example.com/photos/author.jpg",
  "description": "Brief professional bio"
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| Person schema on author/team pages | 5 | Present on author pages? |
| Linked as author in Article schemas | 5 | Article.author references Person? |
| Includes sameAs, jobTitle, worksFor | 5 | Professional identity signals? |

**Step 4.3: Article Schema (15 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/team/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand Name",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  },
  "datePublished": "2025-01-15T08:00:00Z",
  "dateModified": "2025-03-01T10:30:00Z",
  "image": "https://example.com/images/article-image.jpg",
  "description": "Meta description of the article"
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| Article schema on blog/content pages | 5 | Present on content pages? |
| Includes dateModified (not just datePublished) | 5 | dateModified present and accurate? |
| Author is Person type (not just string) | 5 | Proper nested author object? |

**Step 4.4: sameAs Property Audit (15 points)**

**This is the most important single property for GEO.**

```
Check Organization.sameAs for:
1. LinkedIn company URL ✓/✗
2. YouTube channel URL ✓/✗
3. Wikipedia article URL ✓/✗
4. Wikidata entity URL ✓/✗
5. Twitter/X profile URL ✓/✗
6. GitHub organization URL ✓/✗
7. Facebook page URL ✓/✗
8. Crunchbase URL ✓/✗
```

| Criteria | Points | Check |
|----------|--------|-------|
| sameAs property exists in Organization schema | 3 | Present? |
| Contains 3+ valid platform URLs | 4 | Count and validate URLs |
| Includes at least 2 of: LinkedIn, YouTube, Wikipedia, Wikidata | 4 | High-value platforms? |
| All sameAs URLs return 200 (not broken) | 4 | Validate each URL |

**Why sameAs matters:**
- AI models use sameAs to connect disparate information about an entity
- A site with `sameAs` pointing to LinkedIn, YouTube, Wikipedia tells AI: "These are all the same entity — aggregate their authority"
- Without sameAs, AI models may treat your website and your LinkedIn as unrelated entities

**Step 4.5: Speakable Schema (10 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-takeaways"]
  }
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| Speakable property on article pages | 5 | Present? |
| CSS selectors point to real, high-quality summary content | 5 | Selectors valid and meaningful? |

**Note:** Speakable tells AI models which content blocks are best for spoken/cited output. This directly influences which text AI engines extract.

**Step 4.6: BreadcrumbList Schema (5 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog"},
    {"@type": "ListItem", "position": 3, "name": "Article Title", "item": "https://example.com/blog/article"}
  ]
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| BreadcrumbList on interior pages | 3 | Present on non-homepage pages? |
| Accurate hierarchy matching URL structure | 2 | Breadcrumbs match actual site structure? |

**Step 4.7: WebSite + SearchAction Schema (5 points)**

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Brand Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

| Criteria | Points | Check |
|----------|--------|-------|
| WebSite schema on homepage | 3 | Present? |
| SearchAction with valid target URL | 2 | Search actually works at that URL? |

---

### Step 5: Check sameAs Cross-Platform Resolution

**Dedicated deep-dive on sameAs — the most impactful GEO property.**

**Step 5.1: Validate Each sameAs URL**

```
For each URL in Organization.sameAs:
  1. Fetch the URL — does it return 200?
  2. Does the page actually belong to this brand? (not a different entity)
  3. Does the platform profile link back to the main website?
  4. Is the profile active (not abandoned)?
  5. Is the brand name consistent across the platform?
```

**Step 5.2: Identify Missing High-Value sameAs**

```
Check if brand has presence on these platforms but is MISSING from sameAs:
  - LinkedIn: Search linkedin.com/company/{brand}
  - YouTube: Search youtube.com/@{brand}
  - Wikipedia: Wikipedia API check
  - Wikidata: Search wikidata.org
  - GitHub: Search github.com/{brand}
  - Twitter/X: Search x.com/{brand}

Flag any platform where brand has a profile but it's not in sameAs.
```

**Step 5.3: Bidirectional Link Check**

```
For each sameAs target, check if the platform profile links back:
  - LinkedIn "Website" field → points to main domain?
  - YouTube "Links" section → points to main domain?
  - Twitter bio → contains main domain URL?
  - GitHub profile → website field matches?

Bidirectional linking strengthens entity resolution.
```

---

### Step 6: Flag Deprecated and Problematic Schema

**Step 6.1: Deprecated Schema Types**

| Schema Type | Status | Date | Action |
|-------------|--------|------|--------|
| **HowTo** | Rich results removed | September 2023 | Remove or keep for semantics only; no visual benefit |
| **FAQPage** | Restricted | August 2023 | Remove from commercial sites; only works for government/health |
| **Speakable** | Still in beta | Ongoing | Keep — useful for GEO even without rich results |

**Step 6.2: Common Schema Errors to Flag**

```
Critical errors:
  - Multiple Organization schemas with different names on same page
  - author as plain string instead of Person object
  - datePublished in non-ISO format ("March 5, 2025" instead of "2025-03-05")
  - sameAs URLs that 404
  - Missing @context
  - HTTP instead of HTTPS in @context URL

Warnings:
  - Organization schema only on homepage (should be on all pages)
  - dateModified missing from Article schemas
  - No image property in Article schema
  - sameAs with fewer than 3 platforms
  - Logo as string URL instead of ImageObject
```

---

### Step 7: Check JavaScript Rendering Risk

**AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do NOT execute JavaScript.**

**Step 7.1: Detect JS-Injected Schema**

```
Method 1: Compare static HTML vs rendered page
  1. Fetch page with a simple HTTP request (no JS execution)
  2. Search for <script type="application/ld+json"> in the raw HTML
  3. If schema is found in raw HTML → Safe (server-rendered)
  4. If schema is NOT in raw HTML → JS-injected (HIGH RISK)

Method 2: Check framework indicators
  - React/Next.js: Check if using SSR or client-side rendering
  - Vue/Nuxt: Check if using SSR
  - Angular: Check if using Angular Universal
  - WordPress: Usually server-rendered (safe)
  - Shopify: Usually server-rendered (safe)
  - Custom SPA: High risk of JS-only schema
```

**Step 7.2: JS-Rendering Risk Assessment**

| Scenario | Risk Level | Impact |
|----------|-----------|--------|
| Schema in static HTML (SSR) | None | All crawlers can read it |
| Schema injected by Google Tag Manager | High | GTM scripts not executed by AI crawlers |
| Schema injected by React client-side render | Critical | Invisible to all AI crawlers |
| Schema in WordPress/PHP templates | None | Server-rendered by default |
| Schema via Yoast/RankMath plugin | None | Injected server-side |

**If JS-injected schema detected:**
```
CRITICAL FINDING:
  Schema markup is injected via JavaScript and will be INVISIBLE to AI crawlers.

  Impact: GPTBot, ClaudeBot, PerplexityBot, and other AI crawlers will not
  see any structured data on this site.

  Fix: Move schema to server-side rendering. Options:
    1. Server-render JSON-LD in HTML template
    2. Switch to SSR framework (Next.js with getServerSideProps, Nuxt with SSR)
    3. Use a schema plugin that injects server-side
    4. Add JSON-LD directly to page templates
```

---

### Step 8: Generate Missing Schema Templates

**For each missing GEO-critical schema type, generate a ready-to-use JSON-LD template.**

**Step 8.1: Determine What's Missing**

Based on Steps 1-7, compile the list of:
- Schema types completely missing
- Schema types present but incomplete
- Schema types present but with errors

**Step 8.2: Generate Templates**

For each missing schema, generate a complete JSON-LD template pre-populated with:
- Actual brand name (from site analysis)
- Actual URLs (from crawled pages)
- Actual author names (from bylines found)
- Placeholder values clearly marked as `[REPLACE: description]`

**Template format:**

```json
// TEMPLATE: Organization Schema (place on ALL pages in <head>)
// Priority: CRITICAL — enables cross-platform entity resolution
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[ACTUAL BRAND NAME]",
  "url": "[ACTUAL HOMEPAGE URL]",
  "logo": "[REPLACE: URL to logo image, minimum 112x112px]",
  "description": "[REPLACE: 1-2 sentence description of the organization]",
  "foundingDate": "[REPLACE: YYYY-MM-DD]",
  "sameAs": [
    "[REPLACE: LinkedIn company URL]",
    "[REPLACE: YouTube channel URL]",
    "[REPLACE: Twitter/X profile URL]",
    "[REPLACE: Wikipedia article URL if exists]",
    "[REPLACE: Wikidata entity URL if exists]",
    "[REPLACE: GitHub organization URL if applicable]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "email": "[REPLACE: support email]"
  }
}
```

Generate templates for ALL missing types:
- Organization (if missing or incomplete)
- Person/author (if missing)
- Article (if missing from blog pages)
- WebSite + SearchAction (if missing from homepage)
- BreadcrumbList (if missing from interior pages)
- Speakable (if missing from article pages)

**Step 8.3: Implementation Instructions**

For each template, include:
```markdown
### Implementation: {Schema Type}

**Where to place:** {specific pages}
**How to add:**
  - WordPress: Add via theme header.php or SEO plugin custom schema
  - Next.js: Add to page component's <Head> or use next-seo
  - HTML: Add <script type="application/ld+json"> in <head> section
  - Shopify: Add to theme.liquid in <head> section

**Validation:** After adding, test at https://validator.schema.org/
**Google test:** https://search.google.com/test/rich-results

**CRITICAL:** Ensure schema is in the HTML source (not JS-injected).
  Test by viewing page source (Ctrl+U) — schema must be visible there.
```

---

### Phase 9: Scoring and Report

**Step 9.1: Calculate Schema Score (0-100)**

| Component | Max Points | Score |
|-----------|-----------|-------|
| Organization schema (complete with sameAs) | 20 | /20 |
| Article schema (with dateModified) | 15 | /15 |
| Person/Author schema | 15 | /15 |
| sameAs property (3+ platforms, validated) | 15 | /15 |
| Speakable property on articles | 10 | /10 |
| BreadcrumbList on interior pages | 5 | /5 |
| WebSite + SearchAction on homepage | 5 | /5 |
| No deprecated schemas (HowTo/FAQPage removed) | 5 | /5 |
| JSON-LD format (not Microdata/RDFa) | 5 | /5 |
| Valid syntax (no errors) | 5 | /5 |
| **Total** | **100** | **/100** |

**Step 9.2: Score Interpretation**

| Score | Tier | Meaning |
|-------|------|---------|
| 85-100 | Excellent | Schema fully supports AI entity resolution and citation |
| 70-84 | Good | Most GEO-critical schemas present, minor gaps |
| 50-69 | Fair | Key schemas missing; AI entity resolution partially broken |
| 30-49 | Poor | Major gaps; AI models cannot reliably identify entity |
| 0-29 | Critical | Schema missing or broken; entity invisible to AI |

---

### Phase 10: Report Generation

**Output files:**
- `GEO-SCHEMA-REPORT.md` — Full audit report, saved to `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/` *(see SKILL.md → Output Directory)*
- Generated JSON-LD templates (embedded in report or separate code blocks)

```markdown
# GEO Schema & Structured Data Audit: {domain}

**Generated:** {date}
**Domain:** {url}
**Schema Score: {score}/100 — {tier}**

---

## Executive Summary

{2-3 sentence summary: current schema state, most critical gap, single biggest improvement action}

### Score Breakdown

| Component | Max | Score | Status |
|-----------|-----|-------|--------|
| Organization (with sameAs) | 20 | /20 | {status} |
| Article (with dateModified) | 15 | /15 | {status} |
| Person/Author | 15 | /15 | {status} |
| sameAs (3+ platforms) | 15 | /15 | {status} |
| Speakable | 10 | /10 | {status} |
| BreadcrumbList | 5 | /5 | {status} |
| WebSite + SearchAction | 5 | /5 | {status} |
| No deprecated schemas | 5 | /5 | {status} |
| JSON-LD format | 5 | /5 | {status} |
| Validation | 5 | /5 | {status} |
| **Total** | **100** | **/100** | |

---

## Existing Schema Inventory

### Schemas Found

| Page | Schema Types | Format | Valid? |
|------|-------------|--------|--------|
| {url} | {types} | JSON-LD/Microdata/RDFa | Yes/No |

### Validation Issues

| Page | Schema Type | Issue | Severity |
|------|------------|-------|----------|
| {url} | {type} | {description} | Critical/High/Medium/Low |

---

## GEO-Critical Schema Assessment

### Organization Schema
{Detailed assessment}

### sameAs Property
{Detailed audit with cross-platform validation}

### Article Schema
{Detailed assessment}

### Person/Author Schema
{Detailed assessment}

### Speakable Schema
{Detailed assessment}

### Other Schemas
{BreadcrumbList, WebSite+SearchAction assessment}

---

## Deprecated Schema Warning

{List any HowTo or FAQPage schemas found, with removal instructions}

---

## JavaScript Rendering Risk

{JS-injection assessment results}

---

## Generated JSON-LD Templates

{Complete, ready-to-use templates for all missing schemas}

### Template: Organization
{JSON-LD code block with implementation instructions}

### Template: Article
{JSON-LD code block with implementation instructions}

### Template: Person
{JSON-LD code block with implementation instructions}

{Additional templates as needed}

---

## Implementation Priority

### Critical (implement immediately)
{Missing Organization schema, broken sameAs, JS-injected schema}

### High (implement this week)
{Missing Article schema, missing Person schema}

### Medium (implement this month)
{Speakable, BreadcrumbList, SearchAction}

### Low (ongoing maintenance)
{Validation fixes, deprecated schema removal}

---

## Methodology

- **8-step audit:** Detect, validate, rich results check, GEO-critical evaluation, sameAs audit, deprecated flags, JS rendering check, template generation
- **Key insight:** sameAs is the single most important property for GEO — it enables cross-platform entity resolution
- **Date:** {date}
```

---

## Success Criteria

- All target pages scanned for existing schema markup
- Three formats checked (JSON-LD, Microdata, RDFa)
- All GEO-critical schema types evaluated with scoring
- sameAs URLs validated (200 status, correct brand)
- Deprecated schemas (HowTo, FAQPage) flagged
- JavaScript rendering risk assessed
- Complete JSON-LD templates generated for all missing schemas
- Score calculated with full breakdown
- Report saved as `GEO-SCHEMA-REPORT.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

---

## Integration

This workflow feeds into:
- **Audit workflow** — Schema score contributes 10% to composite GEO score *(see `ScoringMethodology.md` for canonical weights)*
- **Technical workflow** — JS rendering findings shared
- **PlatformOptimizer** — Schema requirements per platform
- **Report workflow** — Schema section of client deliverable

**Key Principle:** Schema markup is your entity's machine-readable identity card. Without it, AI models must guess who you are from unstructured text. With complete schema — especially sameAs — you tell AI models exactly who you are and where else to find you.
