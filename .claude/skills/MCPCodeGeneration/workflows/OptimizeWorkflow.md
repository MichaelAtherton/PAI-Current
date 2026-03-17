# OptimizeWorkflow Workflow

**Purpose:** Optimize existing MCP tool usage for token efficiency.

---

## Step 1: Analyze Current Usage

Review the user's code for these anti-patterns:

### Anti-Pattern 1: Logging Full Results
```typescript
// BAD: Entire response in context
const data = await mcpTool({ id });
console.log(data);
```

### Anti-Pattern 2: Sequential Tool Calls Through Context
```typescript
// BAD: Each result flows through model context
TOOL CALL: getData({ id: 1 })
→ [large response in context]
TOOL CALL: getData({ id: 2 })
→ [large response in context]
```

### Anti-Pattern 3: Intermediate Results in Context
```typescript
// BAD: Transform results visible to model
const raw = await fetch();
// [raw data in context]
const transformed = transform(raw);
// [transformed data also in context]
```

### Anti-Pattern 4: PII Exposure
```typescript
// BAD: Sensitive data logged
console.log(customers); // emails, phones visible
```

---

## Step 2: Identify Optimization Opportunities

For each anti-pattern found, note:

1. **Location** - file and line
2. **Pattern** - which anti-pattern
3. **Data size** - estimated tokens consumed
4. **Fix** - recommended optimization

---

## Step 3: Apply Token-Efficient Patterns

### Fix 1: Aggregate Before Logging

```typescript
// GOOD: Only summary in context
const data = await mcpTool({ id });
const summary = {
  total: data.items.length,
  active: data.items.filter(i => i.active).length
};
console.log(`Summary:`, summary);
```

### Fix 2: Process in Execution Environment

```typescript
// GOOD: Loop in code, single summary output
const ids = ['1', '2', '3'];
let processed = 0;

for (const id of ids) {
  const data = await getData({ id });
  await saveData({ data });
  processed++;
}

console.log(`Processed ${processed} items`);
```

### Fix 3: Chain With Variables

```typescript
// GOOD: Variables keep data out of context
const raw = await fetch();
const transformed = raw.items.map(i => ({ ...i, processed: true }));
await save({ items: transformed });
console.log(`Saved ${transformed.length} items`);
```

### Fix 4: Privacy-Preserving Flows

```typescript
// GOOD: PII never logged
const customers = await getCustomers();
for (const c of customers) {
  await createLead({ email: c.email, phone: c.phone });
}
console.log(`Imported ${customers.length} leads`);
```

---

## Step 4: Refactor Code

Apply the fixes identified in Step 2:

1. Replace `console.log(fullData)` with summary logging
2. Convert sequential tool calls to loops with aggregation
3. Move data transformations into code blocks
4. Remove PII from any logged output

---

## Step 5: Verify Optimization

Check that:
- [ ] No full datasets logged to context
- [ ] No PII visible in conversation
- [ ] Loops process data without intermediate logging
- [ ] Final output contains only summaries/counts

---

## Step 6: Report Results

Provide to user:

```
## Optimization Report

### Changes Made
- [List of specific changes]

### Token Savings
- Before: ~X,XXX tokens per operation
- After: ~XXX tokens per operation
- Reduction: XX%

### Privacy Improvements
- [List any PII that was removed from logging]

### Next Steps
- [Any additional recommendations]
```

---

## Common Optimizations by Use Case

### Large Dataset Processing
```typescript
// Process 1000 records, report 1 summary
const records = await getRecords({ limit: 1000 });
const stats = {
  total: records.length,
  byStatus: records.reduce((acc, r) => {
    acc[r.status] = (acc[r.status] || 0) + 1;
    return acc;
  }, {})
};
console.log(`Processed:`, stats);
```

### Multi-Tool Workflows
```typescript
// Chain 3 tools, report 1 result
const source = await toolA();
const transformed = await toolB({ data: source.data });
const result = await toolC({ input: transformed.output });
console.log(`Workflow complete: ${result.id}`);
```

### Batch Operations
```typescript
// Process N items, report success/failure counts
const results = { success: 0, failed: 0 };
for (const item of items) {
  try {
    await processItem(item);
    results.success++;
  } catch {
    results.failed++;
  }
}
console.log(`Batch complete:`, results);
```
