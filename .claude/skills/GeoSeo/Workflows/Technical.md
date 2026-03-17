# Technical SEO Audit Workflow

**8-step technical audit focused on AI crawler compatibility, SSR requirements, and Core Web Vitals**

## Purpose

Perform a comprehensive technical SEO audit optimized for AI search visibility. The fundamental principle: **SSR is MANDATORY** — AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do NOT execute JavaScript. A technically perfect SPA that renders everything client-side is invisible to every AI search engine.

**Core Thesis:** Traditional technical SEO ensures Google can crawl and index your site. GEO technical SEO ensures AI crawlers — which are far less capable than Googlebot — can access, parse, and extract your content.

## When to Use

- Full technical audit of a website for AI visibility
- Diagnosing why a site isn't appearing in AI search results
- Pre-launch technical GEO checklist
- Client onboarding technical assessment
- Investigating AI crawler access issues

## Input

- **URL** (required): The primary domain to audit
- **Pages to check** (optional): Specific pages (default: homepage + 5-8 key pages)
- **Known issues** (optional): Any known technical problems to investigate

## Scoring Weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| SSR / JavaScript Dependency | 25% | AI crawlers cannot execute JS — this is the #1 technical factor |
| Meta Tags | 15% | Title, description, canonical, Open Graph directly affect AI extraction |
| Crawlability | 15% | robots.txt + sitemap determine what AI crawlers can access |
| Security | 10% | HTTPS, security headers affect trust signals |
| Core Web Vitals | 10% | Page experience signals, INP replaced FID (March 2024) |
| Mobile Optimization | 10% | Mobile-first indexing means AI sees mobile version |
| URL Structure | 5% | Clean URLs aid entity and topic classification |
| HTTP Headers | 5% | Response codes, caching, content-type signals |
| Additional Factors | 5% | Internationalization, accessibility, AMP, etc. |

---

## Workflow Steps

### Step 1: HTTP Headers Analysis (Weight: 5%)

**Step 1.1: Response Header Check**

```bash
# Fetch headers for homepage and key pages
curl -sI https://example.com
curl -sI https://example.com/about
curl -sI https://example.com/blog
```

**Extract and assess:**

| Header | What to Check | GEO Impact |
|--------|---------------|------------|
| `Status Code` | Should be 200 for live pages | Non-200 = not crawled |
| `Content-Type` | Should be `text/html; charset=utf-8` | Wrong type = parsing failure |
| `X-Robots-Tag` | Check for noindex, nofollow directives | Blocks AI indexing |
| `Cache-Control` | Reasonable caching strategy | Affects crawl efficiency |
| `Content-Encoding` | gzip or br compression | Affects crawl speed |
| `Server` | Identifies server software | Version exposure = security risk |
| `X-Frame-Options` | Frame protection | Security signal |
| `Strict-Transport-Security` | HSTS enabled | Trust signal |
| `Content-Security-Policy` | CSP present | Trust signal |
| `X-Content-Type-Options` | nosniff present | Security signal |

**Step 1.2: Redirect Chain Analysis**

```
Check redirect behavior:
1. HTTP → HTTPS redirect (should be 301, not 302)
2. www → non-www (or vice versa) redirect
3. Trailing slash consistency
4. Maximum redirect chain length (should be <= 2 hops)

For each redirect:
  - Record: source URL -> status code -> destination URL
  - Flag: 302 redirects (should be 301 for permanent)
  - Flag: Redirect chains > 2 hops
  - Flag: Redirect loops
```

**Scoring (5 points max):**
- Clean 301 redirects, proper HSTS, compression: 5/5
- Minor issues (302 instead of 301, missing compression): 3/5
- Redirect chains, missing HTTPS redirect: 1/5
- Redirect loops, broken redirects: 0/5

---

### Step 2: Crawlability Analysis (Weight: 15%)

**Step 2.1: robots.txt Audit**

```
Fetch: {domain}/robots.txt

Check for these AI crawler user agents:
  - GPTBot (OpenAI — ChatGPT search)
  - OAI-SearchBot (OpenAI — search feature)
  - ChatGPT-User (OpenAI — browsing)
  - ClaudeBot (Anthropic — Claude)
  - PerplexityBot (Perplexity)
  - Google-Extended (Google — Gemini training)
  - Googlebot (Google — search + AI Overviews)
  - bingbot (Microsoft — Bing Copilot + ChatGPT)
  - Bytespider (ByteDance)
  - CCBot (Common Crawl — training data)

For each agent, determine:
  - Allowed (no blocking directive)
  - Blocked (Disallow: /)
  - Partially blocked (specific paths blocked)
  - Not mentioned (default: allowed)
```

