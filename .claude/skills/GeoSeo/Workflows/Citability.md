# GEO Citability Scoring Workflow

**Mode:** Single-page or multi-page AI citability analysis | **Automated + manual fallback**

## When to Use

- User says "citability", "citation readiness", "citable", "score this page"
- User provides a specific URL to analyze for AI citation potential
- Called as subcomponent of the full Audit workflow (GeoAiVisibility subagent)

---

## Core Concept

**Citability** measures how likely an AI engine (ChatGPT, Claude, Perplexity, Gemini) is to directly quote or paraphrase content from a page when answering a user's question. High citability means the content is structured, specific, and self-contained enough that AI models will prefer it as a source.

**The Optimal Citable Passage:**
- **Length:** 134-167 words (research shows this is the sweet spot for AI citation)
- **Self-contained:** Makes sense without needing surrounding paragraphs
- **Fact-rich:** Contains specific numbers, dates, names, or claims
- **Answer-shaped:** Directly answers a question someone would ask
- **Uniquely sourced:** Contains proprietary data, original research, or expert opinion not available elsewhere

---

## Workflow

### Step 1: Attempt Automated Scoring

**Try the Python tool first:**

```bash
python3 ${PAI_DIR}/skills/GeoSeo/Tools/CitabilityScorer.py <url>
```

**Expected output format from the tool:**

```json
{
  "url": "https://example.com/page",
  "overall_score": 72,
  "blocks_analyzed": 12,
  "blocks": [
    {
      "id": 1,
      "text_preview": "First 80 chars...",
      "word_count": 145,
      "scores": {
        "answer_block_quality": 8.5,
        "self_containment": 7.0,
        "structural_readability": 9.0,
        "statistical_density": 6.5,
        "uniqueness": 7.0
      },
      "weighted_score": 76,
      "suggestions": ["Add specific statistics", "Include source attribution"]
    }
  ],
  "top_blocks": [3, 7, 1],
  "bottom_blocks": [9, 11, 5],
  "rewrite_priorities": [9, 11]
}
```

**If the tool succeeds:** Skip to Step 5 (Report Generation) using the tool's output.

**If the tool fails** (not installed, error, unavailable): Proceed to Step 2 for manual analysis.

---

### Step 2: Fetch and Extract Content (Manual Fallback)

```
WebFetch(url)
```

**Extract content blocks.** A "content block" is defined as:

1. **Primary blocks** (prioritized for scoring):
   - Each H2 section (heading + all content until next H2)
   - Hero/above-fold content (first visible content block)
   - Definition paragraphs (paragraphs that define a key term)
   - List-form content (numbered or bulleted lists with context)
   - Table content (data tables with surrounding explanation)

2. **Secondary blocks** (scored if primary blocks < 5):
   - H3 sub-sections
   - Standalone paragraphs over 80 words
   - Blockquotes
   - Callout/highlight boxes

**For each block, record:**
- Block ID (sequential)
- Block type (H2 section, hero, definition, list, table, H3 section, paragraph)
- Full text content
- Word count
- Position on page (above fold, mid-page, footer area)
- Heading text (if applicable)

**Minimum blocks required:** 3. If fewer than 3 blocks can be extracted, the page may be too thin for meaningful citability analysis — flag this and score accordingly.

---

### Step 3: Score Each Content Block

Apply the 5 scoring categories to each block. Score each category 0-10.

#### Category 1: Answer Block Quality (Weight: 30%)

Measures how well the block directly answers a likely user question.

| Score | Criteria |
|-------|----------|
| 9-10 | Directly answers a specific question. Could be copy-pasted as a complete answer. Opens with the answer, not context. |
| 7-8 | Answers a question but needs minor surrounding context. Answer is present but buried after preamble. |
| 5-6 | Related to a question topic but doesn't directly answer. Informative but not answer-shaped. |
| 3-4 | Tangentially related. More promotional than informational. |
| 0-2 | Navigation text, boilerplate, CTAs, or content that answers no plausible question. |

**Evaluation process:**
1. What question would someone ask that this block answers?
2. If you can't articulate the question in under 15 words, score ≤ 5
3. Does the block start with the answer (answer-first) or build up to it?
4. Could an AI quote this block and fully satisfy the user's query?

#### Category 2: Self-Containment (Weight: 25%)

Measures whether the block makes complete sense in isolation.

| Score | Criteria |
|-------|----------|
| 9-10 | Fully self-contained. No pronouns referencing prior content. All acronyms defined. All claims have enough context. |
| 7-8 | Nearly self-contained. One minor reference to outside context that doesn't impede understanding. |
| 5-6 | Partially self-contained. Requires 1-2 pieces of external context to fully understand. |
| 3-4 | Depends heavily on surrounding content. Multiple undefined references. |
| 0-2 | Incomprehensible without prior paragraphs. Fragment of a larger thought. |

