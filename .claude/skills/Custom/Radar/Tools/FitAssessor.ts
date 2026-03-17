#!/usr/bin/env bun
/**
 * FitAssessor.ts - Core fit scoring algorithm for Radar
 *
 * Scores opportunities against TELOS profile and psychological architecture.
 * Used by both interactive assessment and background scanning.
 *
 * Usage:
 *   echo '{"title":"...", "description":"..."}' | bun FitAssessor.ts
 *
 * Output:
 *   JSON FitAssessment object to stdout
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { paiPath } from '../../../hooks/lib/paths';

// ============================================================================
// Types
// ============================================================================

export interface OpportunityData {
  id?: string;
  title: string;
  company?: string;
  description: string;
  requirements?: string[];
  benefits?: string[];
  location?: string;
  compensation?: string;
  url?: string;
  source: 'url' | 'text' | 'manual' | 'rss' | 'scrape';
}

export interface TelosAlignment {
  mission: number;
  goals: number;
  beliefs: number;
  strategies: number;
  narratives: number;
  overall: number;
  details: Record<string, string>;
}

export interface ArchitectureFit {
  autonomy: number;
  structure: number;
  risk: number;
  meaning: number;
  workStyle: number;
  overall: number;
  details: Record<string, string>;
}

export interface HardLimitsCheck {
  passed: boolean;
  violations: string[];
  limits: string[];
}

export interface FitAssessment {
  opportunity: OpportunityData;
  telosAlignment: TelosAlignment;
  architectureFit: ArchitectureFit;
  hardLimits: HardLimitsCheck;
  overallScore: number;
  recommendation: 'surface' | 'investigate' | 'digest' | 'dismiss';
  warnings: string[];
  summary: string;
  assessedAt: string;
}

interface TelosProfile {
  missions: string[];
  goals: string[];
  beliefs: string[];
  strategies: string[];
  narratives: string[];
}

interface ArchitectureProfile {
  autonomyLevel: string;
  structureNeed: string;
  riskTolerance: Record<string, string>;
  meaningDrivers: string[];
  workStyle: {
    environment: string;
    collaboration: string;
    pace: string;
  };
  hardLimits: string[];
  dealbreakers: string[];
  positiveSignals: string[];
  negativeSignals: string[];
}

// ============================================================================
// Profile Loading
// ============================================================================

const TELOS_DIR = paiPath('skills', 'CORE', 'USER', 'TELOS');

function loadTelosFile(filename: string): string {
  const filepath = join(TELOS_DIR, filename);
  if (existsSync(filepath)) {
    return readFileSync(filepath, 'utf-8');
  }
  return '';
}

function extractListItems(content: string): string[] {
  const items: string[] = [];
  const lines = content.split('\n');

  for (const line of lines) {
    // Match lines starting with - **ID**: or - [content]
    const match = line.match(/^[-*]\s+\*\*([A-Z]+\d*)\*\*:\s*(.+)$/);
    if (match) {
      items.push(`${match[1]}: ${match[2]}`);
    } else {
      const simpleMatch = line.match(/^[-*]\s+(.+)$/);
      if (simpleMatch && !simpleMatch[1].startsWith('[')) {
        items.push(simpleMatch[1]);
      }
    }
  }

  return items;
}

function loadTelosProfile(): TelosProfile {
  return {
    missions: extractListItems(loadTelosFile('MISSION.md')),
    goals: extractListItems(loadTelosFile('GOALS.md')),
    beliefs: extractListItems(loadTelosFile('BELIEFS.md')),
    strategies: extractListItems(loadTelosFile('STRATEGIES.md')),
    narratives: extractListItems(loadTelosFile('NARRATIVES.md')),
  };
}

function extractSection(content: string, sectionName: string): string[] {
  const lines = content.split('\n');
  const items: string[] = [];
  let inSection = false;

  for (const line of lines) {
    if (line.includes(`## ${sectionName}`) || line.includes(`### ${sectionName}`)) {
      inSection = true;
      continue;
    }
    if (inSection && line.startsWith('## ')) {
      break;
    }
    if (inSection) {
      const match = line.match(/^\d+\.\s+(.+)$/) || line.match(/^[-*]\s+(.+)$/);
      if (match && !match[1].startsWith('[')) {
        items.push(match[1].trim());
      }
    }
  }

  return items;
}

function extractKeyValue(content: string, key: string): string {
  const lines = content.split('\n');
  for (const line of lines) {
    if (line.includes(`**${key}**:`)) {
      const match = line.match(/\*\*[^*]+\*\*:\s*(.+)/);
      if (match) {
        return match[1].replace(/\[|\]/g, '').trim();
      }
    }
  }
  return '';
}

function loadArchitectureProfile(): ArchitectureProfile {
  const content = loadTelosFile('ARCHITECTURE.md');

  return {
    autonomyLevel: extractKeyValue(content, 'Level') || 'Medium',
    structureNeed: extractKeyValue(content, 'Level') || 'Moderate',
    riskTolerance: {
      career: 'Medium',
      financial: 'Medium',
      social: 'Medium',
      health: 'Low',
    },
    meaningDrivers: extractSection(content, 'Primary Drivers'),
    workStyle: {
      environment: extractKeyValue(content, 'Preferred') || 'Remote',
      collaboration: extractKeyValue(content, 'Collaboration Mode') || 'Small team',
      pace: extractKeyValue(content, 'Pace') || 'Variable',
    },
    hardLimits: extractSection(content, 'Hard Limits'),
    dealbreakers: extractSection(content, 'Dealbreakers'),
    positiveSignals: extractSection(content, 'Positive Signals'),
    negativeSignals: extractSection(content, 'Negative Signals'),
  };
}

// ============================================================================
// Scoring Functions
// ============================================================================

/**
 * Simple keyword-based relevance scoring.
 * In production, this would use semantic similarity or LLM inference.
 */
