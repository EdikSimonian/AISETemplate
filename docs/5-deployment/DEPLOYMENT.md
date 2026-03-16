# Deployment Guide & Runbook

> Deploy your Streamlit app to Streamlit Community Cloud — free, connected directly to your GitHub repo.

---

## Environment Overview

| Environment | URL | How to deploy |
|-------------|-----|--------------|
| Local | http://localhost:8501 | `streamlit run app.py` |
| Production | `https://[your-app].streamlit.app` | Push to `main` → auto-deploys |

---

## Required Secrets

Set these in Streamlit Community Cloud → App Settings → Secrets (TOML format):

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
DEEPINFRA_API_KEY = "your-deepinfra-key"
```

Where to find each:
| Secret | Location |
|--------|---------|
| `SUPABASE_URL` | Supabase Dashboard → Settings → API |
| `SUPABASE_ANON_KEY` | Same page — the `anon` / `public` key |
| `DEEPINFRA_API_KEY` | deepinfra.com → Dashboard → API Keys |

---

## First Deployment (Step by Step)

### 1. Prepare your repo
- [ ] All code pushed to `main`
- [ ] `requirements.txt` is up to date (`pip freeze > requirements.txt`)
- [ ] No `.env` or secrets in the repo

### 2. Set up Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo, branch (`main`), and main file (`app.py`)
5. Click **"Advanced settings"** → add your secrets (TOML format above)
6. Click **"Deploy"**

### 3. Verify Supabase is ready
- [ ] All tables created with correct schema
- [ ] RLS policies enabled and tested on all tables
- [ ] Auth providers configured (email/password at minimum)
- [ ] Auto-create profile trigger installed

### 4. Smoke test the deployment
- [ ] App loads without errors
- [ ] Can sign up as a new user
- [ ] Can log in with existing credentials
- [ ] Core AI feature works end-to-end
- [ ] Check Streamlit Cloud logs for any errors (Manage app → Logs)

---

## Ongoing Deployments

Streamlit Community Cloud auto-deploys every time you push to `main`.

**No action needed** — just merge your PR to `main` and the app updates within ~1 minute.

To monitor: open your app URL → **☰ Manage app** (bottom right) → **Logs**

---

## Pre-Deployment Checklist

Before merging to `main`:

- [ ] Tests passing in CI
- [ ] No secrets committed to the repo
- [ ] `requirements.txt` updated if you added new packages
- [ ] Supabase schema changes applied and migration file committed
- [ ] New environment variables added to Streamlit Cloud secrets

---

## Rollback Procedure

### Option 1: Revert the commit (preferred)
```bash
git revert HEAD
git push origin main
# Streamlit Cloud will re-deploy automatically
```

### Option 2: Reboot the app
- Streamlit Cloud dashboard → **☰ Manage app** → **Reboot app**
- This restarts the app without redeploying (useful for memory/cache issues)

### Option 3: Pin to a previous commit
- Streamlit Cloud → App settings → change the branch/commit
- Or: create a `hotfix/rollback` branch from a known-good commit and deploy that

---

## Supabase Maintenance

### Applying schema changes
```bash
# 1. Write and test your SQL in Supabase Dashboard → SQL Editor
# 2. Save to a migration file
# Format: supabase/migrations/YYYYMMDD_HHMM_description.sql

# 3. Commit the file
git add supabase/migrations/
git commit -m "chore(db): add chat_history table"
```

### Backups
Supabase free tier takes daily backups (retained 7 days).
To manually export: Supabase Dashboard → Settings → Database → Backups

---

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| App shows "ModuleNotFoundError" | Missing package in `requirements.txt` | Add package, push to main |
| Blank page after login | `st.session_state` lost on rerun | Check auth logic in `lib/auth.py` |
| Supabase returns empty data | RLS policy blocking the query | Check RLS policies match your auth state |
| AI feature returns no response | Bad DeepInfra API key or rate limit | Verify key in Cloud secrets; check DeepInfra dashboard |
| App crashes with secret error | Secret not added to Streamlit Cloud | Add to App Settings → Secrets |
| Slow cold start | Normal for free tier | First load after inactivity can take ~30s |

---

## Retrospective Notes

> Fill this in after your Day 5 deploy.

**What went smoothly:**

**What was harder than expected:**

**What we'd do differently:**

**Live URL:**
