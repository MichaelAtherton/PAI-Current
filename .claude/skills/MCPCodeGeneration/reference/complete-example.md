# Complete Example: Mermaid Chart MCP Server to Code

## The Real MCP Server Schema

This is the **actual schema** from the Mermaid Chart MCP server:

```json
{
  "name": "mermaid-chart",
  "version": "1.0.0",
  "tools": [
    {
      "name": "validate_and_render_mermaid_diagram",
      "description": "Renders Mermaid diagrams directly (Mermaid automatically validates during rendering). If successful, returns diagram image. If Mermaid validation fails, returns error details for fixing. One tool, one call, simple workflow.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "clientName": {
            "type": "string",
            "description": "REQUIRED: The name of the client/agent using the MCP server (e.g., 'claude', 'cursor', 'vscode', 'chatgpt', 'copilot') for analytics tracking."
          },
          "diagramType": {
            "type": "string",
            "description": "The type of Mermaid diagram (e.g., 'flowchart', 'sequenceDiagram', 'gantt')."
          },
          "mermaidCode": {
            "type": "string",
            "description": "Mermaid code to render. Mermaid validates automatically during rendering - if invalid, tool returns error details for fixing."
          },
          "prompt": {
            "type": "string",
            "description": "A text description of the diagram to generate."
          }
        },
        "required": ["clientName", "diagramType", "mermaidCode", "prompt"],
        "additionalProperties": false
      }
    }
  ]
}
```

---

## Step 1: Analyze the Schema

**What we have:**
- Server name: `mermaid-chart`
- Tool name: `validate_and_render_mermaid_diagram`
- 4 required parameters, all strings
- Clear descriptions for each parameter

