# GEO AI Crawler Access Workflow

**Mode:** robots.txt and meta-tag analysis for AI crawler access | **Single-domain analysis**

## When to Use

- User says "crawlers", "robots.txt", "ai crawler access", "check crawler access"
- User wants to know which AI engines can crawl their site
- Called as subcomponent of the full Audit workflow (within GeoTechnical subagent)

---

## Core Concept

AI search engines use dedicated crawlers to index content for their models. Blocking these crawlers means your content will not appear in AI-generated answers, even if your traditional SEO is perfect. This workflow identifies which AI crawlers are allowed, blocked, or unaddressed — and quantifies the impact on AI visibility.

**Key Principle:** There is a spectrum between "allow everything" and "block everything." The optimal strategy depends on the site's goals:
- **Maximum AI visibility** → Allow all Tier 1 and Tier 2 crawlers
- **Selective visibility** → Allow Tier 1, consider Tier 2 case-by-case
- **Protect training data** → Block Tier 3 (training-only) while allowing Tier 1 (search)

---

## AI Crawler Registry

### Tier 1 — Critical (Blocking Directly Reduces AI Search Visibility)

| Crawler | Operator | Purpose | robots.txt Token |
|---------|----------|---------|-------------------|
| GPTBot | OpenAI | Powers ChatGPT web browsing and search | `GPTBot` |
| OAI-SearchBot | OpenAI | OpenAI's dedicated search crawler | `OAI-SearchBot` |
| ChatGPT-User | OpenAI | ChatGPT user-initiated browsing | `ChatGPT-User` |
| ClaudeBot | Anthropic | Powers Claude's web access | `ClaudeBot` |
| anthropic-ai | Anthropic | Anthropic's general crawler | `anthropic-ai` |
| PerplexityBot | Perplexity | Powers Perplexity search results | `PerplexityBot` |

### Tier 2 — Important (Blocking Reduces Visibility in Adjacent AI Features)

| Crawler | Operator | Purpose | robots.txt Token |
|---------|----------|---------|-------------------|
| Google-Extended | Google | Gemini/Bard training and Vertex AI | `Google-Extended` |
| GoogleOther | Google | Miscellaneous Google AI uses | `GoogleOther` |
| Applebot-Extended | Apple | Apple Intelligence features | `Applebot-Extended` |
| FacebookBot | Meta | Meta AI features and content understanding | `FacebookBot` |
| Amazonbot | Amazon | Alexa answers and Amazon AI features | `Amazonbot` |

### Tier 3 — Training Only (Blocking Protects Content from Model Training Without Reducing Search Visibility)

| Crawler | Operator | Purpose | robots.txt Token |
|---------|----------|---------|-------------------|
| CCBot | Common Crawl | Open dataset used for training many LLMs | `CCBot` |
| Bytespider | ByteDance | TikTok/ByteDance AI model training | `Bytespider` |
| cohere-ai | Cohere | Cohere model training | `cohere-ai` |

---

## Workflow

### Step 1: Fetch robots.txt

```
WebFetch("{domain}/robots.txt")
```

**If robots.txt exists:**
- Store the full content for analysis
- Proceed to Step 2

**If robots.txt does not exist (404 or empty):**
- Record: "No robots.txt found"
- This means ALL crawlers are implicitly allowed
- Score implications: Full access but no intentional AI strategy
- Skip to Step 3 (meta tag check) then proceed to scoring

**If robots.txt returns error (500, timeout):**
- Record: "robots.txt unreachable"
- Flag as CRITICAL issue (crawlers may interpret errors differently)
- Attempt to proceed with meta tag analysis

---

### Step 2: Parse robots.txt Directives

Parse the robots.txt content and evaluate each AI crawler's access status.

**Parsing rules (follow RFC 9309 and common conventions):**

