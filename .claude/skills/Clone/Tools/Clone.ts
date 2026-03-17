#!/usr/bin/env bun
/**
 * Clone.ts — Interactive PAI instance cloner
 *
 * Creates a non-destructive clone with a new DA identity.
 * Uses clone-manifest.json for deterministic transforms,
 * then optionally verifies with AI.
 *
 * The original is NEVER modified — read-only source.
 *
 * Usage:
 *   bun ~/.claude/skills/Clone/Tools/Clone.ts
 *   bun ~/.claude/skills/Clone/Tools/Clone.ts --source /path/to/.claude
 *   bun ~/.claude/skills/Clone/Tools/Clone.ts --no-verify
 */
import { cpSync, existsSync, readFileSync, readdirSync, rmSync, writeFileSync } from "fs";
import { join, resolve } from "path";
import { spawn, spawnSync } from "child_process";

// ── Helpers ──────────────────────────────────────────────────────────────────

function ask(question: string): string {
  process.stdout.write(question);
  return (prompt("") ?? "").trim();
}

function askYesNo(question: string, defaultNo = true): boolean {
  process.stdout.write(question);
  const answer = (prompt("") ?? "").toLowerCase().trim();
  if (defaultNo) return answer === "y" || answer === "yes";
  return answer !== "n" && answer !== "no";
}

function setNestedField(obj: any, fieldPath: string, value: any): void {
  const parts = fieldPath.split(".");
  let current = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    if (current[parts[i]] === undefined) current[parts[i]] = {};
    current = current[parts[i]];
  }
  current[parts[parts.length - 1]] = value;
}

function getNestedField(obj: any, fieldPath: string): any {
  const parts = fieldPath.split(".");
  let current = obj;
  for (const part of parts) {
    if (current === undefined || current === null) return undefined;
    current = current[part];
  }
  return current;
}

// ── Args ─────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const sourceIdx = args.indexOf("--source");
const sourceOverride = sourceIdx !== -1 ? args[sourceIdx + 1] : undefined;
const noVerify = args.includes("--no-verify");

// ── Source resolution ────────────────────────────────────────────────────────

const root = process.cwd();
const localClaude = join(root, ".claude");
const sourceDir = sourceOverride
  ? resolve(sourceOverride)
  : existsSync(localClaude) ? localClaude : (process.env.PAI_DIR || localClaude);

if (!existsSync(sourceDir)) {
  console.error(`\nSource not found: ${sourceDir}`);
  process.exit(1);
}

// ── Read current identity ────────────────────────────────────────────────────

let currentDA = "unknown";
let currentVersion = "unknown";
const sourceSettingsPath = join(sourceDir, "settings.json");
if (existsSync(sourceSettingsPath)) {
  try {
    const s = JSON.parse(readFileSync(sourceSettingsPath, "utf-8"));
    currentDA = s.daidentity?.name || "unknown";
    currentVersion = s.paiVersion || s.pai?.version || "unknown";
  } catch {}
}

// ── Manifest check ───────────────────────────────────────────────────────────

const manifestPath = join(import.meta.dir, "clone-manifest.json");
let needsAnalyze = false;

if (!existsSync(manifestPath)) {
  console.log(`\nNo clone manifest found. Running CloneAnalyze first...`);
  needsAnalyze = true;
} else {
  try {
    const manifest = JSON.parse(readFileSync(manifestPath, "utf-8"));
    if (manifest.paiVersion !== currentVersion) {
      console.log(`\nManifest is for PAI ${manifest.paiVersion} but current is ${currentVersion}.`);
      console.log(`Running CloneAnalyze to refresh...`);
      needsAnalyze = true;
    }
  } catch {
    console.log(`\nManifest is corrupted. Regenerating...`);
    needsAnalyze = true;
  }
}

if (needsAnalyze) {
  const analyzeScript = join(import.meta.dir, "CloneAnalyze.ts");
  const sourceArgs = sourceOverride ? ["--source", sourceOverride] : [];
  const result = spawnSync("bun", [analyzeScript, ...sourceArgs], {
    stdio: "inherit",
    cwd: root,
  });
  if (result.status !== 0) {
    console.error("\nCloneAnalyze failed. Cannot proceed.");
    process.exit(1);
  }
  console.log();
}

// ── Load manifest ────────────────────────────────────────────────────────────

if (!existsSync(manifestPath)) {
  console.error("Manifest still missing after CloneAnalyze. Cannot proceed.");
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, "utf-8"));

