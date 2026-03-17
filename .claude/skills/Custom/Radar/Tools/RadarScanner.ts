#!/usr/bin/env bun
/**
 * RadarScanner.ts - Background opportunity scanner for Radar
 *
 * Runs as a detached process spawned by StopOrchestrator.
 * Fetches from enabled sources, scores against profile, surfaces matches.
 *
 * Input (via stdin):
 *   { "mode": "background" | "foreground" }
 *
 * Side Effects:
 *   - Updates MEMORY/STATE/radar-state.json
 *   - Appends to Data/surfaced.jsonl
 *   - Appends to Data/dismissed.jsonl
 *   - Voice notification for high matches
 */

import { readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { paiPath } from '../../../hooks/lib/paths';
import { assessFit, type OpportunityData, type FitAssessment } from './FitAssessor';

// ============================================================================
// Paths
// ============================================================================

const RADAR_DIR = paiPath('skills', 'Radar');
const DATA_DIR = join(RADAR_DIR, 'Data');
const STATE_FILE = paiPath('MEMORY', 'STATE', 'radar-state.json');
const SOURCES_FILE = join(DATA_DIR, 'sources.json');
const SURFACED_FILE = join(DATA_DIR, 'surfaced.jsonl');
const DISMISSED_FILE = join(DATA_DIR, 'dismissed.jsonl');

// ============================================================================
// Types
// ============================================================================

interface Source {
  id: string;
  name: string;
  type: 'rss' | 'scrape' | 'api' | 'manual';
  url?: string;
  urls?: string[];
  frequency: string;
  enabled: boolean;
}

interface SourcesConfig {
  sources: Source[];
  lastUpdated: string;
}

interface RadarState {
  last_scan: string | null;
  next_scan: string | null;
  scan_interval_hours: number;
  sources_enabled: string[];
  thresholds: {
    immediate_surface: number;
    daily_digest: number;
    weekly_roundup: number;
  };
  notifications: {
    voice: boolean;
    push: boolean;
    digest: boolean;
    discord: boolean;
  };
  stats: {
    total_scanned: number;
    total_surfaced: number;
    total_dismissed: number;
    last_high_match: string | null;
  };
  cooldown_until: string | null;
}

interface SurfacedEntry {
  id: string;
  title: string;
  company?: string;
  url?: string;
  score: number;
  recommendation: string;
  status: 'new' | 'saved' | 'reviewed';
  scannedAt: string;
  source: string;
  telosScore: number;
  archScore: number;
  warnings: string[];
}

interface ScanInput {
  mode: 'background' | 'foreground';
}

// ============================================================================
// State Management
// ============================================================================

function loadState(): RadarState {
  if (existsSync(STATE_FILE)) {
    return JSON.parse(readFileSync(STATE_FILE, 'utf-8'));
  }
  return {
    last_scan: null,
    next_scan: null,
    scan_interval_hours: 6,
    sources_enabled: ['manual'],
    thresholds: {
      immediate_surface: 0.90,
      daily_digest: 0.75,
      weekly_roundup: 0.50,
    },
    notifications: {
      voice: true,
      push: false,
      digest: true,
      discord: false,
    },
    stats: {
      total_scanned: 0,
      total_surfaced: 0,
      total_dismissed: 0,
      last_high_match: null,
    },
    cooldown_until: null,
  };
}

function saveState(state: RadarState): void {
  const dir = paiPath('MEMORY', 'STATE');
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function loadSources(): SourcesConfig {
  if (existsSync(SOURCES_FILE)) {
    return JSON.parse(readFileSync(SOURCES_FILE, 'utf-8'));
  }
  return {
    sources: [
      {
        id: 'manual',
        name: 'Manual Submission',
        type: 'manual',
        frequency: 'immediate',
        enabled: true,
      },
    ],
    lastUpdated: new Date().toISOString(),
  };
}

// ============================================================================
// Source Fetchers
// ============================================================================

async function fetchRssSource(source: Source): Promise<OpportunityData[]> {
  if (!source.url) return [];

  try {
    const response = await fetch(source.url);
    if (!response.ok) {
      console.error(`[RadarScanner] Failed to fetch RSS ${source.name}: ${response.status}`);
      return [];
    }

    const text = await response.text();
    const opportunities: OpportunityData[] = [];

    // Simple RSS parsing (title and description extraction)
    const itemMatches = text.matchAll(/<item>([\s\S]*?)<\/item>/g);

    for (const match of itemMatches) {
      const itemXml = match[1];
      const titleMatch = itemXml.match(/<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>/);
      const descMatch = itemXml.match(/<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/description>/);
      const linkMatch = itemXml.match(/<link>(.*?)<\/link>/);

      if (titleMatch && descMatch) {
        opportunities.push({
          id: `${source.id}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
          title: titleMatch[1].trim(),
          description: descMatch[1].replace(/<[^>]*>/g, '').trim(),
          url: linkMatch ? linkMatch[1].trim() : undefined,
          source: 'rss',
        });
      }
    }

    console.error(`[RadarScanner] Fetched ${opportunities.length} items from ${source.name}`);
    return opportunities;
  } catch (error) {
    console.error(`[RadarScanner] Error fetching ${source.name}:`, error);
    return [];
  }
}

async function fetchFromSource(source: Source): Promise<OpportunityData[]> {
  switch (source.type) {
    case 'rss':
      return fetchRssSource(source);
    case 'manual':
      // Manual sources don't auto-fetch
      return [];
    case 'scrape':
      // Would integrate with BrightData skill
      console.error(`[RadarScanner] Scrape source ${source.name} not yet implemented`);
      return [];
    case 'api':
      // Would integrate with Research skill
      console.error(`[RadarScanner] API source ${source.name} not yet implemented`);
      return [];
    default:
      return [];
  }
}

// ============================================================================
// Deduplication
// ============================================================================

function loadExistingIds(): Set<string> {
  const ids = new Set<string>();

  // Load from surfaced
  if (existsSync(SURFACED_FILE)) {
    const lines = readFileSync(SURFACED_FILE, 'utf-8').split('\n').filter(l => l.trim());
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.id) ids.add(entry.id);
        if (entry.url) ids.add(entry.url);
        if (entry.title) ids.add(entry.title.toLowerCase());
      } catch {
        // Skip malformed lines
      }
    }
  }

  // Load from dismissed
  if (existsSync(DISMISSED_FILE)) {
    const lines = readFileSync(DISMISSED_FILE, 'utf-8').split('\n').filter(l => l.trim());
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.id) ids.add(entry.id);
        if (entry.url) ids.add(entry.url);
        if (entry.title) ids.add(entry.title.toLowerCase());
      } catch {
        // Skip malformed lines
      }
    }
  }

  return ids;
}

function isNewOpportunity(opp: OpportunityData, existingIds: Set<string>): boolean {
  if (opp.id && existingIds.has(opp.id)) return false;
  if (opp.url && existingIds.has(opp.url)) return false;
  if (existingIds.has(opp.title.toLowerCase())) return false;
  return true;
}

// ============================================================================
// Logging
// ============================================================================

function logSurfaced(assessment: FitAssessment, source: string): void {
  const entry: SurfacedEntry = {
    id: assessment.opportunity.id || `opp_${Date.now()}`,
    title: assessment.opportunity.title,
    company: assessment.opportunity.company,
    url: assessment.opportunity.url,
    score: assessment.overallScore,
    recommendation: assessment.recommendation,
    status: 'new',
    scannedAt: new Date().toISOString(),
    source,
    telosScore: assessment.telosAlignment.overall,
    archScore: assessment.architectureFit.overall,
    warnings: assessment.warnings,
  };

  appendFileSync(SURFACED_FILE, JSON.stringify(entry) + '\n');
}

function logDismissed(assessment: FitAssessment, source: string, reason: string): void {
  const entry = {
    id: assessment.opportunity.id || `opp_${Date.now()}`,
    title: assessment.opportunity.title,
    score: assessment.overallScore,
    reason,
    scannedAt: new Date().toISOString(),
    source,
  };

  appendFileSync(DISMISSED_FILE, JSON.stringify(entry) + '\n');
}

// ============================================================================
// Notifications
// ============================================================================

async function notifyHighMatch(assessment: FitAssessment): Promise<void> {
  try {
    await fetch('http://localhost:8888/notify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: `High match found: ${assessment.opportunity.title}`,
        voice_enabled: true,
        priority: 'high',
      }),
    });
  } catch {
    // Voice server might not be running
  }
}

// ============================================================================
// Main Scan Function
// ============================================================================

async function runScan(mode: 'background' | 'foreground'): Promise<void> {
  console.error(`[RadarScanner] Starting ${mode} scan...`);

  const state = loadState();
  const sourcesConfig = loadSources();
  const existingIds = loadExistingIds();

  // Filter to enabled sources (excluding manual for auto-scan)
  const enabledSources = sourcesConfig.sources.filter(
    s => s.enabled && s.type !== 'manual'
  );

  if (enabledSources.length === 0) {
    console.error('[RadarScanner] No enabled sources for scanning');
    return;
  }

  let totalScanned = 0;
  let totalSurfaced = 0;
  let totalDismissed = 0;
  const highMatches: FitAssessment[] = [];

  // Fetch from each source
  for (const source of enabledSources) {
    console.error(`[RadarScanner] Fetching from ${source.name}...`);
    const opportunities = await fetchFromSource(source);

    for (const opp of opportunities) {
      // Skip if we've seen this before
      if (!isNewOpportunity(opp, existingIds)) {
        continue;
      }

      totalScanned++;

      // Assess fit
      const assessment = assessFit(opp);

      // Route by score
      if (assessment.overallScore >= state.thresholds.weekly_roundup) {
        logSurfaced(assessment, source.id);
        totalSurfaced++;

        if (assessment.overallScore >= state.thresholds.immediate_surface) {
          highMatches.push(assessment);
        }
      } else {
        logDismissed(
          assessment,
          source.id,
          assessment.hardLimits.passed
            ? 'Low overall score'
            : assessment.hardLimits.violations[0]
        );
        totalDismissed++;
      }

      // Track for deduplication
      existingIds.add(opp.title.toLowerCase());
      if (opp.url) existingIds.add(opp.url);
    }
  }

  // Update state
  state.last_scan = new Date().toISOString();
  state.next_scan = new Date(Date.now() + state.scan_interval_hours * 60 * 60 * 1000).toISOString();
  state.stats.total_scanned += totalScanned;
  state.stats.total_surfaced += totalSurfaced;
  state.stats.total_dismissed += totalDismissed;

  if (highMatches.length > 0) {
    state.stats.last_high_match = highMatches[0].opportunity.title;
  }

  saveState(state);

  // Notify for high matches
  if (state.notifications.voice && highMatches.length > 0) {
    await notifyHighMatch(highMatches[0]);
  }

  // Output summary
  console.error(`[RadarScanner] Scan complete:`);
  console.error(`  Scanned: ${totalScanned}`);
  console.error(`  Surfaced: ${totalSurfaced}`);
  console.error(`  Dismissed: ${totalDismissed}`);
  console.error(`  High matches: ${highMatches.length}`);
}

// ============================================================================
// CLI Entry Point
// ============================================================================

async function main() {
  // Read input from stdin
  const decoder = new TextDecoder();
  const reader = Bun.stdin.stream().getReader();
  let input = '';

  const timeoutPromise = new Promise<void>((resolve) => {
    setTimeout(() => resolve(), 500);
  });

  const readPromise = (async () => {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      input += decoder.decode(value, { stream: true });
    }
  })();

  await Promise.race([readPromise, timeoutPromise]);

  let mode: 'background' | 'foreground' = 'foreground';

  if (input.trim()) {
    try {
      const parsed = JSON.parse(input) as ScanInput;
      mode = parsed.mode || 'foreground';
    } catch {
      // Use default mode
    }
  }

  await runScan(mode);
}

// Run if executed directly
if (import.meta.main) {
  main().catch((error) => {
    console.error('[RadarScanner] Fatal error:', error);
    process.exit(1);
  });
}
