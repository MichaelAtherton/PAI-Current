/**
 * TEMPLATE: Server Index File
 * 
 * Replace the following placeholders:
 * - {ServerName} -> Friendly server name (e.g., Google Drive)
 * - {ISO_DATE} -> Generation timestamp (e.g., 2025-01-15T10:30:00Z)
 * - {TOOL_COUNT} -> Number of tools (e.g., 5)
 * - {description} -> Server description
 * - {toolName1}, {toolName2} -> camelCase tool names
 * - {tool_name_1}, {tool_name_2} -> snake_case file names
 * - {ToolName1}, {ToolName2} -> PascalCase type names
 */

/**
 * {ServerName} MCP Server
 * Generated: {ISO_DATE}
 * Tools: {TOOL_COUNT}
 * 
 * {Brief server description if available}
 */

// Export all tools
export { {toolName1} } from './tools/{tool_name_1}';
export { {toolName2} } from './tools/{tool_name_2}';
// ... more exports

// Re-export types for external use
export type {
  {ToolName1}Input,
  {ToolName1}Output
} from './tools/{tool_name_1}';

export type {
  {ToolName2}Input,
  {ToolName2}Output
} from './tools/{tool_name_2}';
// ... more type exports
