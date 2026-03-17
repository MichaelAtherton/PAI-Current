# Example 3: Token-Efficient Usage Patterns

## The Problem

Traditional MCP usage loads all results into context, consuming massive amounts of tokens unnecessarily.

## Scenario: Processing Customer Data

You need to fetch customer data, filter it, transform it, and save to a CRM.

---

## ❌ INEFFICIENT: Traditional MCP Approach

### What Happens

```
USER: "Get customers from sheet and add active ones to Salesforce"

AGENT: 
1. TOOL CALL: sheets.get_data(sheetId: 'customers')
   → Returns 1,000 customer records (loaded into context)
   → Token cost: ~15,000 tokens

2. TOOL CALL: salesforce.create_lead(customer_data_1)
   → Token cost: ~200 tokens

3. TOOL CALL: salesforce.create_lead(customer_data_2)
   → Token cost: ~200 tokens

... (repeated 1,000 times)

TOTAL TOKEN COST: ~215,000 tokens
RESULT: Context window exceeded, request fails
```

### The Issues

1. **Full dataset in context** - All 1,000 records loaded
2. **Repeated data** - Each customer passed through context multiple times
3. **No filtering** - Inactive customers also loaded into context
4. **Context overflow** - Exceeds typical 200k token limit

---

## ✅ EFFICIENT: Code-Based Approach

### Generated Wrappers

```typescript
// ${PAI_DIR}/servers/sheets/tools/get_data.ts
export async function getData(input: GetDataInput): Promise<GetDataOutput> {
  return callMCPTool('sheets__get_data', input);
}

// ${PAI_DIR}/servers/salesforce/tools/create_lead.ts
export async function createLead(input: CreateLeadInput): Promise<CreateLeadOutput> {
  return callMCPTool('salesforce__create_lead', input);
}
```

### Efficient Code

```typescript
// From PAI root
import { getData } from './servers/sheets';
import { createLead } from './servers/salesforce';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { getData } from '../../../../servers/sheets';
// import { createLead } from '../../../../servers/salesforce';

// Fetch data (stays in execution environment)
const allCustomers = await getData({ sheetId: 'customers' });

// Filter in execution environment (not context)
const activeCustomers = allCustomers.filter(c => c.status === 'active');

// Track results
let successCount = 0;
let errorCount = 0;

// Process each (data flows directly, not through context)
for (const customer of activeCustomers) {
  try {
    await createLead({
      firstName: customer.firstName,
      lastName: customer.lastName,
      email: customer.email,
      company: customer.company
    });
    successCount++;
  } catch (error) {
    errorCount++;
  }
}

// Only summary to context
console.log(`Processed ${activeCustomers.length} active customers`);
console.log(`Success: ${successCount}, Errors: ${errorCount}`);
```

### Token Breakdown

```
Import statements: ~80 tokens
getData call: ~40 tokens
Filter operation: ~30 tokens
Loop (structure, not data): ~50 tokens
Summary logging: ~60 tokens

TOTAL: ~260 tokens
```

### Token Savings

```
Traditional: ~215,000 tokens (fails)
Code-based: ~260 tokens (succeeds)
Savings: 99.9%
```

---

## Pattern 1: Filter Before Logging

### ❌ Bad: Full Data to Context

```typescript
const data = await getTool({ id: 'sheet-123' });
console.log('Data:', data); // 10,000 rows in context
```

**Cost:** ~150,000 tokens

### ✅ Good: Filter Then Summarize

```typescript
const data = await getTool({ id: 'sheet-123' });
const filtered = data.filter(row => row.status === 'active');
console.log(`Found ${filtered.length} active of ${data.length} total`);
```

**Cost:** ~50 tokens  
**Savings:** 99.97%

### ✅ Even Better: Show Sample

```typescript
const data = await getTool({ id: 'sheet-123' });
const filtered = data.filter(row => row.status === 'active');

console.log(`Found ${filtered.length} active records`);
console.log('Sample:', filtered.slice(0, 3)); // First 3 only
```

**Cost:** ~200 tokens (includes 3 samples)  
**Savings:** 99.87%

---

## Pattern 2: Aggregate Before Reporting

### ❌ Bad: Return All Data

```typescript
const orders = await getOrders({ dateRange: '2025-01' });
console.log('Orders:', orders); // 5,000 orders
```

**Cost:** ~75,000 tokens

### ✅ Good: Calculate Statistics

```typescript
const orders = await getOrders({ dateRange: '2025-01' });

const stats = {
  total: orders.length,
  totalRevenue: orders.reduce((sum, o) => sum + o.amount, 0),
  avgOrderValue: orders.reduce((sum, o) => sum + o.amount, 0) / orders.length,
  byStatus: {
    pending: orders.filter(o => o.status === 'pending').length,
    completed: orders.filter(o => o.status === 'completed').length,
    cancelled: orders.filter(o => o.status === 'cancelled').length
  }
};

console.log('Order statistics:', stats);
```

**Cost:** ~150 tokens  
**Savings:** 99.8%

---

## Pattern 3: Chain Without Context

### ❌ Bad: Multiple Tool Calls Through Context

```typescript
// Each result flows through context
const doc = await gdrive.getDocument({ id: 'abc123' });
// doc content: 50,000 tokens in context

const processed = await transform.process({ content: doc.content });
// processed content: 50,000 tokens in context again

await salesforce.save({ data: processed });
// data: 50,000 tokens in context again

TOTAL: 150,000 tokens
```

### ✅ Good: Variables Keep Data Out

