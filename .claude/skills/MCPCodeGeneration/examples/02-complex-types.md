# Example 2: Complex Types and Nested Objects

## Scenario

MCP tool with arrays, nested objects, and enums.

## Input: MCP Tool Schema

```json
{
  "name": "create_task",
  "description": "Create a new task with assignees and labels",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Task title"
      },
      "assignees": {
        "type": "array",
        "items": { "type": "string" },
        "description": "List of user IDs to assign"
      },
      "labels": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Task labels/tags"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "description": "Task priority level"
      },
      "metadata": {
        "type": "object",
        "properties": {
          "dueDate": { "type": "string" },
          "estimatedHours": { "type": "number" },
          "category": { "type": "string" }
        },
        "description": "Additional task metadata"
      },
      "attachments": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "filename": { "type": "string" },
            "url": { "type": "string" },
            "size": { "type": "integer" }
          }
        },
        "description": "File attachments"
      }
    },
    "required": ["title", "priority"]
  }
}
```

## Generated Output

### Step 1: Convert Complex Types

**Arrays of primitives:**
```typescript
assignees?: Array<string>
labels?: Array<string>
```

**Enum:**
```typescript
priority: "low" | "medium" | "high" | "urgent"
```

**Nested object:**
```typescript
metadata?: {
  dueDate?: string;
  estimatedHours?: number;
  category?: string;
}
```

**Array of objects:**
```typescript
attachments?: Array<{
  filename?: string;
  url?: string;
  size?: number;
}>
```

### Step 2: Complete Interface

```typescript
interface CreateTaskInput {
  /** Task title */
  title: string;
  
  /** List of user IDs to assign */
  assignees?: Array<string>;
  
  /** Task labels/tags */
  labels?: Array<string>;
  
  /** Task priority level */
  priority: "low" | "medium" | "high" | "urgent";
  
  /** Additional task metadata */
  metadata?: {
    dueDate?: string;
    estimatedHours?: number;
    category?: string;
  };
  
  /** File attachments */
  attachments?: Array<{
    filename?: string;
    url?: string;
    size?: number;
  }>;
}
```

### Alternative: Extract Nested Types

For better readability with complex nested objects:

```typescript
interface TaskMetadata {
  dueDate?: string;
  estimatedHours?: number;
  category?: string;
}

interface TaskAttachment {
  filename?: string;
  url?: string;
  size?: number;
}

interface CreateTaskInput {
  /** Task title */
  title: string;
  
  /** List of user IDs to assign */
  assignees?: Array<string>;
  
  /** Task labels/tags */
  labels?: Array<string>;
  
  /** Task priority level */
  priority: "low" | "medium" | "high" | "urgent";
  
  /** Additional task metadata */
  metadata?: TaskMetadata;
  
  /** File attachments */
  attachments?: Array<TaskAttachment>;
}
```

### Step 3: Complete File

**File: `${PAI_DIR}/servers/project-management/tools/create_task.ts`**

```typescript
interface TaskMetadata {
  dueDate?: string;
  estimatedHours?: number;
  category?: string;
}

interface TaskAttachment {
  filename?: string;
  url?: string;
  size?: number;
}

interface CreateTaskInput {
  /** Task title */
  title: string;
  
  /** List of user IDs to assign */
  assignees?: Array<string>;
  
  /** Task labels/tags */
  labels?: Array<string>;
  
  /** Task priority level */
  priority: "low" | "medium" | "high" | "urgent";
  
  /** Additional task metadata */
  metadata?: TaskMetadata;
  
  /** File attachments */
  attachments?: Array<TaskAttachment>;
}

interface CreateTaskOutput {
  [key: string]: any;
}

/**
 * Create a new task with assignees and labels
 * 
 * @param input - Task creation parameters
 * @returns Created task object
 * 
 * @example
 * ```typescript
 * const task = await createTask({
 *   title: 'Implement feature X',
 *   priority: 'high',
 *   assignees: ['user-123', 'user-456'],
 *   labels: ['feature', 'backend'],
 *   metadata: {
 *     dueDate: '2025-02-01',
 *     estimatedHours: 8
 *   }
 * });
 * ```
 */
export async function createTask(
  input: CreateTaskInput
): Promise<CreateTaskOutput> {
  return callMCPTool('project_management__create_task', input);
}
```

## Usage Examples

### Example 1: Minimal Task

```typescript
// From PAI root
import { createTask } from './servers/project-management';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { createTask } from '../../../../servers/project-management';

const task = await createTask({
  title: 'Review PR #123',
  priority: 'medium'
});

console.log(`Created task: ${task.id}`);
```

### Example 2: Full Featured Task

```typescript
const task = await createTask({
  title: 'Build authentication system',
  priority: 'high',
  assignees: ['user-001', 'user-002'],
  labels: ['security', 'backend', 'high-priority'],
  metadata: {
    dueDate: '2025-02-15',
    estimatedHours: 40,
    category: 'infrastructure'
  },
  attachments: [
    {
      filename: 'spec.pdf',
      url: 'https://example.com/spec.pdf',
      size: 1024000
    }
  ]
});

console.log(`Created task ${task.id} with ${assignees.length} assignees`);
```

### Example 3: Batch Creation with Filtering

```typescript
const taskSpecs = [
  { title: 'Task 1', priority: 'low' as const },
  { title: 'Task 2', priority: 'high' as const },
  { title: 'Task 3', priority: 'medium' as const }
];

const results = await Promise.all(
  taskSpecs.map(spec => createTask(spec))
);

// Filter high priority tasks only
const highPriorityIds = results
  .filter(task => task.priority === 'high')
  .map(task => task.id);

console.log(`Created ${results.length} tasks, ${highPriorityIds.length} high priority`);
```

## Common Patterns for Complex Types

### Pattern 1: Array of Primitives

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
tags?: Array<string>
// OR prefer this for simplicity:
tags?: string[]
```

### Pattern 2: Array of Objects

**JSON Schema:**
```json
{
  "items": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    }
  }
}
```

**TypeScript (inline):**
```typescript
items?: Array<{
  id?: string;
  name?: string;
}>
```

**TypeScript (extracted):**
```typescript
interface Item {
  id?: string;
  name?: string;
}

// In main interface:
items?: Array<Item>
```

### Pattern 3: Enum Values

**JSON Schema:**
```json
{
  "status": {
    "type": "string",
    "enum": ["pending", "active", "completed"]
  }
}
```

**TypeScript:**
```typescript
status?: "pending" | "active" | "completed"
```

### Pattern 4: Nested Objects

**JSON Schema:**
```json
{
  "config": {
    "type": "object",
    "properties": {
      "timeout": { "type": "number" },
      "retries": { "type": "integer" }
    }
  }
}
```

**TypeScript (inline):**
```typescript
config?: {
  timeout?: number;
  retries?: number;
}
```

**TypeScript (extracted):**
```typescript
interface Config {
  timeout?: number;
  retries?: number;
}

// In main interface:
config?: Config
```

## When to Extract Types

**Extract to separate interface when:**
- Used in multiple places
- More than 3 nested properties
- Improves readability significantly
- Represents a clear domain concept

**Keep inline when:**
- Used only once
- Simple (2-3 properties)
- Not a reusable concept

## Key Takeaways

1. ✅ Arrays map to `Array<T>` or `T[]`
2. ✅ Enums map to union types: `"A" | "B" | "C"`
3. ✅ Nested objects can be inline or extracted
4. ✅ Extract types when reused or complex
5. ✅ Use `const` assertion for enum literals in usage
6. ✅ All nested properties follow same optional rules
