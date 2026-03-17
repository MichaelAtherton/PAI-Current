# Design Stack — Full Design Workflow

End-to-end design flow using all three tools. This is a conversational, consultative process — not a passive checklist. Lucy drives discovery, challenges weak ideas, makes opinionated recommendations, and pushes back when choices will produce poor results.

---

## Prerequisites

**MCP servers must be connected BEFORE starting this session.** MCP tools added mid-session won't be available until Claude Code restarts. Verify all three are connected before beginning.

- **Stitch MCP:** Proxy must be running in a separate terminal: `npx @_davideast/stitch-mcp proxy`. Also requires Google Cloud auth (run `npx @_davideast/stitch-mcp init` once if not set up).
- **21st.dev Magic MCP:** User-scoped, auto-connects on startup. Verify with `claude mcp list`.
- **UI/UX Pro Max:** Project skill at `.claude/skills/ui-ux-pro-max/`. Always available — no MCP dependency.

**If Stitch is unavailable:** Skip Phase 3 (mockup) and go directly to Phase 4 (components). The design system MASTER.md + screen descriptions are sufficient for component generation.

---

## Phase 1: Discovery (Conversational — Do Not Rush)

**Goal:** Understand what we're building and for whom before touching any tool.

### Step 1a: Extract Intent

Lucy asks — do not accept vague descriptions. Push for specifics:

> "Before I generate anything, I need three things:
>
> 1. **Who is this for?** Not 'users' — a specific person. A startup founder checking metrics at 6am? A shopper comparing prices on their phone? A patient booking an appointment?
> 2. **What is the one thing they must accomplish?** Not a feature list — the single most important action.
> 3. **What should this feel like?** Not 'modern and clean' — every app says that. Is it calm like a meditation app? Dense like Bloomberg? Playful like Duolingo? Show me a reference if you have one."

**Wait for real answers. If the user says "just a dashboard" or "something clean and modern," push back:**

> "Every generic dashboard looks the same because the brief was generic. Who is sitting in front of this dashboard, and what decision are they trying to make? That changes everything — a sales manager needs different visual hierarchy than a DevOps engineer."

### Step 1b: Identify Product Type and Context

From the user's answers, classify:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, admin panel, landing page, blog, mobile app
- **Industry**: healthcare, fintech, gaming, education, beauty, etc.
- **Emotional tone**: 3-5 adjective keywords (e.g., "trustworthy, dense, efficient")
- **Tech stack**: React, Next.js, Vue, Svelte, or default to html-tailwind
- **Target device**: mobile-first, desktop-first, or responsive-equal

**Lucy confirms understanding before proceeding:**

> "So we're building a [product type] for [specific user persona] in [industry]. The core action is [action]. It should feel [emotional tone]. Stack is [stack]. I'm going to start with the design system, then mockup, then components. Sound right?"

**Do not proceed without confirmation.**

---

## Phase 2: Design System (UI/UX Pro Max — ALWAYS FIRST)

**Goal:** Establish the design system before any visual work. Design decisions drive the mockup, not the other way around.

### Step 2a: Generate Design System

Run the UI/UX Pro Max design system generator with the classified keywords:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <emotional_keywords>" --design-system -p "<Project Name>"
```

**Example:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "fintech dashboard professional dense trustworthy" --design-system -p "TradingView Clone"
```

This returns: recommended pattern, style, color palette, typography pairing, effects, and anti-patterns.

### Step 2b: Challenge and Refine

**Do not blindly accept the first result.** Lucy evaluates:

