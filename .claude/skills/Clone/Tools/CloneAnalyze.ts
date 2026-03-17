#!/usr/bin/env bun
/**
 * CloneAnalyze.ts — AI-powered manifest generator for PAI cloning
 *
 * Analyzes the current PAI installation to discover all identity, path,
 * memory, and state fields. Produces clone-manifest.json.
 *
 * Uses `claude -p` to leverage PAI's self-knowledge — the AI reads
 * the actual docs and settings of THIS version to discover what needs
 * changing during a clone. No hardcoded field names.
 *
 * Usage:
 *   bun ~/.claude/skills/Clone/Tools/CloneAnalyze.ts
 *   bun ~/.claude/skills/Clone/Tools/CloneAnalyze.ts --source /path/to/.claude
 */
import { existsSync, readFileSync, writeFileSync } from "fs";
import { join, resolve } from "path";
import { spawn } from "child_process";

// ── Config ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const sourceIdx = args.indexOf("--source");
const sourceOverride = sourceIdx !== -1 ? args[sourceIdx + 1] : undefined;

const localClaude = join(process.cwd(), ".claude");
const paiDir = sourceOverride
  ? resolve(sourceOverride)
  : existsSync(localClaude) ? localClaude : (process.env.PAI_DIR || join(process.env.HOME!, ".claude"));

const manifestPath = join(import.meta.dir, "clone-manifest.json");

if (!existsSync(paiDir)) {
  console.error(`PAI directory not found: ${paiDir}`);
  process.exit(1);
}

// ── Read current PAI version ─────────────────────────────────────────────────

let paiVersion = "unknown";
let currentDA = "unknown";
const settingsPath = join(paiDir, "settings.json");

if (existsSync(settingsPath)) {
  try {
    const s = JSON.parse(readFileSync(settingsPath, "utf-8"));
    paiVersion = s.paiVersion || s.pai?.version || "unknown";
    currentDA = s.daidentity?.name || "unknown";
  } catch {}
}

console.log(`\nCloneAnalyze — Discovering clone manifest`);
console.log(`  PAI Dir:     ${paiDir}`);
console.log(`  PAI Version: ${paiVersion}`);
console.log(`  Current DA:  ${currentDA}`);
console.log(`  Manifest:    ${manifestPath}`);
console.log();

// ── The Discovery Prompt ─────────────────────────────────────────────────────
// These questions are VERSION-AGNOSTIC. They ask about concepts (identity,
// paths, memory) not specific field names. The AI discovers the field names
// by reading the actual PAI installation.

const discoveryPrompt = `You are analyzing a PAI (Personal AI Infrastructure) installation to build a clone manifest.
Your goal: identify everything that must change when this PAI instance is copied to create a new DA identity in a new directory.

The PAI installation is at: ${paiDir}

STEP 1: Read these files to understand this PAI version:
- ${settingsPath} (central config — READ THIS FIRST)
- Look for any SKILL.md, README, or architecture docs that describe the system
- Look for any identity module (often in hooks/lib/)

STEP 2: Answer these discovery questions. For EACH answer, output a JSON object.

IDENTITY DISCOVERY:
- Where is the DA (Digital Assistant) name stored? Check settings files for name, displayName, fullName fields.
- What other fields reference the DA by name? (catchphrases, greetings, startup messages)
- Are there template patterns that include the DA name? (e.g., "{name} here, ready to go")

PATH DISCOVERY:
- Where is the PAI installation directory path stored? (often called PAI_DIR)
- Are there other fields with absolute paths that would need to change in a clone?

MEMORY DISCOVERY:
- What directories under this installation contain session memory or state that should be wipeable for a "fresh start"?
- Is there a top-level memory file (like MEMORY.md) that should be reset?

STATE DISCOVERY:
- Are there counters, timestamps, or session statistics that should reset in a fresh clone?

OUTPUT FORMAT — Return ONLY a valid JSON object with this exact structure, no markdown fencing:
{
  "transforms": [
    {
      "type": "identity|path|memory|state",
      "file": "relative/path/from/.claude/",
      "field": "dot.notation.field.path (for JSON) or null (for directories/files)",
      "transform": "prompt_user|template:{pattern}|resolve_path|wipe_dir|wipe_file|reset_zero|reset_object",
      "confidence": "high|medium|low",
      "description": "what this field is and why it needs changing"
    }
  ],
  "warnings": [
    {
      "file": "relative/path:line",
      "issue": "description of something that can't be auto-fixed",
      "severity": "high|medium|low"
    }
  ],
  "aiVerificationHints": [
    "Specific things to grep/check after cloning to catch stale references"
  ]
}

RULES:
- Only include fields that ACTUALLY EXIST in this installation
- For identity transforms: "prompt_user" means the clone tool will ask the user for the new value. "template:{pattern}" means apply a pattern with {DA_NAME} as placeholder.
- For path transforms: "resolve_path" means automatically set to the clone's actual path
- For memory transforms: "wipe_dir" means clear directory contents but keep structure, "wipe_file" means reset file to empty/default
- For state transforms: "reset_zero" for counters, "reset_object" for objects that should be emptied
- Set confidence to "high" for fields you're certain about, "medium" for likely, "low" for uncertain
- Include warnings for hardcoded paths in source code that can't be auto-fixed
- Return ONLY the JSON, no explanation text before or after`;

