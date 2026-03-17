# Example 1: Basic Schema to TypeScript Conversion

## Scenario

You have a simple MCP tool with basic string and boolean parameters.

## Input: MCP Tool Schema

```json
{
  "name": "get_document",
  "description": "Retrieve a document from storage",
  "inputSchema": {
    "type": "object",
    "properties": {
      "documentId": {
        "type": "string",
        "description": "The unique identifier for the document"
      },
      "includeMetadata": {
        "type": "boolean",
        "description": "Whether to include document metadata in response"
      },
      "version": {
        "type": "integer",
        "description": "Specific version to retrieve (optional)"
      }
    },
    "required": ["documentId"]
  }
}
```

## Generated Output

### Step 1: Analyze Schema

- Tool name: `get_document`
- Required fields: `["documentId"]`
- Optional fields: `includeMetadata`, `version`
- Types: string, boolean, integer

### Step 2: Generate Interface

```typescript
interface GetDocumentInput {
  /** The unique identifier for the document */
  documentId: string;
  
  /** Whether to include document metadata in response */
  includeMetadata?: boolean;
  
  /** Specific version to retrieve (optional) */
  version?: number;
}
```

**Key observations:**
- `documentId` is required → no `?`
- `includeMetadata` is optional → has `?`
- `version` is optional → has `?`
- `integer` mapped to `number`
- Descriptions preserved as JSDoc comments

### Step 3: Generate Output Interface

Since no output schema provided:

```typescript
interface GetDocumentOutput {
  [key: string]: any;
}
```

### Step 4: Generate Function

```typescript
/**
 * Retrieve a document from storage
 * 
 * @param input - Document retrieval parameters
 * @param input.documentId - The unique identifier for the document
 * @param input.includeMetadata - Whether to include document metadata
 * @param input.version - Specific version to retrieve
 * @returns Document data
 * 
 * @example
 * ```typescript
 * const doc = await getDocument({
 *   documentId: 'doc-123'
 * });
 * ```
 * 
 * @example
 * ```typescript
 * const doc = await getDocument({
 *   documentId: 'doc-123',
 *   includeMetadata: true,
 *   version: 5
 * });
 * ```
 */
export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentOutput> {
  return callMCPTool('storage__get_document', input);
}
```

### Step 5: Complete File

**File: `${PAI_DIR}/servers/storage/tools/get_document.ts`**

```typescript
interface GetDocumentInput {
  /** The unique identifier for the document */
  documentId: string;
  
  /** Whether to include document metadata in response */
  includeMetadata?: boolean;
  
  /** Specific version to retrieve (optional) */
  version?: number;
}

interface GetDocumentOutput {
  [key: string]: any;
}

/**
 * Retrieve a document from storage
 * 
 * @param input - Document retrieval parameters
 * @returns Document data
 * 
 * @example
 * ```typescript
 * const doc = await getDocument({ documentId: 'doc-123' });
 * ```
 */
export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentOutput> {
  return callMCPTool('storage__get_document', input);
}
```

## Usage Example

```typescript
// From PAI root
import { getDocument } from './servers/storage';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { getDocument } from '../../../../servers/storage';

// Minimal required parameters
const doc1 = await getDocument({
  documentId: 'doc-123'
});

// With optional parameters
const doc2 = await getDocument({
  documentId: 'doc-456',
  includeMetadata: true,
  version: 3
});

// Type safety: this would be a TypeScript error
const doc3 = await getDocument({
  documentId: 'doc-789',
  invalidParam: true  // ❌ Error: property doesn't exist
});
```

## Token Efficiency

**Traditional MCP:**
```
Tool definition in context: ~150 tokens
Result 1 in context: ~500 tokens
Result 2 in context: ~500 tokens
Total: ~1,150 tokens
```

**Code-based:**
```
Import statement: ~30 tokens
Function calls: ~40 tokens
(Results stay in variables)
Total: ~70 tokens
```

**Savings: 94% reduction**

## Key Takeaways

1. ✅ Required fields have no `?` in TypeScript
2. ✅ Optional fields have `?` in TypeScript
3. ✅ `integer` maps to `number` in TypeScript
4. ✅ Descriptions become JSDoc comments
5. ✅ Function name is camelCase from snake_case
6. ✅ Interface names are PascalCase
7. ✅ Always include usage examples in JSDoc
