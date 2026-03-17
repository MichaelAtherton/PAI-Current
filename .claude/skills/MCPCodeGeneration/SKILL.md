---
name: MCPCodeGeneration
description: Build token-efficient TypeScript wrappers for MCP (Model Context Protocol) servers. USE WHEN user wants to create MCP server wrappers, optimize token usage with MCP tools, build privacy-preserving MCP workflows, OR add new MCP servers to their infrastructure. Provides templates, best practices, and composable tool patterns.
---

# MCPCodeGeneration

Generate TypeScript wrapper code from MCP server schemas to enable efficient, token-conscious agent interactions. This skill teaches you to convert MCP tools into code-based APIs that can be composed efficiently without bloating the context window.

**Core Problem:** Traditional MCP loads all tool definitions into context upfront and passes intermediate results through the model, consuming excessive tokens.

**Solution:** Generate TypeScript functions from MCP schemas, organize them on the filesystem, and let agents import only what they need while processing data in the execution environment.

**Result:** 90-98% token reduction, better composability, improved privacy handling.

## Workflow Routing

**When executing a workflow, call the notification script via Bash:**

```bash
${PAI_DIR}/tools/skill-workflow-notification WorkflowName MCPCodeGeneration
```

| Workflow | Trigger | File |
|----------|---------|------|
| **GenerateWrapper** | "create wrapper for MCP server", "generate MCP code" | `workflows/GenerateWrapper.md` |
| **OptimizeWorkflow** | "optimize MCP usage", "reduce token usage" | `workflows/OptimizeWorkflow.md` |

## Examples

**Example 1: Generate a wrapper for an MCP server**
```
User: "Generate a TypeScript wrapper for the google-drive MCP server"
→ Invokes GenerateWrapper workflow
→ Analyzes server schema from tools/list endpoint
→ Generates TypeScript interfaces from JSON Schema
→ Creates ${PAI_DIR}/servers/google-drive/ with index.ts, tools/, README.md
→ Outputs composable functions with full JSDoc and type safety
```

**Example 2: Optimize existing MCP usage for token efficiency**
```
User: "My code calls MCP tools in a loop - it's using too many tokens"
→ Invokes OptimizeWorkflow workflow
→ Identifies data aggregation opportunities
→ Refactors to process data in execution environment
→ Reduces token consumption from 50,000+ to ~300 tokens
```

**Example 3: Build a privacy-preserving workflow**
```
User: "Pull customer data from CRM without PII entering context"
→ Invokes GenerateWrapper workflow (if needed)
→ Structures code so sensitive data stays in execution
→ Data flows directly between tools, never logged
→ Conversation history contains only counts/summaries
```

---

## Part 1: Schema Analysis

### Input: MCP Server Schema

MCP servers provide their schema via the `tools/list` endpoint:

```json
{
  "name": "server-name",
  "version": "1.0.0",
  "tools": [
    {
      "name": "tool_name",
      "description": "What the tool does",
      "inputSchema": {
        "type": "object",
        "properties": { ... },
        "required": [ ... ]
      }
    }
  ]
}
```

### What to Extract

For each tool, identify:
- **Tool name** (for function naming)
- **Description** (for JSDoc)
- **Input schema** (for TypeScript interface)
- **Required fields** (for optional vs required parameters)
- **Output schema** (if provided, otherwise use `any`)

---

## Part 2: JSON Schema to TypeScript Conversion

### Conversion Rules

**Basic Types:**
```
JSON Schema          →  TypeScript
─────────────────────────────────────
type: "string"       →  string
type: "number"       →  number
type: "integer"      →  number
type: "boolean"      →  boolean
type: "null"         →  null
```

**Complex Types:**
```
JSON Schema                    →  TypeScript
──────────────────────────────────────────────────
type: "array"                  →  Array<T>
  items: { type: "string" }    →  Array<string>
  items: { type: "object" }    →  Array<Record<string, any>>

type: "object"                 →  Record<string, any>
  (with properties)            →  nested interface

enum: ["A", "B"]              →  "A" | "B"

anyOf/oneOf                   →  union (Type1 | Type2)
```

