# GenerateCompleteGuide Workflow

**Purpose:** Generate a comprehensive single-file guide containing all MCP server files and complete Docker installation instructions that users can follow step-by-step.

---

## Your Role

You are an expert MCP (Model Context Protocol) server developer. You will create a complete, self-contained guide document that includes all file contents and installation instructions in a single file.

---

## Output Format

This workflow creates ONE output file: `${PAI_DIR}/output/[SERVER_NAME]-mcp-complete-guide.md`

This file contains TWO sections:
1. **SECTION 1: FILES TO CREATE** - Complete file contents for copy-paste
2. **SECTION 2: INSTALLATION INSTRUCTIONS** - Step-by-step Docker MCP gateway setup

---

## Step 1: Gather Requirements

Ask the user for these details if not already provided:

1. **Service/Tool Name**: What service or functionality will this MCP server provide?
2. **API Documentation**: If this integrates with an API, get the documentation URL
3. **Required Features**: List the specific features/tools to implement
4. **Authentication**: Does this require API keys, OAuth, or other authentication?
5. **Data Sources**: Will this access files, databases, APIs, or other data sources?

---

## Step 2: Generate the Complete Guide

Create the output file with the following structure:

```bash
mkdir -p ${PAI_DIR}/output
```

Write the complete guide to: `${PAI_DIR}/output/[SERVER_NAME]-mcp-complete-guide.md`

---

## Complete Guide Template

Use this template, replacing all placeholders:

````markdown
# [SERVICE_NAME] MCP Server - Complete Implementation Guide

This guide contains everything needed to build and deploy the [SERVICE_NAME] MCP server with Docker MCP gateway.

---

## SECTION 1: FILES TO CREATE

Create a directory for your project and save all files below:

```bash
mkdir [SERVER_NAME]-mcp-server
cd [SERVER_NAME]-mcp-server
```

---

### File 1: Dockerfile

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

---

### File 2: requirements.txt

```
mcp[cli]>=1.2.0
httpx
[ADD ANY OTHER REQUIRED LIBRARIES]
```

---

### File 3: [SERVER_NAME]_server.py

```python
#!/usr/bin/env python3
"""
Simple [SERVICE_NAME] MCP Server - [SHORT_DESCRIPTION]
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
[CONFIG_VARS - e.g., API_KEY = os.environ.get("API_KEY", "")]

# === UTILITY FUNCTIONS ===
[ADD UTILITY FUNCTIONS AS NEEDED]

# === MCP TOOLS ===
[IMPLEMENT ALL TOOLS HERE]

# Example tool structure:
@mcp.tool()
async def [tool_name]([param]: str = "") -> str:
    """[Single-line description of what this tool does]."""
    logger.info(f"Executing [tool_name] with {[param]}")

    if not [param].strip():
        return "❌ Error: [param] is required"

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

    # Add startup checks
    [ADD CONFIG VALIDATION IF NEEDED]

    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
```

---

### File 4: readme.txt

```
# [SERVICE_NAME] MCP Server

A Model Context Protocol (MCP) server that [DESCRIPTION].

## Purpose

This MCP server provides a secure interface for AI assistants to [MAIN_PURPOSE].

## Features

### Current Implementation

[LIST ALL TOOLS WITH DESCRIPTIONS]
- **`[tool_name_1]`** - [What it does]
- **`[tool_name_2]`** - [What it does]

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
[ADD SERVICE-SPECIFIC REQUIREMENTS - e.g., API credentials]

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:
[PROVIDE NATURAL LANGUAGE EXAMPLES FOR EACH TOOL]
- "[Example query 1]"
- "[Example query 2]"

## Architecture

```
Claude Desktop → MCP Gateway → [SERVICE_NAME] MCP Server → [SERVICE/API]
                       ↓
                Docker Desktop Secrets
                ([LIST SECRET NAMES])
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

1. Add the function to [SERVER_NAME]_server.py
2. Decorate with @mcp.tool()
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

### Troubleshooting

#### Tools Not Appearing
* Verify Docker image built successfully
* Check catalog and registry files
* Ensure Claude Desktop config includes custom catalog
* Restart Claude Desktop

#### Authentication Errors
* Verify secrets with `docker mcp secret list`
* Ensure secret names match in code and catalog
[ADD SERVICE-SPECIFIC TROUBLESHOOTING]

## Security Considerations

* All secrets stored in Docker Desktop secrets
* Never hardcode credentials
* Running as non-root user
* Sensitive data never logged
[ADD SERVICE-SPECIFIC SECURITY NOTES]

## License

MIT License
```

---

### File 5: CLAUDE.md

```markdown
# [SERVICE_NAME] MCP Server Implementation Guide

## Overview
This MCP server provides [SERVICE_NAME] integration, enabling AI assistants to [CAPABILITY DESCRIPTION].

## Key Implementation Details

### Authentication
[DESCRIBE AUTH METHOD]
- Credentials stored securely in Docker secrets
- Never exposed in logs or error messages

### API Structure
[DESCRIBE API DETAILS IF APPLICABLE]
- Base URL: [URL]
- All requests include [AUTH METHOD]
- Supports [HTTP METHODS]
- [RESPONSE FORMAT]

### Error Handling
- All tools include try-catch blocks
- API errors return status codes and messages
- User-friendly error messages with ❌ prefix
- Logging to stderr for debugging

### Tool Design Patterns

