#!/usr/bin/env python3
"""MCP CLI entrypoint exposing a top-level FastMCP server object.

This file is intended for MCP CLI `FILE_SPEC` usage, e.g.:

- `mcp dev server.py`
- `mcp run server.py`

Also supports standalone execution with transport options:

- `python server.py` - stdio transport (default, for MCP CLI)
- `python server.py --transport streamable-http` - streamable HTTP transport
- `python server.py --transport streamable-http --host 0.0.0.0 --port 9639 --path /mcp`
"""

from yandex_mcp.cli import main


if __name__ == "__main__":
    main()