**robots.txt scoring matrix:**

| Scenario | Points (/7) |
|----------|-------------|
| All AI crawlers allowed (or not mentioned) | 7 |
| Key crawlers allowed (GPTBot, PerplexityBot, ClaudeBot) | 5 |
| Only Googlebot/bingbot allowed, AI crawlers blocked | 3 |
| Important content paths blocked for all | 1 |
| Entire site blocked (Disallow: /) | 0 |

**Step 2.2: Sitemap Analysis**

```
Fetch: {domain}/sitemap.xml
Also check: {domain}/sitemap_index.xml

Validate:
1. Sitemap exists and returns 200
2. XML is well-formed
3. URLs in sitemap are valid (200 status)
4. lastmod dates are present and accurate
5. Sitemap is referenced in robots.txt
6. Sitemap size < 50MB and < 50,000 URLs per file
7. Image/video sitemaps (if applicable)
```

**Sitemap scoring:**

| Criteria | Points (/5) |
|----------|-------------|
| Valid sitemap with accurate lastmod dates | 5 |
| Valid sitemap but no lastmod dates | 3 |
| Sitemap exists but has errors | 2 |
| No sitemap.xml found | 0 |

**Step 2.3: IndexNow Protocol**

```
Check for IndexNow implementation:
1. Look for IndexNow key file: {domain}/{key}.txt
2. Check for IndexNow meta tag in HTML
3. Check robots.txt for IndexNow mention
4. If WordPress: check for IndexNow plugin

Why this matters for GEO:
  ChatGPT's search uses Bing's index.
  IndexNow = instant Bing notification = faster ChatGPT discovery.
  Bing Copilot also benefits directly.
```

**Crawlability scoring (15 points max):**

| Component | Max Points |
|-----------|-----------|
| robots.txt AI crawler access | 7 |
| Sitemap quality | 5 |
| IndexNow implementation | 3 |

---

### Step 3: Meta Tags Audit (Weight: 15%)

**Step 3.1: Essential Meta Tags**

For each target page, check:

```html
<!-- Title Tag -->
<title>{50-60 chars, unique per page, includes primary keyword}</title>

<!-- Meta Description -->
<meta name="description" content="{150-160 chars, unique, compelling summary}">

<!-- Canonical URL -->
<link rel="canonical" href="{absolute URL of this page}">

<!-- Robots -->
<meta name="robots" content="index, follow">

<!-- Open Graph (used by AI for context) -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website|article">
<meta property="og:url" content="{canonical URL}">
<meta property="og:image" content="{image URL}">
<meta property="og:site_name" content="{brand name}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">

<!-- Article-specific (if blog/article) -->
<meta property="article:published_time" content="{ISO 8601 date}">
<meta property="article:modified_time" content="{ISO 8601 date}">
<meta property="article:author" content="{author URL}">
```

**Step 3.2: Meta Tag Scoring**

| Signal | Points | Check |
|--------|--------|-------|
| Unique title tags on all pages (50-60 chars) | 3 | Check each page |
| Unique meta descriptions (150-160 chars) | 2 | Check each page |
| Canonical URLs present and correct | 3 | Verify self-referencing or proper canonicalization |
| Open Graph tags complete | 3 | All 5 core OG tags present |
| No conflicting robots directives | 2 | Meta robots vs X-Robots-Tag vs robots.txt |
| article:modified_time on content pages | 2 | Present and accurate |

**Step 3.3: Common Meta Issues to Flag**

```
Critical:
  - Duplicate title tags across pages
  - noindex on important pages
  - Canonical pointing to wrong URL
  - Missing canonical (causes duplicate content)

High:
  - Title tags too long (truncated in results)
  - Missing meta descriptions
  - Missing Open Graph tags
  - article:published_time but no article:modified_time

Medium:
  - Generic titles ("Home", "Welcome")
  - Duplicate meta descriptions
  - Missing Twitter Card tags

Low:
  - Title slightly outside 50-60 char range
  - OG image not optimized size
```

**Meta tags scoring (15 points max):** Sum of individual signal scores above.

