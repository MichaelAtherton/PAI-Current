# Workflow: Build a Pipeline

Use this workflow when the user wants to move from idea to implementation — actually building a CLI-Anything pipeline.

## Prerequisites

Before entering this workflow, ensure you've loaded:
- `references/TechnicalFoundation.md` (architecture patterns, harness structure)
- `references/ActionableRoadmap.md` (if implementing a ranked idea)

## Process

### 1. Define the Pipeline

Specify the exact chain of software tools and their roles:
```
Input → [Tool A: action] → [Tool B: action] → [Tool C: action] → Output
```

For each tool in the chain, identify:
- **Does a CLI-Anything harness already exist?** Check the 11 existing harnesses (GIMP, Blender, Inkscape, Audacity, LibreOffice, OBS, Kdenlive, Shotcut, Zoom, Draw.io, AnyGen)
- **Does the tool need a new harness?** If yes, you'll need to run `/cli-anything <path-or-repo>` for that software
- **What's the input/output format at each stage?** JSON handoff between stages is the pattern.

### 2. Generate Missing Harnesses

For each tool that needs a new harness:

1. **Find the source code** — Clone or locate the software's source repo
2. **Run the pipeline**: `/cli-anything <path-to-source>`
3. **Validate**: `/cli-anything:validate <path>` to check against HARNESS.md standards
4. **Refine if needed**: `/cli-anything:refine <path> [focus-area]`
5. **Test**: `/cli-anything:test <path>`

### 3. Design the Orchestration Layer

The pipeline needs an orchestrator. Options:

**Simple (shell script):**
```bash
cli_anything_gimp resize --input photo.jpg --width 1920 --json | \
cli_anything_inkscape overlay --template brand.svg --json | \
cli_anything_libreoffice insert --doc report.docx --page 3
```

**Medium (Python script):**
A Python script that calls each CLI via subprocess, handles errors, and manages intermediate files.

**Advanced (MCP + PAI Agents):**
Each tool wrapped as an MCP capability. PAI agents orchestrate. Use the **Agents** skill to compose specialized agents for each stage. Use **Delegation** (TeamCreate) for complex multi-agent coordination.

### 4. Handle the Handoff Pattern

Each stage must:
1. Accept input (file path or JSON from stdin)
2. Process using the CLI-Anything harness
3. Output JSON with the result path and metadata
4. Pass to the next stage

The `--json` flag on every CLI-Anything command is what makes this work. Every command returns structured JSON that the next command can consume.

### 5. Add Quality Gates

Between pipeline stages, add checks:
- **File existence**: Did the previous stage actually produce output?
- **Format validation**: Is the output in the expected format?
- **Quality check**: For images, check dimensions/resolution. For audio, check RMS levels. For documents, check page count.
- **Human review point**: For creative pipelines, insert a "human approves" gate at the most judgment-sensitive stage.

### 6. Test the Full Pipeline

1. Run with a single test input end-to-end
2. Check output quality at each stage
3. Identify bottlenecks (which stage is slowest?)
4. Test error handling (what happens if a middle stage fails?)

### 7. Scale (Optional)

Once the pipeline works for 1 input:
- **Batch mode**: Process N inputs in sequence
- **Parallel mode**: Use PAI's agent swarm capabilities to run N instances in parallel
- **Scheduled mode**: Set up a cron or file-watcher trigger

## Routing to Other Skills

| Need | Skill |
|---|---|
| Compose specialized agents for pipeline stages | **Agents** |
| Create agent teams for complex orchestration | **Delegation** (via TeamCreate) |
| Research a tool's capabilities before building | **Research** |
| Debug a failing pipeline stage | **Thinking/Science** (hypothesis testing) |
