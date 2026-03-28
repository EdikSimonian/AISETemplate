import streamlit as st
from supabase_auth import User
from supabase_auth.errors import AuthApiError

from lib.supabase_client import get_supabase


def login(email: str, password: str) -> tuple[User | None, str | None]:
    """Sign in with email and password. Returns (user, error_message)."""
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        st.session_state["user"] = response.user
        return response.user, None
    except AuthApiError as e:
        return None, e.message


def signup(email: str, password: str, name: str) -> User | None:
    """Create a new account. Returns the user on success, None on failure."""
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": {"name": name}},
            }
        )
        return response.user
    except AuthApiError:
        return None


def logout() -> None:
    """Sign out and clear session state."""
    supabase = get_supabase()
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.pop("user", None)


def get_current_user() -> User | None:
    """Return the current user from session state, or None if not logged in."""
    return st.session_state.get("user")