---

### Step 4: Security Audit (Weight: 10%)

**Step 4.1: HTTPS and Certificate**

```
Check:
1. HTTPS enabled (HTTP redirects to HTTPS)
2. Valid SSL/TLS certificate
3. Certificate not expiring within 30 days
4. TLS 1.2 or higher (TLS 1.0/1.1 deprecated)
5. No mixed content (HTTP resources on HTTPS pages)
6. HSTS header present with reasonable max-age
```

**Step 4.2: Security Headers**

| Header | Expected Value | Points |
|--------|---------------|--------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | 2 |
| `X-Content-Type-Options` | `nosniff` | 1 |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | 1 |
| `Content-Security-Policy` | Present with reasonable policy | 2 |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter | 1 |
| `Permissions-Policy` | Present, restricting sensitive APIs | 1 |

**Step 4.3: Security Scoring**

| Category | Max Points |
|----------|-----------|
| HTTPS properly configured | 4 |
| Security headers present | 4 |
| No mixed content | 1 |
| Certificate validity | 1 |
| **Total Security** | **10** |

---

### Step 5: URL Structure Analysis (Weight: 5%)

**Step 5.1: URL Pattern Assessment**

```
Analyze URL patterns across the site:

Good patterns:
  /blog/how-to-optimize-for-ai-search (descriptive, hyphenated)
  /services/seo-audit (hierarchical, meaningful)
  /team/jane-smith (entity-identifiable)

Bad patterns:
  /p?id=12345 (parameter-based, meaningless)
  /blog/2025/03/10/post (excessive date nesting)
  /index.php?page=services&cat=2 (query string based)
  /BLOG/How_To_Optimize (inconsistent case, underscores)
```

**Step 5.2: URL Scoring Criteria**

| Signal | Points | Check |
|--------|--------|-------|
| Descriptive, keyword-rich slugs | 1.5 | URLs contain meaningful words |
| Consistent lowercase with hyphens | 1 | No mixed case, no underscores |
| Logical hierarchy reflecting site structure | 1 | URL depth matches content hierarchy |
| No excessive parameters or session IDs | 1 | Clean URLs without query strings |
| Reasonable depth (4 levels or fewer) | 0.5 | No deeply nested URLs |

**URL structure scoring (5 points max):** Sum of criteria above.

---

### Step 6: Mobile Optimization (Weight: 10%)

**Step 6.1: Mobile Rendering Check**

```
1. Viewport meta tag present:
   <meta name="viewport" content="width=device-width, initial-scale=1">

2. Responsive design (not separate mobile site):
   - Check for m.domain.com or /mobile/ redirects
   - Responsive is preferred for GEO (same URL = same content for crawlers)

3. Content parity:
   - Mobile version has same content as desktop
   - No hidden content on mobile (CSS display:none hiding critical text)
   - Images present and loading on mobile

4. Touch-friendly:
   - Tap targets >= 48px
   - No horizontal scrolling
   - Readable font sizes (>= 16px base)
```

**Step 6.2: Mobile-First Indexing Impact**

```
Google uses mobile version for indexing.
AI crawlers typically see the mobile-rendered version.

Check:
  - Does mobile version include all structured data?
  - Does mobile version include all meta tags?
  - Is content identical between mobile and desktop?
  - Are images properly served on mobile (responsive images)?
```

**Mobile scoring (10 points max):**

| Criteria | Points |
|----------|--------|
| Viewport meta tag present | 2 |
| Responsive design (not separate mobile site) | 2 |
| Content parity with desktop | 3 |
| Touch-friendly, readable | 1 |
| Structured data present on mobile version | 2 |

---

### Step 7: Core Web Vitals Risk Assessment (Weight: 10%)

**IMPORTANT: INP (Interaction to Next Paint) replaced FID (First Input Delay) as of March 2024.**

**Step 7.1: Core Web Vitals Metrics**

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | <= 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | <= 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | <= 0.1 | 0.1 - 0.25 | > 0.25 |

**Step 7.2: Assessment Methods**