// ── Interactive prompts ──────────────────────────────────────────────────────

console.log();
console.log(`\x1b[36m╔══════════════════════════════════════════╗\x1b[0m`);
console.log(`\x1b[36m║       PAI Instance Cloner                ║\x1b[0m`);
console.log(`\x1b[36m╚══════════════════════════════════════════╝\x1b[0m`);
console.log();
console.log(`  Source:      ${sourceDir}`);
console.log(`  Current DA:  ${currentDA}`);
console.log(`  PAI Version: ${currentVersion}`);
console.log(`  Manifest:    ${manifest.transforms.length} transforms loaded`);
console.log();

const dirName = ask(`  Project directory name: `);
if (!dirName) {
  console.error("\n  Directory name is required. Exiting.");
  process.exit(1);
}

const daName = ask(`  New DA identity name: `);
if (!daName) {
  console.error("\n  DA name is required. Exiting.");
  process.exit(1);
}

const fresh = askYesNo(`  Wipe memory for a fresh start? (y/N): `);

// ── Paths ────────────────────────────────────────────────────────────────────

const projectDir = join(root, dirName);
const destDir = join(projectDir, ".claude");

if (existsSync(projectDir)) {
  const overwrite = askYesNo(`\n  "${dirName}" already exists. Overwrite? (y/N): `);
  if (!overwrite) {
    console.log("\n  Cancelled.");
    process.exit(0);
  }
  rmSync(projectDir, { recursive: true, force: true });
}

// ── Confirm ──────────────────────────────────────────────────────────────────

console.log();
console.log(`  \x1b[33m─── Summary ───\x1b[0m`);
console.log(`  Directory:  ${projectDir}`);
console.log(`  DA Name:    ${daName}`);
console.log(`  Fresh:      ${fresh ? "yes — memory will be wiped" : "no — keeping existing memory"}`);
console.log(`  Transforms: ${manifest.transforms.length} from manifest`);
console.log(`  AI Verify:  ${noVerify ? "skipped (--no-verify)" : "yes"}`);
console.log();

const confirmed = askYesNo(`  Proceed? (y/N): `);
if (!confirmed) {
  console.log("\n  Cancelled.");
  process.exit(0);
}

// ── Phase 1: Copy ────────────────────────────────────────────────────────────

console.log();
console.log(`  \x1b[36mPhase 1: Copy\x1b[0m`);
cpSync(sourceDir, destDir, { recursive: true });
console.log(`  Copied .claude/ → ${dirName}/.claude/`);

// ── Phase 2: Apply Manifest Transforms ───────────────────────────────────────

console.log();
console.log(`  \x1b[36mPhase 2: Apply Manifest Transforms\x1b[0m`);

// Group transforms by file for efficient processing
const transformsByFile = new Map<string, typeof manifest.transforms>();
for (const t of manifest.transforms) {
  const list = transformsByFile.get(t.file) || [];
  list.push(t);
  transformsByFile.set(t.file, list);
}

let applied = 0;
let skipped = 0;

