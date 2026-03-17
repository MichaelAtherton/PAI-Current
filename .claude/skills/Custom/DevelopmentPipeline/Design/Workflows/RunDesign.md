# RunDesign — Phases 1, 2, and 3

Thin wrapper that routes to claude-code-design-stack's FullDesign workflow, skipping its Discovery phase (already completed in the Discovery container). Produces all Design deliverables needed for the Scaffold and Specify phases.

---

## Prerequisites (Cold-Start Files)

Before starting, read and verify these files exist:

| File | What to check |
|------|---------------|
| `docs/specs/users/[persona-name].md` | Named persona with JTBD, anxieties, mental models |
| `docs/specs/ux/[feature-name]-ux.md` | Level 3 interaction spec (behavior only, no visual) |

If these files don't exist, Discovery hasn't been completed. Route to `Discovery/Workflows/RunDiscovery.md` first.

## Execution

### Phase 1: Design System Generation

**Route to:** `.claude/skills/Custom/claude-code-design-stack/Workflows/FullDesign.md` — Phase 2 (skip Phase 1 Discovery).

The design stack's Discovery phase is NOT re-run. Instead:

1. Read the persona file and UX spec
2. Extract: product type, industry, emotional tone, target device
3. Run UI/UX Pro Max to generate design system:
   ```bash
   python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <emotional_keywords>" --design-system -p "<Project Name>"
   ```
4. Evaluate result against emotional tone from Phase 0b
5. Present 2-3 options with reasoning
6. After approval, persist:
   ```bash
   python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<approved keywords>" --design-system --persist -p "<Project Name>"
   ```

**Output:** `design-system/MASTER.md` — locked design tokens

### Phase 2: Mockup Generation

Continue following FullDesign.md Phase 3:

1. Create Stitch project via `mcp__stitch__create_project`
2. Craft prompt from MASTER.md + UX spec
3. Generate via `mcp__stitch__generate_screen_from_text`
4. Critique before showing user — does it match design system? Is core action prominent?
5. Iterate with `mcp__stitch__edit_screens` or `mcp__stitch__generate_variants` if needed
6. Present with opinion: 3 things that work, 1 thing to change

**Skip condition:** If Stitch MCP is not connected, skip to Phase 3. Document the skip. UX spec + MASTER.md are sufficient.

**Output:** `design/mockups/[screen-name].png` + `.html` — approved mockup screens

### Phase 3: Component Generation

Continue following FullDesign.md Phase 4:

1. Decompose mockup into components with reasoning
2. Search for inspiration via `mcp__magic__21st_magic_component_inspiration`
3. Generate each component via `mcp__magic__21st_magic_component_builder` with MASTER.md tokens in `standaloneRequestQuery`
4. Validate against UI/UX Pro Max checks (contrast, focus states, touch targets, transitions, ARIA)
5. Fix violations via `mcp__magic__21st_magic_component_refiner`

**Skip condition:** If 21st.dev Magic MCP not connected, use `frontend-design` plugin with MASTER.md tokens.

**Output:** `design/reference/[component-name].html` — polished HTML/JS prototypes

## Deliverable Checklist

Before declaring Design complete, verify ALL of these exist:

- [ ] `design-system/MASTER.md` — locked design tokens (palette, typography, spacing, effects)
- [ ] `design/mockups/[screen-name].png` + `.html` — approved mockup(s) (or documented skip)
- [ ] `design/reference/[component-name].html` — HTML/JS component prototypes
- [ ] User has approved the assembled design

## Session Boundary

Design is complete. Its deliverables are at the file paths listed above.

**If context is heavy** (4+ refine loops, heavy MCP usage), start a new session and resume at Phase 4 (Tech Stack Decision) by reading:
- `design-system/MASTER.md`
- `design/mockups/` directory
- `design/reference/` directory
- Plus the Discovery files (personas, UX specs)

**If context is light**, continue to the orchestrator for Phases 4-5-5b (Scaffold).
