# CLI-Anything: Software Compatibility Model

How to evaluate whether ANY software — open source or proprietary — can be wrapped with CLI-Anything. Load this when evaluating a specific software target or when brainstorming to ensure ideas are grounded in feasible access paths.

---

## The Core Requirement

CLI-Anything doesn't require source code. It requires **a way to communicate with the software programmatically**. Source code is one path. There are five.

## The 5 Access Paths

| # | Access Path | How It Works | Example Software |
|---|---|---|---|
| 1 | **Open Source Code** | Read source, map GUI→internal API, wrap via subprocess | GIMP, Blender, Inkscape, Audacity, LibreOffice, OBS |
| 2 | **Scripting API** | Vendor provides scriptable interface (JS, Python, Lua) | Photoshop (ExtendScript/UXP), After Effects (ExtendScript), SketchUp (Ruby API), AutoCAD (AutoLISP/.NET) |
| 3 | **OS Automation Bridge** | AppleScript (macOS), COM/PowerShell (Windows), D-Bus (Linux) | Final Cut Pro, Logic Pro, Excel, Word, any macOS/Windows app with automation dictionary |
| 4 | **Vendor CLI / Headless Mode** | Software ships with its own CLI or headless binary | FFmpeg, ImageMagick, `aerender` (After Effects), `accoreconsole` (AutoCAD), Blender (`--background`) |
| 5 | **Plugin/Extension API** | Write a plugin that exposes operations, then wrap the plugin | Unity (C# scripting), Unreal (Blueprints/C++), Maya (MEL/Python), Houdini (VEX/Python) |

### How CLI-Anything Adapts Per Path

```
Path 1 (Source):     subprocess.run(["gimp", "--batch", script])
Path 2 (Script API): subprocess.run(["photoshop", "-r", "script.jsx"])
Path 3 (OS Bridge):  subprocess.run(["osascript", "-e", applescript])
Path 4 (Vendor CLI): subprocess.run(["ffmpeg", "-i", input, output])
Path 5 (Plugin):     subprocess.run(["unity", "-executeMethod", "MyPlugin.Run"])
```

The backend pattern (`utils/<software>_backend.py` using `subprocess.run()`) works for ALL five paths. The only thing that changes is what gets invoked.

## Quick Compatibility Filter

Run these 5 questions before deep-diving any software:

| # | Question | Yes → | No → |
|---|---|---|---|
| 1 | **Can you invoke it from the command line at all?** | Continue | Likely incompatible |
| 2 | **Can it run headlessly (without GUI)?** | Strong candidate | Check scripting bridges |
| 3 | **Does it have a scripting API or plugin system?** | Strong candidate | Check OS automation |
| 4 | **Does it already have a full API (REST, MCP, GraphQL)?** | Probably doesn't NEED CLI-Anything | Skip — already agent-accessible |
| 5 | **Is the output capturable (files, stdout, JSON)?** | Continue | May need plugin to export |

### The Compatibility Spectrum

```
BEST FIT ◄────────────────────────────────────────────► WORST FIT

Open-source        Proprietary with     Proprietary with     Web app with
desktop GUI,       scripting API,       no scripting,        full REST API,
no existing CLI    no existing CLI      no headless mode     already automated
(GIMP, Blender)    (Photoshop, Maya)    (some mobile apps)   (vibe-kanban, Figma API)

CLI-Anything       CLI-Anything         Hard but possible    CLI-Anything adds
adds maximum       adds high value      via OS bridges       no value — skip
value here         here too
```

## The "Already Agent-Accessible" Anti-Pattern

**Lesson from vibe-kanban evaluation (2026-03-12):** Software that was DESIGNED for agent consumption (REST API + MCP server + JSON output) does not benefit from CLI-Anything wrapping. You'd be adding a Python CLI layer on top of an already-clean interface.

Signs a software is already agent-accessible:
- Has a documented REST/GraphQL API
- Ships as an MCP server
- Returns JSON natively
- Was built in the AI-agent era with automation in mind

In these cases, agents consume the software directly. No harness needed.

## Proprietary Software Examples

### Tier A: Excellent Candidates (scripting API + headless)
| Software | Access Path | Scripting | Headless | Domain |
|---|---|---|---|---|
| Adobe Photoshop | ExtendScript/UXP | Full API | Yes (jsx batch) | Image editing |
| Adobe After Effects | ExtendScript | Full API | Yes (aerender) | Motion graphics |
| Autodesk Maya | MEL + Python | Full API | Yes (mayapy) | 3D animation |
| Autodesk AutoCAD | AutoLISP + .NET | Full API | Yes (accoreconsole) | CAD/Architecture |
| SketchUp | Ruby API | Full API | Yes (headless) | 3D modeling |
| Houdini | VEX + Python | Full API | Yes (hython) | VFX/Procedural |
| DaVinci Resolve | Python (Fusion) | Partial | Yes (CLI render) | Video editing |

### Tier B: Good Candidates (OS automation bridge)
| Software | Access Path | Scripting | Headless | Domain |
|---|---|---|---|---|
| Final Cut Pro | AppleScript | Limited | Partial | Video editing |
| Logic Pro | AppleScript | Limited | No | Music production |
| Keynote | AppleScript | Moderate | Yes (export) | Presentations |
| Pages/Numbers | AppleScript | Moderate | Yes (export) | Documents/Spreadsheets |
| Microsoft Office (Mac) | AppleScript + COM | Moderate | Partial | Productivity |

### Tier C: Already Have CLIs (extend/standardize)
| Software | Existing CLI | What CLI-Anything Adds |
|---|---|---|
| FFmpeg | Full CLI | Standardized --json, REPL, session state |
| ImageMagick | Full CLI | Standardized --json, REPL, session state |
| Pandoc | Full CLI | Standardized --json, pipeline composability |
| wkhtmltopdf | Full CLI | Standardized --json, REPL |
| yt-dlp | Full CLI | Standardized --json, REPL |

### Tier D: Skip — Already Agent-Accessible
| Software | Why Skip |
|---|---|
| Figma | Full REST API, plugins, MCP server |
| Notion | Full API |
| Airtable | Full API |
| GitHub | Full API + CLI + MCP |
| vibe-kanban | REST API + MCP server built in |

## Using This During Brainstorming

When generating ideas for a domain (real estate, healthcare, education, etc.):

1. **List the professional software used in that domain** — don't limit to the 11 demo harnesses
2. **Classify each by access path** — which of the 5 paths applies?
3. **Run the quick filter** — skip Tier D software, prioritize Tier A/B
4. **Design pipelines using the full software universe** — mix open-source harnesses with proprietary wrappable software
5. **Remember: the world is your oyster** — if you can communicate with the software, CLI-Anything can wrap it