for (const [relFile, transforms] of transformsByFile) {
  const filePath = join(destDir, relFile);

  // Handle directory-level transforms (memory wipe)
  for (const t of transforms) {
    if (t.transform === "wipe_dir") {
      if (!fresh) {
        skipped++;
        continue;
      }
      if (existsSync(filePath)) {
        for (const entry of readdirSync(filePath)) {
          rmSync(join(filePath, entry), { recursive: true, force: true });
        }
        console.log(`    Wiped ${relFile}/`);
        applied++;
      }
      continue;
    }

    if (t.transform === "wipe_file") {
      if (!fresh) {
        skipped++;
        continue;
      }
      if (existsSync(filePath)) {
        writeFileSync(filePath, `# ${daName}\n\nFresh instance — no prior data.\n`);
        console.log(`    Reset ${relFile}`);
        applied++;
      }
      continue;
    }
  }

  // Handle JSON file transforms
  const jsonTransforms = transforms.filter(
    (t: any) => t.field && t.transform !== "wipe_dir" && t.transform !== "wipe_file"
  );

  if (jsonTransforms.length === 0) continue;
  if (!existsSync(filePath)) {
    console.log(`    Skipped ${relFile} (not found)`);
    skipped += jsonTransforms.length;
    continue;
  }

  // Only process JSON files
  if (!relFile.endsWith(".json")) {
    // For non-JSON files, log as notes
    for (const t of jsonTransforms) {
      if (t.transform.startsWith("note:")) {
        console.log(`    Note [${relFile}]: ${t.description || t.transform}`);
      }
    }
    continue;
  }

  try {
    const content = JSON.parse(readFileSync(filePath, "utf-8"));
    let modified = false;

    for (const t of jsonTransforms) {
      if (t.transform === "prompt_user") {
        setNestedField(content, t.field, daName);
        modified = true;
        applied++;
      } else if (t.transform.startsWith("template:")) {
        const template = t.transform.slice("template:".length);
        const value = template.replace(/\{DA_NAME\}/g, daName);
        setNestedField(content, t.field, value);
        modified = true;
        applied++;
      } else if (t.transform === "resolve_path") {
        setNestedField(content, t.field, destDir);
        modified = true;
        applied++;
      } else if (t.transform === "reset_zero") {
        const current = getNestedField(content, t.field);
        if (typeof current === "number") {
          setNestedField(content, t.field, 0);
        } else if (typeof current === "object" && current !== null) {
          // Reset all numeric values in the object to 0
          for (const key of Object.keys(current)) {
            if (typeof current[key] === "number") {
              current[key] = 0;
            }
          }
        }
        modified = true;
        applied++;
      } else if (t.transform === "reset_object") {
        setNestedField(content, t.field, {});
        modified = true;
        applied++;
      } else if (t.transform.startsWith("note:")) {
        console.log(`    Note [${t.field}]: ${t.description || t.transform}`);
        skipped++;
      }
    }

    if (modified) {
      writeFileSync(filePath, JSON.stringify(content, null, 2) + "\n");
      console.log(`    Updated ${relFile} (${jsonTransforms.filter((t: any) => !t.transform.startsWith("note:")).length} fields)`);
    }
  } catch (err: any) {
    console.error(`    Error processing ${relFile}: ${err.message}`);
    skipped += jsonTransforms.length;
  }
}

console.log(`  Applied: ${applied} | Skipped: ${skipped}`);

// ── Phase 3: AI Verification (optional) ──────────────────────────────────────

if (!noVerify && manifest.aiVerificationHints?.length > 0) {
  console.log();
  console.log(`  \x1b[36mPhase 3: AI Verification\x1b[0m`);
  console.log(`  Verifying clone integrity...`);

  const hints = manifest.aiVerificationHints.join("\n- ");
  const verifyPrompt = `You are inside a freshly cloned PAI instance at: ${destDir}

This was cloned from a PAI instance where the DA was named "${currentDA}".
The new DA name is "${daName}".
The new PAI_DIR should be "${destDir}".

Verify the clone is clean by checking:
- ${hints}

Grep for any remaining references to "${currentDA}" that should have been changed to "${daName}".
Grep for any remaining references to the old path "${sourceDir}" that should be "${destDir}".

If you find stale references, fix them. Only change identity and path references — do not modify skill logic, hook behavior, or algorithm structure.

After checking, output a brief summary of what you found and fixed (or "Clean — no stale references found").`;

  try {
    const proc = spawn("claude", ["-p", verifyPrompt, "--output-format", "text"], {
      cwd: destDir,
      stdio: ["pipe", "pipe", "pipe"],
    });

    let stdout = "";
    proc.stdout.on("data", (data: Buffer) => { stdout += data.toString(); });

    await new Promise<void>((resolve, reject) => {
      proc.on("close", (code: number) => {
        if (code === 0) resolve();
        else reject(new Error(`Verification exited with code ${code}`));
      });
      proc.on("error", reject);
    });

    console.log();
    // Trim to reasonable length for display
    const summary = stdout.trim().slice(0, 500);
    console.log(`  Verification result:`);
    for (const line of summary.split("\n")) {
      console.log(`    ${line}`);
    }
  } catch (err: any) {
    console.log(`  Verification skipped: ${err.message}`);
    console.log(`  (Clone is still usable — run manually if needed)`);
  }
}

// ── Warnings ─────────────────────────────────────────────────────────────────

if (manifest.warnings?.length > 0) {
  console.log();
  console.log(`  \x1b[33mWarnings:\x1b[0m`);
  for (const w of manifest.warnings) {
    console.log(`    [${w.severity}] ${w.file}: ${w.issue}`);
  }
}

// ── Done ─────────────────────────────────────────────────────────────────────

console.log();
console.log(`  \x1b[32mClone complete!\x1b[0m`);
console.log();
console.log(`  To launch ${daName}:`);
console.log(`    cd ${projectDir} && claude`);
console.log();
