# Architecture Document

> Complete this document on Day 2 before writing any code.

---

## 1. System Overview

**Architecture style:** Single-tier Python app — Streamlit calls Supabase and DeepInfra directly. No custom backend server.

```
┌─────────────────────────────────────────┐
│         Streamlit App (Python)          │
│         Streamlit Community Cloud       │
│                                         │
│  ┌──────────┐  ┌──────────────────────┐ │
│  │  Pages   │  │     lib/ modules     │ │
│  │ (UI only)│  │ auth, features, etc. │ │
│  └──────────┘  └──────────────────────┘ │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌─────────────────────┐
│   Supabase    │    │     DeepInfra       │
│               │    │                     │
│ • PostgreSQL  │    │ • LLM inference     │
│ • Auth        │    │ • OpenAI-compatible │
│ • Storage     │    │   REST API          │
│ • RLS         │    │                     │
└───────────────┘    └─────────────────────┘
```

---

## 2. Components

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| UI | Streamlit | All user-facing pages and interaction |
| Database | Supabase (PostgreSQL) | Persistent data storage |
| Auth | Supabase Auth | User signup, login, session management |
| File Storage | Supabase Storage | User-uploaded files (if needed) |
| AI Inference | DeepInfra | LLM completions, embeddings, etc. |
| Hosting | Streamlit Community Cloud | Serves the Streamlit app |

---

## 3. Authentication Flow

```
1. User fills login form in Streamlit
2. App calls supabase.auth.sign_in_with_password()
3. Supabase returns a session (access_token + user object)
4. Session stored in st.session_state["user"]
5. All subsequent Supabase queries use the user's JWT
   → Row Level Security (RLS) enforces data isolation automatically
6. On logout: supabase.auth.sign_out(), clear st.session_state
```

---

## 4. Data Flow — AI Feature

```
1. User submits input in Streamlit form
2. lib/[feature].py builds a prompt using the user input + system prompt from prompts/
3. DeepInfra client sends request to DeepInfra API (OpenAI-compatible)
4. Response streamed back to Streamlit via st.write_stream()
5. Result optionally saved to Supabase for history/audit
```

---

## 5. Architecture Decision Records (ADRs)

### ADR-01: No custom backend server

**Status:** Accepted

**Context:** Workshop has 5 days. A custom API layer (Flask, FastAPI) adds infrastructure complexity with little benefit at this scale.

**Decision:** Streamlit calls Supabase and DeepInfra directly from Python. Supabase RLS handles authorization.

**Consequences:** Simpler architecture. Supabase anon key is used (safe with RLS). Not suitable for complex server-side business logic or background jobs.

---

### ADR-02: Supabase for database and auth

**Status:** Accepted

**Context:** Need a hosted database with auth, a free tier, and a Python SDK.

**Decision:** Supabase provides PostgreSQL + Auth + Storage + auto REST API. Free tier covers workshop scale.

**Consequences:** Tied to Supabase's managed service. RLS policies must be set up correctly — if skipped, data is unprotected.

---

### ADR-03: DeepInfra for AI inference

**Status:** Accepted

**Context:** Need an LLM API that is cheap/free for workshop use, OpenAI-compatible (easy SDK), and supports open-source models.

**Decision:** DeepInfra provides a wide range of open models (Llama, Mistral, etc.) with a pay-per-token model and a free starter credit. Its API is OpenAI-compatible so the `openai` Python SDK works without changes.

**Consequences:** Requires a DeepInfra API key. Model availability and latency depend on DeepInfra's infrastructure.

---

### ADR-04: Streamlit for frontend

**Status:** Accepted

**Context:** Team is Python-first. Need a hosted UI with minimal boilerplate.

**Decision:** Streamlit lets us build interactive UIs in pure Python. Streamlit Community Cloud provides free hosting connected directly to a GitHub repo.

**Consequences:** UI is more limited than React/Vue. Not ideal for complex UX patterns. `st.session_state` must be managed carefully to avoid unexpected re-runs.

---

## 6. Security Considerations

- **RLS is mandatory** — every Supabase table must have Row Level Security policies enabled
- **Anon key only** — never use the Supabase service role key in the Streamlit app
- **Secrets** — all keys stored in `.env` locally and `st.secrets` in production, never in code
- **Prompt injection** — sanitize or constrain user input before passing to DeepInfra
- **Auth gates** — check `st.session_state.get("user")` at the top of every protected page

---

## 7. Known Limitations

| Limitation | Mitigation |
|------------|-----------|
| Streamlit re-runs entire script on interaction | Use `st.session_state` and `st.cache_data` carefully |
| No background jobs | Use Supabase Edge Functions or cron if needed |
| DeepInfra rate limits on free tier | Add `st.spinner` + handle API errors gracefully |
| Streamlit Community Cloud cold starts | Acceptable for a workshop |