```
Option 1: CrUX Data (field data)
  Use Chrome UX Report API or PageSpeed Insights API for real-world metrics.

Option 2: Lab Testing
  Use Lighthouse (via PageSpeed Insights or Chrome DevTools)
  for lab-based CWV estimates.

Option 3: Proxy Indicators (when API access unavailable)
  Check for CWV risk factors:
    - Large unoptimized images (LCP risk)
    - No lazy loading on below-fold images (LCP risk)
    - Heavy JavaScript bundles (INP risk)
    - No image dimensions specified (CLS risk)
    - Dynamic ad/content injection (CLS risk)
    - Web fonts without font-display: swap (CLS risk)
```

**Step 7.3: CWV Scoring**

| Scenario | Points (/10) |
|----------|-------------|
| All three metrics "Good" | 10 |
| Two metrics "Good", one "Needs Improvement" | 7 |
| One metric "Good", others "Needs Improvement" | 5 |
| Any metric "Poor" | 3 |
| Multiple metrics "Poor" | 1 |
| Cannot assess (no data available) | 5 (neutral) |

**Step 7.4: GEO-Specific CWV Implications**

```
Why CWV matters for GEO:
  - Google AIO uses page experience signals including CWV
  - Slow pages may be deprioritized in AI Overviews
  - Heavy JS correlates with rendering dependency (see Step 8)
  - Poor INP often indicates heavy client-side JS = risk for AI crawlers

CWV is LESS important for:
  - ChatGPT (uses Bing, less CWV-focused)
  - Perplexity (content quality over speed)
  - But slow sites still get crawled less frequently
```

---

### Step 8: JavaScript Dependency Analysis (Weight: 25%)

**This is the highest-weighted category. SSR is MANDATORY for AI visibility.**

**Step 8.1: Rendering Method Detection**

```
Method 1: View Source vs. Rendered Page
  1. Fetch page with simple HTTP GET (curl/fetch — no JS execution)
  2. Check if main content is in the raw HTML
  3. If content is present -> Server-Side Rendered (SSR) PASS
  4. If content is missing (only <div id="app"></div>) -> Client-Side Rendered FAIL

Method 2: Framework Detection
  - Check for framework signatures in HTML:
    - __NEXT_DATA__ -> Next.js (check if SSR or static)
    - __NUXT__ -> Nuxt.js (check if SSR or SPA mode)
    - <app-root> -> Angular (check for Universal/SSR)
    - <div id="root"> with no content -> React SPA FAIL
    - wp-content in URLs -> WordPress (SSR by default) PASS
    - Shopify CDN -> Shopify (SSR by default) PASS

Method 3: Content Presence Check
  1. Fetch raw HTML
  2. Search for:
     - Main heading text (H1)
     - First paragraph of visible content
     - Navigation links
     - Schema markup (JSON-LD)
  3. If all present in raw HTML -> SSR PASS
  4. If missing from raw HTML -> CSR FAIL
```

**Step 8.2: JavaScript Bundle Analysis**

```
Check:
1. Total JavaScript payload size
   - < 200KB: Good
   - 200-500KB: Acceptable
   - 500KB-1MB: Concerning
   - > 1MB: Critical (likely CSR-dependent)

2. Number of JS files loaded
   - < 5: Minimal dependency
   - 5-15: Moderate
   - > 15: Heavy dependency

3. Critical rendering path
   - Does page render without JS? (disable JS in browser)
   - Which content disappears without JS?
   - Is navigation functional without JS?
```

**Step 8.3: AI Crawler Simulation**

```
Simulate what AI crawlers see:
  1. Fetch page with curl (no JS execution)
  2. Parse the raw HTML
  3. Extract:
     - Title tag
     - Meta description
     - H1-H6 headings
     - Paragraph text
     - Schema markup (JSON-LD)
     - Image alt text
     - Internal links
  4. Compare against what a browser renders with JS
  5. Calculate "content visibility ratio":
     Content visible without JS / Total content with JS

  Scoring:
    100% visibility -> 25/25 (full SSR)
    75-99% visibility -> 20/25 (mostly SSR, some JS-dependent elements)
    50-74% visibility -> 12/25 (significant JS dependency)
    25-49% visibility -> 5/25 (heavy JS dependency)
    0-24% visibility -> 0/25 (client-side rendered — invisible to AI)
```

**Step 8.4: SSR Remediation Guidance**

If JavaScript dependency is detected, provide specific remediation:

