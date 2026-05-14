"""Packaged CLI entrypoint for Yandex MCP server transports."""

import argparse
import logging
import os
import sys
from typing import Any

from . import __version__, mcp, run
from .config import (
    has_process_auth_config,
    reset_request_auth_token,
    set_request_auth_token,
)


DEFAULT_HTTP_HOST = os.environ.get("YANDEX_MCP_HTTP_HOST", "0.0.0.0")
DEFAULT_HTTP_PORT = int(os.environ.get("YANDEX_MCP_HTTP_PORT", "9639"))
DEFAULT_HTTP_PATH = os.environ.get("YANDEX_MCP_HTTP_PATH", "/mcp")

logger = logging.getLogger("yandex_mcp.http_auth")


def _normalize_http_path(path: str) -> str:
    """Normalize the configured HTTP mount path."""
    normalized = path.strip() or "/mcp"
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    return normalized.rstrip("/") or "/"


def _extract_auth_token(headers: dict[str, str]) -> str:
    """Extract a Yandex API token from incoming HTTP headers."""
    authorization = headers.get("authorization", "").strip()
    if authorization:
        scheme, _, value = authorization.partition(" ")
        if scheme.lower() in {"bearer", "oauth"} and value.strip():
            return value.strip()

    return headers.get("x-yandex-token", "").strip()


async def _send_json_response(send: Any, status: int, payload: dict[str, Any]) -> None:
    """Send a small JSON response from an ASGI middleware."""
    import json

    body = json.dumps(payload).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


class StreamableHTTPAuthMiddleware:
    """Inject request-scoped Yandex API tokens into the MCP server runtime."""

    def __init__(self, app: Any, path: str):
        self.app = app
        self.path = path

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope.get("type") != "http" or scope.get("path") != self.path:
            await self.app(scope, receive, send)
            return

        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        has_authorization = bool(headers.get("authorization", "").strip())
        has_x_yandex_token = bool(headers.get("x-yandex-token", "").strip())
        request_token = _extract_auth_token(headers)

        logger.info(
            "Incoming MCP HTTP request: method=%s path=%s has_authorization=%s has_x_yandex_token=%s has_process_auth=%s token_source=%s",
            scope.get("method", ""),
            scope.get("path", ""),
            has_authorization,
            has_x_yandex_token,
            has_process_auth_config(),
            "request" if request_token else "process-or-none",
        )

        if not has_process_auth_config() and not request_token:
            logger.warning(
                "Rejecting MCP HTTP request due to missing credentials: method=%s path=%s",
                scope.get("method", ""),
                scope.get("path", ""),
            )
            await _send_json_response(
                send,
                401,
                {
                    "error": (
                        "Missing Yandex API credentials. Configure process-level credentials "
                        "for the server or send 'Authorization: Bearer <YANDEX_TOKEN>' "
                        "(or 'X-Yandex-Token') with each streamable HTTP request."
                    )
                },
            )
            return

        context_token = set_request_auth_token(request_token) if request_token else None
        try:
            await self.app(scope, receive, send)
        finally:
            if context_token is not None:
                reset_request_auth_token(context_token)


def _run_streamable_http(host: str, port: int, path: str) -> None:
    """Run the MCP server over streamable HTTP."""
    import uvicorn

    normalized_path = _normalize_http_path(path)
    mcp.settings.streamable_http_path = normalized_path
    app = StreamableHTTPAuthMiddleware(mcp.streamable_http_app(), normalized_path)

    print(
        (
            f"Starting Yandex MCP Server v{__version__} with streamable HTTP on "
            f"http://{host}:{port}{normalized_path}"
        ),
        file=sys.stderr,
    )

    uvicorn.run(app, host=host, port=port, log_level="info")


def main() -> None:
    """Main entry point with transport selection."""
    parser = argparse.ArgumentParser(
        description="Yandex MCP Server - MCP server for Yandex Direct and Metrika APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help=(
            "Transport type: stdio (default), streamable-http (preferred HTTP transport), "
            "or legacy sse alias"
        ),
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_HTTP_PORT,
        help=f"Port for streamable HTTP transport (default: {DEFAULT_HTTP_PORT})",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HTTP_HOST,
        help=f"Host for streamable HTTP transport (default: {DEFAULT_HTTP_HOST})",
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_HTTP_PATH,
        help=f"HTTP path for streamable HTTP transport (default: {DEFAULT_HTTP_PATH})",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    if args.transport == "stdio":
        run()
        return

    if args.transport == "sse":
        print(
            "Transport 'sse' is deprecated; starting streamable HTTP for compatibility.",
            file=sys.stderr,
        )

    _run_streamable_http(host=args.host, port=args.port, path=args.path)