**Required vs Optional:**
```
Field in "required" array     →  fieldName: type
Field NOT in "required"       →  fieldName?: type
```

**Descriptions:**
```
"description": "..."          →  /** ... */
                                 fieldName: type
```

### Examples

**Example 1: Simple Properties**

**JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "documentId": {
      "type": "string",
      "description": "The ID of the document"
    },
    "includeMetadata": {
      "type": "boolean",
      "description": "Whether to include metadata"
    }
  },
  "required": ["documentId"]
}
```

**Generated TypeScript:**
```typescript
interface GetDocumentInput {
  /** The ID of the document */
  documentId: string;

  /** Whether to include metadata */
  includeMetadata?: boolean;
}
```

**Example 2: Arrays**

**JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of tags"
    }
  },
  "required": ["tags"]
}
```

**Generated TypeScript:**
```typescript
interface SomethingInput {
  /** List of tags */
  tags: Array<string>;
}
```

**Example 3: Nested Objects**

**JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "filter": {
      "type": "object",
      "properties": {
        "status": { "type": "string" },
        "minValue": { "type": "number" }
      },
      "description": "Filter criteria"
    }
  }
}
```

**Generated TypeScript:**
```typescript
interface QueryInput {
  /** Filter criteria */
  filter?: {
    status?: string;
    minValue?: number;
  };
}
```

**Example 4: Enums**

**JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["pending", "active", "completed"],
      "description": "Task status"
    }
  }
}
```

**Generated TypeScript:**
```typescript
interface UpdateTaskInput {
  /** Task status */
  status?: "pending" | "active" | "completed";
}
```

---

## Part 3: Code Generation Templates

### Template: Tool Wrapper File

**Pattern:**
```typescript
// FILE: ${PAI_DIR}/servers/{SERVER_NAME}/tools/{tool_name}.ts

interface {ToolNamePascal}Input {
  /** {parameter description} */
  {parameterName}: {TypeScriptType};
  // ... more parameters
}

interface {ToolNamePascal}Output {
  // If output schema provided, generate interface
  // Otherwise: [key: string]: any;
  [key: string]: any;
}

/**
 * {tool.description}
 *
 * @param input - Input parameters for {tool_name}
 * @returns {brief description of return value}
 *
 * @example
 * ```typescript
 * const result = await {toolNameCamel}({
 *   // example parameters
 * });
 * ```
 */
export async function {toolNameCamel}(
  input: {ToolNamePascal}Input
): Promise<{ToolNamePascal}Output> {
  return callMCPTool('{server_name}__{tool_name}', input);
}
```

### Template: Index File

**Pattern:**
```typescript
// FILE: ${PAI_DIR}/servers/{SERVER_NAME}/index.ts

/**
 * {Server Name} MCP Server
 * Generated: {ISO_DATE}
 * Tools: {TOOL_COUNT}
 *
 * {Brief server description if available}
 */

// Export all tools
export { {toolNameCamel1} } from './tools/{tool_name_1}';
export { {toolNameCamel2} } from './tools/{tool_name_2}';
// ... more exports

// Re-export types for external use
export type {
  {ToolNamePascal1}Input,
  {ToolNamePascal1}Output
} from './tools/{tool_name_1}';

export type {
  {ToolNamePascal2}Input,
  {ToolNamePascal2}Output
} from './tools/{tool_name_2}';
// ... more type exports
```

### Template: README File

**Pattern:**
```markdown
# {Server Name}

Generated MCP server wrapper for code-based usage.

## Description

{Server description if available}

## Available Tools

### {toolNameCamel}

{Tool description}

**Parameters:**
- `{param1}` (required): {description}
- `{param2}` (optional): {description}

**Returns:** {return description}

**Example:**
\`\`\`typescript
import { {toolNameCamel} } from '../../../servers/{server-name}';

const result = await {toolNameCamel}({
  {param1}: value
});
\`\`\`

## Token Efficiency

This wrapper allows you to:
- Process data in execution environment
- Only return summaries to context
- Chain multiple tools without context bloat
```

---

## Part 4: Naming Conventions

**Critical:** Follow these naming conventions exactly for consistency.

