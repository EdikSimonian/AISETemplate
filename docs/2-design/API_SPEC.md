# API Design

> With Supabase, most CRUD operations are handled automatically via the Supabase client.
> This document covers: the Supabase queries your app uses, and the DeepInfra models and prompts you call.

---

## Supabase Client Queries

Document the key queries your Streamlit app makes so the team has a shared reference.

### Auth

```python
# Sign up
supabase.auth.sign_up({"email": email, "password": password, "options": {"data": {"name": name}}})

# Sign in
supabase.auth.sign_in_with_password({"email": email, "password": password})

# Sign out
supabase.auth.sign_out()

# Get current user
supabase.auth.get_user()
```

---

### [your_table] — CRUD

```python
# List — current user's rows only (RLS handles filtering)
supabase.table("your_table").select("*").order("created_at", desc=True).execute()

# Get one
supabase.table("your_table").select("*").eq("id", row_id).single().execute()

# Create
supabase.table("your_table").insert({
    "title": title,
    "content": content,
    "user_id": user_id
}).execute()

# Update
supabase.table("your_table").update({
    "title": new_title
}).eq("id", row_id).execute()

# Delete
supabase.table("your_table").delete().eq("id", row_id).execute()
```

---

### Error Handling Pattern

```python
from postgrest.exceptions import APIError

try:
    response = supabase.table("your_table").select("*").execute()
    return response.data
except APIError as e:
    st.error(f"Database error: {e.message}")
    return []
```

---

## DeepInfra API

DeepInfra uses the OpenAI-compatible API. Initialize the client once:

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPINFRA_API_KEY"],
    base_url="https://api.deepinfra.com/v1/openai"
)
```

---

### Models Available

| Model | Best for | Speed | Cost |
|-------|---------|-------|------|
| `meta-llama/Meta-Llama-3.1-8B-Instruct` | General tasks, fast | Fast | Low |
| `meta-llama/Meta-Llama-3.1-70B-Instruct` | Complex reasoning | Medium | Medium |
| `mistralai/Mistral-7B-Instruct-v0.3` | Instruction following | Fast | Low |
| `microsoft/WizardLM-2-8x22B` | Complex tasks | Slow | Higher |

Start with `Llama-3.1-8B` during development, upgrade if quality is insufficient.

---

### Chat Completion (streaming)

```python
def stream_response(system_prompt: str, user_message: str):
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        stream=True,
        max_tokens=1024,
        temperature=0.7
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

# In your Streamlit page:
with st.chat_message("assistant"):
    st.write_stream(stream_response(system_prompt, user_input))
```

---

### Chat Completion (non-streaming)

```python
def get_response(system_prompt: str, user_message: str) -> str:
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content
```

---

## Prompt Inventory

Document your system prompts here. Store them as `.txt` or `.md` files in `prompts/`.

| Prompt File | Feature | Description |
|-------------|---------|-------------|
| `prompts/[feature].md` | [feature name] | [what it does] |

---

## Rate Limits & Error Handling

| Error | Cause | Handling |
|-------|-------|---------|
| `RateLimitError` | Too many requests | Catch, show `st.warning`, retry with backoff |
| `AuthenticationError` | Bad API key | Catch, show `st.error("AI service unavailable")` |
| `APIConnectionError` | Network issue | Catch, show `st.error`, offer retry button |

```python
from openai import RateLimitError, AuthenticationError, APIConnectionError

try:
    response = get_response(system_prompt, user_input)
except RateLimitError:
    st.warning("AI service is busy. Please try again in a moment.")
except (AuthenticationError, APIConnectionError) as e:
    st.error("AI service is currently unavailable.")
```
