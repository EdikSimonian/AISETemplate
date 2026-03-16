# Claude Instructions for This Repository

This file gives Claude persistent context about this project so it can assist effectively across all workshop phases.

## Project Overview

<!-- FILL IN: Replace this section with your actual project description -->
- **What we're building:** [e.g., an AI-powered task management app]
- **Primary users:** [e.g., small teams of 2–10 people]
- **Tech stack:** Streamlit (frontend) + Supabase (database/auth) + DeepInfra (AI inference)
- **Deployment:** Streamlit Community Cloud (frontend) + Supabase hosted (backend)

## Stack Details

### Streamlit
- All UI is written in Python using Streamlit
- Use `st.session_state` for managing login state and app state
- Use `st.secrets` for all secrets in production (mirrors `.env` locally)
- Prefer `st.form` for user input to avoid re-runs on every keystroke
- Page structure: `pages/` directory for multi-page apps, `app.py` as entry point

### Supabase
- Client initialized once in `lib/supabase_client.py`
- Use the `supabase-py` library (`from supabase import create_client`)
- Auth: use `supabase.auth.sign_in_with_password()` / `sign_up()`
- Always enforce Row Level Security (RLS) policies on all tables
- Use Supabase Storage for file uploads
- Never call Supabase with the service role key from the frontend — use the anon key + RLS

### DeepInfra
- DeepInfra is OpenAI-compatible — use the `openai` Python SDK pointed at DeepInfra's base URL
- Client initialized in `lib/deepinfra_client.py`
- Default model: `meta-llama/Meta-Llama-3.1-8B-Instruct` (fast and free tier)
- Always stream responses for chat interfaces (`stream=True`)
- Keep system prompts in a dedicated `prompts/` directory, not hardcoded in UI code

## Coding Conventions

- Language: Python 3.11+
- Formatting: Black (88 char line length)
- Imports: isort, stdlib → third-party → local
- Naming: `snake_case` for variables and functions, `PascalCase` for classes
- File structure: feature-based modules under `lib/`
- No business logic in Streamlit page files — delegate to `lib/` modules

## Project Structure

```
app.py                  # Streamlit entry point
pages/                  # Additional Streamlit pages
lib/
  supabase_client.py    # Supabase client singleton
  deepinfra_client.py   # DeepInfra / OpenAI client
  auth.py               # Login, signup, session helpers
  [feature].py          # One module per feature
prompts/                # System prompts for AI features
tests/                  # pytest test files
.env                    # Local secrets (never commit)
.streamlit/secrets.toml # Streamlit secrets format (never commit)
```

## Patterns to Follow

- Check `st.session_state.get("user")` at the top of every protected page
- Wrap Supabase calls in try/except and surface errors via `st.error()`
- Stream DeepInfra responses into `st.write_stream()`
- Write pytest tests for all `lib/` functions — Streamlit UI is not unit tested

## Patterns to Avoid

- Do not put the Supabase service role key in the Streamlit app
- Do not call DeepInfra with user-controlled prompts that bypass your system prompt
- Do not use `st.experimental_rerun()` — use `st.rerun()` (Streamlit 1.27+)
- Do not store sensitive data in `st.session_state` beyond the user session

## Current Phase

<!-- UPDATE this as you move through the workshop -->
- [ ] Requirements
- [ ] Design
- [ ] Development
- [ ] Testing
- [ ] Deployment

## Key Files

- `docs/1-requirements/TEMPLATE.md` — finalized requirements
- `docs/2-design/ARCHITECTURE.md` — architecture decisions
- `docs/2-design/DATA_MODEL.md` — Supabase table schemas + RLS policies
- `lib/supabase_client.py` — database client
- `lib/deepinfra_client.py` — AI inference client
