# Examples & Reference Guide

This directory contains step-by-step tutorials and complete reference materials to help you master MCP code generation.

## Learning Path

Follow these materials in order for the best learning experience:

### 1. Basic Conversion (examples/01-basic-conversion.md)
**What you'll learn:**
- Converting simple JSON Schema to TypeScript interfaces
- Handling required vs optional parameters
- Basic types: string, number, boolean, integer
- Generating function signatures with JSDoc

**Example scenario:** Converting a `get_document` tool with basic parameters

### 2. Complex Types (examples/02-complex-types.md)
**What you'll learn:**
- Arrays and nested arrays
- Nested objects and complex structures
- Enum types and union types
- anyOf/oneOf conversions
- Additional properties handling

**Example scenarios:** Multiple tools showing progressively complex type patterns

### 3. Token Efficiency (examples/03-token-efficiency.md)
**What you'll learn:**
- Real-world before/after token comparisons
- Data aggregation patterns
- Privacy-preserving workflows
- Multi-tool chaining techniques
- When to use code vs direct tool calls

**Example scenarios:** Large dataset processing, customer data migration, report generation

### 4. Complete Example (reference/complete-example.md)
**What you'll learn:**
- Full end-to-end server generation
- From MCP schema to working TypeScript code
- Complete file organization
- Testing and validation
- Production deployment considerations

**Example scenario:** Building a complete Slack MCP server wrapper from scratch

## Quick Reference

### When to Use Each Resource

| Resource | Use When |
|----------|----------|
| 01-basic-conversion.md | Starting from scratch, need fundamentals |
| 02-complex-types.md | Dealing with arrays, unions, nested objects |
| 03-token-efficiency.md | Optimizing token usage, privacy concerns |
| complete-example.md | Need full end-to-end reference |

### Time Investment

- **Basic Conversion:** 15 minutes
- **Complex Types:** 25 minutes  
- **Token Efficiency:** 20 minutes
- **Complete Example:** 30 minutes
- **Total:** ~90 minutes for complete mastery

## What's Covered

### Type Conversions
- ✅ String, number, boolean, integer
- ✅ Arrays (simple and nested)
- ✅ Objects (flat and nested)
- ✅ Enums and literal types
- ✅ Union types (anyOf, oneOf)
- ✅ Additional properties
- ✅ Required vs optional fields

### Code Generation
- ✅ Interface generation
- ✅ Function signatures
- ✅ JSDoc comments
- ✅ File organization
- ✅ Export patterns
- ✅ Naming conventions

### Token Efficiency
- ✅ Before/after comparisons
- ✅ Real token counts
- ✅ Aggregation patterns
- ✅ Privacy preservation
- ✅ Multi-tool workflows
- ✅ When to skip code generation

### Best Practices
- ✅ Error handling
- ✅ Type safety
- ✅ Documentation standards
- ✅ Testing approaches
- ✅ Production readiness

## Hands-On Practice

Each example includes:
1. **Input Schema** - The raw MCP tool definition
2. **Step-by-Step Process** - What to analyze and how
3. **Generated Code** - The complete TypeScript output
4. **Usage Examples** - How to use the generated code
5. **Token Analysis** - Efficiency metrics and comparisons

## What You'll Be Able to Do

After working through these materials, you'll be able to:

✅ Convert any MCP server schema to TypeScript wrappers  
✅ Handle complex nested types and unions  
✅ Achieve 90-98% token reduction in multi-tool workflows  
✅ Build privacy-preserving data pipelines  
✅ Create production-ready server wrappers  
✅ Understand when to use code vs direct tool calls  
✅ Debug and troubleshoot type issues  
✅ Optimize for both performance and maintainability  

## Integration with Main Package

These examples complement the main documentation:

- **SKILL.md** - Complete specification (reference here for details)
- **QUICK_REFERENCE.md** - Fast lookup (reference here for syntax)
- **USAGE.md** - Production patterns (reference here for real-world use)
- **Templates/** - Copy-paste starting points (use after learning here)

## Getting Help

If you get stuck:

1. **Check QUICK_REFERENCE.md** for syntax reminders
2. **Review SKILL.md** for the complete specification
3. **Look at templates/** for correct structure
4. **Read USAGE.md** for production patterns

## Contributing

Found an issue or want to suggest improvements? These examples are meant to be clear and comprehensive. Feedback welcome!

---

**Ready to start?** Begin with `01-basic-conversion.md` and work your way through!
