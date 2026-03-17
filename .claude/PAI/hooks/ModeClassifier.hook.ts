#!/usr/bin/env bun
/**
 * ModeClassifier.hook.ts — Algorithm-default mode selection
 *
 * Design: Algorithm is default. Only unambiguous greetings, ratings,
 * and thanks get MINIMAL. Everything else → Algorithm, where the
 * Complexity Gate (in OBSERVE) decides whether to continue or
 * downshift to NATIVE with full conversation context.
 *
 * TRIGGER: UserPromptSubmit
 */

interface HookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
  prompt: string;
}

type Mode = 'MINIMAL' | 'ALGORITHM';

const GREETING_PATTERN = /^(hi|hello|hey|howdy|good\s+(morning|evening|night|afternoon)|gm|gn)\s*[!.?]*$/i;
const RATING_PATTERN = /^\d{1,2}(\s*\/\s*10)?(\s*[-–:]\s*.{0,40})?$/;
const THANKS_PATTERN = /^(thanks|thank\s+you|thx|ty|cheers)\s*[!.?]*$/i;

function isMinimal(prompt: string): boolean {
  const trimmed = prompt.trim();
  if (trimmed.length > 60) return false;
  return GREETING_PATTERN.test(trimmed) ||
         RATING_PATTERN.test(trimmed) ||
         THANKS_PATTERN.test(trimmed);
}

function buildModeContext(mode: Mode): string {
  if (mode === 'MINIMAL') {
    return `⚠️ MODE CLASSIFICATION (ModeClassifier hook): MINIMAL
Use the MINIMAL output format. Short acknowledgment only.`;
  }
  return `⚠️ MODE CLASSIFICATION (ModeClassifier hook): ALGORITHM
You MUST use ALGORITHM mode. Read PAI/Algorithm/v3.7.0.md FIRST, then follow its instructions exactly. Do NOT use NATIVE mode for this request.
The hook has already classified this prompt. Do NOT re-classify. Do NOT skip Algorithm entry. The Complexity Gate inside OBSERVE will decide if downshift to NATIVE is appropriate — but you must enter the Algorithm to reach it.`;
}

async function main() {
  try {
    const raw = await Promise.race([
      Bun.stdin.text(),
      new Promise<string>((_, reject) =>
        setTimeout(() => reject(new Error('stdin timeout')), 3000)
      ),
    ]);
    const input: HookInput = JSON.parse(raw);
    const prompt = input.prompt || '';
    if (!prompt || prompt.length < 1) { process.exit(0); }

    const mode: Mode = isMinimal(prompt) ? 'MINIMAL' : 'ALGORITHM';
    console.error(`[ModeClassifier] ${mode} for: "${prompt.substring(0, 60)}"`);

    const output = {
      hookSpecificOutput: {
        hookEventName: 'UserPromptSubmit',
        additionalContext: buildModeContext(mode),
      },
    };
    console.log(JSON.stringify(output));
    process.exit(0);
  } catch (err) {
    console.error(`[ModeClassifier] Error: ${err}`);
    process.exit(0);
  }
}

main();
