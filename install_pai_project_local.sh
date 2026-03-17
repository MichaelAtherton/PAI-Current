#!/usr/bin/env bash

#PAI Release
PAI_RELEASE="v4.0.3"



set -euo pipefail

# Paths
PROJECT_DIR="/Users/michaelatherton/PAI_current"
STAGING_DIR="$PROJECT_DIR/.tmp/pai-$PAI_RELEASE-release"
RELEASE_DIR="$STAGING_DIR/Releases/$PAI_RELEASE"
PROJECT_CLAUDE_DIR="$PROJECT_DIR/.claude"
PROJECT_CONFIG_DIR="$PROJECT_DIR/.config/PAI"

echo "1) Prepare project directories"
mkdir -p "$PROJECT_DIR" "$PROJECT_CLAUDE_DIR" "$PROJECT_CONFIG_DIR"

echo "2) Fetch only v4.0.3 .claude payload (shallow+sparse)"
mkdir -p "$PROJECT_DIR/.tmp"
rm -rf "$STAGING_DIR"
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/danielmiessler/Personal_AI_Infrastructure.git "$STAGING_DIR"
git -C "$STAGING_DIR" sparse-checkout set --no-cone "Releases/v4.0.3/.claude"

echo "3) Copy v4.0.3 .claude payload into project-level .claude"
cp -R "$RELEASE_DIR/.claude/." "$PROJECT_CLAUDE_DIR/"

echo "4) Set project-level PAI paths in .claude/settings.json"
python3 - <<'PY'
import json, os
project_dir = "/Users/michaelatherton/PAI_current"
settings_path = os.path.join(project_dir, ".claude", "settings.json")
with open(settings_path, "r", encoding="utf-8") as f:
    s = json.load(f)

env = s.setdefault("env", {})
env["PAI_DIR"] = os.path.join(project_dir, ".claude")
env["PAI_CONFIG_DIR"] = os.path.join(project_dir, ".config", "PAI")
env.setdefault("PROJECTS_DIR", "${HOME}/Projects")
env.setdefault("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS", "1")

with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2)
    f.write("\n")
PY

echo "5) Patch runtime hardcoded ~/.claude paths to honor PAI_DIR"
python3 - <<'PY'
import os

project_dir = "/Users/michaelatherton/PAI_current"
root = os.path.join(project_dir, ".claude")

replacements = {
    os.path.join(root, "PAI/Tools/BuildCLAUDE.ts"): [
        ('const PAI_DIR = join(process.env.HOME!, ".claude");',
         'const PAI_DIR = process.env.PAI_DIR;\nif (!PAI_DIR) throw new Error("PAI_DIR is required");'),
    ],
    os.path.join(root, "PAI/Tools/RebuildPAI.ts"): [
        ('const PAI_DIR = join(HOME, ".claude/PAI");',
         'const PAI_ROOT = process.env.PAI_DIR;\nif (!PAI_ROOT) throw new Error("PAI_DIR is required");\nconst PAI_DIR = join(PAI_ROOT, "PAI");'),
        ('const SETTINGS_PATH = join(HOME, ".claude/settings.json");',
         'const SETTINGS_PATH = join(PAI_ROOT, "settings.json");'),
    ],
    os.path.join(root, "PAI/Tools/IntegrityMaintenance.ts"): [
        ("const PAI_DIR = process.env.HOME + '/.claude';",
         "const PAI_DIR = process.env.PAI_DIR;\nif (!PAI_DIR) throw new Error('PAI_DIR is required');"),
        ("`bun ~/.claude/skills/_SYSTEM/Tools/UpdateSearch.ts recent 5`",
         "`bun ${PAI_DIR}/skills/_SYSTEM/Tools/UpdateSearch.ts recent 5`"),
    ],
    os.path.join(root, "skills/Agents/Tools/ComposeAgent.ts"): [
        ('const BASE_TRAITS_PATH = `${HOME}/.claude/skills/Agents/Data/Traits.yaml`;',
         'const PAI_DIR = process.env.PAI_DIR;\nif (!PAI_DIR) throw new Error("PAI_DIR is required");\nconst BASE_TRAITS_PATH = `${PAI_DIR}/skills/Agents/Data/Traits.yaml`;'),
        ('const USER_TRAITS_PATH = `${HOME}/.claude/PAI/USER/SKILLCUSTOMIZATIONS/Agents/Traits.yaml`;',
         'const USER_TRAITS_PATH = `${PAI_DIR}/PAI/USER/SKILLCUSTOMIZATIONS/Agents/Traits.yaml`;'),
        ('const TEMPLATE_PATH = `${HOME}/.claude/skills/Agents/Templates/DynamicAgent.hbs`;',
         'const TEMPLATE_PATH = `${PAI_DIR}/skills/Agents/Templates/DynamicAgent.hbs`;'),
        ('const CUSTOM_AGENTS_DIR = `${HOME}/.claude/custom-agents`;',
         'const CUSTOM_AGENTS_DIR = `${PAI_DIR}/custom-agents`;'),
    ],
    os.path.join(root, "skills/Security/Recon/Tools/BountyPrograms.ts"): [
        ('const CACHE_DIR = `${process.env.HOME}/.claude/skills/Security/Recon/Data`;',
         'const PAI_DIR = process.env.PAI_DIR;\nif (!PAI_DIR) throw new Error("PAI_DIR is required");\nconst CACHE_DIR = `${PAI_DIR}/skills/Security/Recon/Data`;'),
    ],
}

