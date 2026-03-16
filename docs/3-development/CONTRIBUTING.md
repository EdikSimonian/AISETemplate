# Contributing Guide

## Branch Strategy

```
main          ← production-ready code only
  └── feat/us-01-user-login
  └── feat/us-02-ai-chat-feature
  └── fix/session-state-reset-bug
```

**Rules:**
- Never commit directly to `main`
- One branch per user story or bug fix
- Branch names: `feat/us-XX-short-description` or `fix/short-description`
- Delete branches after merging

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or page |
| `fix` | Bug fix |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `refactor` | Code change that isn't a feat or fix |
| `chore` | Dependencies, config, tooling |

**Examples:**
```
feat(auth): add login and signup pages
feat(ai): stream DeepInfra responses into chat UI
fix(supabase): handle RLS error when user is not authenticated
chore: add black and isort to pre-commit hooks
```

## Pull Request Process

1. Open a PR from your feature branch → `main`
2. Use the PR template — fill it out
3. Self-review your diff before requesting review
4. Get at least one teammate approval
5. CI must be green (lint + tests passing)
6. Squash and merge

## Local Development Setup

```bash
# 1. Clone the repo
git clone [repo-url]
cd [repo-name]

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Open .env and fill in:
#   SUPABASE_URL — from Supabase Dashboard → Settings → API
#   SUPABASE_ANON_KEY — from the same page (use the anon/public key)
#   DEEPINFRA_API_KEY — from deepinfra.com/dashboard

# 5. Run the app
streamlit run app.py
```

## Managing Secrets

**Locally:** use `.env` file (loaded via `python-dotenv` or `os.environ`)

**On Streamlit Community Cloud:** use `st.secrets`
- In the Streamlit Cloud dashboard, add secrets under App Settings → Secrets
- Format is TOML:
  ```toml
  SUPABASE_URL = "https://..."
  SUPABASE_ANON_KEY = "..."
  DEEPINFRA_API_KEY = "..."
  ```
- Access in code: `st.secrets["SUPABASE_URL"]` or `os.environ["SUPABASE_URL"]`

Never commit `.env` or `.streamlit/secrets.toml`.

## Supabase Local Development

For schema changes, always:
1. Make the change in Supabase Dashboard → SQL Editor
2. Copy the SQL into `supabase/migrations/YYYYMMDD_description.sql`
3. Commit the migration file so teammates can apply it

## Environment Variables

| Variable | Where to get it |
|----------|----------------|
| `SUPABASE_URL` | Supabase Dashboard → Settings → API |
| `SUPABASE_ANON_KEY` | Same page — use the `anon` / `public` key |
| `DEEPINFRA_API_KEY` | deepinfra.com → Dashboard → API Keys |
