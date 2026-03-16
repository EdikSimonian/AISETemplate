import os

from supabase import Client, create_client

try:
    import streamlit as st

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
except Exception:
    # Fallback to environment variables (local dev / CI)
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_ANON_KEY"]

_client: Client | None = None


def get_supabase() -> Client:
    """Return a singleton Supabase client."""
    global _client
    if _client is None:
        _client = create_client(url, key)
    return _client
