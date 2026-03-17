# Platform-Specific Optimization Workflow

**Multi-platform AI search readiness assessment and optimization for 5 major AI search engines**

## Purpose

Analyze a website's readiness to be cited by each of the 5 major AI search platforms. Only 11% of domains are cited by both ChatGPT and Google AI Overviews for the same query — optimization is platform-specific, not universal.

**Core Insight:** Each AI search engine has different data sources, different ranking signals, and different technical requirements. A site optimized for Google AIO may be invisible to ChatGPT. This workflow identifies platform-specific gaps and generates targeted optimization plans.

## When to Use

- Assessing which AI platforms a site is optimized for
- Building a platform-specific GEO strategy
- Identifying why a site appears in one AI engine but not another
- Post-audit deep dive into platform readiness
- Client deliverable for platform optimization roadmap

## Input

- **URL** (required): The primary domain to analyze
- **Target platforms** (optional): Specific platforms to focus on (default: all 5)
- **Industry/niche** (optional): Helps contextualize recommendations
- **Priority queries** (optional): 3-5 queries the site should appear for in AI search

## Platform Overview

| Platform | Primary Data Sources | Key Differentiator |
|----------|---------------------|-------------------|
| Google AI Overviews | Google Search index, Knowledge Graph | Requires existing Google rankings |
| ChatGPT | Bing index, Wikipedia, direct crawl (OAI-SearchBot) | Entity consistency matters most |
| Perplexity | Direct crawl (PerplexityBot), Reddit, forums, academic | Community validation critical |
| Gemini | Google index, YouTube, Knowledge Graph, Google Business | Google ecosystem integration |
| Bing Copilot | Bing index, LinkedIn, IndexNow, Microsoft ecosystem | Microsoft platform signals |

---

## Workflow Steps

### Phase 1: Baseline Data Collection

**Step 1.1: Fetch and Analyze Site**

```
1. Fetch homepage and 3-5 key pages (about, service/product pages, blog)
2. Extract: title tags, meta descriptions, heading structure, schema markup
3. Check robots.txt for AI crawler directives
4. Fetch sitemap.xml
5. Note CMS/framework (WordPress, Next.js, etc.)
6. Check for JavaScript rendering dependency
```

**Step 1.2: Technical Baseline**

Record these signals that affect all platforms:
- Server response time
- SSL certificate status
- Mobile responsiveness
- Structured data present
- Content freshness (last modified dates)
- robots.txt AI crawler permissions

---

### Phase 2: Google AI Overviews Assessment (Score: /100)

**Scoring: Content 40pts, Authority 30pts, Technical 30pts**

Google AI Overviews pulls from its existing search index. If you don't rank on page 1, you won't appear in AIO.

