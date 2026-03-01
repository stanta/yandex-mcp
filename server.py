#!/usr/bin/env python3
"""MCP CLI entrypoint exposing a top-level FastMCP server object.

This file is intended for MCP CLI `FILE_SPEC` usage, e.g.:

- `mcp dev server.py`
- `mcp run server.py`
"""

from yandex_mcp import mcp, run


if __name__ == "__main__":
    run()

