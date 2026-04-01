# Phase 2 — Parallel Extraction

**Input:** `output/repo-context/.manifest.json` from Phase 1  
**Agent:** `codebase-intel-extractor` (defined in `agents/extractor.md`) — one instance per subsystem  
**Output:** 
- One `{subsystem-name}.md` per subsystem in `output/repo-context/`
- Completed `output/repo-context/CONTEXT.md` (subsystem index + cross-cutting concerns filled in)

For monorepo packages: all paths are under `output/repo-context/<package-name>/`.

## Step 1: Read the manifest

Determine the manifest path based on repo type from Phase 0:
- **Single repo:** `output/repo-context/.manifest.json`
- **Monorepo package:** `output/repo-context/<package-name>/.manifest.json` (where `<package-name>` is the package name passed from Phase 0)

Read the manifest file at the correct path. Extract the `subsystems` array. All output paths in subsequent steps use the same base directory as the manifest (i.e., `output/repo-context/` for single repo, `output/repo-context/<package-name>/` for monorepo packages).

## Step 2: Spawn parallel extractor agents

For each subsystem in the manifest, spawn one `codebase-intel-extractor` agent using `run_in_background: true`. Pass the agent:

```
subsystem: <subsystem.name>
root_files: <subsystem.root_files>
is_cross_cutting: <subsystem.is_cross_cutting>
manifest: <full manifest JSON — paste entire contents>
output_path: output/repo-context/<subsystem.name>.md
agent_instructions: <paste full contents of agents/extractor.md>
```

Spawn ALL agents before waiting for any to complete. Do not wait for one agent to finish before spawning the next.

## Step 3: Wait for all agents to complete

Monitor all background agents. Do not proceed until every agent has written its output file. If an agent fails or produces no output after a reasonable wait, report the failure to the developer and continue with the remaining subsystems.

## Step 4: Complete CONTEXT.md

After all extractor agents complete, update `output/repo-context/CONTEXT.md`:

**Fill in the subsystem index table:**
For each subsystem file that was successfully written, add a row:
```
| <subsystem-name>.md | <subsystem.inferred_responsibility> | <subsystem.read_when from the written file's frontmatter> |
```

**Fill in the cross-cutting concerns section:**
For each subsystem where `is_cross_cutting: true`, read its written file and extract the `## Cross-cutting injection points` section. Summarize these into the CONTEXT.md `## Cross-cutting concerns` section with file:line references.

## Step 5: Clean up

Delete `output/repo-context/.manifest.json`. This is a working artifact — it should not be committed.

```bash
rm output/repo-context/.manifest.json
```

## Step 6: Report to developer

After CONTEXT.md is finalized and manifest is deleted, report:

1. **Generated:** N subsystem files + CONTEXT.md
2. **Subsystems found:** [list subsystem names]
3. **Output path:** `output/repo-context/`
4. **How to use:** "Load `output/repo-context/CONTEXT.md` at the start of any implementation session. The index will tell you which subsystem files to load for your current task."
5. **Next step:** "Commit the output: `git add output/repo-context/ && git commit -m 'chore: add codebase-intel context pack'`"

## What Phase 2 does NOT do

- Does not modify any source files in the repo
- Does not run Phase 0 or Phase 1
- Does not make decisions about subsystem boundaries — those were fixed in Phase 1
- Does not wait for one extractor to finish before spawning others
