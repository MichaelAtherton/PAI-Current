Radar Augmenter Design Plan

 Overview

 Radar is an always-on opportunity detection system that surfaces matches and warns about mismatches against your TELOS profile
  and psychological architecture.

 ---
 1. Existing Skills to Leverage
 Skill: OSINT
 Radar Use Case: Company/person background on opportunities
 Integration Point: CompanyLookup, PeopleLookup workflows
 ────────────────────────────────────────
 Skill: BrightData
 Radar Use Case: Progressive URL scraping for job boards, news
 Integration Point: 4-tier escalation for bot-protected sites
 ────────────────────────────────────────
 Skill: Research
 Radar Use Case: Multi-source verification (Perplexity + Claude + Gemini)
 Integration Point: Quick/Standard/Extensive modes
 ────────────────────────────────────────
 Skill: Recon
 Radar Use Case: Domain/infrastructure monitoring for companies
 Integration Point: PassiveRecon workflow
 ────────────────────────────────────────
 Skill: Browser
 Radar Use Case: Web page change detection
 Integration Point: Console/network capture for dynamic sites
 ────────────────────────────────────────
 Skill: Agents
 Radar Use Case: Specialized monitoring agents (security, research, analyst)
 Integration Point: AgentFactory trait composition
 ────────────────────────────────────────
 Skill: BackgroundDelegation
 Radar Use Case: Non-blocking periodic scans
 Integration Point: run_in_background: true
 ---
 2. New Components Required

 2.1 New TELOS File: ARCHITECTURE.md

 Location: $PAI_DIR/skills/CORE/USER/TELOS/ARCHITECTURE.md

 Purpose: Captures stable psychological traits for fit scoring.

 # Architecture

 **Your stable psychological architecture - what can't be trained, only selected for.**

 ---

 ## Autonomy Profile

 ### Self-Direction Capacity
 - **Level**: [High / Medium / Low]
 - **Evidence**: [How you know this]

 ### Structure Need
 - **Level**: [Minimal / Moderate / High]
 - **Optimal Environment**: [Description]

 ### External Validation Need
 - **Level**: [Low / Medium / High]

 ---

 ## Work Style Architecture

 ### Environment
 - **Preferred**: [Remote / Hybrid / In-person]
 - **Collaboration Mode**: [Solo / Small team / Large org]
 - **Pace**: [Sprint / Marathon / Variable]

 ### Energy Patterns
 - **Peak Hours**: [time ranges]
 - **Introversion/Extroversion**: [1-10 scale]
 - **Recovery Needs**: [What restores you]

 ---

 ## Risk Profile

 | Domain | Tolerance | Notes |
 |--------|-----------|-------|
 | Career | [High/Med/Low] | |
 | Financial | [High/Med/Low] | |
 | Social | [High/Med/Low] | |
 | Health | [High/Med/Low] | |

 ---

 ## Meaning Sources

 ### Primary Drivers (rank 1-5)
 - [ ] Impact - Making a difference
 - [ ] Mastery - Getting better at things
 - [ ] Autonomy - Self-direction
 - [ ] Connection - Relationships
 - [ ] Recognition - Being valued

 ### Meaning-Making Capacity
 - **Mode**: [Self-generating / Needs external sources / Hybrid]
 - **Evidence**: [How you know this]

 ---

 ## Hard Limits (Non-Negotiables)

 1. [Hard limit 1]
 2. [Hard limit 2]
 3. [Hard limit 3]

 ## Dealbreakers

 1. [Dealbreaker 1]
 2. [Dealbreaker 2]

 ---

 *Review quarterly. Architecture should be stable - if it changes frequently, dig deeper.*

 Integration: Add 'ARCHITECTURE.md' to VALID_FILES in Tools/UpdateTelos.ts

 ---
 2.2 New Skill: Radar

 Location: $PAI_DIR/skills/Radar/

 Structure:
 Radar/
 ├── SKILL.md                    # Main skill file
 ├── Workflows/
 │   ├── Scan.md                 # Run full opportunity scan
 │   ├── Configure.md            # Set up sources and thresholds
 │   ├── Review.md               # Review surfaced opportunities
 │   └── Assess.md               # Assess single opportunity fit
 ├── Tools/
 │   ├── RadarScanner.ts         # Background scanner script
 │   ├── FitAssessor.ts          # Score opportunity against profile
 │   └── SourceFetcher.ts        # Fetch from configured sources
 ├── Data/
 │   ├── sources.json            # Configured opportunity sources
 │   ├── surfaced.jsonl          # Surfaced opportunities log
 │   └── dismissed.jsonl         # Dismissed opportunities
 └── Templates/
     └── opportunity-report.hbs  # Opportunity summary template

 ---
 2.3 State Management

 Location: $PAI_DIR/MEMORY/STATE/radar-state.json

 {
   "last_scan": "2026-02-03T12:00:00Z",
   "next_scan": "2026-02-03T18:00:00Z",
   "scan_interval_hours": 6,
   "sources_enabled": ["hn_whoishiring", "linkedin_saved", "rss_feeds"],
   "thresholds": {
     "immediate_surface": 0.9,
     "daily_digest": 0.75,
     "weekly_roundup": 0.5
   },
   "stats": {
     "total_scanned": 1247,
     "total_surfaced": 23,
     "total_dismissed": 89
   }
 }

 ---
 3. Execution Patterns

 3.1 Background Scanner (Primary)

 Trigger: StopOrchestrator hook with cooldown (every 6 hours)

 Pattern from SystemIntegrity:
 // In StopOrchestrator.hook.ts handler
 async function handleRadarScan(parsed: ParsedTranscript, hookInput: any) {
   const STATE_FILE = `${PAI_DIR}/MEMORY/STATE/radar-state.json`;
   const COOLDOWN_MS = 6 * 60 * 60 * 1000; // 6 hours

   if (isInCooldown(STATE_FILE, COOLDOWN_MS)) {
     return; // Skip if recently scanned
   }

   // Spawn detached scanner
   const child = spawn('bun', [`${PAI_DIR}/skills/Radar/Tools/RadarScanner.ts`], {
     detached: true,
     stdio: ['pipe', 'ignore', 'inherit'],
     env: { ...process.env }
   });

   child.stdin?.write(JSON.stringify({ mode: 'background' }));
   child.stdin?.end();
   child.unref();

   // Update state
   updateState(STATE_FILE, { last_scan: new Date().toISOString() });
 }

 3.2 On-Demand Scan (User-Triggered)

 User: "radar scan" / "check opportunities" / "what matches me"
 → Invoke Radar skill → Scan workflow
 → Returns immediate results + schedules background follow-up

 3.3 Single Assessment

 User: "assess this opportunity: [URL or description]"
 → Invoke Radar skill → Assess workflow
 → Returns fit score with detailed breakdown

 ---
 4. User Interaction Patterns

 4.1 Morning Review Integration

 Add to daily rhythm (if configured):

 ☀️ Good morning, Michael.

 📡 RADAR (since last review):

 HIGH MATCH (0.87):
 "AI Infrastructure Lead at Anthropic"
 ✓ M0: Human flourishing infrastructure
 ✓ Architecture: High autonomy, remote
 ⚠️ B2: Large org (you prefer small teams)

 MEDIUM MATCH (0.76):
 "Open source maintainer - PAI ecosystem"
 ✓ G3: Expand PAI impact
 ✓ Architecture: Solo contributor mode

 [3 more in daily digest] → "show radar digest"

 4.2 Slash Commands
 ┌─────────────────────┬────────────────────────────────────┐
 │       Command       │               Action               │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar              │ Show recent surfaced opportunities │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar scan         │ Run immediate scan                 │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar configure    │ Set sources and thresholds         │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar assess [URL] │ Assess specific opportunity        │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar digest       │ Show daily digest                  │
 ├─────────────────────┼────────────────────────────────────┤
 │ /radar dismiss [id] │ Dismiss opportunity                │
 └─────────────────────┴────────────────────────────────────┘
 4.3 Natural Language Triggers

 - "check for opportunities"
 - "what matches my profile"
 - "scan job boards"
 - "is this role right for me"
 - "radar status"

 4.4 Real-Time Mismatch Warning

 When user mentions pursuing something that conflicts:

 ⚠️ RADAR MISMATCH

 You mentioned applying to: "CTO at FinTech Corp"

 CONFLICTS DETECTED:
 - B2: "Tech should serve human flourishing"
   → This company optimizes for extraction
 - ARCHITECTURE: Risk tolerance MEDIUM
   → Role requires HIGH (PE-backed turnaround)
 - Hard Limit: "No finance industry"

 Confidence: 0.32 (poor fit)

 Proceed anyway? [Y/N]

 ---
 5. Fit Assessment Algorithm

 5.1 Scoring Dimensions

 interface FitAssessment {
   opportunity: OpportunityData;

   // TELOS alignment (40% weight)
   telosAlignment: {
     mission: number;      // 0-1
     goals: number;        // 0-1
     beliefs: number;      // 0-1
     strategies: number;   // 0-1
     narratives: number;   // 0-1
   };

   // Architecture fit (40% weight)
   architectureFit: {
     autonomy: number;     // 0-1
     structure: number;    // 0-1
     risk: number;         // 0-1
     meaning: number;      // 0-1
     workStyle: number;    // 0-1
   };

   // Hard limits (20% weight, but dealbreakers = 0)
   hardLimits: {
     passed: boolean;
     violations: string[];
   };

   // Final score
   overallScore: number;   // 0-1
   recommendation: 'surface' | 'digest' | 'weekly' | 'dismiss';
   warnings: string[];
 }

 5.2 Scoring Logic

 function calculateFitScore(opp: Opportunity, profile: Profile): FitAssessment {
   // Hard limits are dealbreakers
   const limits = checkHardLimits(opp, profile.architecture.hardLimits);
   if (!limits.passed) {
     return { overallScore: 0, recommendation: 'dismiss', ... };
   }

   // Weight: TELOS 40%, Architecture 40%, Limits pass 20%
   const telosScore = assessTelosAlignment(opp, profile.telos);
   const archScore = assessArchitectureFit(opp, profile.architecture);
   const limitsScore = limits.passed ? 1.0 : 0;

   const overall = (telosScore * 0.4) + (archScore * 0.4) + (limitsScore * 0.2);

   return {
     overallScore: overall,
     recommendation: getRecommendation(overall),
     ...
   };
 }

 ---
 6. Opportunity Sources

 6.1 Configurable Sources

 {
   "sources": [
     {
       "id": "hn_whoishiring",
       "name": "HN Who's Hiring",
       "type": "rss",
       "url": "https://hnrss.org/whoishiring/jobs",
       "frequency": "monthly",
       "enabled": true
     },
     {
       "id": "linkedin_saved",
       "name": "LinkedIn Saved Searches",
       "type": "scrape",
       "method": "brightdata",
       "urls": ["https://linkedin.com/jobs/..."],
       "frequency": "daily",
       "enabled": true
     },
     {
       "id": "custom_rss",
       "name": "Custom RSS Feeds",
       "type": "rss",
       "urls": [],
       "frequency": "daily",
       "enabled": false
     },
     {
       "id": "github_trending",
       "name": "GitHub Trending",
       "type": "api",
       "category": "projects",
       "frequency": "weekly",
       "enabled": false
     }
   ]
 }

 6.2 Source Types
 ┌────────┬──────────────────────┬─────────────────┐
 │  Type  │        Method        │   Skill Used    │
 ├────────┼──────────────────────┼─────────────────┤
 │ rss    │ Direct fetch         │ WebFetch        │
 ├────────┼──────────────────────┼─────────────────┤
 │ scrape │ Progressive scraping │ BrightData      │
 ├────────┼──────────────────────┼─────────────────┤
 │ api    │ API calls            │ Direct/Research │
 ├────────┼──────────────────────┼─────────────────┤
 │ manual │ User-submitted       │ None            │
 └────────┴──────────────────────┴─────────────────┘
 ---
 7. Notification Integration

 7.1 Surfacing Channels
 ┌─────────────┬───────────────────┬─────────────────────┐
 │ Score Range │      Action       │       Channel       │
 ├─────────────┼───────────────────┼─────────────────────┤
 │ 0.9+        │ Immediate surface │ Voice + Push (ntfy) │
 ├─────────────┼───────────────────┼─────────────────────┤
 │ 0.75-0.9    │ Daily digest      │ Morning review      │
 ├─────────────┼───────────────────┼─────────────────────┤
 │ 0.5-0.75    │ Weekly roundup    │ Weekly summary      │
 ├─────────────┼───────────────────┼─────────────────────┤
 │ <0.5        │ Dismiss silently  │ None                │
 └─────────────┴───────────────────┴─────────────────────┘
 7.2 Mismatch Warnings

 Philosophy: Warnings are reminders, not blockers. Goals change based on experience.

 - Trigger: User expresses intent toward opportunity with conflicts
 - Tone: Informative, not paternalistic ("Here's what you said before...")
 - Bypass: Single keystroke or word to proceed
 - Update prompt: Offer to update profile when bypassed ("Should I update your architecture?")

 Warning Format:
 📡 Radar note: This differs from your current profile—

 • ARCHITECTURE.md: You set "No finance industry" as a hard limit
 • BELIEFS.md (B2): "Tech should serve human flourishing"

 These were your past goals. If they've evolved, I can update them.

 [Continue anyway] [Update profile] [Tell me more]

 Key Principles:
 1. Never block—always allow easy bypass
 2. Frame as "what you said" not "what you should do"
 3. Respect that goals evolve with experience
 4. Offer profile updates when bypassed repeatedly
 5. Track bypasses to detect pattern drift (inform Vigilance augmenter)

 ---
 8. Implementation Sequence

 Phase 1: Foundation

 1. Create ARCHITECTURE.md template in TELOS
 2. Add to VALID_FILES in UpdateTelos.ts
 3. User populates their architecture profile

 Phase 2: Core Skill

 4. Create Radar skill directory structure
 5. Implement SKILL.md with routing
 6. Create Assess.md workflow (single opportunity)
 7. Create FitAssessor.ts tool

 Phase 3: Scanning

 8. Create sources.json configuration
 9. Implement SourceFetcher.ts
 10. Create Scan.md workflow
 11. Implement RadarScanner.ts background script

 Phase 4: Integration

 12. Add Radar handler to StopOrchestrator
 13. Create state file management
 14. Implement notification routing
 15. Create Review.md and Configure.md workflows

 Phase 5: Polish

 16. Morning review integration
 17. Mismatch warning detection
 18. Digest/summary generation
 19. User documentation

 ---
 9. Files to Create/Modify

 New Files
 ┌────────────────────────────────────────┬──────────────────────────┐
 │                  File                  │         Purpose          │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/CORE/USER/TELOS/ARCHITECTURE.md │ Stable traits profile    │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/SKILL.md                  │ Main skill file          │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Workflows/Scan.md         │ Full scan workflow       │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Workflows/Assess.md       │ Single assessment        │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Workflows/Configure.md    │ Source configuration     │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Workflows/Review.md       │ Review surfaced          │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Tools/RadarScanner.ts     │ Background scanner       │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Tools/FitAssessor.ts      │ Fit scoring              │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Tools/SourceFetcher.ts    │ Source fetching          │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ skills/Radar/Data/sources.json         │ Source config            │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ MEMORY/STATE/radar-state.json          │ Scan state               │
 ├────────────────────────────────────────┼──────────────────────────┤
 │ hooks/handlers/radar.ts                │ StopOrchestrator handler │
 └────────────────────────────────────────┴──────────────────────────┘
 Modified Files
 ┌───────────────────────────────────┬────────────────────────────────────┐
 │               File                │               Change               │
 ├───────────────────────────────────┼────────────────────────────────────┤
 │ skills/Telos/Tools/UpdateTelos.ts │ Add ARCHITECTURE.md to VALID_FILES │
 ├───────────────────────────────────┼────────────────────────────────────┤
 │ hooks/StopOrchestrator.hook.ts    │ Add Radar handler import           │
 └───────────────────────────────────┴────────────────────────────────────┘
 ---
 10. Verification

 Test Scenarios

 1. Architecture Profile
   - Create ARCHITECTURE.md
   - Update via "add to ARCHITECTURE" command
   - Verify backup created
 2. Single Assessment
   - "assess this opportunity: [job URL]"
   - Verify fit score with breakdown
   - Check TELOS and architecture alignment
 3. Background Scan
   - Trigger StopOrchestrator
   - Verify cooldown respected
   - Check surfaced.jsonl populated
 4. Morning Integration
   - Check opportunities surfaced in greeting
   - Verify threshold filtering works
 5. Mismatch Warning
   - Express intent toward poor-fit opportunity
   - Verify warning triggered with conflicts

 ---
 Decisions Made
 ┌────────────────────────┬──────────────────────────────────────────────────────────────┐
 │        Question        │                           Decision                           │
 ├────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Source Priority        │ Minimal start—manual submission only, add sources as needed  │
 ├────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Architecture Discovery │ Guided interview to populate ARCHITECTURE.md                 │
 ├────────────────────────┼──────────────────────────────────────────────────────────────┤
 │ Warning Philosophy     │ Reminders not blockers; easy bypass; offer to update profile │
 └────────────────────────┴──────────────────────────────────────────────────────────────┘
 Open Questions

 1. Scan Frequency: 6 hours reasonable, or should user configure?
 2. Vigilance Handoff: When bypasses accumulate, should Radar notify Vigilance augmenter about potential drift?