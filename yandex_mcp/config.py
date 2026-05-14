"""Configuration constants and auth helpers for Yandex MCP Server."""

import os
from contextvars import ContextVar, Token
from dataclasses import dataclass

# API Endpoints
YANDEX_DIRECT_API_URL = "https://api.direct.yandex.com/json/v5"
YANDEX_DIRECT_API_URL_V501 = "https://api.direct.yandex.com/json/v501"
YANDEX_DIRECT_SANDBOX_URL = "https://api-sandbox.direct.yandex.com/json/v5"
YANDEX_METRIKA_API_URL = "https://api-metrika.yandex.net"

# OAuth Endpoints
YANDEX_OAUTH_URL = "https://oauth.yandex.ru"
YANDEX_OAUTH_AUTHORIZE_URL = "https://oauth.yandex.ru/authorize"
YANDEX_OAUTH_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_OAUTH_DEVICE_URL = "https://oauth.yandex.ru/device"

# Default timeout for API requests
DEFAULT_TIMEOUT = 30.0
REPORT_TIMEOUT = 120.0

YANDEX_WORDSTAT_API_URL = "https://api.wordstat.yandex.net"

# Token storage
TOKEN_STORAGE_PATH = os.path.expanduser("~/.yandex_mcp/tokens.json")

# Default OAuth scopes
DEFAULT_OAUTH_SCOPES = "direct:api,metrika:read,metrika:write"


@dataclass(frozen=True)
class ServerAuthConfig:
    """Resolved server-side authentication configuration."""

    direct_token: str
    metrika_token: str
    unified_token: str
    client_login: str
    use_sandbox: bool
    client_id: str
    client_secret: str

    @property
    def has_static_token(self) -> bool:
        """Return whether any static API token is configured."""
        return bool(self.direct_token or self.metrika_token or self.unified_token)

    @property
    def has_oauth_credentials(self) -> bool:
        """Return whether OAuth app credentials are configured."""
        return bool(self.client_id and self.client_secret)

    @property
    def has_process_credentials(self) -> bool:
        """Return whether the server can authenticate without per-request headers."""
        return self.has_static_token or self.has_oauth_credentials


_request_auth_token: ContextVar[str] = ContextVar("yandex_request_auth_token", default="")


def get_server_auth_config() -> ServerAuthConfig:
    """Load server authentication configuration from the process environment."""
    return ServerAuthConfig(
        direct_token=os.environ.get("YANDEX_DIRECT_TOKEN", "").strip(),
        metrika_token=os.environ.get("YANDEX_METRIKA_TOKEN", "").strip(),
        unified_token=os.environ.get("YANDEX_TOKEN", "").strip(),
        client_login=os.environ.get("YANDEX_CLIENT_LOGIN", "").strip(),
        use_sandbox=os.environ.get("YANDEX_USE_SANDBOX", "false").lower() == "true",
        client_id=os.environ.get("YANDEX_CLIENT_ID", "").strip(),
        client_secret=os.environ.get("YANDEX_CLIENT_SECRET", "").strip(),
    )


def validate_stdio_auth_config() -> None:
    """Ensure stdio transport has process-level credentials configured."""
    auth_config = get_server_auth_config()
    if auth_config.has_process_credentials:
        return

    raise RuntimeError(
        "Yandex MCP server requires credentials before stdio startup. "
        "Configure one of: YANDEX_TOKEN, YANDEX_DIRECT_TOKEN, YANDEX_METRIKA_TOKEN, "
        "or YANDEX_CLIENT_ID together with YANDEX_CLIENT_SECRET."
    )


def has_process_auth_config() -> bool:
    """Return whether process-level credentials are available."""
    return get_server_auth_config().has_process_credentials


def get_request_auth_token() -> str:
    """Return the current per-request token provided by the HTTP transport."""
    return _request_auth_token.get().strip()


def set_request_auth_token(token: str) -> Token[str]:
    """Store a per-request token for the current execution context."""
    return _request_auth_token.set(token.strip())


def reset_request_auth_token(token: Token[str]) -> None:
    """Reset the per-request token context."""
    _request_auth_token.reset(token)
