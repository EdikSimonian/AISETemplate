import os
from collections.abc import Generator

from openai import OpenAI

try:
    import streamlit as st

    api_key = st.secrets["DEEPINFRA_API_KEY"]
    model = st.secrets.get("DEEPINFRA_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")
except Exception:
    api_key = os.environ["DEEPINFRA_API_KEY"]
    model = os.environ.get("DEEPINFRA_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Return a singleton DeepInfra client."""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepinfra.com/v1/openai",
        )
    return _client


def stream_response(system_prompt: str, user_message: str) -> Generator[str, None, None]:
    """Stream a response from DeepInfra. Use with st.write_stream()."""
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
    """Get a full (non-streaming) response from DeepInfra."""
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