**What we need to generate:**
1. TypeScript interface for input
2. TypeScript interface for output (unknown, so we'll use `any`)
3. Wrapper function that calls the MCP tool
4. File organization structure

---

## Step 2: Generate TypeScript Wrappers

### File: `${PAI_DIR}/servers/mermaid-chart/tools/validate_and_render_mermaid_diagram.ts`

```typescript
/**
 * Input parameters for validate_and_render_mermaid_diagram
 */
interface ValidateAndRenderMermaidDiagramInput {
  /** 
   * REQUIRED: The name of the client/agent using the MCP server 
   * (e.g., 'claude', 'cursor', 'vscode', 'chatgpt', 'copilot') for analytics tracking.
   */
  clientName: string;
  
  /** 
   * The type of Mermaid diagram (e.g., 'flowchart', 'sequenceDiagram', 'gantt').
   */
  diagramType: string;
  
  /** 
   * Mermaid code to render. Mermaid validates automatically during rendering - 
   * if invalid, tool returns error details for fixing.
   */
  mermaidCode: string;
  
  /** 
   * A text description of the diagram to generate.
   */
  prompt: string;
}

/**
 * Output from validate_and_render_mermaid_diagram
 * Note: Schema not provided, using any for flexibility
 */
interface ValidateAndRenderMermaidDiagramOutput {
  [key: string]: any;
}

/**
 * Renders Mermaid diagrams directly (Mermaid automatically validates during rendering). 
 * If successful, returns diagram image. If Mermaid validation fails, returns error 
 * details for fixing. One tool, one call, simple workflow.
 * 
 * @param input - Diagram rendering parameters
 * @returns Rendered diagram or validation errors
 * 
 * @example
 * ```typescript
 * const result = await validateAndRenderMermaidDiagram({
 *   clientName: 'claude',
 *   diagramType: 'flowchart',
 *   mermaidCode: 'graph TD\n  A-->B',
 *   prompt: 'Simple flowchart'
 * });
 * ```
 */
export async function validateAndRenderMermaidDiagram(
  input: ValidateAndRenderMermaidDiagramInput
): Promise<ValidateAndRenderMermaidDiagramOutput> {
  return callMCPTool('mermaid_chart__validate_and_render_mermaid_diagram', input);
}
```

### File: `${PAI_DIR}/servers/mermaid-chart/index.ts`

```typescript
/**
 * Mermaid Chart MCP Server
 * Generated: 2025-01-15
 * Tools: 1
 * 
 * Provides diagram rendering capabilities using Mermaid
 */

export { validateAndRenderMermaidDiagram } from './tools/validate_and_render_mermaid_diagram';

// Re-export types for external use
export type { 
  ValidateAndRenderMermaidDiagramInput,
  ValidateAndRenderMermaidDiagramOutput 
} from './tools/validate_and_render_mermaid_diagram';
```

### File: `${PAI_DIR}/servers/mermaid-chart/README.md`

```markdown
# Mermaid Chart MCP Server

Generated wrapper for code-based MCP usage.

## Description

Provides diagram rendering capabilities using Mermaid.

## Available Tools

### validateAndRenderMermaidDiagram

Renders Mermaid diagrams directly (Mermaid automatically validates during rendering). If successful, returns diagram image. If Mermaid validation fails, returns error details for fixing.

**Parameters:**
- `clientName` (required): The name of the client/agent using the MCP server
- `diagramType` (required): The type of Mermaid diagram
- `mermaidCode` (required): Mermaid code to render
- `prompt` (required): A text description of the diagram

**Returns:** Rendered diagram or validation errors

## Usage

```typescript
// From PAI root
import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';

const result = await validateAndRenderMermaidDiagram({
  clientName: 'claude',
  diagramType: 'flowchart',
  mermaidCode: 'graph TD\n  A-->B',
  prompt: 'Simple flowchart'
});
```

## Token Efficiency

This wrapper allows you to process diagram generation without bloating context:
- Generate diagram code in execution environment
- Only return success/failure status to context
- Keep full diagram data in variables
```

---

## Step 3: Use the Generated Code Efficiently

### Example 1: Basic Usage

```typescript
// From PAI root
import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';

// Generate and render a simple diagram
const result = await validateAndRenderMermaidDiagram({
  clientName: 'claude',
  diagramType: 'flowchart',
  mermaidCode: `
    graph TD
      A[Start] --> B[Process]
      B --> C[End]
  `,
  prompt: 'Simple process flow'
});

// Only log summary to context (not full result)
console.log('Diagram rendered successfully');
```

**Token savings**: Instead of loading full result into context, only confirm success.

### Example 2: Batch Processing with Filtering

```typescript
// From PAI root
import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';

// Process multiple diagrams, only report failures
const diagramRequests = [
  { type: 'flowchart', code: 'graph TD\n A-->B', desc: 'Flow 1' },
  { type: 'sequence', code: 'sequenceDiagram\n A->>B: Hi', desc: 'Seq 1' },
  { type: 'gantt', code: 'gantt\n task: a, 2024-01-01, 1d', desc: 'Gantt 1' }
];

const results = await Promise.all(
  diagramRequests.map(req =>
    validateAndRenderMermaidDiagram({
      clientName: 'claude',
      diagramType: req.type,
      mermaidCode: req.code,
      prompt: req.desc
    }).catch(err => ({ error: err.message, request: req }))
  )
);

// Filter and report only failures
const failures = results.filter(r => 'error' in r);

if (failures.length > 0) {
  console.log(`${failures.length} diagrams failed:`);
  failures.forEach(f => console.log(`- ${f.request.desc}: ${f.error}`));
} else {
  console.log(`All ${results.length} diagrams rendered successfully`);
}
```

**Token savings**: 3 full diagram results would be ~3,000 tokens. This logs ~100 tokens.

### Example 3: Dynamic Diagram Generation

```typescript
// From PAI root
import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';

// Generate diagram code programmatically
function generateFlowchart(steps: string[]): string {
  const nodes = steps.map((step, i) => `  ${String.fromCharCode(65 + i)}[${step}]`);
  const connections = steps.slice(0, -1).map((_, i) => 
    `  ${String.fromCharCode(65 + i)} --> ${String.fromCharCode(65 + i + 1)}`
  );
  
  return `graph TD\n${nodes.join('\n')}\n${connections.join('\n')}`;
}

// Use generated code (stays in execution environment)
const processSteps = ['Receive Order', 'Validate', 'Process Payment', 'Ship'];
const mermaidCode = generateFlowchart(processSteps);

const result = await validateAndRenderMermaidDiagram({
  clientName: 'claude',
  diagramType: 'flowchart',
  mermaidCode,
  prompt: 'Order processing flow'
});

// Only expose summary
console.log(`Generated diagram with ${processSteps.length} steps`);
```

**Token savings**: Generated code never enters context, only final summary.

### Example 4: Error Handling with Retry

```typescript
// From PAI root
import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';

async function renderWithRetry(
  mermaidCode: string,
  maxAttempts = 3
): Promise<any> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const result = await validateAndRenderMermaidDiagram({
        clientName: 'claude',
        diagramType: 'flowchart',
        mermaidCode,
        prompt: 'Diagram with retry logic'
      });
      
      console.log(`Rendered successfully on attempt ${attempt}`);
      return result;
      
    } catch (error) {
      if (attempt === maxAttempts) {
        console.error(`Failed after ${maxAttempts} attempts: ${error.message}`);
        throw error;
      }
      
      console.log(`Attempt ${attempt} failed, retrying...`);
      
      // Wait with exponential backoff
      await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
    }
  }
}

// Usage
await renderWithRetry('graph TD\n  A-->B');
```

**Token savings**: Error messages and retries handled in execution environment.

---

## Step 4: Key Patterns Extracted

### Pattern 1: Schema-to-TypeScript Conversion

**JSON Schema Property:**
```json
{
  "clientName": {
    "type": "string",
    "description": "REQUIRED: The name of the client/agent..."
  }
}
```

**Generated TypeScript:**
```typescript
interface SomethingInput {
  /** REQUIRED: The name of the client/agent... */
  clientName: string;
}
```

**Rules:**
- `type: "string"` → `string`
- `type: "number"` or `type: "integer"` → `number`
- `type: "boolean"` → `boolean`
- `type: "array"` → `Array<T>` (infer T from items)
- `type: "object"` → nested interface or `Record<string, any>`
- `required` array determines optional (?) vs required
- `description` becomes JSDoc comment

### Pattern 2: Naming Conventions

**Tool name:** `validate_and_render_mermaid_diagram`

**Generated names:**
- Interface: `ValidateAndRenderMermaidDiagramInput` (PascalCase)
- Function: `validateAndRenderMermaidDiagram` (camelCase)
- File: `validate_and_render_mermaid_diagram.ts` (original snake_case)
- MCP tool ID: `mermaid_chart__validate_and_render_mermaid_diagram` (server__tool)

### Pattern 3: File Organization

```
${PAI_DIR}/servers/
  /{server-name}/           # e.g., mermaid-chart
    index.ts                # Barrel export
    README.md               # Generated docs
    tools/
      {tool-name}.ts        # One file per tool
    types/                  # Optional: shared types
      {server}.types.ts
```

### Pattern 4: Function Signature Template

```typescript
/**
 * {tool.description}
 * 
 * @param input - {brief description}
 * @returns {return description}
 * 
 * @example
 * ```typescript
 * // Usage example
 * ```
 */
export async function {camelCase(toolName)}(
  input: {PascalCase(toolName)}Input
): Promise<{PascalCase(toolName)}Output> {
  return callMCPTool('{serverName}__{toolName}', input);
}
```

### Pattern 5: Token-Efficient Usage

**DON'T:**
```typescript
// Full result loaded into context
const result = await tool({ params });
console.log(result); // Could be 10,000 tokens
```

**DO:**
```typescript
// Process in execution environment
const result = await tool({ params });
const summary = result.items.length;
console.log(`Processed ${summary} items`); // ~20 tokens
```

---

## Step 5: What This Enables

With this generated code, Claude can now:

1. **Import only what's needed:**
   ```typescript
   // From PAI root
   import { validateAndRenderMermaidDiagram } from './servers/mermaid-chart';

   // From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
   // import { validateAndRenderMermaidDiagram } from '../../../../servers/mermaid-chart';
   ```

2. **Get type safety and autocomplete:**
   - IDE knows parameters
   - TypeScript validates input
   - JSDoc shows descriptions

3. **Compose efficiently:**
   ```typescript
   // Chain operations without context bloat
   const data = await tool1.fetch();
   const processed = data.filter(x => x.valid);
   await tool2.save(processed);
   console.log(`Saved ${processed.length} items`); // Only summary
   ```

4. **Handle errors cleanly:**
   ```typescript
   try {
     await tool({ params });
   } catch (error) {
     console.error(`Failed: ${error.message}`);
   }
   ```

---

## Convergent Defaults Applied

1. ✅ **Always use PascalCase for interfaces**
2. ✅ **Always use camelCase for functions**
3. ✅ **Always preserve snake_case for filenames**
4. ✅ **Always include JSDoc comments**
5. ✅ **Always export from index.ts**
6. ✅ **Always generate README.md**
7. ✅ **Only log summaries, not full data**
8. ✅ **Process data in execution environment**

---

## Token Comparison

**Traditional MCP (loading tool definition upfront):**
```
Tool definition: ~800 tokens
3 tool calls with results: ~3,000 tokens
Total: ~3,800 tokens
```

**Code-based MCP:**
```
Import statement: ~50 tokens
3 function calls (results in variables): ~200 tokens
Summary logs: ~100 tokens
Total: ~350 tokens
```

**Savings: 91% reduction** (3,800 → 350 tokens)

---

## Next Steps

This example demonstrates:
- ✅ How to convert a real MCP schema to TypeScript
- ✅ What the file structure should look like
- ✅ How to use generated code efficiently
- ✅ Patterns for token optimization

From this, we can extract the rules and templates for the skill.
