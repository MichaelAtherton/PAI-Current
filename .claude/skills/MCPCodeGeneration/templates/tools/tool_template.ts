/**
 * TEMPLATE: Individual MCP Tool Wrapper
 * 
 * Replace the following placeholders:
 * - {ToolName} -> PascalCase version (e.g., ListFiles)
 * - {toolName} -> camelCase version (e.g., listFiles)
 * - {tool_name} -> snake_case version (e.g., list_files)
 * - {server_name} -> kebab-case server name (e.g., google-drive)
 * - {description} -> Tool description from schema
 * - {parameter descriptions} -> From JSON schema
 */

interface {ToolName}Input {
  /** {parameter description} */
  {parameterName}: {TypeScriptType};
  
  /** {parameter description} */
  {optionalParameter}?: {TypeScriptType};
}

interface {ToolName}Output {
  // If output schema provided, generate interface
  // Otherwise use:
  [key: string]: any;
}

/**
 * {Tool description from schema}
 * 
 * @param input - Input parameters for {tool_name}
 * @returns {Brief description of return value}
 * 
 * @example
 * ```typescript
 * const result = await {toolName}({
 *   {parameterName}: value
 * });
 * ```
 */
export async function {toolName}(
  input: {ToolName}Input
): Promise<{ToolName}Output> {
  return callMCPTool('{server_name}__{tool_name}', input);
}
