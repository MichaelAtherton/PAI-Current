# CLI-Anything: Technical Foundation

Deep technical context from our repo analysis and research agents. Load this when the user needs to understand what CLI-Anything is, how it works, or how to build with it.

---

## What It Is

**Repo**: https://github.com/HKUDS/CLI-Anything
**Organization**: HKUDS — HKU Data Science Lab, University of Hong Kong
**Lead**: Professor Chao Huang (Assistant Professor of AI and Data Science)
**Primary Developer**: yuh-yang (Yuhao) — 19 of 34 commits
**Created**: March 8, 2026 | **Stars at analysis**: 8,163 | **Forks**: 716
**License**: MIT | **Language**: 99.7% Python

CLI-Anything is an automated 7-phase pipeline that analyzes software and generates a production-ready CLI wrapper. The generated CLI speaks both human (pretty tables, REPL) and machine (JSON output), integrating with the real software backend for actual rendering/processing.

**Access model**: The pipeline works with ANY software you can communicate with programmatically — not just open source. The 11 demo harnesses use open-source source code analysis, but the methodology extends to proprietary software via scripting APIs (ExtendScript, Ruby, Python), OS automation bridges (AppleScript, COM), vendor CLIs, and plugin systems. See `references/SoftwareCompatibility.md` for the full access path taxonomy.

It's distributed as a Claude Code plugin. You run `/cli-anything <path-or-repo>` and the LLM follows HARNESS.md to generate the CLI.

## The 7-Phase Pipeline

1. **Analyze** — Scan source code, map GUI actions to internal APIs
2. **Design** — Architect Click CLI command groups, state model, output formats
3. **Implement** — Build CLI with REPL, JSON output, undo/redo
4. **Plan Tests** — Create TEST.md with unit + E2E test plans
5. **Write Tests** — Implement comprehensive test suite
6. **Document** — Run tests, update TEST.md with results
7. **Publish** — Create setup.py, install to PATH via pip

## The Key Technical Insight

This isn't code generation. It's a **methodology encoded as an AI agent prompt**. The plugin is a Markdown file that instructs the LLM to follow HARNESS.md step-by-step. HARNESS.md is the project's most valuable artifact — a transferable playbook for making any software agent-accessible.

## Architecture Pattern

Every generated harness follows this structure:
```
<software>/agent-harness/
├── setup.py
├── <SOFTWARE>.md              # Software-specific SOP
└── cli_anything/<software>/
    ├── __init__.py
    ├── __main__.py
    ├── <software>_cli.py      # Click CLI entry point
    ├── core/                  # Business logic modules
    │   ├── project.py, session.py, export.py, filters.py, layers.py, etc.
    ├── utils/
    │   ├── repl_skin.py       # Shared REPL UI (per-software accent colors)
    │   └── <software>_backend.py  # Real software invocation via subprocess
    └── tests/
        ├── TEST.md
        ├── test_core.py
        └── test_full_e2e.py
```

### Key Architectural Decisions
- **Click framework** (Python's most popular CLI library)
- **Dual-mode**: Stateful REPL (interactive) + subcommand (scripting/piping)
- **Namespace packaging**: `cli_anything.*` — PEP 420, no conflicts between harnesses
- **JSON output**: `--json` flag on every command for agent consumption
- **Session management**: Persistent project state with undo/redo
- **Backend pattern**: `utils/<software>_backend.py` wraps real software via `subprocess.run()`

## Code Quality (What We Verified)

**Strengths:**
- Clean, idiomatic Python
- Consistent error handling with `handle_error` decorator
- Well-structured module separation (core vs CLI vs utils)
- Export presets are data-driven, not hard-coded
- `repl_skin.py` is polished — per-software accent colors, ANSI handling, progress bars, tables

**Known Issues:**
- **The Pillow contradiction** (Issue #48): README claims "No Pillow replacements for GIMP" but `export.py` imports `from PIL import Image`. The GIMP harness primarily uses Pillow, not GIMP's Script-Fu/GEGL.
- `sys.path.insert(0, ...)` — code smell
- No type hints, no linter/formatter config visible
- No CI/CD — test results are self-reported
- No research paper published yet
- Shotcut CLI fails to persist timeline changes in one-shot mode (Issue #14)

## Testing (Claimed)

- **1,508 total tests** across 11 apps (100% pass rate claimed)
- **4-layer pyramid**: unit → E2E native → E2E true backend → CLI subprocess
- Tests fail (not skip) when backends are missing
- Output verification: magic bytes, ZIP structure, pixel analysis, audio RMS levels

## Competitive Positioning

| Tool | Relationship |
|------|-------------|
| Open Interpreter | OI runs arbitrary code; CLI-Anything generates structured CLI wrappers. Different goals. |
| ShellGPT | Translates NL to existing CLI commands; CLI-Anything creates NEW CLIs. |
| Aider | Edits files; CLI-Anything builds tool interfaces. Non-overlapping. |
| Claude Code | CLI-Anything is a plugin FOR Claude Code. Complementary. |
| GUI agents (Computer Use) | CLI-Anything's explicit alternative — structured text vs brittle pixel-clicking. |
| MCP Servers | Both create tool interfaces. MCP = hand-crafted protocol adapters; CLI-Anything auto-generates standalone CLIs. |

## Our Overall Rating: 8/10

The Good: Novel concept, strong execution, excellent methodology docs, explosive growth, smart architecture.
The Concerning: Pillow contradiction, no CI/CD, no paper, single-person concentration risk, no root license.
Bottom Line: A methodology project masquerading as a tool. The real value is HARNESS.md and the plugin, not the 11 generated CLIs.
