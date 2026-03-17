# Brand Mention Scanning Workflow

**Cross-platform brand mention scanning and authority scoring for AI search visibility**

## Purpose

Scan 12+ platforms for unlinked brand mentions and authority signals. Brand mentions (not backlinks) are the dominant ranking factor for AI search engines. Unlinked brand mentions correlate approximately 3x more strongly with AI visibility than traditional backlinks.

**Core Thesis:** AI models build entity understanding from brand mentions across the web, not from link graphs. A brand mentioned 500 times across Reddit, YouTube, and Wikipedia with zero links will outrank a brand with 500 backlinks but no organic discussion.

## When to Use

- Assessing a brand's AI search visibility baseline
- Competitive brand authority comparison
- Identifying platforms where brand presence is weak
- Pre-audit brand mention inventory
- Client onboarding brand assessment

## Input

- **Brand name** (required): The exact brand name to scan
- **Brand URL** (required): The primary domain
- **Competitors** (optional): 1-3 competitor brand names for comparison
- **Industry/niche** (optional): Helps refine search context

## Platform Weights

AI models source entity knowledge unevenly. These weights reflect measured correlation with AI citation frequency:

| Platform | Weight | Rationale |
|----------|--------|-----------|
| **YouTube** | 25% | Google/Gemini trains on transcripts; ChatGPT cites video content |
| **Reddit** | 25% | Primary community signal; Perplexity indexes heavily; Google licenses Reddit data |
| **Wikipedia** | 20% | Highest authority single source; all AI models use as ground truth |
| **LinkedIn** | 15% | Professional entity validation; Bing Copilot indexes; author authority |
| **Other platforms** | 15% | GitHub, Stack Overflow, Quora, Medium, industry forums, podcasts, news |

## Workflow Steps

### Phase 1: Brand Identity Setup

**Step 1.1: Define Search Variants**

Before scanning, establish all searchable forms of the brand:

```
Primary brand name: [exact name]
Variations to search:
- Full legal name (e.g., "Acme Corporation")
- Common name (e.g., "Acme")
- Product names (e.g., "Acme Pro", "Acme Suite")
- Domain without TLD (e.g., "acmecorp")
- Known abbreviations (e.g., "ACME")
- Common misspellings (e.g., "Acmee")
- Founder/CEO name + brand (e.g., "John Smith Acme")
```

**Step 1.2: Establish Competitor Set**

If competitors were not provided, identify 2-3 based on:
- Same industry/niche
- Similar size/stage
- Competing for same AI search queries

---

### Phase 2: Wikipedia Presence Check (Weight: 20%)

**IMPORTANT: Use Python API checks first, not just web search.**

**Step 2.1: Wikipedia API Check**

```python
import requests

def check_wikipedia_presence(brand_name):
    """Check if brand has a Wikipedia article via API"""

    # Step 1: Search for the article
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": brand_name,
        "format": "json",
        "srlimit": 10
    }
    response = requests.get(search_url, params=search_params)
    results = response.json()

    # Step 2: Check for exact title match
    exact_match = None
    partial_matches = []
    for result in results.get("query", {}).get("search", []):
        if result["title"].lower() == brand_name.lower():
            exact_match = result
        elif brand_name.lower() in result["title"].lower():
            partial_matches.append(result)

    # Step 3: If exact match, get article quality
    if exact_match:
        content_url = "https://en.wikipedia.org/w/api.php"
        content_params = {
            "action": "query",
            "titles": exact_match["title"],
            "prop": "revisions|categories|extlinks|langlinks",
            "rvprop": "size",
            "cllimit": "max",
            "ellimit": "max",
            "lllimit": "max",
            "format": "json"
        }
        content = requests.get(content_url, params=content_params)
        return content.json()

    return {"exact_match": False, "partial_matches": partial_matches}
```

**Step 2.2: Wikipedia Scoring Criteria**

| Signal | Points | How to Check |
|--------|--------|--------------|
| Dedicated Wikipedia article exists | 8 | API search exact match |
| Article length > 5,000 bytes | 3 | API revisions size |
| Article has 10+ external links | 2 | API extlinks count |
| Article in 5+ language editions | 2 | API langlinks count |
| Brand mentioned in OTHER Wikipedia articles | 3 | Search for brand in non-brand articles |
| No deletion/notability warnings | 2 | Check categories for "Articles for deletion" |
| **Maximum Wikipedia Score** | **20** | |

