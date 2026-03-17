---
name: MCPServerBuilder
description: Build production-ready MCP servers using Docker and FastMCP. USE WHEN user mentions build MCP server, create MCP server, MCP development, new MCP tools, OR wants to create tools for Claude Desktop. Generates complete server code, Docker configuration, and installation instructions following MCP best practices.
---

# MCPServerBuilder - MCP Server Development Skill

Build complete, production-ready MCP (Model Context Protocol) servers with Docker and FastMCP.

## Workflow Routing

**When executing a workflow, call the notification script via Bash:**

```bash
${PAI_DIR}/tools/skill-workflow-notification [WorkflowName] MCPServerBuilder
```

| Workflow | Trigger | File |
|----------|---------|------|
| **BuildServer** | "build MCP server", "create MCP server" | `workflows/BuildServer.md` |
| **GenerateCompleteGuide** | "generate MCP guide", "complete guide", "single file output" | `workflows/GenerateCompleteGuide.md` |

### Workflow Comparison

| Aspect | BuildServer | GenerateCompleteGuide |
|--------|-------------|----------------------|
| **Output** | 5 separate files | 1 comprehensive guide file |
| **Use case** | Direct file creation | Copy-paste instructions |
| **Best for** | Immediate development | Sharing/documentation |

## Examples

**Example 1: Build a weather MCP server**
```
User: "Build an MCP server for OpenWeatherMap API"
→ Invokes BuildServer workflow
→ Gathers requirements (API key, endpoints, features)
→ Generates 5 files: Dockerfile, requirements.txt, server.py, readme.txt, CLAUDE.md
→ Provides complete installation instructions with catalog setup
→ User gets working MCP server with tools for weather data
```

**Example 2: Build a database query MCP server**
```
User: "Create an MCP server to query my PostgreSQL database"
→ Invokes BuildServer workflow
→ Asks for database connection details and query requirements
→ Generates server with proper input sanitization and error handling
→ Includes Docker secrets configuration for credentials
→ User gets secure MCP server with database query tools
```

**Example 3: Build a file operations MCP server**
```
User: "I need MCP tools to work with files in a specific directory"
→ Invokes BuildServer workflow
→ Creates server with file read, write, list tools
→ Implements proper file path validation and security
→ Generates volume mount configuration for Docker
→ User gets file management tools in Claude Desktop
```

**Example 4: Generate a complete guide for Trello MCP server**
```
User: "Generate a complete guide for a Trello MCP server"
→ Invokes GenerateCompleteGuide workflow
→ Gathers Trello API requirements and tools needed
→ Outputs SINGLE FILE: trello-mcp-complete-guide.md
→ File contains all 5 files + Docker installation instructions
→ User copies file content and follows step-by-step setup
```

## Key Features

### Critical Rules Enforced

The BuildServer workflow ensures compliance with these MCP best practices:

1. **No breaking decorators** - Never uses `@mcp.prompt()` or `prompt` parameter
2. **Single-line docstrings only** - Multi-line docstrings cause gateway panic errors
3. **Empty string defaults** - Uses `param: str = ""` not `param: str = None`
4. **String returns always** - All tools return formatted strings with emojis
5. **Docker-based** - Every server runs in a secure container
6. **Proper error handling** - Graceful failures with user-friendly messages

### Complete File Generation

**BuildServer workflow** generates exactly 5 files for every MCP server:

- **Dockerfile** - Python slim with non-root user
- **requirements.txt** - mcp[cli] and dependencies
- **[server_name]_server.py** - FastMCP server with tools
- **readme.txt** - Complete documentation and troubleshooting
- **CLAUDE.md** - Implementation guide and development notes

**GenerateCompleteGuide workflow** outputs a single comprehensive file containing:
- All 5 file contents (copy-paste ready)
- Complete Docker MCP gateway installation instructions
- Catalog YAML configuration
- Claude Desktop setup steps

### Installation Instructions

Provides step-by-step setup including:

1. Docker image build
2. Secret configuration (if needed)
3. Custom catalog creation
4. Registry updates
5. Claude Desktop configuration
6. Testing and verification

## Implementation Patterns

The workflow includes proven patterns for:

- **API Integration** - httpx with proper timeout and error handling
- **System Commands** - subprocess with security considerations
- **File Operations** - Safe file access with validation
- **Output Formatting** - Consistent emoji usage and multi-line formatting

## Security Model

All generated servers follow these security practices:

- Secrets stored in Docker Desktop secrets (never hardcoded)
- Non-root container execution
- Input sanitization on all parameters
- Sensitive data never logged
- Error messages sanitized to prevent information leakage
