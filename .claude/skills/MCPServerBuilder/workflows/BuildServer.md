# BuildServer Workflow

**Purpose:** Build a complete, production-ready MCP server with Docker and FastMCP.

---

## Your Role

You are an expert MCP (Model Context Protocol) server developer. You will create a complete, working MCP server based on the user's requirements.

---

## Step 1: Gather Requirements

Ask the user for these details if not already provided:

1. **Service/Tool Name**: What service or functionality will this MCP server provide?
2. **API Documentation**: If this integrates with an API, get the documentation URL
3. **Required Features**: List the specific features/tools to implement
4. **Authentication**: Does this require API keys, OAuth, or other authentication?
5. **Data Sources**: Will this access files, databases, APIs, or other data sources?

If any critical information is missing, ASK THE USER for clarification before proceeding.

---

## Step 2: Review Critical Rules

**MUST FOLLOW - These prevent Claude Desktop from breaking:**

1. **NO `@mcp.prompt()` decorators** - They break Claude Desktop
2. **NO `prompt` parameter to FastMCP()** - It breaks Claude Desktop
3. **NO type hints from typing module** - No `Optional`, `Union`, `List[str]`, etc.
4. **NO complex parameter types** - Use `param: str = ""` not `param: str = None`
5. **SINGLE-LINE DOCSTRINGS ONLY** - Multi-line docstrings cause gateway panic errors
6. **DEFAULT TO EMPTY STRINGS** - Use `param: str = ""` never `param: str = None`
7. **ALWAYS return strings from tools** - All tools must return formatted strings
8. **ALWAYS use Docker** - The server must run in a Docker container
9. **ALWAYS log to stderr** - Use the logging configuration provided
10. **ALWAYS handle errors gracefully** - Return user-friendly error messages

---

## Step 3: Create Files

Create the MCP server files in the output directory.

### 3.1: Create Output Directory

```bash
mkdir -p ${PAI_DIR}/output/[SERVER_NAME]-mcp-server
```

Replace `[SERVER_NAME]` with the actual server name (e.g., `weather`, `postgres`, `github`).

### 3.2: Create File 1 - Dockerfile

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/Dockerfile`

**Content Template:**
```dockerfile
# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set Python unbuffered mode
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY [SERVER_NAME]_server.py .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Run the server
CMD ["python", "[SERVER_NAME]_server.py"]
```

### 3.3: Create File 2 - requirements.txt

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/requirements.txt`

**Content Template:**
```
mcp[cli]>=1.2.0
httpx
# Add any other required libraries based on the user's needs
```

### 3.4: Create File 3 - [SERVER_NAME]_server.py

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/[SERVER_NAME]_server.py`

**Content Template:**
```python
#!/usr/bin/env python3
"""
Simple [SERVICE_NAME] MCP Server - [DESCRIPTION]
"""
import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("[SERVER_NAME]-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("[SERVER_NAME]")

# Configuration
# Add any API keys, URLs, or configuration here
# API_TOKEN = os.environ.get("[SERVER_NAME_UPPER]_API_TOKEN", "")

# === UTILITY FUNCTIONS ===
# Add utility functions as needed

# === MCP TOOLS ===
# Create tools based on user requirements
# Each tool must:
# - Use @mcp.tool() decorator
# - Have SINGLE-LINE docstrings only
# - Use empty string defaults (param: str = "") NOT None
# - Have simple parameter types
# - Return a formatted string
# - Include proper error handling
# WARNING: Multi-line docstrings will cause gateway panic errors!

@mcp.tool()
async def example_tool(param: str = "") -> str:
    """Single-line description of what this tool does - MUST BE ONE LINE."""
    logger.info(f"Executing example_tool with {param}")

    try:
        # Implementation here
        result = "example"
        return f"✅ Success: {result}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting [SERVICE_NAME] MCP server...")

    # Add any startup checks
    # if not API_TOKEN:
    #     logger.warning("[SERVER_NAME_UPPER]_API_TOKEN not set")

    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
```

### 3.5: Create File 4 - README.md

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/README.md`

**Content Template:**
```md
# [SERVICE_NAME] MCP Server

A Model Context Protocol (MCP) server that [DESCRIPTION].

## Purpose

This MCP server provides a secure interface for AI assistants to [MAIN_PURPOSE].

## Features

### Current Implementation
- **`[tool_name_1]`** - [What it does]
- **`[tool_name_2]`** - [What it does]
[LIST ALL TOOLS]

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
[ADD ANY SERVICE-SPECIFIC REQUIREMENTS]

## Installation

See INSTALLATION.md for complete step-by-step instructions.

## Usage Examples

In Claude Desktop, you can ask:
- "[Natural language example 1]"
- "[Natural language example 2]"
[PROVIDE EXAMPLES FOR EACH TOOL]

## Architecture

```
Claude Desktop → MCP Gateway → [SERVICE_NAME] MCP Server → [SERVICE/API]
                     ↓
          Docker Desktop Secrets
            ([SECRET_NAMES])
