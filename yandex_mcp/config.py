"""Configuration constants for Yandex MCP Server."""

import os

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
