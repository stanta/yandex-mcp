"""Tests for OAuth module."""

import time
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from yandex_mcp.oauth import OAuthToken, YandexOAuthClient
from yandex_mcp.token_storage import TokenStorage
import tempfile
import os


class TestOAuthToken:
    """Tests for OAuthToken dataclass."""

    def test_token_creation(self):
        """Test basic token creation."""
        token = OAuthToken(
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            token_type="bearer",
            expires_in=3600,
        )
        assert token.access_token == "test_access_token"
        assert token.refresh_token == "test_refresh_token"
        assert token.token_type == "bearer"
        assert token.expires_in == 3600

    def test_is_expired_false_when_fresh(self):
        """Test that fresh token is not expired."""
        token = OAuthToken(
            access_token="test",
            expires_in=3600,
            created_at=time.time(),
        )
        assert not token.is_expired

    def test_is_expired_true_when_old(self):
        """Test that old token is expired."""
        token = OAuthToken(
            access_token="test",
            expires_in=100,
            created_at=time.time() - 200,
        )
        assert token.is_expired

    def test_expires_at_calculation(self):
        """Test expiration timestamp calculation."""
        created = time.time()
        token = OAuthToken(
            access_token="test",
            expires_in=3600,
            created_at=created,
        )
        assert token.expires_at == pytest.approx(created + 3600, abs=1)


class TestYandexOAuthClient:
    """Tests for YandexOAuthClient."""

    def test_client_initialization_with_env(self, monkeypatch):
        """Test client initialization from environment variables."""
        monkeypatch.setenv("YANDEX_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("YANDEX_CLIENT_SECRET", "test_client_secret")
        
        client = YandexOAuthClient()
        assert client.client_id == "test_client_id"
        assert client.client_secret == "test_client_secret"

    def test_client_initialization_defaults(self):
        """Test client initialization with defaults."""
        client = YandexOAuthClient(
            client_id="my_client_id",
            client_secret="my_client_secret",
        )
        assert client.client_id == "my_client_id"
        assert client.client_secret == "my_client_secret"
        assert client.redirect_uri == "oob"

    def test_get_authorization_url(self):
        """Test authorization URL generation."""
        client = YandexOAuthClient(
            client_id="test_id",
            client_secret="test_secret",
            scopes="direct:api,metrika:read",
        )
        url = client.get_authorization_url()
        assert "response_type=code" in url
        assert "client_id=test_id" in url
        assert "scope=" in url
        assert "direct%3Aapi" in url or "direct:api" in url

    def test_get_authorization_url_with_state(self):
        """Test authorization URL with state parameter."""
        client = YandexOAuthClient(
            client_id="test_id",
            client_secret="test_secret",
        )
        url = client.get_authorization_url(state="random_state")
        assert "state=random_state" in url


class TestTokenStorage:
    """Tests for TokenStorage."""

    def test_save_and_load_token(self):
        """Test saving and loading tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = TokenStorage(storage_path=os.path.join(tmpdir, "tokens.json"))
            
            token = OAuthToken(
                access_token="test_access",
                refresh_token="test_refresh",
                expires_in=3600,
            )
            storage.save_token("direct", token)
            
            loaded = storage.load_token("direct")
            assert loaded is not None
            assert loaded.access_token == "test_access"
            assert loaded.refresh_token == "test_refresh"

    def test_load_nonexistent_token(self):
        """Test loading non-existent token returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = TokenStorage(storage_path=os.path.join(tmpdir, "tokens.json"))
            loaded = storage.load_token("nonexistent")
            assert loaded is None

    def test_clear_token(self):
        """Test clearing a token."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = TokenStorage(storage_path=os.path.join(tmpdir, "tokens.json"))
            
            token = OAuthToken(access_token="test", expires_in=3600)
            storage.save_token("direct", token)
            
            result = storage.clear_token("direct")
            assert result is True
            assert storage.load_token("direct") is None

    def test_clear_nonexistent_token(self):
        """Test clearing non-existent token returns False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = TokenStorage(storage_path=os.path.join(tmpdir, "tokens.json"))
            result = storage.clear_token("nonexistent")
            assert result is False

    def test_list_services(self):
        """Test listing services with tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = TokenStorage(storage_path=os.path.join(tmpdir, "tokens.json"))
            
            token = OAuthToken(access_token="test", expires_in=3600)
            storage.save_token("direct", token)
            storage.save_token("metrika", token)
            
            services = storage.list_services()
            assert "direct" in services
            assert "metrika" in services
