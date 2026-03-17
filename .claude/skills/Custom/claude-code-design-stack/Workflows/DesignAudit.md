# Design Stack — Design Audit Workflow

Analyze an existing app's design quality and produce actionable recommendations. Uses Stitch to extract current patterns, UI/UX Pro Max to identify gaps, and 21st.dev Magic to generate replacement components. This is an opinionated audit — Lucy calls out problems directly, not diplomatically.

---

## When to Use

- Existing app looks generic, inconsistent, or "AI-generated"
- User wants to raise visual quality without a full redesign
- User wants a design system extracted from what already exists
- Before a launch or demo — "make this look professional"

---

## Step 1: Capture and Extract

Get the current state. Accept any of:
- Screenshot(s) of the existing app
- URL to a running instance (use Browser/Playwright to capture)
- Path to local dev server

Feed screenshots to Stitch MCP to extract current design patterns — colors, typography, layout structure, component styles.

## Step 2: Run the Audit (UI/UX Pro Max)

This is not a gentle review. Run the extracted patterns against every UI/UX Pro Max priority level and report honestly.

### 2a: Visual Quality Scan

Check against the "Common Rules for Professional UI" section:

| Check | What to Look For |
|-------|-----------------|
| Icons | Emojis used as icons? Inconsistent icon sets? Wrong sizes? |
| Hover states | Layout shift on hover? Missing cursor-pointer? No transitions? |
| Brand assets | Incorrect logos? Missing favicons? |
| Colors | Is the palette coherent or random? Are there 7 different grays? |
| Typography | More than 2 font families? Inconsistent sizes? Bad line heights? |
| Spacing | Is spacing consistent or eyeballed? Different padding on similar elements? |

### 2b: Accessibility Audit (Priority 1-2)

Run every critical check:
- Color contrast ratios (measure actual values, don't guess)
- Focus states present on all interactive elements?
- Touch targets meet 44x44px minimum?
- Form inputs have associated labels?
- Images have alt text?
- ARIA labels on icon-only buttons?

### 2c: Responsive Audit

Check at 375px, 768px, 1280px:
- Content hidden behind fixed elements?
- Horizontal scrolling?
- Text readable at mobile sizes (16px minimum)?
- Core actions accessible without scrolling?

### 2d: Design Consistency

The hardest question: **does this app look like one product, or like 5 different developers each picked their own styles?**

- Are border-radius values consistent?
- Are shadow styles consistent?
- Are button styles consistent across pages?
- Is the color usage systematic or ad-hoc?

## Step 3: Deliver the Audit Report

**Be direct. Sugarcoating doesn't help.**

```
DESIGN AUDIT: [App Name]
Score: [1-10] — [one-line verdict]

CRITICAL ISSUES (fix before showing anyone):
- [Issue]: [specific location] — [what's wrong] — [how to fix]
- ...

QUALITY ISSUES (fix before launch):
- [Issue]: [specific location] — [what's wrong] — [how to fix]
- ...

CONSISTENCY ISSUES (fix for polish):
- [Issue]: [specific locations] — [what's inconsistent] — [what it should be]
- ...

CURRENT DESIGN SYSTEM (extracted):
- Style: [identified style or "none — inconsistent"]
- Palette: [current colors used, with notes on conflicts]
- Typography: [current fonts, with notes on inconsistencies]
- Spacing: [current spacing patterns or "no system"]

RECOMMENDED DESIGN SYSTEM:
- Style: [recommended] — [why]
- Palette: [recommended] — [specific hex values to standardize on]
- Typography: [recommended pairing] — [specific font swaps]
- Spacing: [recommended scale]

COMPONENT REPLACEMENTS:
[List each generic/broken component and what 21st.dev component should replace it]
```

## Step 4: Prioritize and Plan

Don't dump 30 issues and walk away. Help the user prioritize:

> "I found [N] issues. Here's what I'd fix in order:
>
> **First 30 minutes:** [2-3 critical issues that have the biggest visual impact with the least effort — usually color/typography standardization]
> **Next hour:** [3-5 component replacements using 21st.dev Magic]
> **Polish pass:** [remaining consistency issues]
>
> Want me to start with the first batch?"

## Step 5: Implement (if approved)

For each approved fix:

1. **Design system fixes** — Generate and persist:
   ```bash
   python3 skills/ui-ux-pro-max/scripts/search.py "<product keywords>" --design-system --persist -p "<Project Name>"
   ```

2. **Component replacements** — For each component to replace:
   - Search for inspiration first: `mcp__magic__21st_magic_component_inspiration({ message, searchQuery })`
   - Generate replacement: `mcp__magic__21st_magic_component_builder({ message, searchQuery, absolutePathToCurrentFile, absolutePathToProjectDirectory, standaloneRequestQuery })` — embed new design tokens in `standaloneRequestQuery`
   - Refine if needed: `mcp__magic__21st_magic_component_refiner({ userMessage, absolutePathToRefiningFile, context })`
   - One component per request, applying the new design system tokens

3. **Before/after verification** — Screenshot each change. Don't claim improvement without visual proof.

> "Here's the [component] before and after. The old version [specific problem]. The new version [specific improvement]. Accessibility: [what was fixed]."

## What This Audit Does NOT Do

- Say "looks good overall with a few minor issues" when it doesn't
- List problems without actionable fixes
- Recommend a complete rewrite when targeted fixes would work
- Skip accessibility because "it's just an internal tool"
