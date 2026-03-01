"""MCP tools for OAuth flow management."""

from mcp.server.fastmcp import FastMCP

from ..oauth import oauth_client
from ..token_storage import token_storage


mcp = FastMCP("yandex_oauth")


@mcp.tool()
async def oauth_get_authorization_url(
    state: str = None,
) -> str:
    """Get authorization URL for OAuth flow.
    
    Use this to start the web-based OAuth authorization.
    User will be redirected to Yandex to log in and grant permissions.
    
    Args:
        state: Optional state parameter for CSRF protection
        
    Returns:
        URL to redirect user to for authorization
    """
    url = oauth_client.get_authorization_url(state=state)
    return f"""Please visit this URL to authorize the application:

{url}

After authorization, you will be redirected to a page with a verification code.
Use that code with the oauth_exchange_code tool."""


@mcp.tool()
async def oauth_exchange_code(
    code: str,
    service: str = "direct",
) -> str:
    """Exchange authorization code for access token.
    
    Use this after the user has authorized via the OAuth URL.
    
    Args:
        code: Authorization code from OAuth callback
        service: Service to store token for ('direct' or 'metrika')
        
    Returns:
        Success message with token info
    """
    token = await oauth_client.exchange_code_for_token(code)
    token_storage.save_token(service, token)
    return f"""Successfully obtained token for {service}!

Access token: {token.access_token[:20]}...
Token type: {token.token_type}
Expires in: {token.expires_in} seconds
Has refresh token: {token.refresh_token is not None}"""


@mcp.tool()
async def oauth_get_device_code() -> str:
    """Get device code for headless OAuth flow.
    
    Use this for server/CLI applications without browser access.
    User will need to visit a URL and enter a code manually.
    
    Returns:
        Instructions with device code and verification URL
    """
    device_info = await oauth_client.get_device_code()
    return f"""Please complete the following steps:

1. Visit: {device_info['verification_url']}
2. Enter this code: {device_info['user_code']}
3. Grant permissions to the application

Then use oauth_poll_device_token with device_code='{device_info['device_code']}'
to complete the authorization."""


@mcp.tool()
async def oauth_poll_device_token(
    device_code: str,
    service: str = "direct",
    interval: int = 5,
    timeout: int = 600,
) -> str:
    """Poll for device token after user authorization.
    
    Call this after user has entered the device code on Yandex website.
    
    Args:
        device_code: Device code from oauth_get_device_code
        service: Service to store token for ('direct' or 'metrika')
        interval: Polling interval in seconds
        timeout: Maximum wait time in seconds
        
    Returns:
        Success message with token info
    """
    token = await oauth_client.poll_for_token(
        device_code=device_code,
        interval=interval,
        timeout=timeout,
    )
    token_storage.save_token(service, token)
    return f"""Successfully obtained token for {service}!

Access token: {token.access_token[:20]}...
Token type: {token.token_type}
Expires in: {token.expires_in} seconds
Has refresh token: {token.refresh_token is not None}"""


@mcp.tool()
async def oauth_check_token_status(
    service: str = "direct",
) -> str:
    """Check OAuth token status for a service.
    
    Args:
        service: Service to check ('direct' or 'metrika')
        
    Returns:
        Token status information
    """
    import datetime
    
    token = token_storage.load_token(service)
    if not token:
        return f"No token found for service '{service}'"
    
    status = "valid"
    if token.is_expired:
        status = "expired"
    
    expires_at_str = "N/A"
    if token.expires_at:
        expires_at = datetime.datetime.fromtimestamp(token.expires_at)
        expires_at_str = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""Token status for '{service}':
- Status: {status}
- Expires at: {expires_at_str}
- Has refresh token: {token.refresh_token is not None}
- Token type: {token.token_type}"""


@mcp.tool()
async def oauth_refresh_token(service: str = "direct") -> str:
    """Refresh an expired OAuth token.
    
    Args:
        service: Service to refresh token for ('direct' or 'metrika')
        
    Returns:
        Success message with new token info
    """
    token = token_storage.load_token(service)
    if not token:
        return f"No token found for service '{service}'"
    
    if not token.refresh_token:
        return f"No refresh token available for service '{service}'"
    
    oauth_client.set_token(token)
    new_token = await oauth_client.refresh_token()
    token_storage.save_token(service, new_token)
    
    return f"""Successfully refreshed token for {service}!

New access token: {new_token.access_token[:20]}...
Expires in: {new_token.expires_in} seconds"""


@mcp.tool()
async def oauth_revoke_token(service: str = "direct") -> str:
    """Remove stored OAuth token for a service.
    
    Args:
        service: Service to revoke token for ('direct' or 'metrika')
        
    Returns:
        Confirmation message
    """
    if token_storage.clear_token(service):
        return f"Successfully removed token for service '{service}'"
    return f"No token found for service '{service}'"


def register_oauth_tools(mcp_server: FastMCP) -> None:
    """Register OAuth tools with MCP server."""
    mcp_server.add_tool(oauth_get_authorization_url)
    mcp_server.add_tool(oauth_exchange_code)
    mcp_server.add_tool(oauth_get_device_code)
    mcp_server.add_tool(oauth_poll_device_token)
    mcp_server.add_tool(oauth_check_token_status)
    mcp_server.add_tool(oauth_refresh_token)
    mcp_server.add_tool(oauth_revoke_token)