**Step 2.3: Wikipedia Mention Depth**

Beyond the brand's own article, search for mentions in:
- Industry articles (e.g., brand mentioned in "Cloud Computing" article)
- Competitor articles (brand mentioned as alternative)
- Founder/CEO personal article
- Technology/product category articles
- Geographic region articles (if locally relevant)

Record each mention with context snippet and article title.

---

### Phase 3: YouTube Scanning (Weight: 25%)

**Step 3.1: YouTube Search Queries**

Execute these searches (use WebSearch or direct YouTube search):

```
"{brand_name}" - exact match
"{brand_name}" review
"{brand_name}" tutorial
"{brand_name}" vs
"{brand_name}" alternative
"{brand_name}" {industry_term}
```

**Step 3.2: YouTube Scoring Criteria**

| Signal | Points | How to Check |
|--------|--------|--------------|
| 50+ videos mentioning brand | 5 | Search result count |
| Videos from channels with 10K+ subscribers | 5 | Check top results channel sizes |
| Brand's own channel exists with 10+ videos | 4 | Direct channel search |
| Videos in last 6 months (freshness) | 4 | Filter by upload date |
| Brand mentioned in video titles (not just descriptions) | 3 | Title analysis |
| Tutorial/educational content about brand | 2 | Content type analysis |
| Brand comparisons ("X vs Y") exist | 2 | Search "{brand} vs" |
| **Maximum YouTube Score** | **25** | |

**Step 3.3: YouTube Data to Capture**

For each of the top 10 results, record:
- Video title
- Channel name and subscriber count
- View count
- Upload date
- Whether brand is in title, description, or spoken (transcript)
- Sentiment (positive/negative/neutral)

---

### Phase 4: Reddit Scanning (Weight: 25%)

**Step 4.1: Reddit Search Queries**

```
site:reddit.com "{brand_name}"
site:reddit.com "{brand_name}" review
site:reddit.com "{brand_name}" recommendation
site:reddit.com "{brand_name}" vs
site:reddit.com "{brand_name}" experience
```

Also check specific subreddits relevant to the brand's industry.

**Step 4.2: Reddit Scoring Criteria**

| Signal | Points | How to Check |
|--------|--------|--------------|
| 100+ threads mentioning brand | 5 | Search result count |
| Mentions in subreddits with 100K+ members | 5 | Identify subreddit sizes |
| Positive sentiment in recommendations | 4 | Analyze comment tone |
| Brand mentioned as answer to "what should I use" questions | 4 | Look for recommendation threads |
| Active within last 3 months | 3 | Filter by recency |
| Brand has official Reddit presence | 2 | Check for verified accounts |
| Community-created subreddit exists | 2 | Search r/{brand_name} |
| **Maximum Reddit Score** | **25** | |

**Step 4.3: Reddit Qualitative Analysis**

Capture:
- Top subreddits where brand is discussed
- Common positive themes (e.g., "reliable", "good support")
- Common negative themes (e.g., "expensive", "buggy")
- Whether brand is organically recommended or only self-promoted
- Thread engagement levels (upvotes, comment counts)

---

### Phase 5: LinkedIn Scanning (Weight: 15%)

**Step 5.1: LinkedIn Search Queries**

```
site:linkedin.com "{brand_name}"
site:linkedin.com/company "{brand_name}"
site:linkedin.com/posts "{brand_name}"
"{brand_name}" site:linkedin.com review OR recommendation
```

**Step 5.2: LinkedIn Scoring Criteria**

| Signal | Points | How to Check |
|--------|--------|--------------|
| Company page exists with complete profile | 3 | Direct search |
| 1,000+ followers on company page | 2 | Company page data |
| Key employees have active profiles | 2 | Search founder/CEO profiles |
| Brand mentioned in industry thought leadership posts | 3 | Post search |
| Brand mentioned in LinkedIn articles (long-form) | 2 | Article search |
| Employee advocacy (employees sharing brand content) | 2 | Post engagement analysis |
| Brand appears in LinkedIn news/newsletters | 1 | News search |
| **Maximum LinkedIn Score** | **15** | |

---

### Phase 6: Other Platform Scanning (Weight: 15%)

**Step 6.1: Scan Each Platform**

Distribute the 15 points across 7+ additional platforms:

