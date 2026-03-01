# Testing Yandex MCP Server with mcp[cli]

This guide explains how to test the Yandex MCP Server using the MCP CLI tools included in the `mcp[cli]` package.

## Installation

The MCP CLI tools are included when you install the package with the `cli` extra:

```bash
pip install yandex-mcp[cli]
# Or install from source:
pip install -e ".[cli]"
```

Alternatively, you can install the MCP CLI directly:

```bash
pip install "mcp[cli]>=1.0.0"
```

## Prerequisites

Before testing, ensure you have:

1. **API Credentials**: Set up your Yandex API credentials in `.env` file:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your credentials:
 YANDEX_CLIENT_ID=your_client_id
 YANDEX_CLIENT_SECRET=your_client_secret
   ```

2. **Python Environment**: Make sure you're in a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

## Testing Methods

### Method 1: Run Server and Inspect with CLI

The MCP CLI provides the `mcp` command to inspect and test MCP servers. Here's how to use it:

#### 1.1 List Available Tools

Start the server and query what tools are available:

```bash
# Run the server in one terminal
python -m yandex_mcp

# In another terminal, use npx to run the MCP CLI (if available)
# Or use the Python-based approach below
```

#### 1.2 Using mcp dev Command

The `mcp dev` command starts an interactive development session.

> Important: `mcp dev` expects a **Python file path** (`FILE_SPEC`), not a package name.

```bash
# Start development mode for this project
mcp dev server.py
```

If you run `mcp dev yandex-mcp`, MCP CLI treats `yandex-mcp` as a file path
and fails with:

```text
File not found: .../yandex-mcp
```

This will:
- Start the MCP server
- Open an interactive prompt where you can:
  - List all available tools
  - Call tools with arguments
  - View resources and prompts
  - Debug tool execution

#### 1.3 Using mcp run Command

Run the server and test specific tools:

```bash
# Run the server directly
mcp run server.py
```

### Method 2: Direct Python Testing

You can also test the MCP server directly using Python:

```python
# test_mcp_server.py
import asyncio
from yandex_mcp import mcp

async def test_server():
    # Initialize the server
    async with mcp.server.stdio.stdio_server() as (read, write):
        # Get the server capabilities
        capabilities = mcp.server.ServerCapabilities(
            tools=mcp.server.ToolProvider(),
            resources=mcp.server.ResourceProvider(),
            prompts=mcp.server.PromptProvider()
        )
        
        # List available tools
        print("Available tools:")
        for tool in mcp._tool_manager.list_tools():
            print(f"  - {tool.name}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

### Method 3: Using the Inspector

The MCP Inspector is launched by `mcp dev`:

```bash
# Start server + inspector
mcp dev server.py
```

This opens a web-based interface where you can:
- Browse all available tools
- Test tools with sample inputs
- View tool schemas and documentation

## Testing Individual Services

### Test Yandex Direct API Tools

```bash
# Run the server and test specific Direct API tools
mcp dev server.py

# In the interactive prompt:
> list tools
> call get_campaigns {"limit": 5}
> call get_keywords {"campaign_id": 123456}
```

### Test Yandex Metrika Tools

```bash
# Test Metrika tools
mcp dev server.py

# In the interactive prompt:
> call get_counters
> call get_goals {"counter_id": 123456}
```

## Verifying Server Capabilities

Check what the server provides:

```bash
# Start inspector (tool/resource/prompt discovery happens there)
mcp dev server.py
```

Expected capabilities include:
- **Tools**: ~30+ tools for Direct and Metrika APIs
- **Resources**: API configuration and status
- **Prompts**: OAuth flow prompts

## Troubleshooting

### Issue: "mcp: command not found"

If the `mcp` command is not found after installation:

```bash
# Check installation
pip show mcp

# Verify CLI is installed
mcp --help

# Or use directly
python -c "from mcp.cli import main; main()"
```

### Issue: "File not found: .../yandex-mcp"

This happens when `mcp dev` receives a package name instead of a file path.

```bash
# ✅ Correct
mcp dev server.py

# ❌ Incorrect for mcp dev/mcp run
mcp dev yandex-mcp
```

### Issue: Server Won't Start

Check environment variables:

```bash
# Verify .env file is in the correct location
ls -la .env

# Check variables are loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('YANDEX_DIRECT_TOKEN'))"
```

### Issue: Import Errors

Ensure all dependencies are installed:

```bash
pip install -e .
pip install "mcp[cli]>=1.0.0"
```

## CI/CD Testing

For automated testing in CI pipelines:

```bash
# Install dependencies
pip install -e ".[dev,cli]"

# Run unit tests
pytest tests/ -v

# Run MCP server validation
python -c "
from yandex_mcp import mcp
import json

# Get server initialization
init_result = mcp.server.initialize()
print('Server initialized successfully')
print(json.dumps(init_result, indent=2))
"
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `mcp dev server.py` | Start development mode + inspector |
| `mcp run server.py` | Run MCP server directly |
| `mcp --help` | Show CLI help |
| `python -m yandex_mcp` | Run this server module directly |

## Additional Resources

- [MCP SDK Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Yandex Direct API Docs](https://yandex.com/dev/direct)
- [Yandex Metrika API Docs](https://yandex.com/dev/metrika)