```typescript
// Data stays in variables (execution environment)
const doc = await gdrive.getDocument({ id: 'abc123' });
const processed = await transform.process({ content: doc.content });
await salesforce.save({ data: processed });

console.log('Document processed and saved');

TOTAL: ~50 tokens
```

**Savings:** 99.97%

---

## Pattern 4: Batch Processing

### ❌ Bad: Individual Results to Context

```typescript
const ids = ['1', '2', '3', ... '100'];

for (const id of ids) {
  const result = await process({ id });
  console.log(`Processed ${id}:`, result); // Each result in context
}
```

**Cost:** ~50,000 tokens (500 per result × 100)

### ✅ Good: Batch Summary

```typescript
const ids = ['1', '2', '3', ... '100'];
const results = [];

for (const id of ids) {
  const result = await process({ id });
  results.push(result);
}

console.log(`Processed ${results.length} items`);
console.log(`Successful: ${results.filter(r => r.success).length}`);
console.log(`Failed: ${results.filter(r => !r.success).length}`);
```

**Cost:** ~100 tokens  
**Savings:** 99.8%

---

## Pattern 5: Privacy-Preserving Flows

### ❌ Bad: PII Exposed to Context

```typescript
const customers = await getCustomers();
console.log('Customers:', customers); // Emails, phones visible

for (const c of customers) {
  console.log(`Processing ${c.email}`); // PII in context
  await createLead({ email: c.email, phone: c.phone });
}
```

**Issues:**
- Personal data in context
- Could be logged/stored
- Compliance risk

### ✅ Good: PII Never Enters Context

```typescript
const customers = await getCustomers();

// Process without logging PII
for (const c of customers) {
  await createLead({
    email: c.email,    // Flows directly, never logged
    phone: c.phone,    // Flows directly, never logged
    name: c.name       // Flows directly, never logged
  });
}

console.log(`Imported ${customers.length} leads`); // Only count
```

**Benefits:**
- Zero PII in context
- Compliant with privacy regulations
- Safe for logging/auditing

---

## Pattern 6: Error Handling

### ❌ Bad: Full Errors to Context

```typescript
try {
  const result = await process({ id: 'xyz' });
  console.log('Result:', result); // Full result
} catch (error) {
  console.log('Error:', error); // Full stack trace
}
```

### ✅ Good: Error Summary Only

```typescript
try {
  const result = await process({ id: 'xyz' });
  console.log('Processing completed successfully');
} catch (error) {
  console.log(`Error: ${error.message}`); // Message only
}
```

---

## Real-World Example: Weekly Report Generation

### Task

Generate weekly sales report from multiple sources:
1. Fetch orders from database (10,000 rows)
2. Fetch leads from CRM (5,000 rows)
3. Fetch pipeline data (2,000 opportunities)
4. Calculate metrics
5. Generate summary report

### ❌ Traditional MCP: FAILS

```
Token requirements:
- Orders: ~150,000 tokens
- Leads: ~75,000 tokens
- Pipeline: ~30,000 tokens
- Tool definitions: ~2,000 tokens
TOTAL: ~257,000 tokens → EXCEEDS CONTEXT WINDOW
```

### ✅ Code-Based: SUCCEEDS

```typescript
// From PAI root
import { queryOrders } from './servers/database';
import { getLeads } from './servers/crm';
import { getPipeline } from './servers/crm';
import { createReport } from './servers/reporting';

// From a skill tool (.claude/skills/SomeSkill/tools/Tool.ts)
// import { queryOrders } from '../../../../servers/database';
// import { getLeads } from '../../../../servers/crm';
// import { getPipeline } from '../../../../servers/crm';
// import { createReport } from '../../../../servers/reporting';

// Fetch all data (stays in execution environment)
const [orders, leads, pipeline] = await Promise.all([
  queryOrders({ dateRange: 'THIS_WEEK' }),
  getLeads({ createdThisWeek: true }),
  getPipeline({ status: 'open' })
]);

// Calculate metrics in environment
const metrics = {
  ordersCount: orders.length,
  ordersRevenue: orders.reduce((sum, o) => sum + o.amount, 0),
  newLeads: leads.length,
  pipelineValue: pipeline.reduce((sum, p) => sum + p.amount, 0)
};

// Generate report with metrics (not raw data)
const report = await createReport({
  title: 'Weekly Sales Report',
  metrics
});

console.log('Report generated successfully');
console.log(`Orders: ${metrics.ordersCount} ($${metrics.ordersRevenue.toLocaleString()})`);
console.log(`New leads: ${metrics.newLeads}`);
console.log(`Pipeline: $${metrics.pipelineValue.toLocaleString()}`);
```

**Token cost:** ~400 tokens  
**vs Traditional:** Would fail (257k tokens)

---

## Summary: Token Efficiency Checklist

When using generated MCP wrappers:

- [ ] ✅ Fetch data into variables
- [ ] ✅ Process/filter in execution environment
- [ ] ✅ Only log summaries/counts/samples
- [ ] ✅ Chain operations with variables
- [ ] ✅ Batch process without intermediate logs
- [ ] ✅ Keep PII out of context
- [ ] ✅ Log error messages only (not stacks)
- [ ] ✅ Calculate aggregates before reporting
- [ ] ✅ Use first N items for samples
- [ ] ✅ Think: "What's the minimum information needed in context?"

## Expected Results

Following these patterns typically yields:
- **90-99% token reduction**
- **Faster response times** (less for model to process)
- **Better privacy** (sensitive data not in context)
- **Scalability** (can handle larger datasets)
- **Reliability** (won't exceed context limits)
