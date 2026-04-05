# OpenClaw Quick Start Guide

## Prerequisites

1. OpenClaw installed and running
2. Yandex OAuth token or OAuth application credentials
3. Python 3.10+ installed

## Installation

### Option 1: pip install (Recommended)

```bash
pip install yandex-mcp
```

### Option 2: From source

```bash
git clone https://github.com/SvechaPVL/yandex-mcp.git
cd yandex-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

### Step 1: Get Yandex API Token

1. Go to [Yandex OAuth](https://oauth.yandex.ru/)
2. Create an application or use existing one
3. Get your OAuth token with permissions:
   - `direct:api` — Yandex Direct API access
   - `metrika:read` — Read access to Metrika statistics
   - `metrika:write` — Write access to Metrika (if needed)

### Step 2: Configure OpenClaw

Add the following to `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_TOKEN": "your_oauth_token_here"
      }
    }
  }
}
```

### Step 3: Set Environment Variable

```bash
export YANDEX_TOKEN=your_oauth_token_here
```

Or add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export YANDEX_TOKEN=your_oauth_token_here' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Restart OpenClaw Gateway

```bash
openclaw gateway restart
```

## Verification

### Check MCP Server Status

```bash
openclaw mcp list
```

Expected output:

```
yandex-direct (python -m yandex_mcp)
```

### View Available Tools

```bash
openclaw mcp show yandex-direct --json
```

This should show all 170 tools available.

## Usage Examples

Once configured, you can use natural language commands with your OpenClaw agent:

### Campaign Management

- "Show all my campaigns in Yandex Direct"
- "Pause campaign 12345"
- "Create a new text campaign for Moscow"
- "What's the budget for campaign 67890?"

### Analytics

- "What are the site stats for the last week?"
- "Show me conversion rates for the last month"
- "Compare this week's traffic to last week"

### Keyword Research

- "Get top search queries for 'купить iphone'"
- "Show regional distribution for 'доставка еды'"
- "What are the trending queries in Moscow?"

### Ad Management

- "Create a new text ad for campaign 12345"
- "Show all ads in ad group 67890"
- "Pause all ads with low CTR"

## Troubleshooting

### Server Not Found

If `openclaw mcp list` doesn't show yandex-direct:

1. Check Python path:

   ```bash
   which python
   ```

2. Verify installation:

   ```bash
   python -m yandex_mcp --help
   ```

3. Check OpenClaw logs:
   ```bash
   openclaw gateway logs
   ```

### Authentication Errors

If you get authentication errors:

1. Verify token is set:

   ```bash
   echo $YANDEX_TOKEN
   ```

2. Check token permissions at [Yandex OAuth](https://oauth.yandex.ru/)

3. Try regenerating the token

### Tool Not Working

If a specific tool doesn't work:

1. Check tool description:

   ```bash
   openclaw mcp show yandex-direct --json | jq '.tools[] | select(.name=="direct_get_campaigns")'
   ```

2. Test directly:
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"direct_get_campaigns","arguments":{}}}' | python -m yandex_mcp
   ```

## Advanced Configuration

### Using OAuth Flow (Recommended for Apps)

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_CLIENT_ID": "your_client_id",
        "YANDEX_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

Then use OAuth tools:

- `oauth_get_authorization_url` — Get authorization URL
- `oauth_exchange_code` — Exchange code for tokens
- `oauth_check_token_status` — Check token status

### SSE Transport (Remote)

1. Start the server:

   ```bash
   yandex-mcp --transport sse --port 3000
   ```

2. Configure OpenClaw:
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

### Agency Accounts

If you manage multiple Yandex accounts:

```json
{
  "mcpServers": {
    "yandex-direct": {
      "command": "python",
      "args": ["-m", "yandex_mcp"],
      "env": {
        "YANDEX_TOKEN": "your_token",
        "YANDEX_CLIENT_LOGIN": "client_login"
      }
    }
  }
}
```

## Support

- GitHub Issues: https://github.com/SvechaPVL/yandex-mcp/issues
- Documentation: https://github.com/SvechaPVL/yandex-mcp#readme
- OpenClaw Docs: https://docs.openclaw.ai/cli/mcp
