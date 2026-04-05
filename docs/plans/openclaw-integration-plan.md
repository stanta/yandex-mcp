# OpenClaw Integration Plan for Yandex MCP Server

## Overview

This plan outlines the steps to integrate the Yandex MCP Server with OpenClaw, enabling AI agents running on OpenClaw to manage Yandex Direct advertising campaigns, analyze Metrika statistics, and perform Wordstat keyword research through natural language commands.

## Current State

- **MCP Server**: Yandex MCP Server v1.1.0 (Python, FastMCP)
- **Transport**: stdio (stdin/stdout JSON-RPC 2.0)
- **Tools**: 170 tools across Yandex Direct (113), Metrika (43), Wordstat (5), OAuth (9)
- **Authentication**: Static token or OAuth 2.0 flow
- **Entry Point**: `server.py` or `python -m yandex_mcp`

## OpenClaw MCP Integration Requirements

Based on OpenClaw documentation, MCP servers are configured in `~/.openclaw/openclaw.json` under the `mcpServers` key with the following structure:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      },
      "transport": "stdio"
    }
  }
}
```

## Implementation Plan

### Phase 1: Package Preparation (Code Changes)

#### Step 1.1: Add PyPI Package Support

**Goal**: Make the server installable via `pip` or `uvx` for easier OpenClaw integration.

**Changes**:

1. Update [`pyproject.toml`](pyproject.toml:1) to add proper entry points:

   ```toml
   [project.scripts]
   yandex-mcp = "yandex_mcp:mcp.run"
   ```

2. Ensure the package can be run as a module:
   ```bash
   python -m yandex_mcp
   ```

**Files to modify**:

- [`pyproject.toml`](pyproject.toml:1)

#### Step 1.2: Add SSE Transport Support (Optional)

**Goal**: Support HTTP/SSE transport for remote OpenClaw deployments.

**Changes**:

1. Add SSE transport option to [`server.py`](server.py:1):

   ```python
   import argparse

   parser = argparse.ArgumentParser()
   parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
   parser.add_argument("--port", type=int, default=3000)
   parser.add_argument("--host", default="0.0.0.0")
   args = parser.parse_args()

   if args.transport == "sse":
       mcp.run(transport="sse", port=args.port, host=args.host)
   else:
       mcp.run()
   ```

2. Add `uvicorn` to dependencies in [`pyproject.toml`](pyproject.toml:1):
   ```toml
   dependencies = [
       ...
       "uvicorn>=0.30.0",
   ]
   ```

**Files to modify**:

- [`server.py`](server.py:1)
- [`pyproject.toml`](pyproject.toml:1)

#### Step 1.3: Add Health Check Endpoint

**Goal**: Provide a health check for monitoring and OpenClaw status verification.

**Changes**:

1. Add optional health check when running in SSE mode:
   ```python
   @mcp.custom_route("/health", methods=["GET"])
   async def health_check(request):
       return {"status": "ok", "version": __version__}
   ```

**Files to modify**:

- [`yandex_mcp/__init__.py`](yandex_mcp/__init__.py:1)

### Phase 2: Documentation Updates

#### Step 2.1: Add OpenClaw Installation Section to README

**Goal**: Provide clear instructions for OpenClaw users.

**Content to add**:

````markdown
## OpenClaw Integration

### Option 1: Local Installation (Recommended)

1. Install the package:
   ```bash
   pip install yandex-mcp
   ```
````

2. Add to `~/.openclaw/openclaw.json`:

   ```json
   {
     "mcpServers": {
       "yandex-direct": {
         "command": "python",
         "args": ["-m", "yandex_mcp"],
         "env": {
           "YANDEX_TOKEN": "${YANDEX_TOKEN}"
         }
       }
     }
   }
   ```

3. Set environment variable:

   ```bash
   export YANDEX_TOKEN=your_oauth_token_here
   ```

4. Restart OpenClaw gateway:
   ```bash
   openclaw gateway restart
   ```

### Option 2: Using uvx (No Installation)

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "uvx",
      "args": ["yandex-mcp"],
      "env": {
        "YANDEX_TOKEN": "${YANDEX_TOKEN}"
      }
    }
  }
}
```

