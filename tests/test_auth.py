"""
Tests for lib/auth.py
Supabase client is mocked — no real network calls.
"""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_supabase(monkeypatch):
    """Replace get_supabase() with a mock client."""
    client = MagicMock()
    monkeypatch.setattr("lib.auth.get_supabase", lambda: client)
    return client


@pytest.fixture
def mock_session_state(monkeypatch):
    """Provide a simple dict as st.session_state."""
    state = {}
    monkeypatch.setattr("lib.auth.st.session_state", state)
    return state


class TestLogin:
    def test_returns_user_on_valid_credentials(self, mock_supabase, mock_session_state):
        fake_user = MagicMock()
        mock_supabase.auth.sign_in_with_password.return_value = MagicMock(user=fake_user)

        from lib.auth import login

        result = login("user@example.com", "password123")

        assert result == fake_user
        assert mock_session_state["user"] == fake_user

    def test_returns_none_on_invalid_credentials(self, mock_supabase, mock_session_state):
        from gotrue.errors import AuthApiError

        mock_supabase.auth.sign_in_with_password.side_effect = AuthApiError(
            message="Invalid credentials", status=400, code="invalid_credentials"
        )

        from lib.auth import login

        result = login("user@example.com", "wrongpassword")

        assert result is None
        assert "user" not in mock_session_state


class TestLogout:
    def test_clears_session_state(self, mock_supabase, mock_session_state):
        mock_session_state["user"] = MagicMock()

        from lib.auth import logout

        logout()

        assert "user" not in mock_session_state
        mock_supabase.auth.sign_out.assert_called_once()


class TestGetCurrentUser:
    def test_returns_user_when_logged_in(self, mock_session_state):
        fake_user = MagicMock()
        mock_session_state["user"] = fake_user

        from lib.auth import get_current_user

        assert get_current_user() == fake_user

    def test_returns_none_when_not_logged_in(self, mock_session_state):
        from lib.auth import get_current_user

        assert get_current_user() is None
