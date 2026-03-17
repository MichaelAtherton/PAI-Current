# Assess - Single Opportunity Assessment

**Deep assessment of a specific opportunity against your full TELOS and Architecture profile.**

---

## Trigger

- "assess this opportunity: [URL or description]"
- "is this right for me: [opportunity]"
- "check fit for [opportunity]"
- "/radar assess [URL]"

---

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `opportunity` | Yes | URL, job posting, or description of opportunity |

---

## Workflow

### Step 1: Parse Opportunity

Extract opportunity details from the input:

```typescript
interface OpportunityData {
  title: string;
  company?: string;
  description: string;
  requirements?: string[];
  benefits?: string[];
  location?: string;
  compensation?: string;
  url?: string;
  source: 'url' | 'text' | 'manual';
}
```

**If URL provided:**
1. Fetch page content via WebFetch
2. Extract structured data
3. If bot-protected, escalate to BrightData

**If text provided:**
1. Parse directly from description
2. Identify key attributes

### Step 2: Load Profile

Load user's TELOS and Architecture:

```
Read: skills/CORE/USER/TELOS/MISSION.md
Read: skills/CORE/USER/TELOS/GOALS.md
Read: skills/CORE/USER/TELOS/BELIEFS.md
Read: skills/CORE/USER/TELOS/STRATEGIES.md
Read: skills/CORE/USER/TELOS/NARRATIVES.md
Read: skills/CORE/USER/TELOS/ARCHITECTURE.md
```

### Step 3: Score Against TELOS (40%)

For each TELOS dimension, assess alignment:

| Dimension | Assessment |
|-----------|------------|
| Mission (M#) | Does this advance your core missions? |
| Goals (G#) | Does this help achieve specific goals? |
| Beliefs (B#) | Is this consistent with your beliefs? |
| Strategies (S#) | Does this fit your current strategies? |
| Narratives (N#) | Can you authentically tell this story? |

Each dimension scored 0-1. Average = TELOS score.

### Step 4: Score Against Architecture (40%)

| Dimension | Assessment |
|-----------|------------|
| Autonomy | Does this match your self-direction capacity? |
| Structure | Does the structure need match? |
| Risk | Is the risk level appropriate? |
| Meaning | Does this align with your meaning sources? |
| Work Style | Does environment/pace/collaboration fit? |

Each dimension scored 0-1. Average = Architecture score.

### Step 5: Check Hard Limits (20%)

Read hard limits from ARCHITECTURE.md:
- If ANY hard limit violated → overall score = 0
- If all pass → limits score = 1.0

### Step 6: Calculate Overall Score

```
overall = (telos_score * 0.4) + (arch_score * 0.4) + (limits_score * 0.2)
```

### Step 7: Generate Report

Output detailed assessment:

```
📡 RADAR ASSESSMENT

[Opportunity Title]
[Company] | [Location]

─────────────────────────────────────

OVERALL FIT: [score]/1.00 ([recommendation])

─────────────────────────────────────

TELOS ALIGNMENT (0.XX)

✓ M0: [Mission alignment explanation]
✓ G2: [Goal alignment explanation]
⚠️ B1: [Belief concern if any]

─────────────────────────────────────

ARCHITECTURE FIT (0.XX)

✓ Autonomy: [High/matches your High preference]
✓ Work Style: [Remote/matches your preference]
⚠️ Structure: [High process may conflict with Minimal need]

─────────────────────────────────────

HARD LIMITS

✓ All hard limits pass

─────────────────────────────────────

SUMMARY

[2-3 sentence summary of fit, highlighting key alignments and concerns]

RECOMMENDATION: [Surface / Investigate / Digest / Dismiss]
```

---

## Output

Returns FitAssessment object:

```typescript
interface FitAssessment {
  opportunity: OpportunityData;
  telosAlignment: {
    mission: number;
    goals: number;
    beliefs: number;
    strategies: number;
    narratives: number;
    overall: number;
  };
  architectureFit: {
    autonomy: number;
    structure: number;
    risk: number;
    meaning: number;
    workStyle: number;
    overall: number;
  };
  hardLimits: {
    passed: boolean;
    violations: string[];
  };
  overallScore: number;
  recommendation: 'surface' | 'investigate' | 'digest' | 'dismiss';
  warnings: string[];
  summary: string;
}
```

---

## Side Effects

- Logs assessment to `Data/surfaced.jsonl` if score >= 0.50
- Updates `MEMORY/STATE/radar-state.json` stats

---

## Example

```
User: assess this opportunity: https://jobs.anthropic.com/...

📡 RADAR ASSESSMENT

AI Infrastructure Lead
Anthropic | San Francisco (Remote OK)

─────────────────────────────────────

OVERALL FIT: 0.87/1.00 (HIGH MATCH)

─────────────────────────────────────

TELOS ALIGNMENT (0.92)

✓ M0: Directly advances "build infrastructure for human flourishing"
✓ G1: Aligns with "expand AI safety impact"
✓ B2: Consistent with "tech should serve humanity"

─────────────────────────────────────

ARCHITECTURE FIT (0.80)

✓ Autonomy: High autonomy role matches your High capacity
✓ Work Style: Remote-first matches preference
⚠️ Structure: Large org may not match "Small team" preference

─────────────────────────────────────

HARD LIMITS

✓ All hard limits pass

─────────────────────────────────────

SUMMARY

Strong mission alignment with your core focus on human flourishing
infrastructure. The main concern is organizational size—you prefer
small teams, and Anthropic is growing rapidly. Worth investigating
team structure specifically.

RECOMMENDATION: Investigate
```