### Option 3: From Source

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "/path/to/yandex-mcp/.venv/bin/python",
      "args": ["server.py"],
      "cwd": "/path/to/yandex-mcp",
      "env": {
        "YANDEX_TOKEN": "${YANDEX_TOKEN}"
      }
    }
  }
}
```

### Option 4: SSE Transport (Remote)

1. Start the server:

   ```bash
   yandex-mcp --transport sse --port 3000
   ```

2. Add to `~/.openclaw/openclaw.json`:
   ```json
   {
     "mcpServers": {
       "yandex-direct": {
         "url": "http://localhost:3000/sse",
         "transport": "http"
       }
     }
   }
   ```

### Verification

After configuration, verify the connection:

```bash
openclaw mcp list
# Should show yandex-direct

openclaw mcp show yandex-direct --json
# Should show tools list
```

### Example Usage

Once connected, you can use natural language commands:

- "Show all my campaigns in Yandex Direct"
- "Pause campaign 12345"
- "What are the site stats for the last week?"
- "Create a new text ad for campaign 67890"
- "Get top search queries for 'купить iphone'"

````

**Files to modify**:
- [`README.md`](README.md:1)
- [`README.ru.md`](README.ru.md:1)

#### Step 2.2: Create OpenClaw-Specific Configuration Example

**Goal**: Provide a ready-to-use configuration file.

**Content**:
```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_TOKEN": "${YANDEX_TOKEN}",
        "YANDEX_CLIENT_LOGIN": "${YANDEX_CLIENT_LOGIN}"
      }
    }
  }
}
````

**Files to create**:

- [`examples/openclaw-config.json`](examples/openclaw-config.json:1)

### Phase 3: Testing & Validation

#### Step 3.1: Test Local stdio Integration

**Steps**:

1. Install package: `pip install -e .`
2. Configure OpenClaw with local stdio config
3. Run: `openclaw mcp list`
4. Verify tools are discovered: `openclaw mcp show yandex-direct --json`
5. Test a simple command: "Show my Yandex Direct campaigns"

**Expected Result**: All 170 tools should be available and functional.

#### Step 3.2: Test SSE Transport

**Steps**:

1. Start server: `yandex-mcp --transport sse --port 3000`
2. Configure OpenClaw with SSE URL
3. Verify connection and tool discovery
4. Test API calls through SSE transport

**Expected Result**: Same functionality as stdio, but over HTTP.

#### Step 3.3: Test OAuth Flow

**Steps**:

1. Configure with `YANDEX_CLIENT_ID` and `YANDEX_CLIENT_SECRET`
2. Use `oauth_get_authorization_url` tool
3. Complete authorization flow
4. Verify token is stored and refreshed automatically

**Expected Result**: OAuth flow works seamlessly within OpenClaw.

### Phase 4: Advanced Features

#### Step 4.1: Add Tool Descriptions for OpenClaw

**Goal**: Improve tool discoverability in OpenClaw's agent interface.

**Changes**:

1. Ensure all tool descriptions are clear and actionable
2. Add examples in tool descriptions where helpful
3. Use consistent naming conventions

**Files to modify**:

- All tool files in [`yandex_mcp/tools/`](yandex_mcp/tools/)

#### Step 4.2: Add Error Handling for OpenClaw

**Goal**: Provide clear error messages that OpenClaw agents can understand.

**Changes**:

1. Standardize error response format
2. Include actionable suggestions in error messages
3. Add error codes for common issues

**Files to modify**:

- [`yandex_mcp/client.py`](yandex_mcp/client.py:1)
- [`yandex_mcp/utils.py`](yandex_mcp/utils.py:1)

#### Step 4.3: Add Rate Limiting Awareness

**Goal**: Handle Yandex API rate limits gracefully.

**Changes**:

1. Detect rate limit responses (HTTP 429)
2. Implement exponential backoff
3. Return informative messages about rate limits

