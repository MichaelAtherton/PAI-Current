---
name: DevelopmentPipeline
description: Unified 14-phase development pipeline from raw idea to deployed MVP. Chains AgentBuild, claude-code-design-stack, and WebDesign through discovery, visual design, specification, implementation, and deployment. USE WHEN development pipeline, full pipeline, idea to MVP, end to end build, complete build process, discovery to deployment, design and build, pipeline build, run the pipeline, start pipeline.
---

# DevelopmentPipeline

Unified orchestration pipeline that takes a raw product idea through 14 phases — discovery, visual design, specification, implementation, and deployment — to a live Railway URL.

**Architecture:** 4 containerized zones (Discovery, Design, Specify, Build) where context saturation occurs, plus inline orchestration for mechanical phases (Scaffold, Ship).

**Source of truth:** `output/DevelopmentPipeline/PIPELINE.md`

## Customization

**Before executing, check for user customizations at:**
`.claude/PAI/USER/SKILLCUSTOMIZATIONS/DevelopmentPipeline/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Starting the Development Pipeline — idea to deployed MVP"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **DevelopmentPipeline** skill — orchestrating the full idea-to-MVP pipeline...
   ```

## Active Project Check (Before Routing)

Before routing, check for active AgentBuild projects:

1. Read all `PID-*.json` files in `.claude/skills/Custom/AgentBuild/projects/`
2. Filter to `status: "active"` projects
3. If an active project exists with `currentPhase` in a pipeline phase → offer to resume
4. If no active project → route to workflow below

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **FullPipeline** | "full pipeline", "idea to MVP", "end to end", "run the pipeline" | `Workflows/FullPipeline.md` |
| **RunDiscovery** | "discovery", "refine idea", "explore idea", "who is the user" | `Discovery/Workflows/RunDiscovery.md` |
| **RunDesign** | "design system", "mockups", "components", "visual design" | `Design/Workflows/RunDesign.md` |
| **RunSpecify** | "edge cases", "specifications", "spec hardening", "knowledge capture" | `Specify/Workflows/RunSpecify.md` |
| **RunBuild** | "build loop", "build features", "implement specs", "start building" | `Build/Workflows/RunBuild.md` |

**Individual phase triggers** — route directly to the source skill workflow:

| User Says | Route To |
|-----------|----------|
| "phase 0", "orientation" | `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 0 |
| "tech stack", "environment bootstrap" | `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 1 |
| "build task", "next feature" | `.claude/skills/Custom/AgentBuild/Workflows/BuildLoop.md` |
| "error recovery" | `.claude/skills/Custom/AgentBuild/Workflows/ErrorRecovery.md` |
| "MVP gate", "are we ready" | `.claude/skills/Custom/AgentBuild/Workflows/MvpGate.md` |
| "deploy", "railway" | `.claude/skills/Custom/AgentBuild/Modules/DeployRailway.md` |
| "measure success" | `.claude/skills/Custom/AgentBuild/Workflows/MeasureSuccess.md` |
| "retrospective" | `.claude/skills/Custom/AgentBuild/Workflows/BuildRetrospective.md` |
| "design audit" | `.claude/skills/Custom/claude-code-design-stack/Workflows/DesignAudit.md` |
| "quick component" | `.claude/skills/Custom/claude-code-design-stack/Workflows/QuickComponent.md` |

## Examples

**Example 1: Full pipeline from scratch**
```
User: "I have an idea for a habit tracker — run the full pipeline"
→ Invokes FullPipeline workflow
→ Starts at Phase 0 (Orientation) in Discovery container
→ Progresses through all 14 phases with session boundaries at each container handoff
→ Ends with a live Railway URL and retrospective
```

**Example 2: Just the design phases**
```
User: "I have personas and UX specs already — design this"
→ Invokes RunDesign workflow
→ Cold-starts from existing persona/UX files
→ Produces design-system/MASTER.md, mockups, and validated components
```

**Example 3: Resume mid-pipeline**
```
User: "Continue the pipeline — design is done, ready to specify"
→ Detects active project, reads currentPhase from PID registry
→ Routes to RunSpecify or FullPipeline at the appropriate phase
```

## Architecture

```
DevelopmentPipeline/          ← Parent skill (router + orchestrator)
├── SKILL.md                  ← This file
├── Workflows/
│   └── FullPipeline.md       ← Sequential conductor
├── Discovery/                ← Child: Phases 0, 0b
│   ├── SKILL.md
│   └── Workflows/
│       └── RunDiscovery.md
├── Design/                   ← Child: Phases 1, 2, 3
│   ├── SKILL.md
│   └── Workflows/
│       └── RunDesign.md
├── Specify/                  ← Child: Phases 6, 7
│   ├── SKILL.md
│   └── Workflows/
│       └── RunSpecify.md
├── Build/                    ← Child: Phases 8, 8e
│   ├── SKILL.md
│   └── Workflows/
│       └── RunBuild.md
└── Tools/                    ← Empty (orchestration only)
```

## Key Reference

- **Pipeline specification:** `output/DevelopmentPipeline/PIPELINE.md`
- **AgentBuild skill:** `.claude/skills/Custom/AgentBuild/SKILL.md`
- **Design stack:** `.claude/skills/Custom/claude-code-design-stack/SKILL.md`
- **WebDesign:** `.claude/skills/WebDesign/SKILL.md`
- **Ralph Wiggum:** `.claude/skills/ralph-wiggum/README.md`
