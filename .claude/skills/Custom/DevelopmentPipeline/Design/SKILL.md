---
name: Design
description: Design container for the DevelopmentPipeline — design system generation, mockup creation, and component generation (Phases 1, 2, 3). Produces MASTER.md, mockup screens, and validated HTML/JS components. USE WHEN design system, mockups, components, visual design, pipeline design, design generation, create design, full design.
---

# Design

**Pipeline container: Phases 1, 2, and 3**

Takes persona files and UX specs from Discovery and produces a complete visual design: design system tokens (MASTER.md), mockup screens, and polished HTML/JS component files. This is a high-iteration zone with heavy MCP tool usage (Stitch, 21st.dev Magic).

## Customization

**Before executing, check for user customizations at:**
`.claude/PAI/USER/SKILLCUSTOMIZATIONS/DevelopmentPipeline/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Starting Design — design system, mockups, and components"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **RunDesign** workflow in the **DevelopmentPipeline** skill — generating visual design...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **RunDesign** | "design system", "mockups", "components", "visual design", "full design" | `Workflows/RunDesign.md` |

## Cold-Start Input Spec

This container can be invoked standalone. It needs:

| Required File | Source |
|---------------|--------|
| `docs/specs/users/[persona-name].md` | Discovery output |
| `docs/specs/ux/[feature-name]-ux.md` | Discovery output |
| Orientation sentences (what + done) | Discovery output (or provided directly) |

## Deliverables (Cold-Start Contract)

When Design completes, these files MUST exist:

| Artifact | File Path | Content |
|----------|-----------|---------|
| Design system | `design-system/MASTER.md` | Locked design tokens: palette, typography, spacing, effects |
| Mockup screens | `design/mockups/[screen-name].png` + `.html` | Approved visual reference |
| Component files | `design/reference/[component-name].html` | HTML/JS prototypes (visual reference, not production code) |
| Pipeline state | `projects/PID-{hex}.json` → `currentPhase: "scaffold"` | Phase tracking |

**Cold-start test:** A fresh session with ONLY these files + persona/UX files + `output/DevelopmentPipeline/PIPELINE.md` can execute Phase 4 (Tech Stack Decision).

**Note:** Phase 5b (component validation) runs in the orchestrator AFTER Phase 4 (tech stack) because validation rules are framework-specific.

## Examples

**Example 1: Full design from Discovery output**
```
User: "Discovery is done — design this"
→ Reads persona and UX spec files
→ Phase 1: Generates design system via UI/UX Pro Max → MASTER.md
→ Phase 2: Creates mockups via Stitch MCP
→ Phase 3: Generates components via 21st.dev Magic
→ All deliverables saved to documented paths
```

**Example 2: Standalone with existing specs**
```
User: "I have user personas and UX specs — create a design system and components"
→ Cold-starts from existing files
→ Runs all three design phases
→ Outputs ready for Scaffold phase
```

## Source Workflows

- Phases 1-3: `.claude/skills/Custom/claude-code-design-stack/Workflows/FullDesign.md` (skip Phase 1 Discovery — already done)
- Mockup skip fallback: UX spec + MASTER.md sufficient if Stitch MCP unavailable
- Component skip fallback: `frontend-design` plugin if 21st.dev Magic unavailable