- Does the recommended style match the emotional tone from Phase 1?
- Does the color palette work for the target industry? (Healthcare shouldn't look like a gaming app)
- Does the typography support the information density needed?
- Are there anti-patterns flagged that conflict with the user's vision?

**If something doesn't fit, run supplemental searches:**

```bash
# Alternative styles
python3 skills/ui-ux-pro-max/scripts/search.py "alternative keywords" --domain style

# Alternative typography
python3 skills/ui-ux-pro-max/scripts/search.py "elegant professional serif" --domain typography

# Color alternatives for the industry
python3 skills/ui-ux-pro-max/scripts/search.py "fintech trustworthy" --domain color
```

**Present 2-3 options with reasoning, not just one:**

> "The design system generator recommends **Neo-Brutalism** for this product type, but I disagree for your use case. Here's why, and here are three alternatives:
>
> **Option A: Data-Dense Minimal** — Clean grids, monospace numbers, subtle borders. Best for your 'efficient, dense' requirements. Risk: can feel cold.
> **Option B: Soft Corporate** — Rounded corners, warm neutrals, clear hierarchy. Best for the 'trustworthy' requirement. Risk: can feel generic.
> **Option C: Dark Professional** — Dark backgrounds, high-contrast data, accent colors for alerts. Best for the 'Bloomberg-like' reference. Risk: harder to get accessibility right.
>
> I'd push for Option A with warm accent colors from Option B. What resonates?"

### Step 2c: Lock Design System and Persist

Once the user approves, persist the design system:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<approved keywords>" --design-system --persist -p "<Project Name>"
```

Then get stack-specific implementation guidelines:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<relevant keywords>" --stack <chosen-stack>
```

**Output:** `design-system/MASTER.md` with all tokens, rules, and anti-patterns locked in.

---

## Phase 3: Mockup Generation (Stitch)

**Goal:** Generate a high-fidelity visual reference that follows the locked design system.

**Skip condition:** If Stitch MCP tools are not connected (added mid-session, proxy not running, or auth expired), skip to Phase 4. Document this in the output.

### Stitch MCP Tool Reference

The Stitch MCP exposes these tools (prefixed `mcp__stitch__` in Claude Code):

| Tool | Purpose | Key Parameters |
|------|---------|---------------|
| `create_project` | Create a new Stitch project container | `title` (string) |
| `generate_screen_from_text` | **Primary tool** — Generate a screen from a text prompt | `projectId`, `prompt`, `screenId` (optional) |
| `edit_screens` | Edit existing screens with a text prompt | `projectId`, `prompt`, `screenIds` |
| `generate_variants` | Generate alternative versions of a screen | `projectId`, `prompt`, `screenIds` |
| `get_screen_code` | Retrieve the generated HTML/CSS code | `projectId`, `screenId` |
| `get_screen_image` | Retrieve screenshot as base64 image | `projectId`, `screenId` |
| `list_projects` | List all Stitch projects | — |
| `list_screens` | List screens in a project | `projectId` |
| `build_site` | Map screens to routes for a full site | `projectId`, `routes[]` |

**Important:** `generate_screen_from_text` can take several minutes. Do NOT retry on timeout — the generation may still succeed. Use `get_screen` to check later.

### Step 3a: Create Project and Craft the Prompt

First, create a Stitch project:
```
mcp__stitch__create_project({ title: "<Project Name>" })
```

Then craft a detailed prompt for screen generation. Don't just pass the user's original description — include the locked design system:

```
mcp__stitch__generate_screen_from_text({
  projectId: "<from create_project>",
  prompt: "Generate a [screen name] for a [product type].
    Style: [locked style from MASTER.md]
    Colors: primary #0F172A, secondary #334155, accent #CA8A04 (minimal use — CTA buttons only), background #F8FAFC
    Typography: Lexend headings, Source Sans 3 body
    Layout: [layout pattern from MASTER.md]
    Core action: [the one thing from Phase 1]
    User context: [who is using this and how]
    Key elements: [specific UI elements needed]"
})
```

### Step 3b: Retrieve and Critique

After generation completes, retrieve both the image and code:

```
mcp__stitch__get_screen_image({ projectId, screenId })
mcp__stitch__get_screen_code({ projectId, screenId })
```

**Critique the output yourself before showing the user:**

- Does it match the locked design system?
- Is the visual hierarchy clear — does the core action stand out?
- Are there elements that look generic or don't serve the user's goal?
- Would the target user persona actually find this intuitive?

**If the mockup doesn't match, use `edit_screens` to refine or `generate_variants` for alternatives. Don't show the user a bad mockup and ask them to fix it.**

### Step 3c: Present with Opinion

Show the mockup image with commentary:

> "Here's the mockup. Three things I like and one thing I'd change:
>
> **Good:** [specific element] creates strong visual hierarchy for the core action.
> **Good:** [specific element] matches the [emotional tone] we discussed.
> **Good:** [specific element] follows [industry] conventions users will expect.
> **Change:** [specific element] feels generic — I'd replace it with [alternative] because [reasoning].
>
> Want to iterate on this, or is this direction approved?"

**Iterate until approved. Do not proceed with a mockup the user hasn't endorsed.**

---

## Phase 4: Component Decomposition and Generation (21st.dev Magic)

**Goal:** Build polished, reactive components that implement the mockup using the locked design system.

**Skip condition:** If 21st.dev Magic MCP is not connected (added mid-session), use the `frontend-design` plugin skill + design system MASTER.md to generate components manually. Document this in the output.

### 21st.dev Magic MCP Tool Reference

The 21st.dev Magic MCP exposes these tools (prefixed `mcp__magic__` in Claude Code):

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `21st_magic_component_builder` | **Primary tool** — Generate a new UI component from description | Creating each decomposed component |
| `21st_magic_component_inspiration` | Browse existing components for reference/inspiration | Before generating, to find similar components as starting points |
| `21st_magic_component_refiner` | Redesign/improve an existing component | After initial generation, to polish or fix issues |
| `logo_search` | Find brand logos in JSX/TSX/SVG format | When components need company logos or brand assets |

#### `21st_magic_component_builder` — Primary Generation Tool

```
mcp__magic__21st_magic_component_builder({
  message: "<full context of what's needed>",
  searchQuery: "<2-4 word component search, e.g. 'client card grid'>",
  absolutePathToCurrentFile: "<path to file being edited>",
  absolutePathToProjectDirectory: "<project root>",
  standaloneRequestQuery: "<specific component description with design context>"
})
```

**The `standaloneRequestQuery` is where you embed the design system.** Include:
- Component purpose and content
- Color palette from MASTER.md
- Typography from MASTER.md
- Specific interaction states needed
- Accessibility requirements

**Example:**
```
standaloneRequestQuery: "Create a client card component for a coaching platform.
  Navy (#0F172A) text, slate (#334155) secondary text, gold (#CA8A04) accent on status badge only.
  Background #F8FAFC with subtle shadow. Lexend font for name, Source Sans 3 for details.
  Card shows: client name, role, industry, last briefing date, status badge (Ready/In Progress/Delivered).
  Hover: translateY(-2px) with shadow-lg. cursor-pointer. 12px border-radius."
```

#### `21st_magic_component_inspiration` — Browse Before Building

```
mcp__magic__21st_magic_component_inspiration({
  message: "<what you're looking for>",
  searchQuery: "<2-4 word search, e.g. 'dashboard card grid'>"
})
```

Use this BEFORE generating to see what existing components look like. Helps avoid generating from scratch when a good starting point exists.

#### `21st_magic_component_refiner` — Polish After Generation

```
mcp__magic__21st_magic_component_refiner({
  userMessage: "<what to improve>",
  absolutePathToRefiningFile: "<path to the component file>",
  context: "<specific UI elements and aspects to improve>"
})
```

Use this AFTER initial generation to fix specific issues — spacing, hover states, responsive behavior, accessibility gaps.

#### `logo_search` — Brand Assets

```
mcp__magic__logo_search({
  queries: ["company-name"],
  format: "TSX"  // or "JSX" or "SVG"
})
```

Use when components need professional brand logos (e.g., client company logos in the roster).

### Step 4a: Decompose with Reasoning

Break the approved mockup into components, but explain the decomposition:

> "I'm breaking this into [N] components. Here's my thinking:
>
> 1. **[Component name]** — [why this is a separate component, not just part of the page]
> 2. **[Component name]** — [what interaction states it needs]
> ...
>
> Any components I'm missing? Anything that should be split differently?"

### Step 4b: Inspiration Search (Optional but Recommended)

Before generating, search for similar components:

```
mcp__magic__21st_magic_component_inspiration({
  message: "Looking for [component type] components for a professional dashboard",
  searchQuery: "[2-4 word search]"
})
```

This surfaces existing components that may be close to what's needed — faster than generating from scratch.

### Step 4c: Generate Each Component

For each component, call the builder with full design system context in `standaloneRequestQuery`.

**One component per request. Complex components (e.g., a data table with sorting, filtering, pagination) should be called out:**

> "This data table component is complex — 21st.dev works best with focused components. I'm going to generate the table shell, sort controls, filter bar, and pagination as separate pieces and compose them. This gives better results than asking for everything at once."

### Step 4d: Refine if Needed

If a generated component is close but not right, use the refiner:

```
mcp__magic__21st_magic_component_refiner({
  userMessage: "Improve the hover state and fix the spacing on the status badge",
  absolutePathToRefiningFile: "<path to component>",
  context: "The card hover effect is too aggressive (scale instead of translateY). Status badge needs gold (#CA8A04) background with white text. Padding between name and role is too tight."
})
```

### Step 4c: Validate Each Component

After generation, run each component through UI/UX Pro Max checks:

**Priority 1 — Accessibility:**
- Color contrast 4.5:1 (check with the locked palette)
- Focus states on all interactive elements
- ARIA labels on icon-only buttons
- Touch targets 44x44px minimum

**Priority 2 — Interaction:**
- Loading/disabled states for async actions
- Error feedback near the problem
- cursor-pointer on clickable elements

**Priority 5 — Typography:**
- Font sizes match locked design system
- Line heights 1.5-1.75 for body text
- Line length 65-75 characters

**Fix violations before presenting. Don't deliver inaccessible components.**

---

## Phase 5: Assembly and Verification

**Goal:** Compose the final page from components and verify it meets the brief.

### Step 5a: Layout Composition

Assemble components into the page layout matching the approved mockup. Reference the Stitch output for spatial arrangement.

### Step 5b: Responsive Verification

Check at:
- Mobile (375px)
- Tablet (768px)
- Desktop (1280px)
- Wide (1440px)

Use UI/UX Pro Max responsive guidelines. **Flag any breakpoint where the core action is not immediately visible:**

> "On mobile, the [core action] is pushed below the fold by [element]. I'm moving [element] into a collapsible section so the core action is visible on load."

### Step 5c: Full Accessibility Audit

Run the complete UI/UX Pro Max pre-delivery checklist (from the skill's "Pre-Delivery Checklist" section). Every item must pass.

### Step 5d: Persist Page-Specific Overrides (if needed)

If this page deviates from the master design system:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<page-specific keywords>" --design-system --persist -p "<Project Name>" --page "<page-name>"
```

### Step 5e: Present Final Result

Use Browser/Playwright to screenshot the assembled page. Present with a summary:

> "Here's the final [page name]:
>
> **Design system:** [style name] / [palette name] / [font pairing]
> **Components:** [N] generated via 21st.dev Magic
> **Accessibility:** All priority 1-2 checks passing
> **Responsive:** Verified at 375px, 768px, 1280px, 1440px
> **Core action:** [action] is above the fold on all breakpoints
>
> Design system persisted to `design-system/MASTER.md` for consistency across future pages."

---

## What This Workflow Does NOT Do

- Accept "make it look nice" as a brief
- Show the user a bad mockup and ask them to fix it
- Generate components without validating accessibility
- Proceed without explicit approval at each phase gate
- Use default/generic design choices when the design system recommends something specific
