#!/usr/bin/env python3
"""MCP CLI entrypoint exposing a top-level FastMCP server object.

This file is intended for MCP CLI `FILE_SPEC` usage, e.g.:

- `mcp dev server.py`
- `mcp run server.py`

Also supports standalone execution with transport options:

- `python server.py` - stdio transport (default, for MCP CLI)
- `python server.py --transport sse` - HTTP/SSE transport (for remote clients)
- `python server.py --transport sse --port 3000` - Custom port
- `python server.py --transport sse --host 0.0.0.0 --port 3000` - Custom host and port
"""

import argparse
import sys

from yandex_mcp import mcp, run, __version__


def main() -> None:
    """Main entry point with transport selection."""
    parser = argparse.ArgumentParser(
        description="Yandex MCP Server - MCP server for Yandex Direct and Metrika APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python server.py                      # stdio transport (default, for MCP CLI)
  python server.py --transport sse      # HTTP/SSE transport
  python server.py --transport sse --port 8080  # Custom port

For OpenClaw integration, use stdio transport (default):
  openclaw mcp set yandex-direct '{"command": "python", "args": ["server.py"]}'
    """
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type: stdio (default) or sse (HTTP with Server-Sent Events)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port for SSE transport (default: 3000)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE transport (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    args = parser.parse_args()
    
    if args.transport == "sse":
        print(f"Starting Yandex MCP Server v{__version__} on {args.host}:{args.port}", file=sys.stderr)
        import uvicorn
        from mcp.server.fastmcp import FastMCP
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
        
        # Get the app from MCP
        app = mcp.streamable_http_app()
        
        # Configure uvicorn to run the app
        uvicorn_config = uvicorn.Config(
            app,
            host=args.host,
            port=args.port,
            log_level="info"
        )
        server = uvicorn.Server(uvicorn_config)
        server.run()
    else:
        # stdio is the default for MCP CLI
        mcp.run()


if __name__ == "__main__":
    main()
