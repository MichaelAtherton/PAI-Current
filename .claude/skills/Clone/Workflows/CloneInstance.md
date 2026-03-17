# Clone Instance Workflow

## When to Use
When the user says: "clone", "clone PAI", "new instance", "new identity", "create a copy", "duplicate PAI"

## In-Session Clone (Primary — runs inside Claude Code)

Execute these steps directly using Claude Code tools. Do NOT shell out to scripts.
Follow EVERY step. Do NOT skip steps. Each step exists because skipping it caused a bug.

---

### Step 1: Gather Inputs

Use `AskUserQuestion` with FOUR questions:

1. **Directory name** — "What should the project directory be named?" (text input)
2. **DA identity name** — "What should the new DA be named?" (text input)
3. **Fresh start** — "Wipe memory for a clean slate?" (Yes / No, keep existing memory)
4. **API keys** — "Copy API keys to the clone?" (Yes — share keys / No — blank them out)

---

### Step 2: Resolve Paths

```
sourceRoot = <current project root>           (e.g., ~/Personal_AI_Infrastructure-v2+)
sourceDir  = sourceRoot/.claude               (PAI config directory)
projectDir = ~/<directory-name>               (ALWAYS in home directory)
destDir    = projectDir/.claude
```

**Rules:**
- Clones are ALWAYS placed in `~/`, NEVER inside the source project
- Verify sourceDir exists and has settings.json
- If projectDir already exists → ask to overwrite before proceeding
- Read sourceDir/settings.json to capture OLD DA name and OLD PAI_DIR for later replacement

---

### Step 3: Copy FULL Project

```bash
rsync -a \
  --exclude='node_modules' \
  --exclude='.fastembed_cache' \
  --exclude='output' \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='.playwright-mcp' \
  <sourceRoot>/ \
  ~/<directory-name>/
```

**CRITICAL: Copy the ENTIRE project, not just `.claude/`.** The clone must have:
- All skills, hooks, tools
- Package.json, bun.lock (for dependency install)
- README, LICENSE, docs
- Packs, images, releases
- Root-level .env, .env.example, .gitignore, .gitattributes

**Exclude:**
- `node_modules/` — reinstall fresh
- `.fastembed_cache/` — regenerated on demand
- `output/` — session-specific artifacts
- `.git/` — fresh repo (see Step 4)
- `.DS_Store` — macOS noise
- `.playwright-mcp/` — regenerated

The original is NEVER modified — read-only source.

---

### Step 4: Init Fresh Git + Install Dependencies

```bash
cd ~/<directory-name>
git init
bun install
bun add -d bun-types
```

The `bun add -d bun-types` ensures Node type declarations (`fs`, `path`, `process`) are available even if not yet in `package.json`. Without this, hooks will show IDE type errors.

Do NOT commit yet — commit AFTER all transforms are applied (Step 7).

---

### Step 5: Transform Identity and Paths

This is the most critical step. There are MULTIPLE files that contain identity and path references.

#### 5a: Read settings.json to discover current values

```
OLD_DA_NAME = settings.json → daidentity.name     (e.g., "Lucy")
OLD_PAI_DIR = settings.json → env.PAI_DIR          (e.g., "/Users/.../old/.claude")
OLD_PROJECT = parent directory of OLD_PAI_DIR       (e.g., "/Users/.../old")
NEW_DA_NAME = <user input>
NEW_PAI_DIR = ~/<directory-name>/.claude
NEW_PROJECT = ~/<directory-name>
```

#### 5b: Transform settings.json (JSON — use Edit tool)

- `env.PAI_DIR` → NEW_PAI_DIR
- `daidentity.name` → NEW_DA_NAME
- `daidentity.fullName` → "{NEW_DA_NAME} - Personal AI"
- `daidentity.displayName` → NEW_DA_NAME
- `daidentity.startupCatchphrase` → replace OLD_DA_NAME with NEW_DA_NAME
- `counts.*` → reset all to 0, `updatedAt` → ""

#### 5c: Transform .claude/.env (dotfile — use Edit tool)

- `DA=` → NEW_DA_NAME
- `PAI_DIR=` → NEW_PAI_DIR
- `PAI_SOURCE_APP=` → NEW_DA_NAME

#### 5d: Transform root .env (dotfile — use Edit tool)

- `PAI_DIR=` → `$HOME/<directory-name>/.claude`
- `DA=` → NEW_DA_NAME
- **API keys**: If user chose to blank them → replace each key value with `YOUR_KEY_HERE`
- **API keys**: If user chose to keep them → leave as-is but WARN that keys are shared

#### 5e: Bulk replace DA name in ALL text files

```bash
cd ~/<directory-name>/.claude
find . -type f \( -name "*.md" -o -name "*.ts" -o -name "*.sh" -o -name "*.json" -o -name "*.env" -o -name ".env" \) \
  -exec grep -l "OLD_DA_NAME" {} \; | while read f; do
  sed -i '' "s/OLD_DA_NAME/NEW_DA_NAME/g" "$f"
done
```

**CRITICAL: Include dotfiles.** The `.env` file has no extension — it WILL be missed by `*.env` glob.
Use both `-name "*.env"` AND `-name ".env"` patterns.

Also grep the root-level files:
```bash
cd ~/<directory-name>
find . -maxdepth 1 -type f -exec grep -l "OLD_DA_NAME" {} \; | while read f; do
  sed -i '' "s/OLD_DA_NAME/NEW_DA_NAME/g" "$f"
done
```

#### 5f: Replace old project path references