1. **Specific User-agent blocks** take priority over wildcard (`*`) blocks
2. **Allow** directives override **Disallow** for the same path when in the same User-agent block
3. **Disallow: /** blocks everything
4. **Disallow:** (empty) blocks nothing (allows all)
5. Pattern matching: `*` matches any sequence, `$` matches end of URL

**For each crawler in the registry, determine:**

```
ACCESS STATUS:
- ALLOWED     → No block exists, or specific Allow overrides Disallow
- BLOCKED     → Explicit Disallow: / for this crawler
- PARTIAL     → Disallow for specific paths (e.g., /api/ blocked but / allowed)
- INHERITED   → No specific rule; inherits from User-agent: * block
- UNKNOWN     → robots.txt error or ambiguous directives
```

**Check for common blocking patterns:**

```
# Pattern 1: Blanket AI block (common but harmful for visibility)
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

# Pattern 2: Wildcard block (blocks everything including AI)
User-agent: *
Disallow: /

# Pattern 3: Selective block (blocks training, allows search)
User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

# Pattern 4: Path-based block (allows most, blocks sensitive areas)
User-agent: GPTBot
Disallow: /admin/
Disallow: /api/
Allow: /

# Pattern 5: AI-aware configuration (optimal)
User-agent: GPTBot
Allow: /blog/
Allow: /docs/
Disallow: /admin/
Disallow: /internal/

User-agent: CCBot
Disallow: /
```

**Record for each crawler:**
- Crawler name and tier
- Access status (ALLOWED/BLOCKED/PARTIAL/INHERITED/UNKNOWN)
- Specific directives found (quote the exact lines)
- Blocked paths (if PARTIAL)
- Whether status comes from specific block or wildcard inheritance

---

### Step 3: Check Page-Level Meta Directives

Fetch the homepage and up to 5 key pages to check for page-level AI directives.

```
WebFetch("{domain}")
WebFetch("{domain}/blog")  # if exists
WebFetch("{domain}/about") # if exists
```

**Check for these meta tags in page HTML:**

```html
<!-- Standard noindex (affects all engines including AI) -->
<meta name="robots" content="noindex">
<meta name="robots" content="noindex, nofollow">

<!-- AI-specific directives (emerging standard) -->
<meta name="robots" content="noai">
<meta name="robots" content="noimageai">

<!-- Specific crawler directives -->
<meta name="GPTBot" content="noindex">
<meta name="ClaudeBot" content="noindex">

<!-- X-Robots-Tag in HTTP headers (check if visible in fetch) -->
X-Robots-Tag: noai
X-Robots-Tag: noimageai
```

**Also check for:**
- `data-noai` attributes on content sections (emerging convention)
- AI opt-out headers in HTTP response
- `.well-known/ai-plugin.json` (OpenAI plugin manifest — signals AI engagement)

**Record:**
- Which pages have AI-restrictive meta tags
- Whether restrictions are site-wide or page-specific
- Any conflicting signals (robots.txt allows but meta tag blocks, or vice versa)

---

### Step 4: Check for AI-Specific Files

Check for the presence of files that signal intentional AI engagement:

```
WebFetch("{domain}/llms.txt")        → llms.txt for LLM guidance
WebFetch("{domain}/llms-full.txt")   → Extended llms.txt
WebFetch("{domain}/.well-known/ai-plugin.json")  → OpenAI plugin manifest
WebFetch("{domain}/sitemap.xml")     → Sitemap (general but important for AI crawling)
```

**For each file, record:**
- Exists (yes/no)
- Valid format (yes/no/partial)
- Quality assessment (brief)

---

### Step 5: Calculate Crawler Access Score

#### Component 1: Tier 1 Access (50% of total score)

```
tier1_crawlers = [GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, anthropic-ai, PerplexityBot]
tier1_allowed = count of ALLOWED or PARTIAL in tier1_crawlers
tier1_total = 6

tier1_score = (tier1_allowed / tier1_total) × 100

# Weighting: The "big three" matter most
# GPTBot + ClaudeBot + PerplexityBot each worth 2x
weighted_tier1_allowed = 0
for crawler in tier1_crawlers:
  if crawler in [GPTBot, ClaudeBot, PerplexityBot]:
    weighted_tier1_allowed += 2 if ALLOWED else (1 if PARTIAL else 0)
  else:
    weighted_tier1_allowed += 1 if ALLOWED else (0.5 if PARTIAL else 0)

weighted_tier1_total = 9  # (3 × 2) + (3 × 1)
tier1_score = (weighted_tier1_allowed / weighted_tier1_total) × 100
```

#### Component 2: Tier 2 Access (25% of total score)

```
tier2_crawlers = [Google-Extended, GoogleOther, Applebot-Extended, FacebookBot, Amazonbot]
tier2_allowed = count of ALLOWED or PARTIAL in tier2_crawlers
tier2_total = 5

tier2_score = (tier2_allowed / tier2_total) × 100
```

#### Component 3: No Blanket Blocks (15% of total score)

```
blanket_block_score = 100  # Start at 100, deduct for blanket blocks

if "User-agent: *" has "Disallow: /":
  blanket_block_score = 0  # Total blanket block

elif site-wide noai meta tag found:
  blanket_block_score = 10  # Almost as bad

elif more than 3 AI crawlers individually blocked with "Disallow: /":
  blanket_block_score = 30  # Selective but heavy-handed

elif any conflicting directives found:
  blanket_block_score = 60  # Confused configuration
else:
  blanket_block_score = 100  # Clean
```

#### Component 4: AI-Specific Files (10% of total score)

```
ai_files_score = 0

if llms.txt exists and valid:       ai_files_score += 40
if llms-full.txt exists and valid:  ai_files_score += 20
if ai-plugin.json exists:           ai_files_score += 20
if sitemap.xml exists and valid:    ai_files_score += 20
```

#### Composite Score

```
crawler_access_score = (
  tier1_score       × 0.50 +
  tier2_score       × 0.25 +
  blanket_block_score × 0.15 +
  ai_files_score    × 0.10
)
```

Round to nearest integer.

#### Score Interpretation

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Intentionally AI-optimized crawler configuration |
| 75-89 | Good | Most AI crawlers allowed, minor gaps |
| 60-74 | Fair | Some critical crawlers blocked or no intentional strategy |
| 40-59 | Poor | Multiple critical crawlers blocked |
| 0-39 | Critical | All or most AI crawlers blocked; invisible to AI search |

---

### Step 6: Generate Recommendations

Based on the analysis, produce actionable recommendations:

**If Tier 1 crawlers are blocked:**

```
CRITICAL: {crawler_name} is blocked. This prevents your content from appearing in
{platform_name} responses.

FIX: Add to robots.txt:
User-agent: {crawler_token}
Allow: /

Or selectively allow key content:
User-agent: {crawler_token}
Allow: /blog/
Allow: /docs/
Allow: /about/
Disallow: /admin/
Disallow: /internal/
```

**If blanket block exists:**

```
CRITICAL: User-agent: * with Disallow: / blocks ALL crawlers including AI search engines.

FIX: Replace blanket block with selective rules:
# Allow search engines (traditional + AI)
User-agent: Googlebot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Block training-only crawlers if desired
User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /
```

**If no robots.txt exists:**

```
MEDIUM: No robots.txt found. All crawlers are implicitly allowed, but you have no
control over which paths are accessible.

FIX: Create robots.txt at domain root with intentional AI crawler directives.
See recommended template below.
```

**If no AI-specific files exist:**

```
MEDIUM: No llms.txt file found. Creating one gives you direct control over how
LLMs understand and represent your site.

FIX: Create /llms.txt with site overview, key pages, and content descriptions.
Run the LlmsTxt workflow for guided generation.
```

**Recommended robots.txt template (include in report):**

```
# AI Search Crawlers — Allow for visibility
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

# Google AI Features
User-agent: Google-Extended
Allow: /

# Apple Intelligence
User-agent: Applebot-Extended
Allow: /

# Training-Only Crawlers — Block if you want to protect training data
User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: cohere-ai
Disallow: /

# General crawlers
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /internal/
Disallow: /api/
Disallow: /tmp/

Sitemap: https://{domain}/sitemap.xml
```

---

### Step 7: Output Report

Generate `GEO-CRAWLER-ACCESS.md` in the output directory *(see SKILL.md → Output Directory for path convention: `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`)*:

```markdown
# GEO AI Crawler Access Report: {domain}

**Date:** {YYYY-MM-DD}
**Overall Score:** {score}/100 ({rating})
**robots.txt Status:** {exists/missing/error}

---

## Executive Summary

{2-3 sentences summarizing the AI crawler access posture. Lead with the most critical finding.}

---

## Crawler Access Matrix

### Tier 1 — Critical (AI Search Visibility)

| Crawler | Operator | Status | Directive Source | Impact |
|---------|----------|--------|------------------|--------|
| GPTBot | OpenAI | 🟢/🔴 ALLOWED/BLOCKED | {line from robots.txt} | ChatGPT search |
| OAI-SearchBot | OpenAI | 🟢/🔴 | {source} | OpenAI search |
| ChatGPT-User | OpenAI | 🟢/🔴 | {source} | ChatGPT browsing |
| ClaudeBot | Anthropic | 🟢/🔴 | {source} | Claude answers |
| anthropic-ai | Anthropic | 🟢/🔴 | {source} | Anthropic indexing |
| PerplexityBot | Perplexity | 🟢/🔴 | {source} | Perplexity search |

**Tier 1 Score: {score}/100**

### Tier 2 — Important (Adjacent AI Features)

| Crawler | Operator | Status | Directive Source | Impact |
|---------|----------|--------|------------------|--------|
| Google-Extended | Google | 🟢/🔴 | {source} | Gemini/AI Overviews |
| GoogleOther | Google | 🟢/🔴 | {source} | Google AI features |
| Applebot-Extended | Apple | 🟢/🔴 | {source} | Apple Intelligence |
| FacebookBot | Meta | 🟢/🔴 | {source} | Meta AI |
| Amazonbot | Amazon | 🟢/🔴 | {source} | Alexa/Amazon AI |

**Tier 2 Score: {score}/100**

### Tier 3 — Training Only

| Crawler | Operator | Status | Directive Source | Notes |
|---------|----------|--------|------------------|-------|
| CCBot | Common Crawl | 🟢/🔴 | {source} | OK to block |
| Bytespider | ByteDance | 🟢/🔴 | {source} | OK to block |
| cohere-ai | Cohere | 🟢/🔴 | {source} | OK to block |

---

## Score Breakdown

| Component | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Tier 1 Access | 50% | {score}/100 | {X/6 crawlers allowed} |
| Tier 2 Access | 25% | {score}/100 | {X/5 crawlers allowed} |
| No Blanket Blocks | 15% | {score}/100 | {status} |
| AI-Specific Files | 10% | {score}/100 | {files found} |
| **TOTAL** | **100%** | **{score}/100** | |

---

## Page-Level Directives

| Page | noai Meta | noindex | AI-Restrictive Headers |
|------|-----------|---------|------------------------|
| {url} | {yes/no} | {yes/no} | {yes/no} |
{...checked pages}

---

## AI-Specific Files

| File | Status | Quality |
|------|--------|---------|
| /llms.txt | {exists/missing} | {assessment} |
| /llms-full.txt | {exists/missing} | {assessment} |
| /.well-known/ai-plugin.json | {exists/missing} | {assessment} |
| /sitemap.xml | {exists/missing} | {assessment} |

---

## Current robots.txt

```
{full robots.txt content, or "Not found"}
```

---

## Recommendations

### Critical (Fix Immediately)
{numbered list of critical fixes with exact robots.txt changes}

### Important (Fix This Week)
{numbered list of important improvements}

### Optional (Best Practice)
{numbered list of nice-to-have optimizations}

### Recommended robots.txt Configuration

```
{Complete recommended robots.txt tailored to this site}
```

---

## Impact Analysis

**If all recommendations are implemented:**
- Current score: {current}/100
- Projected score: {projected}/100
- AI platforms with improved access: {list}

---

*Generated by PAI GeoSeo Crawler Access Analyzer — {date}*
```

---

## Error Handling

| Error | Response |
|-------|----------|
| Domain unreachable | Abort with error. Cannot assess crawler access. |
| robots.txt returns 5xx | Flag as CRITICAL. Crawlers may interpret server errors as blocks. |
| robots.txt is extremely large (>100KB) | Parse first 500 lines only. Note truncation. |
| Ambiguous directives | Report ambiguity. Score conservatively (assume blocked). |
| robots.txt has syntax errors | Note errors. Parse best-effort. Recommend cleanup. |

## Dependencies

- **Tools:** WebFetch (required)
- **Output:** `GEO-CRAWLER-ACCESS.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`
