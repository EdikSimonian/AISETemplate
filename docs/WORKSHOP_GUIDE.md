# Workshop Guide — One Week Software Engineering Sprint

**Stack: Streamlit + Supabase + DeepInfra**

## Goals

By the end of this workshop, your team will have:
- A working AI-powered app built from scratch in Python
- Hands-on experience with every phase of the software engineering lifecycle
- A deployed, publicly accessible product

---

## Account Setup (Before Day 1)

Each team member should have these accounts ready:

| Service | URL | Free? | What for |
|---------|-----|-------|---------|
| GitHub | github.com | Yes | Code hosting, CI |
| Supabase | supabase.com | Yes | Database + Auth |
| DeepInfra | deepinfra.com | Yes (credits) | LLM API |
| Streamlit Community Cloud | share.streamlit.io | Yes | App hosting |

---

## Daily Schedule

### Day 1 — Requirements & Kickoff

**Morning: Problem framing**
- [ ] Read and discuss the project brief (provided by facilitator)
- [ ] Fill in [`docs/1-requirements/TEMPLATE.md`](1-requirements/TEMPLATE.md):
  - Problem statement and personas
  - User stories — include at least one AI-powered feature
  - MoSCoW prioritization — be realistic about 5 days
- [ ] Create GitHub Issues for each user story

**Afternoon: Acceptance criteria + project setup**
- [ ] Complete [`docs/1-requirements/ACCEPTANCE_CRITERIA.md`](1-requirements/ACCEPTANCE_CRITERIA.md)
- [ ] Create a Supabase project (free tier)
- [ ] Get a DeepInfra API key
- [ ] Clone the template repo, set up `.env`, run `streamlit run app.py` locally

**AI tasks for Day 1:**
- Prompt: *"Generate 10 user stories for [your app description] including Supabase data features and one DeepInfra AI feature"*
- Prompt: *"What requirements am I missing for a Streamlit + Supabase + AI app?"*

**Deliverable:** Signed-off requirements + GitHub Issues + local dev environment running

---

### Day 1–2 — Design

**Morning (Day 2): Architecture + data model**
- [ ] Fill in [`docs/2-design/ARCHITECTURE.md`](2-design/ARCHITECTURE.md)
- [ ] Fill in [`docs/2-design/DATA_MODEL.md`](2-design/DATA_MODEL.md) with SQL for all tables
- [ ] Create tables in Supabase SQL Editor and verify they work
- [ ] Enable RLS on every table and write policies

**Afternoon (Day 2): AI feature design**
- [ ] Fill in [`docs/2-design/API_SPEC.md`](2-design/API_SPEC.md) with your Supabase queries and DeepInfra calls
- [ ] Write your system prompt(s) to `prompts/` directory
- [ ] Team review — resolve any open questions before coding starts

**AI tasks for Day 2:**
- Prompt: *"Design the Supabase schema for these user stories: [paste stories]"*
- Prompt: *"Write RLS policies for my [table name] table"*
- Prompt: *"Design the system prompt and DeepInfra call for my AI feature: [describe feature]"*

**Deliverable:** Tables created in Supabase, RLS enabled, AI feature designed

---

### Day 2–4 — Development

**Setup (Day 2, end of day):**
- [ ] Set up `lib/supabase_client.py` and `lib/deepinfra_client.py`
- [ ] Build auth pages (`Login`, `Signup`) and test with Supabase
- [ ] Set up CI pipeline — push to GitHub, verify Actions passes

**Development rhythm (Day 3–4):**
- Work in feature branches, open PRs for each user story
- Each feature: write the `lib/` function first, then the Streamlit page
- Test locally after every feature before moving on
- Daily standup: what did you build? what's blocked?

**AI tasks for Day 3–4:**
- Use Claude Code (`claude`) in your terminal — it has context from `CLAUDE.md`
- Scaffold features: *"Write a Streamlit page and lib/ function for [feature]"*
- Debug: paste error + stack trace into Claude
- Review diffs: *"Review this Streamlit + Supabase code for bugs and security issues"*

**Deliverable:** Core features implemented, auth working, AI feature integrated

---

### Day 4–5 — Testing

**Day 4 afternoon:**
- [ ] Fill in [`docs/4-testing/TEST_PLAN.md`](4-testing/TEST_PLAN.md)
- [ ] Set up pytest if not already done (`pip install pytest pytest-cov pytest-mock`)
- [ ] Write tests for `lib/` functions — mock Supabase and DeepInfra calls

**Day 5 morning:**
- [ ] Fill in [`docs/4-testing/TEST_CASES.md`](4-testing/TEST_CASES.md)
- [ ] Cover all acceptance criteria with at least one test each
- [ ] Push and verify CI pipeline is green (lint + tests passing)
- [ ] Manual test of all core flows

**AI tasks for Day 4–5:**
- Prompt: *"Write pytest tests for this lib/ function, mock the Supabase client"*
- Prompt: *"What edge cases am I missing in tests for a Supabase + Streamlit app?"*
- Prompt: *"Generate test fixtures for my [table] schema"*

**Deliverable:** Test suite passing in CI, all acceptance criteria verified

---

### Day 5 — Deployment

**Morning:**
- [ ] Fill in [`docs/5-deployment/DEPLOYMENT.md`](5-deployment/DEPLOYMENT.md)
- [ ] Ensure `requirements.txt` is up to date
- [ ] Create app on Streamlit Community Cloud:
  - Connect GitHub repo
  - Set main file to `app.py`
  - Add secrets (SUPABASE_URL, SUPABASE_ANON_KEY, DEEPINFRA_API_KEY)
  - Deploy

**Afternoon:**
- [ ] Run smoke tests on the live URL
- [ ] Demo the app to the group
- [ ] Team retrospective — fill in the retrospective section of DEPLOYMENT.md

**AI tasks for Day 5:**
- Prompt: *"Review my Streamlit + Supabase + DeepInfra app for security issues before deployment"*
- Prompt: *"Generate a deployment checklist for Streamlit Community Cloud with Supabase"*

**Deliverable:** Live app URL, smoke tests passed, retrospective done

---

## Team Roles (Rotate Daily)

| Role | Responsibility |
|------|---------------|
| Driver | Writing code or docs |
| Navigator | Reviewing, suggesting, catching mistakes |
| AI Operator | Running AI prompts, evaluating output, integrating suggestions |
| Note-taker | Capturing decisions, blockers, and rationale in docs |

## Definition of Done

A feature is done when:
1. `lib/` function implemented and reviewed via PR
2. Streamlit page implemented and manually tested
3. Tests written and passing in CI
4. Acceptance criteria from Day 1 are met
5. RLS verified — no data leaking between users