### Server Names
```
MCP Schema: "google-drive"
Directory: ${PAI_DIR}/servers/google-drive/
Import: from '../../../servers/google-drive'  # From inside .claude/skills/SomeSkill/
```

### Tool Names

**Source:** `validate_and_render_mermaid_diagram`

**Generated Names:**
- **Function name:** `validateAndRenderMermaidDiagram` (camelCase)
- **Input interface:** `ValidateAndRenderMermaidDiagramInput` (PascalCase)
- **Output interface:** `ValidateAndRenderMermaidDiagramOutput` (PascalCase)
- **File name:** `validate_and_render_mermaid_diagram.ts` (snake_case, preserved)
- **MCP tool ID:** `server_name__validate_and_render_mermaid_diagram`

### Conversion Functions

```javascript
// camelCase: first word lowercase, rest capitalized
"validate_and_render" → "validateAndRender"

// PascalCase: all words capitalized
"validate_and_render" → "ValidateAndRender"

// snake_case: preserve original
"validate_and_render" → "validate_and_render"
```

---

## Part 5: File Organization

### Directory Structure

```
${PAI_DIR}/servers/
  /{server-name}/              # e.g., google-drive, salesforce
    index.ts                   # Barrel export file
    README.md                  # Generated documentation
    tools/                     # Individual tool wrappers
      {tool_name_1}.ts
      {tool_name_2}.ts
      ...
    types/                     # Optional: shared types
      {server-name}.types.ts   # Common types used across tools
  /lib/
    mcp-client.ts              # Shared MCP utilities
```

### When to Create types/ Directory

**Create `types/` when:**
- Multiple tools share common types
- Complex type definitions used across tools
- Server has domain-specific types

**Skip `types/` when:**
- Each tool has unique types
- Simple server with 1-3 tools
- No type reuse

---

## Part 6: Token-Efficient Usage Patterns

### Pattern 1: Filter Before Logging

**DON'T:**
```typescript
const data = await getTool({ id });
console.log(data); // Entire dataset in context
```

**DO:**
```typescript
const data = await getTool({ id });
const summary = data.items.filter(i => i.active).length;
console.log(`Found ${summary} active items`); // Only summary
```

### Pattern 2: Process in Execution Environment

**DON'T:**
```typescript
// Each result flows through context
const doc = await gdrive.getDocument({ id: '1' });
await salesforce.create({ content: doc.content });

const doc2 = await gdrive.getDocument({ id: '2' });
await salesforce.create({ content: doc2.content });
```

**DO:**
```typescript
// Process multiple in environment, report summary
const ids = ['1', '2', '3', '4', '5'];
let successCount = 0;

for (const id of ids) {
  const doc = await gdrive.getDocument({ id });
  await salesforce.create({ content: doc.content });
  successCount++;
}

console.log(`Processed ${successCount} documents`);
```

### Pattern 3: Chain Without Context

**DON'T:**
```typescript
// Intermediate results in context
TOOL CALL: fetch({ id })
→ returns data
TOOL CALL: transform({ data })
→ returns transformed
TOOL CALL: save({ transformed })
```

**DO:**
```typescript
// Variables keep data in execution environment
const data = await fetch({ id });
const transformed = data.items.map(i => ({ ...i, processed: true }));
await save({ items: transformed });
console.log(`Saved ${transformed.length} items`);
```

### Pattern 4: Aggregate Before Reporting

**DON'T:**
```typescript
const sheet = await getSheet({ id });
console.log(sheet.rows); // 10,000 rows in context
```

**DO:**
```typescript
const sheet = await getSheet({ id });
const stats = {
  total: sheet.rows.length,
  active: sheet.rows.filter(r => r.status === 'active').length,
  revenue: sheet.rows.reduce((sum, r) => sum + r.amount, 0)
};
console.log(`Sheet stats:`, stats); // ~100 tokens vs 10,000
```

### Pattern 5: Privacy-Preserving Flows

**DON'T:**
```typescript
const customers = await getCustomers();
console.log(customers); // Exposes PII to context

for (const c of customers) {
  await createLead({ email: c.email, phone: c.phone });
}
```

