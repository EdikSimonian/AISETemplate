# Software Engineering Workshop Template

A one-week structured workshop template for building AI-powered apps using **Streamlit**, **Supabase**, and **DeepInfra** — fully in Python, fully free tier.

## Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | [Streamlit](https://streamlit.io) | Python UI, hosted on Streamlit Community Cloud |
| Database & Auth | [Supabase](https://supabase.com) | PostgreSQL, authentication, file storage |
| AI Inference | [DeepInfra](https://deepinfra.com) | LLM and image model API (OpenAI-compatible) |

## Workshop Overview

| Day | Phase | Goal |
|-----|-------|------|
| Day 1 | Requirements | Define the problem, users, and success criteria |
| Day 1–2 | Design | Architecture, data model, AI feature design |
| Day 2–4 | Development | Build with Streamlit + Supabase + DeepInfra |
| Day 4–5 | Testing | Validate correctness, coverage, and edge cases |
| Day 5 | Deployment | Ship to Streamlit Community Cloud |

## Quick Start

1. Click **"Use this template"** on GitHub to create your repo
2. Create a free [Supabase](https://supabase.com) project
3. Create a free [DeepInfra](https://deepinfra.com) account and get an API key
4. Copy `.env.example` → `.env` and fill in your keys
5. Read [`docs/WORKSHOP_GUIDE.md`](docs/WORKSHOP_GUIDE.md) for the daily schedule
6. Use [`docs/AI_PROMPTS.md`](docs/AI_PROMPTS.md) for ready-to-use prompts at each phase

## Local Setup

```bash
# 1. Clone your repo
git clone [your-repo-url]
cd [your-repo-name]

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_ANON_KEY, DEEPINFRA_API_KEY

# 5. Run the app
streamlit run app.py
```

## Repository Structure

```
app.py                      # Streamlit entry point
pages/                      # Additional app pages
lib/
  supabase_client.py        # Supabase client
  deepinfra_client.py       # DeepInfra / AI client
  auth.py                   # Auth helpers
prompts/                    # AI system prompts
tests/                      # pytest tests
requirements.txt
.env.example
.github/
  ISSUE_TEMPLATE/           # User story and bug templates
  PULL_REQUEST_TEMPLATE.md
  workflows/ci.yml          # Lint, test, deploy pipeline
docs/
  WORKSHOP_GUIDE.md         # Daily schedule and deliverables
  AI_PROMPTS.md             # Phase-by-phase AI prompt library
  1-requirements/
  2-design/
  3-development/
  4-testing/
  5-deployment/
CLAUDE.md                   # AI assistant standing instructions
```

## Deliverables Checklist

- [ ] Requirements doc with user stories and acceptance criteria
- [ ] Supabase schema with RLS policies
- [ ] Working Streamlit app with AI feature
- [ ] Test suite passing in CI
- [ ] Deployed to Streamlit Community Cloud
- [ ] Retrospective notes