```bash
# In all config files, replace old project path with new
grep -rl "OLD_PROJECT" ~/<directory-name>/.claude/*.json ~/<directory-name>/.claude/.env ~/<directory-name>/.env 2>/dev/null
```

Fix any matches with Edit tool.

#### 5g: Rebuild CLAUDE.md from template

```bash
cd ~/<directory-name>
PAI_DIR=~/<directory-name>/.claude bun .claude/PAI/Tools/BuildCLAUDE.ts
```

This resolves template variables ({DAIDENTITY.NAME}, {PRINCIPAL.NAME}, etc.) with the clone's settings. Without this, CLAUDE.md may contain stale values from the source.

---

### Step 6: Memory Wipe (if fresh start requested)

**This step has three sub-steps. ALL are required.**

#### 6a: Delete ALL files AND symlinks

```bash
find ~/<directory-name>/.claude/MEMORY -mindepth 1 -not -type d -delete
```

**CRITICAL: Use `-not -type d`**, not `-type f`. Memory directories contain symlinks that `-type f` won't catch. This was a real bug.

#### 6b: Remove empty subdirectories

```bash
find ~/<directory-name>/.claude/MEMORY -mindepth 1 -type d -empty -delete
```

#### 6c: Recreate top-level structure

```bash
mkdir -p ~/<directory-name>/.claude/MEMORY/{LEARNING,RELATIONSHIP,RESEARCH,SECURITY,STATE,VOICE,WORK}
```

#### 6d: VERIFY zero files remain

```bash
find ~/<directory-name>/.claude/MEMORY -not -type d | wc -l
```

Must be 0. If not, repeat 6a-6c. Hooks running in the current session may write files between copy and wipe — this is expected. The wipe must come AFTER all other transforms.

---

### Step 7: Commit Initial State

```bash
cd ~/<directory-name>
git add -A
git commit -m "Initial clone from PAI vX.X — DA: <da-name> (fresh start)"
```

Commit AFTER all transforms so the first commit is clean.

---

### Step 8: Verify (COMPREHENSIVE)

This is not optional. Every sub-check must pass.

#### 8a: Root-level parity check

```bash
ls -1A <sourceRoot>/ | wc -l    # Source item count
ls -1A ~/<directory-name>/ | wc -l   # Clone item count
```

Difference should be exactly 3-4 (node_modules, .fastembed_cache, output, .git are excluded but node_modules is reinstalled and .git is fresh).

#### 8b: Identity verification (ZERO tolerance)

```bash
# Check ALL file types — no extension filter
grep -r "OLD_DA_NAME" ~/<directory-name>/.claude/settings.json \
  ~/<directory-name>/.claude/.env \
  ~/<directory-name>/.env 2>/dev/null
```

Must return ZERO matches. If any found → fix with Edit tool.

#### 8c: Path verification (ZERO tolerance)

```bash
grep -r "OLD_PROJECT" ~/<directory-name>/.claude/settings.json \
  ~/<directory-name>/.claude/.env \
  ~/<directory-name>/.env 2>/dev/null
```

Must return ZERO matches (the upstream `pai.repoUrl` referencing `github.com/danielmiessler/Personal_AI_Infrastructure` is EXPECTED and correct — it's the project URL, not a local path).

#### 8d: Memory verification (if fresh start)

```bash
find ~/<directory-name>/.claude/MEMORY -not -type d | wc -l
```

Must be 0.

#### 8e: Settings identity confirmation

```bash
python3 -c "
import json
d = json.load(open('~/<directory-name>/.claude/settings.json'.replace('~', '$HOME')))
print(f'DA: {d[\"daidentity\"][\"name\"]}')
print(f'PAI_DIR: {d[\"env\"][\"PAI_DIR\"]}')
print(f'Catchphrase: {d[\"daidentity\"][\"startupCatchphrase\"]}')
"
```

All must show NEW values.

#### 8f: API key audit (if keys were blanked)

```bash
grep -c "YOUR_KEY_HERE" ~/<directory-name>/.env
```

Should match the number of keys that were blanked.

---

### Step 9: Report

Summarize:
- Clone location: `~/<directory-name>/`
- DA identity: NEW_DA_NAME
- Fresh start: yes/no
- API keys: copied/blanked
- Root items: N (vs source N)
- Memory files: 0 (if fresh)
- Identity refs clean: yes/no
- Path refs clean: yes/no
- Git: initialized with N files
- How to launch: `cd ~/<directory-name> && claude`

---

## Known Gotchas (learned the hard way)

1. **`.env` is invisible to `*.ext` globs** — dotfiles with no extension need explicit `-name ".env"` patterns
2. **Symlinks survive `find -type f -delete`** — always use `-not -type d` to catch symlinks too
3. **Hooks write to memory during the session** — wipe memory LAST, after all other transforms
4. **`PAI_DIR` env var in shell profile may be stale** — scripts should prefer `cwd/.claude` over `$PAI_DIR`
5. **Root `.env` contains API keys** — always ask the user about key handling
6. **Clone must be in `~/`** — placing inside source project creates nesting issues
7. **Copy the FULL project** — `.claude/` alone is not a functional PAI instance; it needs package.json, tools, docs, etc.

---

## Terminal Clone (Alternative — standalone script)

For running outside a Claude Code session:

```bash
bun .claude/skills/Clone/Tools/Clone.ts
bun .claude/skills/Clone/Tools/Clone.ts --source /path/to/.claude
```

Note: Terminal scripts may not have all the fixes from this workflow. The in-session workflow is the authoritative implementation.

---

## Post-Clone

After cloning, the user launches the new instance:
```bash
cd ~/<directory-name> && claude
```

The new DA identity will greet them on first launch.
