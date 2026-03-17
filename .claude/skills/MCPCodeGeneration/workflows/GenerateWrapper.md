# GenerateWrapper Workflow

**Purpose:** Generate TypeScript wrapper code from an MCP server schema.

---

## Step 1: Obtain the MCP Server Schema

Get the schema from one of these sources:

**Option A: From running server**
```bash
# Use MCP inspector or direct call to tools/list
```

**Option B: From user-provided JSON**
The user provides the schema directly.

**Option C: From existing MCP connection**
Query the server's `tools/list` endpoint.

---

## Step 2: Analyze the Schema

For each tool in the schema, extract:

1. **Tool name** - for function naming
2. **Description** - for JSDoc
3. **Input schema** - for TypeScript interface
4. **Required fields** - for optional vs required parameters
5. **Output schema** - if provided, otherwise use `any`

---

## Step 3: Generate TypeScript Interfaces

Apply JSON Schema to TypeScript conversion rules from SKILL.md Part 2:

```
type: "string"    →  string
type: "number"    →  number
type: "integer"   →  number
type: "boolean"   →  boolean
type: "array"     →  Array<T>
type: "object"    →  interface or Record<string, any>
enum: [...]       →  union type
```

Mark fields in `required` array as required, others as optional with `?`.

---

## Step 4: Generate Wrapper Functions

For each tool, create a wrapper file following the template:

```typescript
// FILE: ${PAI_DIR}/servers/{server-name}/tools/{tool_name}.ts

interface {ToolNamePascal}Input {
  /** {description} */
  {paramName}: {type};
}

interface {ToolNamePascal}Output {
  [key: string]: any;
}

/**
 * {tool description}
 *
 * @param input - Input parameters
 * @returns Tool output
 *
 * @example
 * ```typescript
 * const result = await {toolNameCamel}({ ... });
 * ```
 */
export async function {toolNameCamel}(
  input: {ToolNamePascal}Input
): Promise<{ToolNamePascal}Output> {
  return callMCPTool('{server}__{tool}', input);
}
```

---

## Step 5: Create Index File

Generate `${PAI_DIR}/servers/{server-name}/index.ts`:

```typescript
/**
 * {Server Name} MCP Server
 * Generated: {date}
 * Tools: {count}
 */

export { tool1 } from './tools/tool_1';
export { tool2 } from './tools/tool_2';

export type { Tool1Input, Tool1Output } from './tools/tool_1';
export type { Tool2Input, Tool2Output } from './tools/tool_2';
```

---

## Step 6: Create README

Generate `${PAI_DIR}/servers/{server-name}/README.md` with:

- Server description
- Available tools list
- Usage examples
- Token efficiency notes

---

## Step 7: Verify Output

Check that:
- [ ] All tool files compile (no TypeScript errors)
- [ ] Index exports all tools
- [ ] README documents all tools
- [ ] Naming conventions followed (camelCase functions, PascalCase interfaces)

---

## Output

Report to user:
- Number of tools wrapped
- Directory location
- Sample usage code
- Estimated token savings