| Platform | Max Points | Search Method |
|----------|-----------|---------------|
| **GitHub** | 3 | `site:github.com "{brand_name}"` — repos, issues, discussions |
| **Stack Overflow** | 2 | `site:stackoverflow.com "{brand_name}"` — questions, answers, tags |
| **Quora** | 2 | `site:quora.com "{brand_name}"` — questions and answers |
| **Medium** | 2 | `site:medium.com "{brand_name}"` — articles mentioning brand |
| **Industry forums** | 2 | Search top 3 industry-specific forums |
| **Podcast directories** | 2 | Search Apple Podcasts, Spotify for brand mentions |
| **News sites** | 2 | `"{brand_name}" site:techcrunch.com OR site:forbes.com OR site:bloomberg.com` |

**Step 6.2: GitHub Scoring (if applicable)**

- Official repository exists: 1 pt
- 100+ stars on any repo: 1 pt
- Active community contributions: 1 pt

**Step 6.3: Stack Overflow Scoring (if applicable)**

- Brand has an official tag: 1 pt
- 50+ questions about brand: 1 pt

**Step 6.4: News and Podcast Scoring**

- Featured in major publications: 1 pt
- Mentioned in 3+ podcasts: 1 pt

---

### Phase 7: Competitive Comparison

**Step 7.1: Run Phases 2-6 for Each Competitor**

Apply the same scanning methodology to each competitor brand. Use abbreviated scanning (top 5 results per platform instead of top 10) to maintain efficiency.

**Step 7.2: Competitive Matrix Template**

```markdown
## Brand Mention Competitive Matrix

| Platform | {Brand} | {Competitor 1} | {Competitor 2} | {Competitor 3} |
|----------|---------|-----------------|-----------------|-----------------|
| YouTube (25) | /25 | /25 | /25 | /25 |
| Reddit (25) | /25 | /25 | /25 | /25 |
| Wikipedia (20) | /20 | /20 | /20 | /20 |
| LinkedIn (15) | /15 | /15 | /15 | /15 |
| Other (15) | /15 | /15 | /15 | /15 |
| **TOTAL** | **/100** | **/100** | **/100** | **/100** |
| **Tier** | | | | |
```

---

### Phase 8: Scoring and Classification

**Step 8.1: Calculate Composite Score**

Sum all platform scores for a total 0-100:

| Score Range | Tier | Description |
|-------------|------|-------------|
| **85-100** | Dominant | Brand is a household name in its space. AI models will cite it by default. Mentioned across all platforms with high frequency and positive sentiment. |
| **70-84** | Strong | Brand has solid cross-platform presence. AI models likely to cite in relevant queries. Some platform gaps exist but overall authority is clear. |
| **50-69** | Moderate | Brand is known but not dominant. AI models may cite depending on query specificity. Notable gaps on 1-2 major platforms. |
| **30-49** | Weak | Brand has limited cross-platform presence. AI models unlikely to cite unless query is very specific. Major gaps on multiple platforms. |
| **0-29** | Minimal | Brand is essentially invisible to AI models. Little to no organic discussion across platforms. Requires foundational brand building. |

**Step 8.2: Gap Analysis**

For each platform where the brand scored below 50% of available points:

```markdown
### Gap: {Platform Name}

**Current Score:** X/{max_points}
**Issue:** [Description of what's missing]
**Impact:** [How this affects AI visibility]
**Recommendation:** [Specific action to improve]
**Priority:** [High/Medium/Low]
**Estimated Effort:** [Hours/weeks to address]
```

**Step 8.3: Linked vs. Unlinked Mention Ratio**

For each platform, estimate:
- Total mentions found
- Mentions that include a link to the brand's domain
- Unlinked mentions (the ones that matter most for GEO)

```markdown
### Mention Link Analysis

| Platform | Total Mentions | Linked | Unlinked | Unlinked % |
|----------|---------------|--------|----------|------------|
| YouTube | | | | % |
| Reddit | | | | % |
| Wikipedia | | | | % |
| LinkedIn | | | | % |
| Other | | | | % |
| **Total** | | | | **%** |
```

**Note:** Higher unlinked percentage is actually better for GEO. AI models treat organic, unlinked mentions as stronger authority signals than promotional linked mentions.

---

### Phase 9: Recommendations Generation

**Step 9.1: Platform-Specific Recommendations**

For each platform scoring below tier threshold, generate actionable recommendations:

**YouTube Recommendations (if score < 15/25):**
- Create brand channel with consistent uploads
- Engage YouTube creators for reviews/mentions
- Produce tutorial content demonstrating product
- Optimize video descriptions with entity-rich text

**Reddit Recommendations (if score < 15/25):**
- Monitor and engage authentically in relevant subreddits
- Never astroturf — Reddit communities detect this instantly
- Create useful resources that get organically shared
- Consider an official brand account for support threads

**Wikipedia Recommendations (if score < 12/20):**
- Assess notability criteria (independent sources required)
- Do NOT edit Wikipedia directly (conflict of interest)
- Ensure reliable third-party sources exist that could support an article
- Focus on getting press coverage that Wikipedia editors would cite

**LinkedIn Recommendations (if score < 8/15):**
- Complete company page with full description
- Encourage employee advocacy posts
- Publish thought leadership articles
- Engage with industry discussions

**Step 9.2: Cross-Platform Strategy**

Generate a 90-day brand mention improvement plan:

```markdown
### 90-Day Brand Mention Strategy

**Month 1: Foundation**
- [3-4 specific actions]

**Month 2: Amplification**
- [3-4 specific actions]

**Month 3: Authority Building**
- [3-4 specific actions]

**Expected Score Improvement:** +X-Y points
**Target Tier:** [next tier up]
```

---

### Phase 10: Report Generation

**Output file: `GEO-BRAND-MENTIONS.md`** in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/` *(see SKILL.md → Output Directory)*

Generate the report with this structure:

```markdown
# GEO Brand Mention Report: {Brand Name}

**Generated:** {date}
**Domain:** {brand_url}
**Industry:** {industry}

---

## Executive Summary

**Brand Mention Score: {score}/100 — {tier}**

{2-3 sentence summary of brand's cross-platform mention landscape, key strengths, and primary gaps.}

### Score Breakdown

| Platform | Score | Weight | Tier |
|----------|-------|--------|------|
| YouTube | /25 | 25% | |
| Reddit | /25 | 25% | |
| Wikipedia | /20 | 20% | |
| LinkedIn | /15 | 15% | |
| Other | /15 | 15% | |
| **Total** | **/100** | **100%** | **{tier}** |

---

## Platform Deep Dive

### YouTube ({score}/25)
{Detailed findings, top mentions, sentiment analysis}

### Reddit ({score}/25)
{Detailed findings, top subreddits, sentiment analysis}

### Wikipedia ({score}/20)
{Article status, mention inventory, quality assessment}

### LinkedIn ({score}/15)
{Company page analysis, thought leadership presence}

### Other Platforms ({score}/15)
{GitHub, Stack Overflow, Quora, Medium, forums, podcasts, news}

---

## Competitive Comparison

{Competitive matrix from Phase 7}

---

## Mention Link Analysis

{Linked vs. unlinked breakdown from Phase 8.3}

---

## Gap Analysis

{Per-platform gap analysis from Phase 8.2}

---

## Recommendations

### Immediate Actions (Week 1-2)
{Quick wins}

### 90-Day Strategy
{Month-by-month plan from Phase 9.2}

### Long-Term Authority Building
{6-12 month strategic recommendations}

---

## Methodology

- **Scoring:** Platform-weighted 0-100 composite score
- **Platform weights:** YouTube 25%, Reddit 25%, Wikipedia 20%, LinkedIn 15%, Other 15%
- **Thesis:** Unlinked brand mentions correlate ~3x more strongly with AI visibility than backlinks
- **Tools:** Web search, Wikipedia API, platform-specific searches
- **Date:** {date}
```

---

## Success Criteria

- All 5 platform categories scanned with documented findings
- Wikipedia checked via API (not just web search)
- Composite score calculated with platform weights
- At least 7 "Other" platforms checked
- Competitive comparison completed (if competitors provided)
- Gap analysis generated for underperforming platforms
- Actionable recommendations with timeline provided
- Report saved as `GEO-BRAND-MENTIONS.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

---

## Integration

This workflow feeds into:
- **Audit workflow** — Brand mention score contributes 20% to composite GEO score *(see `ScoringMethodology.md` for canonical weights)*
- **Report workflow** — Brand section of client deliverable
- **PlatformOptimizer** — Platform gaps inform optimization priorities

**Key Principle:** AI models learn about brands from organic discussion, not link building. A brand that people talk about on Reddit, YouTube, and Wikipedia is a brand that AI will cite. Focus on earning genuine mentions, not manufacturing links.