// ── Run Claude for Discovery ─────────────────────────────────────────────────

console.log(`Running AI discovery...`);
console.log();

const TIMEOUT_MS = 120_000; // 2 minute hard timeout

function runClaude(prompt: string): Promise<string> {
  return new Promise((resolve, reject) => {
    // Stream output so user can see Claude working
    const proc = spawn("claude", ["-p", prompt, "--output-format", "text"], {
      cwd: paiDir,
      stdio: ["pipe", "pipe", "inherit"], // stderr → terminal (shows Claude's progress)
      env: { ...process.env },
    });

    let stdout = "";
    let ticks = 0;

    // Simple elapsed timer — Claude's own stderr shows real progress
    const progress = setInterval(() => {
      ticks++;
      const secs = ticks * 2;
      process.stdout.write(`\r  Elapsed: ${secs}s...`.padEnd(30));
    }, 2000);

    // Hard timeout
    const timeout = setTimeout(() => {
      clearInterval(progress);
      proc.kill();
      reject(new Error(`Timed out after ${TIMEOUT_MS / 1000}s. Claude may be overloaded — try again.`));
    }, TIMEOUT_MS);

    proc.stdout.on("data", (data: Buffer) => { stdout += data.toString(); });

    proc.on("close", (code: number) => {
      clearInterval(progress);
      clearTimeout(timeout);
      process.stdout.write("\r" + " ".repeat(40) + "\r");
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        reject(new Error(`claude exited with code ${code}`));
      }
    });

    proc.on("error", (err: Error) => {
      clearInterval(progress);
      clearTimeout(timeout);
      reject(err);
    });
  });
}

try {
  const rawOutput = await runClaude(discoveryPrompt);

  // Extract JSON from the response (Claude may wrap it in text)
  let jsonStr = rawOutput;
  const jsonMatch = rawOutput.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    jsonStr = jsonMatch[0];
  }

  const discovered = JSON.parse(jsonStr);

  // Build the manifest
  const manifest = {
    manifestVersion: "1.0",
    paiVersion,
    generatedAt: new Date().toISOString(),
    generatedBy: "CloneAnalyze skill (AI-powered discovery)",
    sourceDir: paiDir,
    currentDA,
    ...discovered,
  };

  // Validate structure
  if (!Array.isArray(manifest.transforms) || manifest.transforms.length === 0) {
    console.error("Warning: AI returned no transforms. Manifest may be incomplete.");
    console.error("Raw output:", rawOutput.slice(0, 500));
  }

  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");

  // Report
  const identity = manifest.transforms.filter((t: any) => t.type === "identity").length;
  const paths = manifest.transforms.filter((t: any) => t.type === "path").length;
  const memory = manifest.transforms.filter((t: any) => t.type === "memory").length;
  const state = manifest.transforms.filter((t: any) => t.type === "state").length;
  const warnings = manifest.warnings?.length || 0;

  console.log(`Manifest generated successfully!`);
  console.log();
  console.log(`  Transforms discovered:`);
  console.log(`    Identity: ${identity}`);
  console.log(`    Paths:    ${paths}`);
  console.log(`    Memory:   ${memory}`);
  console.log(`    State:    ${state}`);
  console.log(`    Total:    ${manifest.transforms.length}`);
  console.log();
  if (warnings > 0) {
    console.log(`  Warnings: ${warnings}`);
    for (const w of manifest.warnings) {
      console.log(`    - [${w.severity}] ${w.file}: ${w.issue}`);
    }
    console.log();
  }
  console.log(`  Saved to: ${manifestPath}`);
  console.log();

} catch (err: any) {
  console.error(`\nError during AI discovery:`);
  console.error(err.message);
  console.error(`\nMake sure 'claude' CLI is available and you have an active session.`);
  process.exit(1);
}
