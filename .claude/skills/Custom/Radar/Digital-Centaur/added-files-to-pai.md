SUMMARY: Explaining the Radar skill integration with PAI/Telos system.

  🔍 ANALYSIS:                                                                                                    
   
  Files Added                                                                                                     
                                                                     
  TELOS Integration                                                   
  File: skills/CORE/USER/TELOS/ARCHITECTURE.md                                     
  Purpose: New psychological profile template for stable traits, hard limits, dealbreakers
  Radar Skill (New)                                               
  ┌───────────────────────────────────────────────┬─────────────────────────────────────────────────┐
  │                     File                      │                     Purpose                     │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/SKILL.md                         │ Main skill file with triggers and documentation │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Workflows/Assess.md              │ Single opportunity assessment workflow          │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Workflows/Scan.md                │ Full scan workflow                              │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Workflows/Configure.md           │ Source configuration workflow                   │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Workflows/Review.md              │ Review surfaced opportunities                   │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Tools/FitAssessor.ts             │ Core scoring algorithm                          │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Tools/RadarScanner.ts            │ Background scanner                              │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Tools/SourceFetcher.ts           │ Source fetching utility                         │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Data/sources.json                │ Source configuration                            │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Data/surfaced.jsonl              │ Surfaced opportunities log                      │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Data/dismissed.jsonl             │ Dismissed opportunities log                     │
  ├───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
  │ skills/Radar/Templates/opportunity-report.hbs │ Report template                                 │
  └───────────────────────────────────────────────┴─────────────────────────────────────────────────┘
  State & Hooks
  ┌───────────────────────────────┬──────────────────────────────────────┐
  │             File              │               Purpose                │
  ├───────────────────────────────┼──────────────────────────────────────┤
  │ MEMORY/STATE/radar-state.json │ Scanner state, cooldowns, thresholds │
  ├───────────────────────────────┼──────────────────────────────────────┤
  │ hooks/handlers/radar.ts       │ StopOrchestrator handler             │
  └───────────────────────────────┴──────────────────────────────────────┘
  Files Modified
  ┌───────────────────────────────────┬──────────────────────────────────────────────┐
  │               File                │                    Change                    │
  ├───────────────────────────────────┼──────────────────────────────────────────────┤
  │ skills/Telos/Tools/UpdateTelos.ts │ Added 'ARCHITECTURE.md' to VALID_FILES array │
  ├───────────────────────────────────┼──────────────────────────────────────────────┤
  │ hooks/StopOrchestrator.hook.ts    │ Added handleRadar import and call            │
  └───────────────────────────────────┴──────────────────────────────────────────────┘
  Slash Commands Added

  The skill registers these triggers (not formal slash commands, but skill invocations):
  ┌─────────────────────┬─────────────────────────────┐
  │       Trigger       │           Action            │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar              │ Show surfaced opportunities │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar scan         │ Run immediate scan          │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar assess <url> │ Assess specific opportunity │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar configure    │ Configure sources           │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar digest       │ Show daily digest           │
  ├─────────────────────┼─────────────────────────────┤
  │ /radar dismiss <id> │ Dismiss opportunity         │
  └─────────────────────┴─────────────────────────────┘
  Natural Language Triggers

  - "radar", "opportunities", "job search", "career match"
  - "assess this opportunity", "check fit", "is this right for me"
  - "scan for opportunities"

  Integration Points

  1. TELOS Reading - FitAssessor reads MISSION.md, GOALS.md, BELIEFS.md, STRATEGIES.md, NARRATIVES.md,
  ARCHITECTURE.md to score fit
  2. StopOrchestrator Hook - Background scans triggered every 6 hours (when sources enabled)
  3. Voice Notifications - High matches announced via voice server
  4. State Persistence - All scans logged to JSONL files in Data/

  📊 STATUS: Skill is registered and visible in skill list. Background scanning will activate when non-manual
  sources are enabled in sources.json.