```markdown
### SSR Remediation Plan

**Current State:** {CSR/Partial SSR/Full SSR}
**Content Visibility:** {X}% without JavaScript
**Risk Level:** {Critical/High/Medium/Low}

**Remediation by Framework:**

**React SPA -> Next.js SSR:**
  - Migrate to Next.js with getServerSideProps or getStaticProps
  - Use Server Components (React 18+) for content pages
  - Keep interactivity client-side, render content server-side

**Vue SPA -> Nuxt SSR:**
  - Migrate to Nuxt.js with SSR mode enabled
  - Use asyncData or useFetch for server-side data loading
  - Configure nuxt.config with ssr: true

**Angular SPA -> Angular Universal:**
  - Add @nguniversal/express-engine
  - Implement server-side rendering module
  - Pre-render static pages with Scully/Angular Prerender

**Any Framework -> Static Site Generation (SSG):**
  - For content that doesn't change frequently
  - Pre-render pages at build time
  - Fastest option for AI crawlers

**WordPress/Shopify:**
  - Already SSR by default
  - Check that JS plugins aren't hiding content
  - Verify schema is in source HTML (not JS-injected)

**Quick Fix (if migration not feasible):**
  - Implement pre-rendering service (Rendertron, Prerender.io)
  - Serve pre-rendered HTML to bot user agents
  - Note: This is a workaround, not a solution
```

---

### Phase 9: Issue Classification and Prioritization

**Step 9.1: Severity Classification**

All findings classified into four severity levels:

| Severity | Definition | Timeline |
|----------|-----------|----------|
| **Critical** | Site is fundamentally invisible to AI crawlers. Blocks all GEO progress. | Fix within 1 week |
| **High** | Major AI visibility impact. Significantly reduces citation probability. | Fix within 2 weeks |
| **Medium** | Moderate impact. Reduces optimization effectiveness but not blocking. | Fix within 1 month |
| **Low** | Minor impact. Best practice improvement. | Fix when convenient |

**Step 9.2: Common Issues by Severity**

```
CRITICAL:
  - Client-side rendering (content invisible without JS)
  - robots.txt blocks all AI crawlers
  - Site returns 5xx errors
  - No HTTPS
  - noindex on important pages

HIGH:
  - Key AI crawlers blocked (GPTBot, PerplexityBot)
  - No sitemap.xml
  - Schema markup only injected via JS
  - Redirect loops on key pages
  - Multiple canonical issues

MEDIUM:
  - Missing meta descriptions
  - No IndexNow implementation
  - Incomplete Open Graph tags
  - Security headers missing
  - CWV in "Needs Improvement" range
  - No speakable schema

LOW:
  - Title tags slightly outside optimal length
  - Minor URL structure inconsistencies
  - Missing Twitter Card tags
  - Image optimization opportunities
  - Font-display not set
```

---

### Phase 10: Scoring and Report

**Step 10.1: Calculate Weighted Score**

```
Total Score =
  (SSR_JS_Score / 25 * 25) +
  (Meta_Tags_Score / 15 * 15) +
  (Crawlability_Score / 15 * 15) +
  (Security_Score / 10 * 10) +
  (CWV_Score / 10 * 10) +
  (Mobile_Score / 10 * 10) +
  (URL_Score / 5 * 5) +
  (Headers_Score / 5 * 5) +
  (Additional_Score / 5 * 5)

Maximum: 100
```

**Step 10.2: Score Interpretation**

| Score | Tier | Meaning |
|-------|------|---------|
| 85-100 | Excellent | Technically optimized for AI crawlers |
| 70-84 | Good | Minor issues, AI crawlers can access most content |
| 50-69 | Fair | Significant gaps affecting AI visibility |
| 30-49 | Poor | Major technical barriers to AI discovery |
| 0-29 | Critical | Fundamentally broken for AI crawlers |

---

### Phase 11: Report Generation

**Output file: `GEO-TECHNICAL-AUDIT.md`** in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/` *(see SKILL.md → Output Directory)*

```markdown
# GEO Technical SEO Audit: {domain}

**Generated:** {date}
**Domain:** {url}
**Technical Score: {score}/100 — {tier}**

---

## Executive Summary

{2-3 sentence summary: rendering method, biggest blocker, most impactful fix}

### Score Breakdown

