"""Shared fixtures for Yandex MCP tests."""

import os
import pytest


@pytest.fixture(autouse=True)
def _set_dummy_token(monkeypatch):
    """Provide a dummy token so tools can register without real credentials."""
    monkeypatch.setenv("YANDEX_TOKEN", "test-token-for-registration")


@pytest.fixture
def mcp_instance():
    """Return a fresh FastMCP instance with all tools registered."""
    from yandex_mcp import mcp
    return mcp
