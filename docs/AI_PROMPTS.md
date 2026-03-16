# AI Prompt Library

Ready-to-use prompts for each workshop phase, tailored to the **Streamlit + Supabase + DeepInfra** stack.

---

## Phase 1 — Requirements

### Generate user stories from a problem description
```
I'm building [brief description of your app] using Streamlit, Supabase, and DeepInfra (LLM API).
The primary users are [describe users].

Generate 10 user stories in the format:
"As a [persona], I want to [action] so that [outcome]."

Include a mix of:
- Data management features (CRUD via Supabase)
- AI-powered features (using an LLM via DeepInfra)
- Auth and user account features
```

### Identify missing requirements
```
Here are my current requirements for a Streamlit + Supabase app:
[paste your requirements doc]

What important requirements am I likely missing? Focus on:
- Auth edge cases (password reset, expired sessions)
- Data ownership and privacy (who can see whose data)
- AI feature guardrails (what happens with bad LLM output)
- Error states (API down, no results, rate limits)
```

### MoSCoW prioritization
```
Here are my user stories for a one-week workshop project:
[paste stories]

Help me prioritize using MoSCoW. Constraints:
- 5 days to build and deploy
- Team of [size] with Python experience but new to Streamlit/Supabase
- Must have a working AI feature using DeepInfra

Be realistic about what a small team can finish in 5 days.
```

---

## Phase 2 — Design

### Design the Supabase schema
```
Here are the user stories my app needs to support:
[paste user stories]

Design the Supabase (PostgreSQL) schema. For each table include:
- Column names, types, and constraints
- Primary and foreign keys (use UUIDs, reference auth.users for user_id)
- Row Level Security (RLS) policies for each table
- Any indexes needed for common queries
- Any triggers (e.g. auto-update updated_at, auto-create profile on signup)

Format each table as a SQL CREATE TABLE statement ready to run in the Supabase SQL editor.
```

### Design the AI feature
```
I want to add an AI feature to my Streamlit app using DeepInfra (OpenAI-compatible API).

Feature description: [describe what the AI should do]
User input: [what the user provides]
Expected output: [what the AI should return]

Design:
1. A system prompt for this feature (stored in prompts/ directory)
2. The Python function signature in lib/ that calls DeepInfra
3. How to display the result in Streamlit (streaming or not?)
4. What to save to Supabase (if anything)
5. Error handling strategy
```

### Architecture review
```
Here is my proposed Streamlit + Supabase + DeepInfra architecture:
[paste your ARCHITECTURE.md]

Review for:
1. Supabase RLS — am I protecting data correctly?
2. Secret management — are API keys handled safely?
3. Session state — am I managing Streamlit state correctly?
4. AI safety — could users abuse the DeepInfra integration?
5. Anything that would cause problems at workshop demo time
```

### Compare AI feature approaches
```
I want to add an AI feature where [describe feature].
I'm using DeepInfra with the Llama-3.1-8B-Instruct model.

Compare these implementation approaches:
1. Single LLM call with a detailed system prompt
2. Chain of two LLM calls (plan then execute)
3. Structured output (force JSON response) + validation

For each: pros, cons, complexity, and your recommendation for a 5-day workshop timeline.
```

---

## Phase 3 — Development

### Scaffold a Streamlit page
```
Using Streamlit and supabase-py, scaffold a complete page for:
[describe the feature, e.g. "a task list where users can create, view, and delete tasks"]

The page should:
- Check st.session_state["user"] at the top and stop if not logged in
- Call lib/[feature].py functions (don't put DB logic in the page)
- Use st.form for user input
- Show st.error() for errors, st.success() for success
- Call st.rerun() after mutations

Also write the corresponding lib/[feature].py with the Supabase queries.
```

### Scaffold auth pages
```
Write two Streamlit pages for a Supabase auth flow:

1. pages/Login.py — email/password login form
   - On success: store user in st.session_state["user"], redirect to main page
   - On failure: show st.error with a helpful message

2. pages/Signup.py — email/password/name signup form
   - Validate inputs before calling Supabase
   - On success: show confirmation message

Also write lib/auth.py with:
- login(email, password) -> user | None
- signup(email, password, name) -> user | None
- logout() -> None
- get_current_user() -> user | None

Use the supabase-py library.
```