for path, pairs in replacements.items():
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    updated = content
    for old, new in pairs:
        updated = updated.replace(old, new)
    if updated != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"patched: {path}")
PY

echo "6) Rewrite runtime fallback patterns to strict PAI_DIR in code files"
python3 - <<'PY'
import os

project_dir = "/Users/michaelatherton/PAI_current"
root = os.path.join(project_dir, ".claude")

strict_expr = '(() => { const v = process.env.PAI_DIR; if (!v) throw new Error("PAI_DIR is required"); return v; })()'

code_exts = (".ts", ".js", ".py", ".sh", ".tsx")
runtime_replacements = [
    ("process.env.PAI_DIR || join(HOME, \".claude\")", strict_expr),
    ("process.env.PAI_DIR || join(HOME, '.claude')", strict_expr),
    ("process.env.PAI_DIR || join(process.env.HOME!, \".claude\")", strict_expr),
    ("process.env.PAI_DIR || join(process.env.HOME!, '.claude')", strict_expr),
    ("process.env.PAI_DIR || path.join(process.env.HOME!, \".claude\")", strict_expr),
    ("process.env.PAI_DIR || path.join(process.env.HOME!, '.claude')", strict_expr),
    ("process.env.PAI_DIR || resolve(process.env.HOME!, \".claude\")", strict_expr),
    ("process.env.PAI_DIR || resolve(process.env.HOME!, '.claude')", strict_expr),
    ("process.env.PAI_DIR || `${process.env.HOME}/.claude`", strict_expr),
    ("process.env.PAI_DIR || `${HOME}/.claude`", strict_expr),
    ("process.env.PAI_DIR || (process.env.HOME + '/.claude')", strict_expr),
    ("process.env.PAI_DIR || (process.env.HOME + \"/.claude\")", strict_expr),
    ("process.env.PAI_DIR || (() => { const v = process.env.PAI_DIR; if (!v) throw new Error(\"PAI_DIR is required\"); return v; })()", strict_expr),
    ("join(homedir(), \".claude\")", strict_expr),
    ("join(homedir(), '.claude')", strict_expr),
    ("join(process.env.HOME!, \".claude\")", strict_expr),
    ("join(process.env.HOME!, '.claude')", strict_expr),
    ("join(HOME, \".claude\")", strict_expr),
    ("join(HOME, '.claude')", strict_expr),
    ("path.join(process.env.HOME!, \".claude\")", strict_expr),
    ("path.join(process.env.HOME!, '.claude')", strict_expr),
    ("resolve(process.env.HOME!, \".claude\")", strict_expr),
    ("resolve(process.env.HOME!, '.claude')", strict_expr),
    ("PAI_DIR=\"${PAI_DIR:-$HOME/.claude}\"", ": \"${PAI_DIR:?PAI_DIR is required}\""),
    ("PAI_DIR=\"${PAI_DIR:-${HOME}/.claude}\"", ": \"${PAI_DIR:?PAI_DIR is required}\""),
    ('os.environ.get("PAI_DIR", "~/.claude")', 'os.environ["PAI_DIR"]'),
    ("os.environ.get('PAI_DIR', '~/.claude')", 'os.environ["PAI_DIR"]'),
]

