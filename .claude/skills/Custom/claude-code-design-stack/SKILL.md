---
name: claude-code-design-stack
description: "Consultative three-tool design system — Google Stitch MCP (mockups), UI/UX Pro Max (design intelligence + CLI), 21st.dev Magic (components). Drives discovery, challenges weak briefs, makes opinionated recommendations. Workflows: full design (discovery->system->mockup->components), quick component (generate+validate), design audit (critique+fix existing UI). USE WHEN design workflow, full design, mockup first, design stack, design audit, improve UI, upgrade design, new landing page, new dashboard, polished components, design system, visual quality, make it look better, UI review, redesign."
user_invocable: false
---

# Claude Code Design Stack

Consultative three-tool design system that drives discovery, challenges weak design briefs, and produces polished output. Each tool handles a different layer: design intelligence -> mockup -> components.

**This is not a passive tool set.** The workflows push back on vague requests, present options with tradeoffs, and validate accessibility before delivery.

## Important: MCP Session Requirement

MCP servers must be connected **before** starting a Claude Code session. Tools from MCPs added mid-session won't be available until restart. Always verify Stitch and 21st.dev Magic are connected before beginning a design workflow.

## Tools (All Installed)

### UI/UX Pro Max — Design Intelligence (Project Skill)

CLI-based, always available. No MCP dependency.

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system -p "<Project>"  # Generate design system
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "<Project>"  # Persist to MASTER.md
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <style|color|typography|chart|ux|landing>  # Domain search
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --stack <nextjs|react|vue|svelte|html-tailwind>  # Stack guidelines
```

### Google Stitch MCP — Mockup Generation (Project MCP)

**Requires proxy running:** `npx @_davideast/stitch-mcp proxy`

| MCP Tool | Purpose |
|----------|---------|
| `mcp__stitch__create_project` | Create a new Stitch project container |
| `mcp__stitch__generate_screen_from_text` | **Primary** — Generate UI screen from text prompt (may take minutes, do NOT retry) |
| `mcp__stitch__edit_screens` | Edit existing screens with text prompt |
| `mcp__stitch__generate_variants` | Generate alternative versions of a screen |
| `mcp__stitch__get_screen_code` | Retrieve generated HTML/CSS code |
| `mcp__stitch__get_screen_image` | Retrieve screenshot as base64 image |
| `mcp__stitch__list_projects` | List all Stitch projects |
| `mcp__stitch__list_screens` | List screens in a project |
| `mcp__stitch__build_site` | Map screens to routes for a full site |

### 21st.dev Magic — Component Library (User MCP)

Always available at user scope. No proxy needed.

| MCP Tool | Purpose | When |
|----------|---------|------|
| `mcp__magic__21st_magic_component_inspiration` | Browse existing components for reference | Before generating — find starting points |
| `mcp__magic__21st_magic_component_builder` | **Primary** — Generate a new component from description | Creating each component. Embed design tokens in `standaloneRequestQuery` |
| `mcp__magic__21st_magic_component_refiner` | Redesign/polish an existing component | After generation — fix spacing, hover states, accessibility |
| `mcp__magic__logo_search` | Find brand logos in JSX/TSX/SVG | When components need company logos |

**Key parameter:** `standaloneRequestQuery` in the builder tool is where you embed the full design system context — colors, fonts, spacing, interaction states from MASTER.md.

## Workflows

### Full Design — `Workflows/FullDesign.md`
Consultative end-to-end process. Starts with discovery (who, what, why) before touching any tool. Challenges vague briefs. Generates design system first (UI/UX Pro Max), then mockup (Stitch), then components (21st.dev Magic). Presents options with reasoning at each phase. Validates accessibility before delivery.

### Quick Component — `Workflows/QuickComponent.md`
Fast path for a single component. Checks for existing design system. Pushes back on under-specified requests ("a card component" is not a spec). Generates via 21st.dev, validates against UI/UX Pro Max rules, fixes violations before presenting.

### Design Audit — `Workflows/DesignAudit.md`
Honest critique of existing UI. Extracts current patterns via Stitch, runs full audit against UI/UX Pro Max rules (accessibility, visual quality, consistency). Delivers a scored report with prioritized fixes. Generates replacement components via 21st.dev. Before/after screenshots required.

## Core Principles

1. **Design system before mockup.** The design system drives the mockup, not the other way around. Always run UI/UX Pro Max first.
2. **Push back on vague briefs.** "Make it look modern and clean" is not a design brief. Extract the user, the action, and the emotional tone.
3. **Present options with tradeoffs.** Never present one recommendation without alternatives and reasoning.
4. **Validate before delivery.** Every component passes accessibility and interaction checks. Don't deliver broken work.
5. **Persist design decisions.** Use `--persist` to save the design system so future pages stay consistent.

## Sources

- [Google Stitch MCP](https://github.com/davideast/stitch-mcp)
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [21st.dev Magic MCP](https://mcp.harishgarg.com/use/21stdev-magic/mcp-server/with/claude-code)
- [Original TikTok by @jensheitmann_](https://www.tiktok.com/@jensheitmann_/video/7613073206722727198)