**Step 2.1: Content Signals (40 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Q&A structured content on key pages | 10 | Check for question headings (H2/H3 with "?") followed by direct answers |
| Direct answer paragraphs (40-60 words) | 8 | Analyze content blocks — do pages lead with concise answers before elaborating? |
| Question headings match search intent | 8 | Compare heading questions against target queries |
| Content covers topic comprehensively | 7 | Check for supporting sections, subtopics, related entities |
| Lists and structured formatting | 4 | Count ordered/unordered lists, tables, definition lists |
| Fresh content (updated within 6 months) | 3 | Check dateModified in schema, last-modified headers |

**Assessment procedure:**
```
For each of 3-5 key pages:
  1. Extract all H2 and H3 headings
  2. Count headings that contain question words (what, how, why, when, where, which, can, does, is)
  3. For each question heading, check if the immediately following paragraph is 40-60 words and directly answers the question
  4. Check if content includes structured lists, comparison tables, or step-by-step formats
  5. Score based on percentage of pages meeting criteria
```

**Step 2.2: Authority Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Top-10 Google rankings for target queries | 12 | Search target queries, check if site appears on page 1 |
| E-E-A-T signals (author bios, credentials) | 6 | Check for author pages, bylines, credential mentions |
| Domain authority indicators | 5 | Age, backlink profile quality (not quantity) |
| Cited by other authoritative sources | 4 | Search for brand mentions on .edu, .gov, major publications |
| Google Knowledge Panel exists | 3 | Search brand name, check for Knowledge Panel |

**Step 2.3: Technical Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Pages indexed in Google | 8 | `site:{domain}` search count |
| Schema markup (Organization, Article, speakable) | 7 | Parse JSON-LD from pages |
| Page speed (LCP < 2.5s) | 5 | Lighthouse or CrUX data |
| Mobile-first content parity | 5 | Compare mobile vs desktop content |
| HTTPS with valid certificate | 3 | Direct check |
| Clean URL structure | 2 | Analyze URL patterns |

---

### Phase 3: ChatGPT Assessment (Score: /100)

**Scoring: Entity 35pts, Content 40pts, Crawler 25pts**

ChatGPT uses Bing's index as a foundation, Wikipedia for entity knowledge, and its own OAI-SearchBot crawler for direct access. Entity consistency across platforms is the primary signal.

**Step 3.1: Entity Signals (35 points)**

| Signal | Points | How to Assess |
|--------|--------|--------------|
| Wikipedia article exists for brand/entity | 10 | Wikipedia API check (see BrandMentions workflow) |
| Consistent entity information across platforms | 8 | Compare brand name, description, founding date across Google, Bing, LinkedIn, Wikipedia |
| Bing Knowledge Card exists | 7 | Search brand on Bing, check for entity card |
| Entity appears in Wikidata | 5 | Search wikidata.org for brand entity |
| Consistent NAP (Name, Address, Phone) across web | 5 | Check consistency across directories |

**Assessment procedure:**
```
1. Search Wikipedia API for brand entity
2. Search Bing for brand name — check for Knowledge Card
3. Search Wikidata for brand entity ID
4. Compare entity attributes across Wikipedia, Bing, LinkedIn, Google
5. Flag any inconsistencies (different founding dates, different descriptions, name variations)
6. Score based on presence and consistency
```

**Step 3.2: Content Signals (40 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Content indexed in Bing | 10 | `site:{domain}` on Bing, check page count |
| Definitive, quotable statements | 8 | Analyze content for clear, authoritative sentences that could be cited |
| Comprehensive topic coverage | 8 | Check for pillar pages covering topics in depth |
| Unique data, research, or insights | 7 | Look for original statistics, studies, proprietary data |
| Clear content organization (headings, sections) | 4 | Structural analysis of key pages |
| Author attribution with expertise signals | 3 | Check for author bios linking to credentials |

**Step 3.3: Crawler Access Signals (25 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| OAI-SearchBot allowed in robots.txt | 10 | Parse robots.txt for `User-agent: OAI-SearchBot` |
| ChatGPT-User allowed in robots.txt | 5 | Parse robots.txt for `User-agent: ChatGPT-User` |
| GPTBot allowed in robots.txt | 5 | Parse robots.txt for `User-agent: GPTBot` |
| Content accessible without JavaScript | 5 | Check if key content requires JS rendering |

**robots.txt check:**
```
Fetch {domain}/robots.txt
Check for these user agents:
  - OAI-SearchBot (search feature crawler)
  - ChatGPT-User (browsing feature)
  - GPTBot (training data — less critical for search but signals openness)

Scoring:
  - All three allowed: 20/20
  - OAI-SearchBot + ChatGPT-User allowed: 15/20
  - Only GPTBot allowed: 5/20
  - All blocked: 0/20
  - No mention (default allow): 20/20
```

---

### Phase 4: Perplexity Assessment (Score: /100)

**Scoring: Community 30pts, Source Quality 30pts, Freshness 20pts, Technical 20pts**

Perplexity heavily indexes Reddit, forums, and community discussions. It values primary sources and fresh content. Community validation is its key differentiator.

**Step 4.1: Community Validation Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Brand discussed positively on Reddit | 10 | Search `site:reddit.com "{brand}"` — analyze sentiment |
| Brand mentioned in relevant forums | 6 | Search industry forums for brand mentions |
| Community-generated content about brand | 6 | Look for user reviews, discussions, how-tos |
| Brand recommended in "what should I use" threads | 5 | Search recommendation threads |
| Active community engagement (brand responds) | 3 | Check if brand has official presence in communities |

**Step 4.2: Source Quality Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Primary source content (original research, data) | 10 | Check for original statistics, studies, datasets |
| Cited by academic or authoritative sources | 7 | Search Google Scholar, .edu sites |
| Clear sourcing and references in content | 5 | Check if content cites its own sources |
| Factual accuracy and verifiability | 5 | Assess claims — are they specific and verifiable? |
| Expert authorship signals | 3 | Author credentials, institutional affiliations |

**Step 4.3: Freshness Signals (20 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Content updated within 30 days | 8 | Check dateModified, last-modified headers |
| Regular publishing cadence | 5 | Analyze blog/news post dates |
| Time-sensitive content kept current | 4 | Check for outdated statistics, dead links |
| Sitemap lastmod dates recent | 3 | Parse sitemap.xml lastmod values |

**Step 4.4: Technical Signals (20 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| PerplexityBot allowed in robots.txt | 8 | Parse robots.txt for `User-agent: PerplexityBot` |
| Fast page loads (< 3s) | 4 | Response time check |
| Clean, crawlable HTML | 4 | Check for SSR, minimal JS dependency |
| Sitemap.xml present and valid | 4 | Fetch and validate sitemap |

---

### Phase 5: Gemini Assessment (Score: /100)

**Scoring: Google Ecosystem 35pts, Knowledge Graph 30pts, Content 35pts**

Gemini is deeply integrated with Google's ecosystem. YouTube presence, Google Business Profile, and Knowledge Graph connections are critical differentiators.

**Step 5.1: Google Ecosystem Signals (35 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| YouTube channel exists with regular content | 10 | Search YouTube for brand channel |
| Google Business Profile complete and active | 8 | Search brand on Google Maps |
| Google Merchant Center (if e-commerce) | 5 | Check for product listings in Google Shopping |
| Google News inclusion | 5 | Search Google News for brand |
| YouTube videos rank for target queries | 4 | Search target queries on YouTube |
| Google Podcasts/YouTube podcasts | 3 | Check for podcast presence |

**YouTube assessment detail:**
```
1. Search YouTube for brand channel
2. Check: subscriber count, video count, upload frequency
3. Check: video descriptions include entity-rich text
4. Check: videos have transcripts/captions enabled
5. Check: channel "About" section has complete brand description
6. Score based on presence, activity, and quality
```

**Step 5.2: Knowledge Graph Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Google Knowledge Panel exists | 10 | Search brand name on Google |
| Knowledge Panel is complete (logo, description, details) | 6 | Assess completeness of panel |
| Entity connected to related entities | 5 | Check "People also search for" in panel |
| sameAs connections to 3+ platforms | 5 | Check Organization schema for sameAs |
| Consistent entity data across Google properties | 4 | Compare Knowledge Panel vs Business Profile vs YouTube |

**Step 5.3: Content Signals (35 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Topical depth — comprehensive coverage of domain | 10 | Assess if site covers topic thoroughly vs superficially |
| Content aligned with Google's Helpful Content criteria | 8 | Check for first-person expertise, original insights |
| Structured data supporting content (Article, Person, Organization) | 7 | Parse JSON-LD from pages |
| Internal linking creating topical clusters | 5 | Analyze internal link structure |
| Multi-format content (text, images, video embeds) | 5 | Check for content variety on key pages |

---

### Phase 6: Bing Copilot Assessment (Score: /100)

**Scoring: Bing Signals 30pts, Content 30pts, Microsoft Ecosystem 20pts, Technical 20pts**

Bing Copilot uses Bing's index plus Microsoft ecosystem signals. IndexNow protocol, LinkedIn presence, and Bing Webmaster Tools verification provide advantages.

**Step 6.1: Bing-Specific Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Pages indexed in Bing | 8 | `site:{domain}` on Bing |
| Bing Webmaster Tools verified (check meta tag) | 7 | Look for `<meta name="msvalidate.01">` tag |
| IndexNow protocol implemented | 8 | Check for IndexNow API key file at `{domain}/indexnow-key.txt` or similar |
| Bing entity card exists | 7 | Search brand on Bing, check for entity card |

**IndexNow check:**
```
1. Check for IndexNow key file: {domain}/{key}.txt
2. Check for IndexNow meta tag or HTTP header
3. Check sitemap for IndexNow ping endpoint
4. If WordPress: check for IndexNow plugin

Why it matters: ChatGPT's search feature uses Bing's index.
IndexNow = instant Bing indexing = faster ChatGPT discovery.
```

**Step 6.2: Content Signals (30 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Clear, structured content with headings | 8 | Heading hierarchy analysis |
| FAQ sections with direct answers | 7 | Check for FAQ patterns |
| Comprehensive about/company page | 5 | Assess completeness |
| Blog with regular updates | 5 | Check publishing frequency |
| Content has clear authorship | 5 | Author attribution on articles |

**Step 6.3: Microsoft Ecosystem Signals (20 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| LinkedIn company page (complete, active) | 8 | Search LinkedIn for company |
| LinkedIn employee profiles reference brand | 5 | Check if employees list company |
| Brand mentioned on LinkedIn articles/posts | 4 | Search LinkedIn for brand mentions |
| Microsoft/GitHub integrations (if tech company) | 3 | Check for GitHub presence |

**Step 6.4: Technical Signals (20 points)**

| Signal | Points | How to Assess |
|--------|--------|---------------|
| Fast page loads (< 2s TTFB) | 6 | Response time measurement |
| Mobile-optimized pages | 5 | Mobile rendering check |
| HTTPS with modern TLS | 4 | Certificate and protocol check |
| bingbot allowed in robots.txt | 5 | Parse robots.txt |

---

### Phase 7: Cross-Platform Synergies

**Step 7.1: Identify Synergy Opportunities**

Actions that improve readiness across multiple platforms simultaneously:

```markdown
### High-Leverage Cross-Platform Actions

| Action | Platforms Improved | Impact |
|--------|-------------------|--------|
| Add Organization schema with sameAs to 5+ platforms | All 5 | Enables entity resolution across all AI engines |
| Create/optimize YouTube channel | Gemini, Google AIO, ChatGPT | YouTube is indexed by Google AND Bing |
| Complete LinkedIn company page | Bing Copilot, ChatGPT, Perplexity | LinkedIn indexed by Bing; community signal for Perplexity |
| Implement IndexNow | Bing Copilot, ChatGPT | Both use Bing's index |
| Allow all AI crawlers in robots.txt | ChatGPT, Perplexity | Direct access enables citation |
| Publish original research/data | All 5 | Unique content cited across all platforms |
| Earn Reddit community mentions | Perplexity, Google AIO, ChatGPT | Reddit data licensed by Google; indexed by all |
| Wikipedia article (if notable) | ChatGPT, Gemini, All | Highest single-source authority signal |
| SSR rendering (no JS dependency) | All 5 | AI crawlers cannot execute JavaScript |
| Add speakable schema | Google AIO, Gemini | Voice search and AI snippet extraction |
```

**Step 7.2: Platform Overlap Analysis**

```
For each pair of platforms, calculate:
  - Shared requirements met
  - Shared requirements missed
  - Unique requirements for each

Identify: Which platform improvements create the most cross-platform benefit?
```

---

### Phase 8: Scoring and Report

**Step 8.1: Calculate Per-Platform Scores**

Each platform scored independently 0-100 using its specific criteria above.

**Step 8.2: Calculate Composite Readiness Score**

```
Composite = (Google_AIO * 0.25) + (ChatGPT * 0.25) + (Perplexity * 0.20) + (Gemini * 0.15) + (Bing_Copilot * 0.15)
```

**Step 8.3: Platform Readiness Tiers**

| Score | Tier | Meaning |
|-------|------|---------|
| 80-100 | Optimized | Platform actively citing this site |
| 60-79 | Ready | Site meets most platform requirements |
| 40-59 | Partial | Significant gaps in platform readiness |
| 20-39 | Weak | Major optimization needed |
| 0-19 | Not Ready | Fundamental platform requirements missing |

---

### Phase 9: Report Generation

**Output file: `GEO-PLATFORM-OPTIMIZATION.md`** in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/` *(see SKILL.md → Output Directory)*

```markdown
# GEO Platform Optimization Report: {domain}

**Generated:** {date}
**Domain:** {url}
**Industry:** {industry}

---

## Executive Summary

**Composite Platform Readiness: {score}/100**

Only 11% of domains are cited by both ChatGPT and Google AI Overviews for the same query. Platform-specific optimization is essential.

### Platform Readiness Overview

| Platform | Score | Tier | Key Gap |
|----------|-------|------|---------|
| Google AI Overviews | /100 | | |
| ChatGPT | /100 | | |
| Perplexity | /100 | | |
| Gemini | /100 | | |
| Bing Copilot | /100 | | |
| **Composite** | **/100** | | |

---

## Google AI Overviews ({score}/100)

### Content Signals ({score}/40)
{Detailed findings}

### Authority Signals ({score}/30)
{Detailed findings}

### Technical Signals ({score}/30)
{Detailed findings}

### Recommendations
{Prioritized action items}

---

## ChatGPT ({score}/100)

### Entity Signals ({score}/35)
{Detailed findings}

### Content Signals ({score}/40)
{Detailed findings}

### Crawler Access ({score}/25)
{Detailed findings}

### Recommendations
{Prioritized action items}

---

## Perplexity ({score}/100)

### Community Validation ({score}/30)
{Detailed findings}

### Source Quality ({score}/30)
{Detailed findings}

### Freshness ({score}/20)
{Detailed findings}

### Technical ({score}/20)
{Detailed findings}

### Recommendations
{Prioritized action items}

---

## Gemini ({score}/100)

### Google Ecosystem ({score}/35)
{Detailed findings}

### Knowledge Graph ({score}/30)
{Detailed findings}

### Content ({score}/35)
{Detailed findings}

### Recommendations
{Prioritized action items}

---

## Bing Copilot ({score}/100)

### Bing Signals ({score}/30)
{Detailed findings}

### Content ({score}/30)
{Detailed findings}

### Microsoft Ecosystem ({score}/20)
{Detailed findings}

### Technical ({score}/20)
{Detailed findings}

### Recommendations
{Prioritized action items}

---

## Cross-Platform Synergies

### High-Leverage Actions
{Actions that improve multiple platforms simultaneously, ranked by cross-platform impact}

### Platform Overlap Analysis
{Which platforms share requirements, where unique optimization is needed}

---

## Priority Action Plan

### Critical (Week 1)
{Actions that unblock multiple platforms}

### High (Week 2-4)
{Platform-specific optimizations with highest impact}

### Medium (Month 2-3)
{Authority building and content creation}

### Low (Ongoing)
{Maintenance and monitoring}

---

## Methodology

- **Platforms assessed:** Google AI Overviews, ChatGPT, Perplexity, Gemini, Bing Copilot
- **Scoring:** Platform-specific criteria weighted by signal importance
- **Key stat:** Only 11% of domains cited by both ChatGPT and Google AIO for same query
- **Date:** {date}
```

---

## Success Criteria

- All 5 platforms assessed with individual scores
- Platform-specific scoring criteria fully applied
- Crawler access checked for all relevant AI user agents
- Cross-platform synergies identified and ranked
- Actionable recommendations generated per platform
- Priority action plan with timeline
- Report saved as `GEO-PLATFORM-OPTIMIZATION.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`

---

## Integration

This workflow feeds into:
- **Audit workflow** — Platform readiness contributes 10% to composite GEO score *(see `ScoringMethodology.md` for canonical weights)*
- **Crawlers workflow** — Technical crawler access details
- **Schema workflow** — Structured data requirements per platform
- **Report workflow** — Platform section of client deliverable

**Key Principle:** Optimize for each platform individually. A one-size-fits-all approach means you'll rank on zero AI platforms instead of five. Start with the platform where you have the most existing authority, then expand.