### Build a streaming AI chat feature
```
Write a Streamlit chat interface that:
1. Shows chat history (stored in Supabase table: chat_messages)
2. Accepts user input via st.chat_input
3. Streams the DeepInfra response using st.write_stream
4. Saves both user message and assistant response to Supabase after streaming

Stack:
- Streamlit for UI
- supabase-py for persistence
- openai SDK pointed at DeepInfra (base_url="https://api.deepinfra.com/v1/openai")
- Model: meta-llama/Meta-Llama-3.1-8B-Instruct

The system prompt should be loaded from prompts/chat_system.md
```

### Debug an error
```
I'm getting this error in my Streamlit + Supabase app:
[paste error message and stack trace]

Relevant code:
[paste code]

Explain the cause and provide a fix.
Note: this is a Streamlit app — re-runs happen on every interaction, which may be relevant.
```

### Code review
```
Review this Streamlit + Supabase code:
[paste code]

Check specifically for:
1. Supabase RLS — is the query safe if the user manipulates their session?
2. Streamlit session state — any risk of state leaking between users?
3. AI prompt injection — can a user manipulate the LLM via their input?
4. Secrets — are API keys accessed safely (st.secrets or os.environ)?
5. Error handling — are Supabase and DeepInfra errors caught and shown to the user?
```

---

## Phase 4 — Testing

### Generate tests for a lib/ module
```
Write pytest tests for this Python module:
[paste lib/[feature].py]

Since this calls Supabase, mock the Supabase client using unittest.mock.
Cover:
- Happy path: expected input returns expected output
- Empty result: Supabase returns empty list
- Supabase APIError: function handles it gracefully
- Input validation: invalid inputs are rejected before hitting Supabase

Use descriptive test names like test_get_tasks_returns_empty_list_when_no_tasks_exist.
```

### Generate tests for AI functions
```
Write pytest tests for this DeepInfra integration function:
[paste lib/deepinfra function]

Since this calls an external API, mock the openai client.
Cover:
- Successful response: returns expected text
- RateLimitError: function raises or returns appropriate fallback
- APIConnectionError: function raises or returns appropriate fallback
- Empty/malformed response: function handles gracefully
```

### Find untested edge cases
```
Here are my functions and their tests:

Functions:
[paste lib/ code]

Tests:
[paste test code]

What Supabase or DeepInfra-specific edge cases are missing?
Consider: expired auth tokens, RLS policy violations, rate limits, network timeouts, and malformed AI responses.
```

---

## Phase 5 — Deployment

### Generate requirements.txt
```
Here are my Python imports across the project:
[paste a list or the import lines from your files]

Generate a requirements.txt for a Streamlit app using:
- streamlit
- supabase-py
- openai (for DeepInfra)
- Any other packages I'm using

Pin major versions. Add pytest, black, isort, flake8 as dev dependencies in a comment block.
```

### Write Supabase RLS policies
```
I have this Supabase table:
[paste CREATE TABLE SQL]

Write RLS policies for:
- SELECT: users can only see rows where user_id = auth.uid()
- INSERT: users can only insert rows where user_id = auth.uid()
- UPDATE: users can only update their own rows
- DELETE: users can only delete their own rows

Format as SQL ready to run in the Supabase SQL editor.
Also add the ALTER TABLE to enable RLS.
```

### Generate a deployment checklist
```
Generate a deployment checklist for a Streamlit app deploying to Streamlit Community Cloud with:
- Supabase as the database (PostgreSQL + Auth)
- DeepInfra as the AI inference API

The checklist should cover:
1. Code readiness (tests, linting, requirements.txt)
2. Supabase readiness (schema, RLS, auth config)
3. Secret configuration in Streamlit Cloud
4. Post-deploy smoke tests specific to this stack
5. Common failure modes to watch for
```

### Security review
```
Review my Streamlit + Supabase + DeepInfra app for security issues:
[paste your app.py and key lib/ files, or describe the architecture]

Check for:
1. Supabase anon key exposure (is it safe with RLS in place?)
2. DeepInfra key leakage (is it only in st.secrets / os.environ?)
3. Prompt injection via user input
4. Missing auth checks on protected pages
5. Data isolation — can one user access another's data?
6. Session management — is logout complete?
```