```

## Development

### Local Testing

```bash
# Set environment variables for testing
export [SECRET_NAME]="test-value"

# Run directly
python [SERVER_NAME]_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python [SERVER_NAME]_server.py
```

### Adding New Tools

1. Add the function to `[SERVER_NAME]_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Authentication Errors
- Verify secrets with `docker mcp secret list`
- Ensure secret names match in code and catalog

## Security Considerations

- All secrets stored in Docker Desktop secrets
- Never hardcode credentials
- Running as non-root user
- Sensitive data never logged

## License

MIT License
```

### 3.6: Create File 5 - INSTALLATION.md

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/INSTALLATION.md`

**Content Template:**
```md
# Installation Instructions

Complete step-by-step guide to install and configure this MCP server.

## Step 1: Navigate to Project Directory

```bash
cd ${PAI_DIR}/output/[SERVER_NAME]-mcp-server
```

## Step 2: Build Docker Image

```bash
docker build -t [SERVER_NAME]-mcp-server .
```

## Step 3: Set Up Secrets (if needed)

```bash
# Only if the server needs API keys or secrets
docker mcp secret set [SECRET_NAME]="your-secret-value"

# Verify secrets
docker mcp secret list
```

## Step 4: Create Custom Catalog

```bash
# Create catalogs directory if it doesn't exist
mkdir -p ~/.docker/mcp/catalogs

# Create or edit custom.yaml
nano ~/.docker/mcp/catalogs/custom.yaml
```

Add this entry to custom.yaml:

```yaml
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  [SERVER_NAME]:
    description: "[DESCRIPTION]"
    title: "[SERVICE_NAME]"
    type: server
    dateAdded: "[CURRENT_DATE]"
    image: [SERVER_NAME]-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      - name: [tool_name_1]
      - name: [tool_name_2]
    secrets:
      - name: [SECRET_NAME]
        env: [ENV_VAR_NAME]
        example: [EXAMPLE_VALUE]
    metadata:
      category: [Choose: productivity|monitoring|automation|integration]
      tags:
        - [relevant_tag_1]
        - [relevant_tag_2]
      license: MIT
      owner: local
```

## Step 5: Update Registry

```bash
# Edit registry file
nano ~/.docker/mcp/registry.yaml
```

Add this entry under the existing `registry:` key:

```yaml
registry:
  # ... existing servers ...
  [SERVER_NAME]:
    ref: ""
```

**IMPORTANT**: The entry must be under the `registry:` key, not at the root level.

## Step 6: Configure Claude Desktop

Find your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Edit the file and add your custom catalog to the args array:

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-v", "[YOUR_HOME]/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

Replace `[YOUR_HOME]` with:
- **macOS**: `/Users/your_username`
- **Windows**: `C:\\Users\\your_username` (use double backslashes)
- **Linux**: `/home/your_username`

## Step 7: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. Your new tools should appear!

## Step 8: Test Your Server

```bash
# Verify it appears in the list
docker mcp server list

# If you don't see your server, check logs:
docker logs [container_name]
```

## Troubleshooting

### Docker Build Fails
- Check Python syntax in [SERVER_NAME]_server.py
- Verify all dependencies are in requirements.txt
- Check Docker daemon is running

### Server Not Appearing in Claude Desktop
- Verify catalog file syntax (YAML is whitespace-sensitive)
- Check registry.yaml has entry under `registry:` key
- Ensure Claude Desktop config includes custom catalog path
- Restart Claude Desktop completely

### Tools Not Working
- Check Docker logs: `docker logs [container_name]`
- Verify secrets are set: `docker mcp secret list`
- Test server directly: `python [SERVER_NAME]_server.py`

### Permission Errors
- Server runs as non-root user (mcpuser)
- Check file permissions if mounting volumes
- Verify Docker socket access
```

### 3.7: Generate Complete Guide (AUTOMATIC)

**This step is MANDATORY.** After creating the 5 individual files, ALWAYS generate a comprehensive single-file guide.

Use the Write tool to create:

**Path:** `${PAI_DIR}/output/[SERVER_NAME]-mcp-complete-guide.md`

This file MUST contain:

1. **SECTION 1: FILES TO CREATE** - All 5 file contents with full code (copy-paste ready)
2. **SECTION 2: INSTALLATION INSTRUCTIONS** - Complete Docker MCP gateway setup steps:
   - Step 1: Save the files
   - Step 2: Build Docker image
   - Step 3: Get credentials (if needed)
   - Step 4: Initial authentication (if OAuth)
   - Step 5: Set up Docker secrets
   - Step 6: Create custom catalog YAML (with ALL tools listed)
   - Step 7: Update registry.yaml
   - Step 8: Configure Claude Desktop config.json
   - Step 9: Restart Claude Desktop
   - Step 10: Test the server