function scoreRelevance(opportunity: string, profileItems: string[]): number {
  if (profileItems.length === 0) return 0.5; // Neutral if no profile

  const oppLower = opportunity.toLowerCase();
  let matches = 0;
  let total = profileItems.length;

  for (const item of profileItems) {
    const keywords = item.toLowerCase().split(/\s+/).filter(w => w.length > 4);
    for (const keyword of keywords) {
      if (oppLower.includes(keyword)) {
        matches++;
        break;
      }
    }
  }

  // Base score of 0.3, up to 1.0 based on matches
  return Math.min(1.0, 0.3 + (matches / total) * 0.7);
}

function assessTelosAlignment(
  opportunity: OpportunityData,
  telos: TelosProfile
): TelosAlignment {
  const oppText = `${opportunity.title} ${opportunity.description} ${opportunity.company || ''}`;

  const mission = scoreRelevance(oppText, telos.missions);
  const goals = scoreRelevance(oppText, telos.goals);
  const beliefs = scoreRelevance(oppText, telos.beliefs);
  const strategies = scoreRelevance(oppText, telos.strategies);
  const narratives = scoreRelevance(oppText, telos.narratives);

  const overall = (mission + goals + beliefs + strategies + narratives) / 5;

  return {
    mission,
    goals,
    beliefs,
    strategies,
    narratives,
    overall,
    details: {
      mission: mission >= 0.7 ? 'Aligns with core mission' : 'Limited mission alignment',
      goals: goals >= 0.7 ? 'Supports current goals' : 'Indirect goal support',
      beliefs: beliefs >= 0.7 ? 'Consistent with beliefs' : 'Neutral to beliefs',
      strategies: strategies >= 0.7 ? 'Fits current strategies' : 'May require strategy adjustment',
      narratives: narratives >= 0.7 ? 'Can authentically represent' : 'Narrative alignment unclear',
    },
  };
}