updated = 0
for base, _, files in os.walk(root):
    if "/PAI-Install" in base:
        continue
    for name in files:
        if not name.endswith(code_exts):
            continue
        path = os.path.join(base, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            continue
        new_content = content
        for old, new in runtime_replacements:
            new_content = new_content.replace(old, new)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1

print(f"runtime files rewritten: {updated}")
PY

echo "7) Verify no runtime fallback-to-home patterns remain in code files"
python3 - <<'PY'
import os
import re
import sys

project_dir = "/Users/michaelatherton/PAI_current"
root = os.path.join(project_dir, ".claude")
code_exts = (".ts", ".js", ".py", ".sh", ".tsx")

patterns = [
    r'process\.env\.PAI_DIR\s*\|\|\s*(join|path\.join|resolve)\(',
    r'process\.env\.PAI_DIR\s*\|\|\s*`[^`]*\.claude[^`]*`',
    r'process\.env\.PAI_DIR\s*\|\|\s*\([^)]*\.claude[^)]*\)',
    r'join\(homedir\(\),\s*["\']\.claude["\']\)',
    r'join\(HOME,\s*["\']\.claude["\']\)',
    r'join\(process\.env\.HOME!,\s*["\']\.claude["\']\)',
    r'path\.join\(process\.env\.HOME!,\s*["\']\.claude["\']\)',
    r'resolve\(process\.env\.HOME!,\s*["\']\.claude["\']\)',
    r'PAI_DIR="\$\{PAI_DIR:-\$HOME/\.claude\}"',
    r'PAI_DIR="\$\{PAI_DIR:-\$\{HOME\}/\.claude\}"',
    r'os\.environ\.get\(\s*["\']PAI_DIR["\']\s*,\s*["\']~\/\.claude["\']\s*\)',
]

compiled = [re.compile(p) for p in patterns]
hits = []

for base, _, files in os.walk(root):
    if "/PAI-Install" in base:
        continue
    for name in files:
        if not name.endswith(code_exts):
            continue
        path = os.path.join(base, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(lines, 1):
            for rx in compiled:
                if rx.search(line):
                    hits.append((path, i, line.strip()))
                    break

if hits:
    print("ERROR: runtime fallback patterns still present:")
    for p, ln, t in hits[:60]:
        print(f"  {p}:{ln}: {t}")
    if len(hits) > 60:
        print(f"  ... and {len(hits) - 60} more")
    sys.exit(1)

print("ok: no runtime fallback-to-home patterns found in code files")
PY

echo "8) Rewrite literal .claude home-path references across text files"
python3 - <<'PY'
import os

project_dir = "/Users/michaelatherton/PAI_current"
root = os.path.join(project_dir, ".claude")

TEXT_EXTS = (
    ".md", ".md.template", ".txt",
    ".yaml", ".yml", ".hbs",
    ".ts", ".js", ".py", ".sh", ".tsx",
    ".json",
)
REPLACEMENTS = [
    ("~/.claude", "${PAI_DIR}"),
    ("${HOME}/.claude", "${PAI_DIR}"),
    ("$HOME/.claude", "${PAI_DIR}"),
]

updated = 0
updated_files = []
for base, _, files in os.walk(root):
    for name in files:
        if not name.endswith(TEXT_EXTS):
            continue
        path = os.path.join(base, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            continue
        new_content = content
        for old, new in REPLACEMENTS:
            new_content = new_content.replace(old, new)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1
            updated_files.append(path)

print(f"rewritten files: {updated}")
for p in updated_files[:20]:
    print(f"  {p}")
if len(updated_files) > 20:
    print(f"  ... and {len(updated_files) - 20} more")
PY

echo "9) Verify no literal ~/.claude or \$HOME/.claude references remain"
python3 - <<'PY'
import os
import sys

project_dir = "/Users/michaelatherton/PAI_current"
root = os.path.join(project_dir, ".claude")
TEXT_EXTS = (
    ".md", ".md.template", ".txt",
    ".yaml", ".yml", ".hbs",
    ".ts", ".js", ".py", ".sh", ".tsx",
    ".json",
)
TOKENS = ("~/.claude", "${HOME}/.claude", "$HOME/.claude")

hits = []
for base, _, files in os.walk(root):
    for name in files:
        if not name.endswith(TEXT_EXTS):
            continue
        path = os.path.join(base, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            continue
        for token in TOKENS:
            if token in content:
                hits.append((path, token))

if hits:
    print("ERROR: literal home-path references still present:")
    for path, token in hits[:40]:
        print(f"  {path} :: {token}")
    if len(hits) > 40:
        print(f"  ... and {len(hits) - 40} more")
    sys.exit(1)

print("ok: no literal ~/.claude, ${HOME}/.claude, or $HOME/.claude references found")
PY

echo "10) Create project-local .env for keys (optional now)"
touch "$PROJECT_CONFIG_DIR/.env"
chmod 600 "$PROJECT_CONFIG_DIR/.env"

echo "11) Verify key files"
ls -ld "$PROJECT_CLAUDE_DIR"
ls -l "$PROJECT_CLAUDE_DIR/settings.json"
ls -l "$PROJECT_CONFIG_DIR/.env"

echo "12) IMPORTANT"
echo "Do NOT run $PROJECT_CLAUDE_DIR/install.sh for no-symlink mode."
echo "Open Cursor in $PROJECT_DIR so project-level .claude/settings.json is active."
echo "13) Cleaning up staging"
rm -rf "$STAGING_DIR"
echo "Staging removed: $STAGING_DIR"