#### Parameter Validation
```python
if not param.strip():
    return "❌ Error: Parameter is required"
```

#### Success Responses
```python
return f"✅ Action completed successfully"
```

#### List Formatting
```python
result = "📊 Items:\n"
for item in items:
    result += f"- {item['name']} (ID: {item['id']})\n"
```

### ID Management
[DESCRIBE HOW IDS ARE USED IF APPLICABLE]

### Common Workflows
[DESCRIBE TYPICAL USAGE PATTERNS]

### Rate Limits
[DESCRIBE ANY RATE LIMITING]

### Data Formatting
[DESCRIBE DATA FORMATS - dates, special values, etc.]

### Security Notes
[SERVICE-SPECIFIC SECURITY CONSIDERATIONS]

### Testing Recommendations
1. Create test data first
2. Use get_* tools to verify creation
3. Test with non-critical data
4. Monitor API usage

### Common Issues
[LIST COMMON ISSUES AND SOLUTIONS]

### Extension Points
[LIST FEATURES NOT IMPLEMENTED THAT COULD BE ADDED]

## Best Practices
1. Always validate required parameters
2. Return structured, readable responses
3. Include IDs in responses for chaining operations
4. Use appropriate emoji prefixes for clarity
5. Handle errors gracefully with informative messages
6. Log operations for debugging
7. Keep docstrings single-line
8. Default parameters to empty strings
```

---

## SECTION 2: INSTALLATION INSTRUCTIONS FOR THE USER

### Step 1: Save the Files

```bash
# Create project directory
mkdir [SERVER_NAME]-mcp-server
cd [SERVER_NAME]-mcp-server

# Save all 5 files in this directory
```

---

### Step 2: Build Docker Image

```bash
docker build -t [SERVER_NAME]-mcp-server .
```

---

### Step 3: Set Up Secrets

[CUSTOMIZE BASED ON REQUIRED SECRETS]

```bash
# Get your API credentials from [CREDENTIALS_SOURCE]

# Set the required secrets
docker mcp secret set [SECRET_NAME_1]="your-value-here"
docker mcp secret set [SECRET_NAME_2]="your-value-here"

# Verify secrets are set
docker mcp secret list
```

---

### Step 4: Create Custom Catalog

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
    dateAdded: "[CURRENT_DATE_ISO8601]"
    image: [SERVER_NAME]-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      [LIST ALL TOOLS]
      - name: [tool_name_1]
      - name: [tool_name_2]
    secrets:
      [LIST ALL SECRETS]
      - name: [SECRET_NAME]
        env: [ENV_VAR_NAME]
        example: [EXAMPLE_VALUE]
    metadata:
      category: [productivity|monitoring|automation|integration]
      tags:
        - [relevant_tag_1]
        - [relevant_tag_2]
      license: MIT
      owner: local
```

---

### Step 5: Update Registry

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

---

### Step 6: Configure Claude Desktop

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

---

### Step 7: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. Your new [SERVICE_NAME] tools should appear!

---

### Step 8: Test Your Server

```bash
# Verify it appears in the list
docker mcp server list

# Test the server is working
# In Claude Desktop, try: "[EXAMPLE TEST QUERY]"

# If you don't see your server or encounter issues, check logs:
docker logs $(docker ps -a --filter ancestor=[SERVER_NAME]-mcp-server:latest -q)
```

---

### Getting Your Credentials

[CUSTOMIZE - PROVIDE SPECIFIC INSTRUCTIONS FOR OBTAINING API CREDENTIALS]

1. Go to [CREDENTIALS_URL]
2. [Step-by-step instructions]
3. Copy the required values
4. Use in Step 3 above

---

Now you're ready to use [SERVICE_NAME] through Claude Desktop! Try commands like:
- "[EXAMPLE_COMMAND_1]"
- "[EXAMPLE_COMMAND_2]"
- "[EXAMPLE_COMMAND_3]"

````

---

## Step 3: Confirm Guide Creation

After creating the guide file, output this message:

```
✅ Complete MCP Server Guide generated!

📁 Location: ${PAI_DIR}/output/[SERVER_NAME]-mcp-complete-guide.md

This single file contains:
• Section 1: All 5 files to create (Dockerfile, requirements.txt, server code, readme, CLAUDE.md)
• Section 2: Complete Docker MCP gateway installation instructions

The user can follow this guide step-by-step to build and deploy the MCP server.
```

---

## Critical Rules Checklist

Before completing, verify the generated guide includes:

- [ ] Dockerfile with python:3.11-slim and non-root user
- [ ] requirements.txt with mcp[cli]>=1.2.0 and all dependencies
- [ ] Server code with NO @mcp.prompt() and NO prompt parameter
- [ ] ALL tool docstrings are SINGLE-LINE only
- [ ] ALL parameters default to empty strings ("") not None
- [ ] No complex type hints (no Optional, Union, List[str])
- [ ] All tools return formatted strings
- [ ] readme.txt with features, examples, and architecture
- [ ] CLAUDE.md with implementation guide
- [ ] Docker build instructions
- [ ] Secret setup instructions (docker mcp secret set)
- [ ] Custom catalog YAML with all tools listed
- [ ] Registry update instructions
- [ ] Claude Desktop config with custom catalog path
- [ ] Current date in ISO 8601 format for catalog dateAdded
- [ ] All placeholders replaced with actual values