function assessArchitectureFit(
  opportunity: OpportunityData,
  arch: ArchitectureProfile
): ArchitectureFit {
  const oppText = `${opportunity.title} ${opportunity.description}`.toLowerCase();

  // Autonomy scoring
  let autonomy = 0.5;
  if (oppText.includes('autonomous') || oppText.includes('self-directed') || oppText.includes('independent')) {
    autonomy = arch.autonomyLevel === 'High' ? 0.9 : 0.7;
  }
  if (oppText.includes('supervised') || oppText.includes('structured')) {
    autonomy = arch.autonomyLevel === 'Low' ? 0.9 : 0.4;
  }

  // Structure scoring
  let structure = 0.5;
  if (oppText.includes('startup') || oppText.includes('early stage') || oppText.includes('ambiguity')) {
    structure = arch.structureNeed === 'Minimal' ? 0.9 : 0.4;
  }
  if (oppText.includes('established') || oppText.includes('process') || oppText.includes('enterprise')) {
    structure = arch.structureNeed === 'High' ? 0.9 : 0.5;
  }

  // Risk scoring
  let risk = 0.5;
  if (oppText.includes('equity') || oppText.includes('startup') || oppText.includes('founding')) {
    risk = arch.riskTolerance.career === 'High' ? 0.9 : 0.4;
  }

  // Meaning scoring based on positive/negative signals
  let meaning = 0.5;
  for (const signal of arch.positiveSignals) {
    if (oppText.includes(signal.toLowerCase())) {
      meaning = Math.min(1.0, meaning + 0.15);
    }
  }
  for (const signal of arch.negativeSignals) {
    if (oppText.includes(signal.toLowerCase())) {
      meaning = Math.max(0.1, meaning - 0.15);
    }
  }

  // Work style scoring
  let workStyle = 0.5;
  const location = (opportunity.location || '').toLowerCase();
  if (location.includes('remote') && arch.workStyle.environment === 'Remote') {
    workStyle = 0.9;
  } else if (location.includes('hybrid') && arch.workStyle.environment === 'Hybrid') {
    workStyle = 0.8;
  } else if (!location.includes('remote') && arch.workStyle.environment === 'Remote') {
    workStyle = 0.3;
  }

  const overall = (autonomy + structure + risk + meaning + workStyle) / 5;

  return {
    autonomy,
    structure,
    risk,
    meaning,
    workStyle,
    overall,
    details: {
      autonomy: autonomy >= 0.7 ? 'Matches autonomy preference' : 'Autonomy level may not fit',
      structure: structure >= 0.7 ? 'Structure level aligns' : 'Structure mismatch possible',
      risk: risk >= 0.7 ? 'Risk profile appropriate' : 'Risk level concerns',
      meaning: meaning >= 0.7 ? 'Meaning drivers present' : 'Limited meaning alignment',
      workStyle: workStyle >= 0.7 ? 'Work style compatible' : 'Work style adjustment needed',
    },
  };
}

function checkHardLimits(
  opportunity: OpportunityData,
  arch: ArchitectureProfile
): HardLimitsCheck {
  const oppText = `${opportunity.title} ${opportunity.description} ${opportunity.company || ''}`.toLowerCase();
  const violations: string[] = [];

  // Check hard limits
  for (const limit of arch.hardLimits) {
    const limitLower = limit.toLowerCase();
    // Extract key terms from the limit
    const terms = limitLower.split(/\s+/).filter(t => t.length > 3);

    for (const term of terms) {
      if (oppText.includes(term) && (
        limitLower.includes('no ') ||
        limitLower.includes('never') ||
        limitLower.includes('not ')
      )) {
        violations.push(`Hard limit violated: ${limit}`);
        break;
      }
    }
  }

  // Check dealbreakers
  for (const dealbreaker of arch.dealbreakers) {
    const dbLower = dealbreaker.toLowerCase();
    const terms = dbLower.split(/\s+/).filter(t => t.length > 3);

    for (const term of terms) {
      if (oppText.includes(term)) {
        violations.push(`Dealbreaker triggered: ${dealbreaker}`);
        break;
      }
    }
  }

  return {
    passed: violations.length === 0,
    violations,
    limits: arch.hardLimits,
  };
}

