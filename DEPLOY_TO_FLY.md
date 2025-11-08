# Deploy Streamlit Dashboard to Fly.io

## Prerequisites
- Fly.io CLI installed (`brew install flyctl` on macOS)
- Logged in to Fly.io (`fly auth login`)
- Supabase connection string ready

## Deployment Steps

### 1. Navigate to the dashboard directory
```bash
cd /Users/eeshans/dev/soma-streamlit-dashboard
```

### 2. Create the Fly.io app (one-time setup)
```bash
fly launch --no-deploy --app soma-streamlit-dashboard --region sjc
```

**Note:** This will create the app but NOT deploy yet. We need to add secrets first.

### 3. Set Supabase connection string as secret
```bash
fly secret set SUPABASE_CONNECTION_STRING="postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres" --app soma-streamlit-dashboard
```

Replace `[PASSWORD]` and `[PROJECT]` with your actual Supabase credentials.

**Find your connection string:**
- Go to Supabase dashboard → Project → Connect
- Copy PostgreSQL connection string
- Use the one with `[PASSWORD]` placeholder
- Format: `postgresql://postgres:password@xxx.supabase.co:5432/postgres`

### 4. Deploy
```bash
fly deploy --app soma-streamlit-dashboard
```

First deploy takes ~2-3 minutes. Wait for it to complete.

### 5. Verify deployment
```bash
fly status --app soma-streamlit-dashboard
```

Or visit: https://soma-streamlit-dashboard.fly.dev

### 6. View logs (if needed)
```bash
fly logs --app soma-streamlit-dashboard
```

---

## What we did:
- ✅ Created `Dockerfile` (Streamlit in Python 3.11 container)
- ✅ Created `fly.toml` (Fly.io config with port 8501)
- ✅ Updated `app.py` to read `SUPABASE_CONNECTION_STRING` from environment
- ✅ Updated Astro iframe to point to `https://soma-streamlit-dashboard.fly.dev`

## Files created/modified:
- `/soma-streamlit-dashboard/Dockerfile` (NEW)
- `/soma-streamlit-dashboard/fly.toml` (NEW)
- `/soma-streamlit-dashboard/app.py` (MODIFIED - added env variable support)
- `/soma-portfolio/src/pages/projects/ab-test-simulator.astro` (MODIFIED - updated iframe URL)

---

## Troubleshooting

**App won't start:**
- Check logs: `fly logs --app soma-streamlit-dashboard`
- Usually means Supabase connection failed
- Verify `SUPABASE_CONNECTION_STRING` secret is set correctly

**Streamlit shows blank page:**
- Check if database has data (no events yet = empty dashboard)
- Try playing the puzzle on the portfolio first to generate events

**CORS/Embed errors:**
- Fly.io should handle CORS automatically
- Make sure iframe is `https://`

---

Ready to deploy? Run the commands above in order. Let me know if you hit any snags!
