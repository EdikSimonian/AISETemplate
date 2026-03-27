import os
from collections.abc import Generator

from openai import OpenAI

try:
    import streamlit as st

    api_key = st.secrets.get("LITELLM_API_KEY", "")
    model = st.secrets.get("LITELLM_MODEL", "gpt-4o-mini")
except Exception:
    api_key = os.environ.get("LITELLM_API_KEY", "")
    model = os.environ.get("LITELLM_MODEL", "gpt-4o-mini")

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Return a singleton LiteLLM client."""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=api_key or "no-key",
            base_url="https://ai.simonian.online/v1",
        )
    return _client


def stream_response(system_prompt: str, user_message: str) -> Generator[str, None, None]:
    """Stream a response from LiteLLM. Use with st.write_stream()."""
    client = get_client()
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message[:4000]},  # guard against huge inputs
        ],
        stream=True,
        max_tokens=1024,
        temperature=0.7,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content


def get_response(system_prompt: str, user_message: str) -> str:
    """Get a full (non-streaming) response from LiteLLM."""
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message[:4000]},
        ],
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