**Red flags that reduce score:**
- Starts with "This", "It", "They", "The above", "As mentioned"
- Contains undefined acronyms
- References "our product" without naming it
- Uses relative terms ("the previous method", "compared to the above")

#### Category 3: Structural Readability (Weight: 20%)

Measures how AI-parseable the block's structure is.

| Score | Criteria |
|-------|----------|
| 9-10 | Clear heading, logical paragraph structure, uses lists/tables where appropriate, proper markdown/HTML semantics. |
| 7-8 | Good structure with minor issues (e.g., one overly long paragraph). |
| 5-6 | Adequate structure but dense. No lists where lists would help. Single wall of text. |
| 3-4 | Poor structure. Unclear hierarchy. Mixed content types without separation. |
| 0-2 | No structure. Run-on content. HTML soup with no semantic meaning. |

**Structural signals that boost score:**
- Descriptive heading that summarizes the block
- Paragraphs under 80 words
- Numbered or bulleted lists for multi-item content
- Tables for comparative data
- Bold/emphasis on key terms
- Short sentences (under 25 words average)

#### Category 4: Statistical Density (Weight: 15%)

Measures the concentration of specific, verifiable facts and data.

| Score | Criteria |
|-------|----------|
| 9-10 | 3+ specific statistics, named sources, dates, and quantified claims per 150 words. First-party data or original research. |
| 7-8 | 2-3 specific data points per 150 words. Mix of quantitative and qualitative claims. |
| 5-6 | 1-2 data points but mostly qualitative assertions. Some specificity. |
| 3-4 | Vague claims without evidence. "Many companies", "most users", "significant growth" without numbers. |
| 0-2 | Pure opinion or marketing language with zero specific data. |

**What counts as a "specific fact":**
- Named percentages: "72% of enterprises"
- Named quantities: "$4.2B market" or "150,000 customers"
- Named dates: "launched in Q3 2024" or "since 2018"
- Named entities: "according to Gartner" or "used by Microsoft and Google"
- Comparative data: "3x faster than" (with named comparison)

**What does NOT count:**
- "Leading provider" (vague)
- "Significant market share" (unquantified)
- "Many customers trust us" (unspecific)
- "Fast-growing" (relative without baseline)

#### Category 5: Uniqueness (Weight: 10%)

Measures whether this content offers value an AI couldn't generate itself.

| Score | Criteria |
|-------|----------|
| 9-10 | Proprietary data, original research, unique expert perspective, or first-person experience that cannot be found elsewhere. |
| 7-8 | Valuable synthesis of public information with original analysis or unique framing. Industry insider perspective. |
| 5-6 | Well-curated public information with some original commentary. Competent but not differentiated. |
| 3-4 | Generic information available from many sources. AI could write equivalent content. |
| 0-2 | Boilerplate, templated content, or thin rewriting of commonly available information. |

**High uniqueness signals:**
- "Our research found..." with original data
- Named case studies with specific outcomes
- Expert quotes from identified individuals
- Proprietary benchmarks or methodologies
- First-hand experience descriptions

---

### Step 4: Calculate Scores

#### Per-Block Weighted Score

```
block_score = (
  answer_block_quality × 0.30 +
  self_containment     × 0.25 +
  structural_readability × 0.20 +
  statistical_density  × 0.15 +
  uniqueness           × 0.10
) × 10
```

This produces a 0-100 score per block.

#### Overall Page Score

```
page_score = average(top_75pct_of_block_scores)
```

Use the top 75% of blocks (rounded up) to avoid penalizing a page for having a few navigation or boilerplate blocks. A page with 12 blocks uses the top 9.

#### Score Interpretation

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | AI engines will preferentially cite this content |
| 75-89 | Good | Strong citation potential with minor gaps |
| 60-74 | Fair | Some citable content but inconsistent quality |
| 40-59 | Poor | Rarely cited; content too generic or poorly structured |
| 0-39 | Critical | Content is not structured for AI consumption |

---

### Step 5: Generate Rewrite Suggestions

For the **3 lowest-scoring blocks**, generate specific rewrite guidance:

**For each low-scoring block, provide:**

