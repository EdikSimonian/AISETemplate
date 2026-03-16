# Coding Standards

> Python-specific standards for the Streamlit + Supabase + DeepInfra stack.

---

## General Principles

1. **Streamlit pages are thin** — no business logic in page files; delegate to `lib/`
2. **One responsibility per module** — `lib/auth.py` handles auth, `lib/tasks.py` handles tasks
3. **Fail visibly** — use `st.error()` for user-facing errors, `raise` for programmer errors
4. **Cache wisely** — use `@st.cache_data` for expensive reads, never cache auth state

---

## Naming

| Thing | Convention | Example |
|-------|-----------|---------|
| Variables & functions | snake_case | `user_id`, `get_tasks()` |
| Classes | PascalCase | `SupabaseClient` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_MODEL` |
| Files | snake_case | `supabase_client.py`, `auth.py` |
| Streamlit pages | Snake_case with number prefix | `pages/1_Dashboard.py` |
| Database tables | snake_case | `user_tasks`, `chat_history` |

---

## Project Structure

```
app.py                      # Entry point — login gate + navigation
pages/
  1_Dashboard.py            # Page files — UI only
  2_[Feature].py
lib/
  supabase_client.py        # Returns initialized Supabase client
  deepinfra_client.py       # Returns initialized OpenAI client (DeepInfra)
  auth.py                   # login(), logout(), get_current_user()
  [feature].py              # One file per domain feature
prompts/
  [feature]_system.md       # System prompts — one file per AI feature
tests/
  test_[feature].py         # pytest tests for lib/ functions
supabase/
  migrations/               # SQL migration files
```

---

## Streamlit Patterns

### Auth gate — put at top of every protected page
```python
if not st.session_state.get("user"):
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state["user"]
```

### Forms — use `st.form` to batch inputs
```python
with st.form("create_task"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    submitted = st.form_submit_button("Create")

if submitted:
    if not title:
        st.error("Title is required.")
    else:
        create_task(user_id=user.id, title=title, content=content)
        st.success("Task created!")
        st.rerun()
```

### Streaming AI responses
```python
with st.chat_message("assistant"):
    response = st.write_stream(stream_response(system_prompt, user_input))
# Save to Supabase after stream completes
save_message(user_id=user.id, role="assistant", content=response)
```

---

## Supabase Patterns

### Always check the response
```python
# Good
response = supabase.table("tasks").select("*").execute()
tasks = response.data  # list of dicts

# Handle empty results gracefully
if not tasks:
    st.info("No tasks yet.")
```

### Use `.single()` for expected-one queries
```python
# Raises exception if 0 or 2+ rows — handle it
try:
    task = supabase.table("tasks").select("*").eq("id", task_id).single().execute()
except Exception:
    st.error("Task not found.")
    st.stop()
```

### Never build SQL strings from user input
```python
# Good — parameterized via supabase-py
supabase.table("tasks").select("*").eq("status", user_input).execute()

# Bad — never do this
supabase.rpc("raw_query", {"sql": f"SELECT * WHERE status = '{user_input}'"})
```

---

## DeepInfra / AI Patterns

### Keep system prompts in files, not in code
```python
# Good
from pathlib import Path
system_prompt = Path("prompts/task_assistant_system.md").read_text()

# Bad
system_prompt = "You are a helpful assistant that..."  # hardcoded in UI file
```

### Always constrain AI output for structured tasks
```python
system_prompt = """
You are a task analyzer. Respond ONLY with a JSON object in this exact format:
{"priority": "high|medium|low", "tags": ["tag1", "tag2"], "summary": "one sentence"}
Do not include any other text.
"""
```

### Sanitize user input before sending to AI
```python
def sanitize_input(text: str, max_length: int = 2000) -> str:
    # Trim whitespace and enforce max length
    return text.strip()[:max_length]
```

---

## Error Handling

```python
# Pattern for Supabase errors
from postgrest.exceptions import APIError

try:
    response = supabase.table("tasks").insert(data).execute()
except APIError as e:
    st.error(f"Could not save: {e.message}")
    return

# Pattern for DeepInfra errors
from openai import RateLimitError, APIConnectionError

try:
    result = get_ai_response(prompt)
except RateLimitError:
    st.warning("AI is busy — please try again shortly.")
except APIConnectionError:
    st.error("Could not reach AI service.")
```

---

## Testing

- Test all `lib/` functions with pytest
- Do not unit test Streamlit UI code — it requires a running Streamlit server
- Use `pytest-mock` or `unittest.mock` to mock Supabase and DeepInfra calls
- Test files go in `tests/test_[module].py`

```python
# Example: tests/test_auth.py
from unittest.mock import MagicMock, patch
from lib.auth import validate_email

def test_validate_email_rejects_invalid():
    assert validate_email("notanemail") is False

def test_validate_email_accepts_valid():
    assert validate_email("user@example.com") is True
```
