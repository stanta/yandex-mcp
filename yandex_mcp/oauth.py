"""OAuth client for Yandex APIs with authorization code and device flows."""

import os
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from .config import (
    DEFAULT_OAUTH_SCOPES,
    TOKEN_STORAGE_PATH,
    YANDEX_OAUTH_AUTHORIZE_URL,
    YANDEX_OAUTH_DEVICE_URL,
    YANDEX_OAUTH_TOKEN_URL,
    DEFAULT_TIMEOUT,
)


@dataclass
class OAuthToken:
    """Represents an OAuth token with metadata."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    created_at: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        """Check if token is expired (with 5-minute buffer)."""
        if not self.expires_in:
            return False
        buffer = 300  # 5 minutes
        return time.time() > (self.created_at + self.expires_in - buffer)

    @property
    def expires_at(self) -> Optional[float]:
        """Get expiration timestamp."""
        if not self.expires_in:
            return None
        return self.created_at + self.expires_in


class YandexOAuthClient:
    """OAuth client for Yandex Direct and Metrika APIs."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: str = "oob",
        scopes: Optional[str] = None,
    ):
        """Initialize OAuth client.
        
        Args:
            client_id: Yandex OAuth application client ID
            client_secret: Yandex OAuth application client secret
            redirect_uri: OAuth redirect URI (default: oob for console apps)
            scopes: Comma-separated OAuth scopes
        """
        self.client_id = client_id or os.environ.get("YANDEX_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("YANDEX_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri
        self.scopes = scopes or os.environ.get("YANDEX_OAUTH_SCOPES", DEFAULT_OAUTH_SCOPES)
        self._token: Optional[OAuthToken] = None

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate authorization URL for web-based OAuth flow.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            URL to redirect user to for authorization
        """
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
        }
        if state:
            params["state"] = state

        # Build URL manually to avoid encoding issues
        scope_param = self.scopes.replace(",", "%2C")
        url = f"{YANDEX_OAUTH_AUTHORIZE_URL}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={scope_param}"
        if state:
            url += f"&state={state}"
        return url

    async def exchange_code_for_token(self, code: str) -> OAuthToken:
        """Exchange authorization code for access token.
        
        Args:
            code: Authorization code received from OAuth callback
            
        Returns:
            OAuthToken with access and refresh tokens
            
        Raises:
            ValueError: If OAuth credentials are not configured
            httpx.HTTPStatusError: If token exchange fails
        """
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "OAuth credentials not configured. "
                "Set YANDEX_CLIENT_ID and YANDEX_CLIENT_SECRET environment variables."
            )

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }

        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(YANDEX_OAUTH_TOKEN_URL, data=data)
            response.raise_for_status()
            token_data = response.json()

        self._token = OAuthToken(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "bearer"),
            expires_in=token_data.get("expires_in"),
        )
        return self._token

    async def get_device_code(self) -> dict:
        """Initiate device OAuth flow for headless applications.
        
        Returns:
            Dict with device_code, user_code, verification_url, interval, and expires_in
            
        Raises:
            ValueError: If OAuth credentials are not configured
        """
        if not self.client_id:
            raise ValueError(
                "OAuth client_id not configured. "
                "Set YANDEX_CLIENT_ID environment variable."
            )

        data = {
            "client_id": self.client_id,
            "scope": self.scopes,
        }

        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(YANDEX_OAUTH_DEVICE_URL, data=data)
            response.raise_for_status()
            return response.json()

    async def poll_for_token(
        self,
        device_code: str,
        interval: int = 5,
        timeout: int = 600,
    ) -> OAuthToken:
        """Poll for token using device code.
        
        Args:
            device_code: Device code from get_device_code()
            interval: Polling interval in seconds
            timeout: Maximum wait time in seconds
            
        Returns:
            OAuthToken with access and refresh tokens
            
        Raises:
            TimeoutError: If token not obtained within timeout
            httpx.HTTPStatusError: If polling fails
        """
        start_time = time.time()
        expires_at = start_time + timeout

        while time.time() < expires_at:
            await self._check_device_code(device_code)
            
            data = {
                "grant_type": "device_code",
                "code": device_code,
                "client_id": self.client_id,
            }

            async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
                response = await client.post(YANDEX_OAUTH_TOKEN_URL, data=data)
                
                if response.status_code == 200:
                    token_data = response.json()
                    self._token = OAuthToken(
                        access_token=token_data["access_token"],
                        refresh_token=token_data.get("refresh_token"),
                        token_type=token_data.get("token_type", "bearer"),
                        expires_in=token_data.get("expires_in"),
                    )
                    return self._token
                elif response.status_code == 403:
                    # Still waiting for user authorization
                    error_data = response.json()
                    if error_data.get("error") == "authorization_pending":
                        await self._sleep(interval)
                        continue
                    elif error_data.get("error") == "expired_token":
                        raise TimeoutError("Device code expired. Please try again.")
                    else:
                        response.raise_for_status()
                else:
                    response.raise_for_status()

        raise TimeoutError("Token acquisition timed out. Please try again.")

    async def _check_device_code(self, device_code: str) -> None:
        """Validate device code with Yandex."""
        # Yandex doesn't have a validation endpoint, this is a placeholder
        # in case they add one in the future
        pass

    async def _sleep(self, seconds: int) -> None:
        """Async sleep helper."""
        import asyncio
        await asyncio.sleep(seconds)

    async def refresh_token(self, refresh_token: Optional[str] = None) -> OAuthToken:
        """Refresh an expired access token.
        
        Args:
            refresh_token: Refresh token (uses stored if not provided)
            
        Returns:
            New OAuthToken with fresh access and refresh tokens
            
        Raises:
            ValueError: If no refresh token available
        """
        token_to_use = refresh_token or (self._token.refresh_token if self._token else None)
        if not token_to_use:
            raise ValueError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token_to_use,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(YANDEX_OAUTH_TOKEN_URL, data=data)
            response.raise_for_status()
            token_data = response.json()

        self._token = OAuthToken(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token", token_to_use),
            token_type=token_data.get("token_type", "bearer"),
            expires_in=token_data.get("expires_in"),
        )
        return self._token

    def set_token(self, token: OAuthToken) -> None:
        """Set the current token."""
        self._token = token

    def get_token(self) -> Optional[OAuthToken]:
        """Get the current token."""
        return self._token

    async def get_valid_token(self) -> Optional[OAuthToken]:
        """Get a valid token, refreshing if necessary.
        
        Returns:
            Valid OAuthToken or None if no token available
        """
        if not self._token:
            return None
            
        if self._token.is_expired and self._token.refresh_token:
            return await self.refresh_token()
        
        if self._token.is_expired:
            return None
            
        return self._token


# Global OAuth client instance
oauth_client = YandexOAuthClient()