**Files to modify**:

- [`yandex_mcp/client.py`](yandex_mcp/client.py:1)

### Phase 5: Publishing & Distribution

#### Step 5.1: Publish to PyPI

**Goal**: Enable `pip install yandex-mcp` for easy installation.

**Steps**:

1. Build package: `python -m build`
2. Upload to PyPI: `twine upload dist/*`
3. Verify installation: `pip install yandex-mcp`

#### Step 5.2: Submit to OpenClaw MCP Registry

**Goal**: Make the server discoverable in OpenClaw's ecosystem.

**Steps**:

1. Create a listing on OpenClaw's MCP registry
2. Add metadata: description, tags, documentation link
3. Submit for review

#### Step 5.3: Create Docker Image (Optional)

**Goal**: Enable containerized deployment for OpenClaw.

**Content**:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["yandex-mcp", "--transport", "sse", "--port", "3000"]
```

**Files to create**:

- [`Dockerfile`](Dockerfile:1)
- [`docker-compose.yml`](docker-compose.yml:1)

## Configuration Reference

### Environment Variables

| Variable               | Required | Description                      |
| ---------------------- | -------- | -------------------------------- |
| `YANDEX_TOKEN`         | Yes\*    | Static OAuth token               |
| `YANDEX_CLIENT_ID`     | Yes\*    | OAuth application ID             |
| `YANDEX_CLIENT_SECRET` | Yes\*    | OAuth application secret         |
| `YANDEX_CLIENT_LOGIN`  | No       | Agency account login             |
| `YANDEX_USE_SANDBOX`   | No       | Use sandbox API (`true`/`false`) |

\*Either `YANDEX_TOKEN` or (`YANDEX_CLIENT_ID` + `YANDEX_CLIENT_SECRET`) is required.

### OpenClaw Configuration Examples

#### Minimal Configuration

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Full Configuration with OAuth

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_CLIENT_ID": "your_client_id",
        "YANDEX_CLIENT_SECRET": "your_client_secret",
        "YANDEX_CLIENT_LOGIN": "agency_login"
      }
    }
  }
}
```

#### SSE Transport Configuration

```json
{
  "mcpServers": {
    "yandex-direct": {
      "url": "http://localhost:3000/sse",
      "transport": "http"
    }
  }
}
```

## Timeline

| Phase                        | Duration | Dependencies |
| ---------------------------- | -------- | ------------ |
| Phase 1: Package Preparation | 1-2 days | None         |
| Phase 2: Documentation       | 1 day    | Phase 1      |
| Phase 3: Testing             | 2-3 days | Phase 1, 2   |
| Phase 4: Advanced Features   | 3-5 days | Phase 3      |
| Phase 5: Publishing          | 1-2 days | Phase 4      |

**Total Estimated Time**: 8-13 days

## Success Criteria

1. ✅ Server can be installed via `pip install yandex-mcp`
2. ✅ Server is discoverable by OpenClaw via `openclaw mcp list`
3. ✅ All 170 tools are available in OpenClaw
4. ✅ Natural language commands work correctly
5. ✅ OAuth flow works within OpenClaw
6. ✅ Error messages are clear and actionable
7. ✅ Documentation is complete and accurate

## Risks & Mitigations

| Risk                      | Impact | Mitigation                               |
| ------------------------- | ------ | ---------------------------------------- |
| Yandex API changes        | High   | Version pinning, monitoring              |
| OpenClaw MCP spec changes | Medium | Follow official docs, test regularly     |
| Rate limiting             | Medium | Implement backoff, clear error messages  |
| OAuth token expiration    | Low    | Automatic refresh, clear status messages |

## References

- [OpenClaw MCP Documentation](https://docs.openclaw.ai/cli/mcp)
- [OpenClaw Configuration Guide](https://docs.openclaw.ai/gateway/configuration)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Yandex Direct API v5](https://yandex.ru/dev/direct/doc/)
- [Yandex Metrika API](https://yandex.ru/dev/metrika/doc/)