1. **Current score** and which categories dragged it down
2. **The core problem** in one sentence
3. **Rewrite strategy** — specific instructions:

   - If **Answer Block Quality** is low:
     > "Restructure to lead with the answer. The key claim '{extracted claim}' should be the first sentence. Remove the preamble '{first sentence}'."

   - If **Self-Containment** is low:
     > "Replace '{pronoun/reference}' with the specific noun. Define '{acronym}' on first use. Add context: this block is about {topic}."

   - If **Structural Readability** is low:
     > "Break the {X}-word paragraph into 3 shorter paragraphs. Convert the inline list to a bulleted list. Add a descriptive heading."

   - If **Statistical Density** is low:
     > "Replace '{vague claim}' with a specific number. Add a source citation after '{claim}'. Quantify '{qualitative statement}'."

   - If **Uniqueness** is low:
     > "This reads as generic advice. Add: a specific case study, a proprietary data point, or a named expert perspective. What does {brand} know about this that others don't?"

4. **Example rewrite** — Rewrite the first 2-3 sentences of the block demonstrating the improvements. Mark changes in bold.

---

### Step 6: Output Report

Generate `GEO-CITABILITY-SCORE.md` in the output directory *(see SKILL.md → Output Directory for path convention: `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`)*:

```markdown
# GEO Citability Score: {url}

**Date:** {YYYY-MM-DD}
**Overall Score:** {score}/100 ({rating})
**Blocks Analyzed:** {count}
**Scoring Method:** {automated/manual}

---

## Score Breakdown

| Category | Weight | Average Score |
|----------|--------|---------------|
| Answer Block Quality | 30% | {avg}/10 |
| Self-Containment | 25% | {avg}/10 |
| Structural Readability | 20% | {avg}/10 |
| Statistical Density | 15% | {avg}/10 |
| Uniqueness | 10% | {avg}/10 |

---

## Top Performing Blocks

### Block {id}: "{heading or first 60 chars...}"
- **Score:** {score}/100
- **Strengths:** {what makes this block citable}
- **Word count:** {count} (optimal range: 134-167)

{Repeat for top 3 blocks}

---

## Lowest Performing Blocks (Rewrite Priority)

### Block {id}: "{heading or first 60 chars...}"
- **Score:** {score}/100
- **Primary weakness:** {category}
- **Problem:** {one sentence}
- **Rewrite strategy:** {specific instructions}
- **Example rewrite:**
  > {rewritten opening sentences with improvements in bold}

{Repeat for bottom 3 blocks}

---

## All Blocks

| # | Type | Heading/Preview | Words | ABQ | SC | SR | SD | UQ | Score |
|---|------|-----------------|-------|-----|----|----|----|----|-------|
| 1 | {type} | {preview} | {wc} | {s} | {s} | {s} | {s} | {s} | {s} |
{...all blocks}

**Legend:** ABQ=Answer Block Quality, SC=Self-Containment, SR=Structural Readability, SD=Statistical Density, UQ=Uniqueness

---

## Optimal Passage Length Analysis

| Length Bucket | Block Count | Avg Score | Assessment |
|---------------|-------------|-----------|------------|
| Under 80 words | {n} | {avg} | Too short for citation |
| 80-133 words | {n} | {avg} | Usable but suboptimal |
| 134-167 words | {n} | {avg} | Optimal citation length |
| 168-250 words | {n} | {avg} | Usable, consider trimming |
| Over 250 words | {n} | {avg} | Too long, split into blocks |

---

## Recommendations

### Immediate Actions (Quick Wins)
1. {Highest impact, lowest effort change}
2. {Second priority}
3. {Third priority}

### Content Restructuring
{Broader recommendations for improving citability across the page}

### Content Additions
{Missing content that would improve scores — definitions, statistics, case studies}

---

*Generated by PAI GeoSeo Citability Scorer — {date}*
```

---

## Multi-Page Mode

When analyzing multiple pages (e.g., as part of a full audit):

1. Run Steps 1-5 for each page
2. After all pages scored, add a **comparative summary**:

```markdown
## Cross-Page Citability Summary

| Page | Score | Strongest Category | Weakest Category |
|------|-------|--------------------|-------------------|
| {url} | {score} | {category} | {category} |
{...all pages}

**Site-wide average:** {avg}/100
**Best performing page:** {url} ({score})
**Most improvement needed:** {url} ({score})
**Most common weakness:** {category across all pages}
```

---

## Error Handling

| Error | Response |
|-------|----------|
| URL unreachable | Report error, do not score |
| Page has no extractable content | Score 0, flag "No content found" |
| Fewer than 3 content blocks | Score available blocks, flag "Thin content" |
| Python tool not available | Fall back to manual analysis (Step 2) |
| Page is behind login/paywall | Report limitation, score visible content only |
| Non-HTML content (PDF, etc.) | Attempt extraction, note content type in report |

## Dependencies

- **Tools:** WebFetch (required), `Tools/CitabilityScorer.py` (optional)
- **Output:** `GEO-CITABILITY-SCORE.md` in `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/`