| Category | Weight | Score | Max | Status |
|----------|--------|-------|-----|--------|
| SSR / JS Dependency | 25% | /25 | 25 | {status} |
| Meta Tags | 15% | /15 | 15 | {status} |
| Crawlability | 15% | /15 | 15 | {status} |
| Security | 10% | /10 | 10 | {status} |
| Core Web Vitals | 10% | /10 | 10 | {status} |
| Mobile Optimization | 10% | /10 | 10 | {status} |
| URL Structure | 5% | /5 | 5 | {status} |
| HTTP Headers | 5% | /5 | 5 | {status} |
| Additional | 5% | /5 | 5 | {status} |
| **Total** | **100%** | **/100** | **100** | **{tier}** |

---

## Critical Findings

{List all Critical and High severity issues with remediation steps}

---

## Step 1: HTTP Headers
{Detailed findings}

## Step 2: Crawlability
### robots.txt
{AI crawler access matrix}
### Sitemap
{Sitemap analysis}
### IndexNow
{IndexNow status}

## Step 3: Meta Tags
{Per-page meta tag audit}

## Step 4: Security
{HTTPS, headers, certificate assessment}

## Step 5: URL Structure
{URL pattern analysis}

## Step 6: Mobile Optimization
{Viewport, responsiveness, content parity}

## Step 7: Core Web Vitals
{LCP, INP, CLS assessment — note: INP replaced FID March 2024}

## Step 8: JavaScript Dependency
{Rendering method, content visibility ratio, SSR assessment}
{AI crawler simulation results}

---

## Issue Summary

### Critical Issues ({count})
{Issue, impact, fix, timeline for each}

### High Issues ({count})
{Issue, impact, fix, timeline for each}

### Medium Issues ({count})
{Issue, impact, fix, timeline for each}

### Low Issues ({count})
{Issue, impact, fix, timeline for each}

---

## Remediation Priority

### Week 1 (Critical)
{Ordered action items}

### Week 2-4 (High)
{Ordered action items}

### Month 2-3 (Medium)
{Ordered action items}

### Ongoing (Low)
{Ordered action items}

---

## AI Crawler Compatibility Matrix

| Crawler | User Agent | Allowed | Content Visible | Status |
|---------|-----------|---------|-----------------|--------|
| GPTBot | GPTBot | Yes/No | Yes/Partial/No | {status} |
| OAI-SearchBot | OAI-SearchBot | Yes/No | Yes/Partial/No | {status} |
| ChatGPT-User | ChatGPT-User | Yes/No | Yes/Partial/No | {status} |
| ClaudeBot | ClaudeBot | Yes/No | Yes/Partial/No | {status} |
| PerplexityBot | PerplexityBot | Yes/No | Yes/Partial/No | {status} |
| Google-Extended | Google-Extended | Yes/No | Yes/Partial/No | {status} |
| Googlebot | Googlebot | Yes/No | Yes/Partial/No | {status} |
| bingbot | bingbot | Yes/No | Yes/Partial/No | {status} |

---

## Methodology

- **8-step audit:** Headers, crawlability, meta tags, security, URL structure, mobile, CWV, JS dependency
- **Scoring weights:** SSR 25%, Meta 15%, Crawlability 15%, Security 10%, CWV 10%, Mobile 10%, URL 5%, Headers 5%, Additional 5%
- **Key fact:** INP replaced FID as Core Web Vital (March 2024)
- **Key fact:** AI crawlers do NOT execute JavaScript — SSR is mandatory
- **Key fact:** IndexNow matters because ChatGPT uses Bing's index
- **Date:** {date}
```

---

## Success Criteria

- All 8 analysis steps completed with findings
- SSR/JS dependency assessed (highest-weight category)
- robots.txt checked for all major AI crawler user agents
- Core Web Vitals assessed with correct metrics (INP not FID)
- All issues classified by severity (Critical/High/Medium/Low)
- Weighted score calculated with full breakdown
- AI Crawler Compatibility Matrix completed
- Remediation plan with timelines generated
- Report saved as `GEO-TECHNICAL-AUDIT.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

---

## Integration

This workflow feeds into:
- **Audit workflow** — Technical score contributes 15% to composite GEO score *(see `ScoringMethodology.md` for canonical weights)*
- **Crawlers workflow** — Detailed crawler access analysis
- **Schema workflow** — JS rendering affects schema visibility
- **PlatformOptimizer** — Technical requirements per platform
- **Report workflow** — Technical section of client deliverable

**Key Principle:** If AI crawlers can't see your content, nothing else matters. SSR is not a nice-to-have — it is the foundation. Fix rendering first, then optimize everything else.
