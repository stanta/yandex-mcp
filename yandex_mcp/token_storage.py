"""Token storage for OAuth tokens."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

from .config import TOKEN_STORAGE_PATH
from .oauth import OAuthToken


class TokenStorage:
    """Secure file-based storage for OAuth tokens."""

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize token storage.
        
        Args:
            storage_path: Path to token storage file
        """
        self.storage_path = Path(storage_path or TOKEN_STORAGE_PATH)

    def _ensure_directory(self) -> None:
        """Ensure the storage directory exists."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def save_token(self, service: str, token: OAuthToken) -> None:
        """Save OAuth token for a service.
        
        Args:
            service: Service name (e.g., 'direct', 'metrika')
            token: OAuthToken to store
        """
        tokens = self._load_all()
        
        tokens[service] = {
            "access_token": token.access_token,
            "refresh_token": token.refresh_token,
            "token_type": token.token_type,
            "expires_in": token.expires_in,
            "created_at": token.created_at,
        }
        
        self._ensure_directory()
        self._write_all(tokens)

    def load_token(self, service: str) -> Optional[OAuthToken]:
        """Load OAuth token for a service.
        
        Args:
            service: Service name (e.g., 'direct', 'metrika')
            
        Returns:
            OAuthToken if found, None otherwise
        """
        tokens = self._load_all()
        token_data = tokens.get(service)
        
        if not token_data:
            return None
            
        return OAuthToken(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "bearer"),
            expires_in=token_data.get("expires_in"),
            created_at=token_data.get("created_at", 0),
        )

    def clear_token(self, service: str) -> bool:
        """Remove OAuth token for a service.
        
        Args:
            service: Service name (e.g., 'direct', 'metrika')
            
        Returns:
            True if token was removed, False if not found
        """
        tokens = self._load_all()
        if service in tokens:
            del tokens[service]
            self._write_all(tokens)
            return True
        return False

    def clear_all(self) -> None:
        """Remove all stored tokens."""
        self._write_all({})

    def list_services(self) -> list:
        """List all services with stored tokens.
        
        Returns:
            List of service names
        """
        return list(self._load_all().keys())

    def _load_all(self) -> Dict[str, Any]:
        """Load all tokens from storage."""
        if not self.storage_path.exists():
            return {}
        
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _write_all(self, tokens: Dict[str, Any]) -> None:
        """Write all tokens to storage."""
        # Set restrictive permissions (owner read/write only)
        old_umask = os.umask(0o077)
        try:
            with open(self.storage_path, "w") as f:
                json.dump(tokens, f, indent=2)
        finally:
            os.umask(old_umask)


# Global token storage instance
token_storage = TokenStorage()