**DO:**
```typescript
const customers = await getCustomers();
// Data flows directly, never logged
for (const c of customers) {
  await createLead({
    email: c.email,    // Never in context
    phone: c.phone     // Never in context
  });
}
console.log(`Imported ${customers.length} leads`); // Only count
```

---

## Part 7: Convergent Defaults

### Code Generation Defaults

1. **ALWAYS** use camelCase for function names
2. **ALWAYS** use PascalCase for interface names
3. **ALWAYS** preserve snake_case for file names
4. **ALWAYS** include JSDoc comments with `@param` and `@returns`
5. **ALWAYS** export from `index.ts` for clean imports
6. **ALWAYS** generate `README.md` with usage examples
7. **ALWAYS** add `@example` in JSDoc when possible
8. **ALWAYS** mark optional parameters with `?`
9. **NEVER** duplicate type definitions across files
10. **NEVER** expose internal MCP tool IDs to users

### Usage Defaults

1. **ALWAYS** check `${PAI_DIR}/servers/` directory before generating
2. **ALWAYS** import from generated wrappers, not direct MCP calls
3. **ALWAYS** process data in execution environment
4. **ALWAYS** filter/transform before logging
5. **ONLY** log summaries, counts, or first N items
6. **NEVER** log full datasets to context
7. **NEVER** log sensitive data (emails, phones, SSNs, etc.)
8. **NEVER** pass large intermediate results through context

### Error Handling Defaults

1. **ALWAYS** use try-catch for MCP tool calls
2. **ALWAYS** log errors concisely (message only, not full stack)
3. **CONSIDER** retry logic with exponential backoff
4. **CONSIDER** graceful degradation when tools fail

---

## Part 8: Quick Reference

### Generation Checklist

- [ ] Analyze MCP server schema
- [ ] Extract tool names and descriptions
- [ ] Convert input schema to TypeScript interface
- [ ] Generate output interface (or use `any`)
- [ ] Create wrapper function with proper signature
- [ ] Add JSDoc comments
- [ ] Create file in `${PAI_DIR}/servers/{name}/tools/`
- [ ] Create index.ts with exports
- [ ] Create README.md with documentation
- [ ] Test generated code compiles

### Usage Checklist

- [ ] Import from `${PAI_DIR}/servers/{name}`
- [ ] Process data in execution environment
- [ ] Filter/transform before logging
- [ ] Only log summaries or counts
- [ ] Chain tools with variables
- [ ] Handle errors gracefully
- [ ] Avoid exposing PII to context

---

## Part 9: Edge Cases and Special Handling

### Missing Output Schema

When `outputSchema` is not provided:

```typescript
interface ToolNameOutput {
  [key: string]: any;
}
```

### Array of Primitives

**JSON Schema:**
```json
{
  "tags": {
    "type": "array",
    "items": { "type": "string" }
  }
}
```

**TypeScript:**
```typescript
tags: Array<string>
// OR
tags: string[]
```

### Union Types (anyOf/oneOf)

**JSON Schema:**
```json
{
  "value": {
    "oneOf": [
      { "type": "string" },
      { "type": "number" }
    ]
  }
}
```

**TypeScript:**
```typescript
value: string | number
```

### Additional Properties

**JSON Schema:**
```json
{
  "type": "object",
  "additionalProperties": true
}
```

**TypeScript:**
```typescript
interface ToolInput {
  [key: string]: any;
}
```

### Nested Arrays

**JSON Schema:**
```json
{
  "matrix": {
    "type": "array",
    "items": {
      "type": "array",
      "items": { "type": "number" }
    }
  }
}
```

**TypeScript:**
```typescript
matrix: Array<Array<number>>
// OR
matrix: number[][]
```

---

## Summary

This skill enables you to:

1. **Convert** MCP server schemas to TypeScript wrapper code
2. **Organize** code into a consistent filesystem structure
3. **Use** generated code to minimize token consumption
4. **Compose** multiple tools efficiently
5. **Preserve** privacy by keeping data in execution environment

**Key insight:** LLMs are better at writing code than calling tools directly. By converting MCP tools to code, we leverage what LLMs are trained on while solving token bloat.

**Expected outcome:** 90-98% token reduction compared to traditional MCP usage.