function getRecommendation(score: number): 'surface' | 'investigate' | 'digest' | 'dismiss' {
  if (score >= 0.90) return 'surface';
  if (score >= 0.75) return 'investigate';
  if (score >= 0.50) return 'digest';
  return 'dismiss';
}

function generateSummary(
  assessment: Omit<FitAssessment, 'summary'>
): string {
  const { telosAlignment, architectureFit, hardLimits, overallScore } = assessment;

  if (!hardLimits.passed) {
    return `This opportunity violates ${hardLimits.violations.length} hard limit(s). ` +
      `Primary concern: ${hardLimits.violations[0]}. ` +
      `Score reduced to zero regardless of other factors.`;
  }

  const strengths: string[] = [];
  const concerns: string[] = [];

  if (telosAlignment.mission >= 0.7) strengths.push('strong mission alignment');
  if (telosAlignment.goals >= 0.7) strengths.push('supports current goals');
  if (architectureFit.autonomy >= 0.7) strengths.push('autonomy level fits');
  if (architectureFit.workStyle >= 0.7) strengths.push('work style compatible');

  if (telosAlignment.mission < 0.5) concerns.push('limited mission alignment');
  if (architectureFit.autonomy < 0.5) concerns.push('autonomy mismatch');
  if (architectureFit.structure < 0.5) concerns.push('structure concerns');
  if (architectureFit.workStyle < 0.5) concerns.push('work style mismatch');

  let summary = '';

  if (strengths.length > 0) {
    summary += `Strengths: ${strengths.join(', ')}. `;
  }

  if (concerns.length > 0) {
    summary += `Concerns: ${concerns.join(', ')}. `;
  }

  if (overallScore >= 0.8) {
    summary += 'Overall strong fit worth pursuing.';
  } else if (overallScore >= 0.6) {
    summary += 'Moderate fit; worth investigating further.';
  } else {
    summary += 'Limited fit; may not be ideal match.';
  }

  return summary;
}

// ============================================================================
// Main Assessment Function
// ============================================================================

export function assessFit(opportunity: OpportunityData): FitAssessment {
  const telos = loadTelosProfile();
  const arch = loadArchitectureProfile();

  const telosAlignment = assessTelosAlignment(opportunity, telos);
  const architectureFit = assessArchitectureFit(opportunity, arch);
  const hardLimits = checkHardLimits(opportunity, arch);

  // Calculate overall score
  // Hard limit violations = 0 score
  let overallScore: number;
  if (!hardLimits.passed) {
    overallScore = 0;
  } else {
    // 40% TELOS, 40% Architecture, 20% hard limits pass
    overallScore = (telosAlignment.overall * 0.4) + (architectureFit.overall * 0.4) + 0.2;
  }

  const recommendation = getRecommendation(overallScore);

  // Generate warnings
  const warnings: string[] = [];
  if (hardLimits.violations.length > 0) {
    warnings.push(...hardLimits.violations);
  }
  if (architectureFit.workStyle < 0.5) {
    warnings.push('Work style may not match preferences');
  }
  if (telosAlignment.beliefs < 0.5) {
    warnings.push('May conflict with stated beliefs');
  }

  const partialAssessment = {
    opportunity,
    telosAlignment,
    architectureFit,
    hardLimits,
    overallScore,
    recommendation,
    warnings,
    assessedAt: new Date().toISOString(),
  };

  return {
    ...partialAssessment,
    summary: generateSummary(partialAssessment),
  };
}

// ============================================================================
// CLI Entry Point
// ============================================================================

async function main() {
  // Read opportunity from stdin
  const decoder = new TextDecoder();
  const reader = Bun.stdin.stream().getReader();
  let input = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    input += decoder.decode(value, { stream: true });
  }

  if (!input.trim()) {
    console.error('Usage: echo \'{"title":"...", "description":"..."}\' | bun FitAssessor.ts');
    process.exit(1);
  }

  try {
    const opportunity = JSON.parse(input) as OpportunityData;
    const assessment = assessFit(opportunity);
    console.log(JSON.stringify(assessment, null, 2));
  } catch (error) {
    console.error('Error assessing opportunity:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.main) {
  main();
}