**Template structure:**
```markdown
# [SERVICE_NAME] MCP Server - Complete Implementation Guide

This guide contains everything needed to build and deploy the [SERVICE_NAME] MCP server with Docker MCP gateway.

---

## SECTION 1: FILES TO CREATE

[Include full content of all 5 files with code blocks]

---

## SECTION 2: INSTALLATION INSTRUCTIONS FOR THE USER

[Include all 10 steps with commands and YAML/JSON configs]
```

See `workflows/GenerateCompleteGuide.md` for the full template.

### 3.8: Confirm File Creation

After creating all files, output this message to the user:

```
✅ MCP Server files created successfully!

📁 Files Location: ${PAI_DIR}/output/[SERVER_NAME]-mcp-server/
   - Dockerfile
   - requirements.txt
   - [SERVER_NAME]_server.py
   - README.md
   - INSTALLATION.md

📄 Complete Guide: ${PAI_DIR}/output/[SERVER_NAME]-mcp-complete-guide.md
   - Contains all files + Docker installation instructions in one document

Next steps:
1. Open the complete guide for copy-paste deployment
2. Or use individual files in the server directory
3. Follow the installation steps to deploy with Docker MCP gateway
```

---

## Implementation Patterns Reference

When implementing tools in the server, use these proven patterns:

### Correct Tool Implementation

```python
@mcp.tool()
async def fetch_data(endpoint: str = "", limit: str = "10") -> str:
    """Fetch data from API endpoint with optional limit."""
    # Check for empty strings, not just truthiness
    if not endpoint.strip():
        return "❌ Error: Endpoint is required"

    try:
        # Convert string parameters as needed
        limit_int = int(limit) if limit.strip() else 10
        # Implementation
        return f"✅ Fetched {limit_int} items"
    except ValueError:
        return f"❌ Error: Invalid limit value: {limit}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### API Integration Pattern

```python
async with httpx.AsyncClient() as client:
    try:
        response = await client.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Process and format data
        return f"✅ Result: {formatted_data}"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

### System Commands Pattern

```python
import subprocess

try:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=10,
        shell=True  # Only if needed
    )
    if result.returncode == 0:
        return f"✅ Output:\n{result.stdout}"
    else:
        return f"❌ Error:\n{result.stderr}"
except subprocess.TimeoutExpired:
    return "⏱️ Command timed out"
```

### File Operations Pattern

```python
try:
    with open(filename, 'r') as f:
        content = f.read()
    return f"✅ File content:\n{content}"
except FileNotFoundError:
    return f"❌ File not found: {filename}"
except Exception as e:
    return f"❌ Error reading file: {str(e)}"
```

---

## Output Formatting Guidelines

Use emojis for visual clarity:
- ✅ Success operations
- ❌ Errors or failures
- ⏱️ Time-related information
- 📊 Data or statistics
- 🔍 Search or lookup operations
- ⚡ Actions or commands
- 🔒 Security-related information
- 📁 File operations
- 🌐 Network operations
- ⚠️ Warnings

Format multi-line output clearly:

```python
return f"""📊 Results:
- Field 1: {value1}
- Field 2: {value2}
- Field 3: {value3}

Summary: {summary}"""
```

---

## Final Generation Checklist

Before completing, verify:

**Individual Files:**
- [ ] All 5 files created in `${PAI_DIR}/output/[SERVER_NAME]-mcp-server/`
- [ ] No @mcp.prompt() decorators used
- [ ] No prompt parameter in FastMCP()
- [ ] No complex type hints
- [ ] ALL tool docstrings are SINGLE-LINE only
- [ ] ALL parameters default to empty strings ("") not None
- [ ] All tools return strings
- [ ] Check for empty strings with .strip() not just truthiness
- [ ] Error handling in every tool
- [ ] All placeholders replaced with actual values
- [ ] Usage examples provided in README.md
- [ ] Security handled via Docker secrets
- [ ] Installation instructions complete and accurate
- [ ] Current date in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

**Complete Guide (MANDATORY):**
- [ ] `[SERVER_NAME]-mcp-complete-guide.md` created in `${PAI_DIR}/output/`
- [ ] SECTION 1 contains all 5 file contents (copy-paste ready)
- [ ] SECTION 2 contains all 10 Docker installation steps
- [ ] Custom catalog YAML includes ALL tools
- [ ] Claude Desktop config includes custom catalog path
- [ ] All placeholders replaced with actual values
