#!/usr/bin/env bun
/**
 * SourceFetcher.ts - Fetch opportunities from configured sources
 *
 * Handles different source types (RSS, scrape, API) and returns
 * standardized opportunity data.
 *
 * Usage:
 *   echo '{"sourceId":"hn_whoishiring"}' | bun SourceFetcher.ts
 *
 * Output:
 *   JSON array of OpportunityData objects
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { paiPath } from '../../../hooks/lib/paths';
import type { OpportunityData } from './FitAssessor';

// ============================================================================
// Types
// ============================================================================

interface Source {
  id: string;
  name: string;
  type: 'rss' | 'scrape' | 'api' | 'manual';
  url?: string;
  urls?: string[];
  endpoint?: string;
  frequency: string;
  enabled: boolean;
}

interface SourcesConfig {
  sources: Source[];
}

interface FetchInput {
  sourceId?: string;
  url?: string;
  type?: 'rss' | 'scrape' | 'api';
}

// ============================================================================
// Source Loading
// ============================================================================

const SOURCES_FILE = paiPath('skills', 'Radar', 'Data', 'sources.json');

function loadSources(): SourcesConfig {
  if (existsSync(SOURCES_FILE)) {
    return JSON.parse(readFileSync(SOURCES_FILE, 'utf-8'));
  }
  return { sources: [] };
}

function getSource(sourceId: string): Source | null {
  const config = loadSources();
  return config.sources.find(s => s.id === sourceId) || null;
}

// ============================================================================
// RSS Fetching
// ============================================================================

async function fetchRss(url: string): Promise<OpportunityData[]> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(`[SourceFetcher] RSS fetch failed: ${response.status}`);
      return [];
    }

    const text = await response.text();
    const opportunities: OpportunityData[] = [];

    // Parse RSS items
    const itemMatches = text.matchAll(/<item>([\s\S]*?)<\/item>/g);

    for (const match of itemMatches) {
      const itemXml = match[1];

      // Extract fields
      const titleMatch = itemXml.match(/<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?<\/title>/);
      const descMatch = itemXml.match(/<description>(?:<!\[CDATA\[)?([\s\S]*?)(?:\]\]>)?<\/description>/);
      const linkMatch = itemXml.match(/<link>(.*?)<\/link>/);
      const pubDateMatch = itemXml.match(/<pubDate>(.*?)<\/pubDate>/);

      if (titleMatch && descMatch) {
        // Clean HTML from description
        const cleanDescription = descMatch[1]
          .replace(/<[^>]*>/g, '')
          .replace(/&nbsp;/g, ' ')
          .replace(/&amp;/g, '&')
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>')
          .replace(/&quot;/g, '"')
          .trim();

        // Try to extract company name from title or description
        let company: string | undefined;
        const companyMatch = titleMatch[1].match(/^([^|@-]+)\s*[|@-]/);
        if (companyMatch) {
          company = companyMatch[1].trim();
        }

        // Try to extract location
        let location: string | undefined;
        const locationMatch = cleanDescription.match(/(?:Location|Based in|Office):\s*([^\n,]+)/i);
        if (locationMatch) {
          location = locationMatch[1].trim();
        }
        if (!location && cleanDescription.toLowerCase().includes('remote')) {
          location = 'Remote';
        }

        opportunities.push({
          id: `rss_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
          title: titleMatch[1].trim(),
          company,
          description: cleanDescription.slice(0, 2000), // Limit description length
          url: linkMatch ? linkMatch[1].trim() : undefined,
          location,
          source: 'rss',
        });
      }
    }

    return opportunities;
  } catch (error) {
    console.error('[SourceFetcher] RSS fetch error:', error);
    return [];
  }
}

// ============================================================================
// API Fetching (Placeholder)
// ============================================================================

async function fetchApi(_endpoint: string): Promise<OpportunityData[]> {
  // This would integrate with specific APIs
  // For now, return empty array
  console.error('[SourceFetcher] API fetching not yet implemented');
  return [];
}

// ============================================================================
// Scrape Fetching (Placeholder)
// ============================================================================

async function fetchScrape(_urls: string[]): Promise<OpportunityData[]> {
  // This would integrate with BrightData skill
  // For now, return empty array
  console.error('[SourceFetcher] Scrape fetching not yet implemented - use BrightData skill');
  return [];
}

// ============================================================================
// Main Fetch Function
// ============================================================================

export async function fetchFromSource(sourceId: string): Promise<OpportunityData[]> {
  const source = getSource(sourceId);

  if (!source) {
    console.error(`[SourceFetcher] Source not found: ${sourceId}`);
    return [];
  }

  if (!source.enabled) {
    console.error(`[SourceFetcher] Source disabled: ${sourceId}`);
    return [];
  }

  switch (source.type) {
    case 'rss':
      if (source.url) {
        return fetchRss(source.url);
      }
      if (source.urls && source.urls.length > 0) {
        const results: OpportunityData[] = [];
        for (const url of source.urls) {
          const items = await fetchRss(url);
          results.push(...items);
        }
        return results;
      }
      return [];

    case 'api':
      if (source.endpoint) {
        return fetchApi(source.endpoint);
      }
      return [];

    case 'scrape':
      if (source.urls && source.urls.length > 0) {
        return fetchScrape(source.urls);
      }
      return [];

    case 'manual':
      // Manual sources don't auto-fetch
      return [];

    default:
      console.error(`[SourceFetcher] Unknown source type: ${source.type}`);
      return [];
  }
}

export async function fetchFromUrl(url: string, type: 'rss' | 'scrape' | 'api' = 'rss'): Promise<OpportunityData[]> {
  switch (type) {
    case 'rss':
      return fetchRss(url);
    case 'api':
      return fetchApi(url);
    case 'scrape':
      return fetchScrape([url]);
    default:
      return [];
  }
}

// ============================================================================
// CLI Entry Point
// ============================================================================

async function main() {
  // Read input from stdin
  const decoder = new TextDecoder();
  const reader = Bun.stdin.stream().getReader();
  let input = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    input += decoder.decode(value, { stream: true });
  }

  if (!input.trim()) {
    console.error('Usage: echo \'{"sourceId":"..."}\' | bun SourceFetcher.ts');
    console.error('   or: echo \'{"url":"...", "type":"rss"}\' | bun SourceFetcher.ts');
    process.exit(1);
  }

  try {
    const params = JSON.parse(input) as FetchInput;
    let opportunities: OpportunityData[];

    if (params.sourceId) {
      opportunities = await fetchFromSource(params.sourceId);
    } else if (params.url) {
      opportunities = await fetchFromUrl(params.url, params.type);
    } else {
      console.error('[SourceFetcher] Must provide sourceId or url');
      process.exit(1);
    }

    console.log(JSON.stringify(opportunities, null, 2));
  } catch (error) {
    console.error('[SourceFetcher] Error:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.main) {
  main();
}
