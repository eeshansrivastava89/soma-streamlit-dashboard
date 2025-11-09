# SOMA Analytics Dashboard

Real-time Streamlit dashboard for A/B test analysis. **Status:** Deployed on Fly.io (private).

## Quick Start

**Deployed:** Fly.io (local/private access only)  
**Local Run:** `streamlit run app.py`  
**Data Source:** Supabase PostgreSQL (queries: v_variant_stats, v_conversion_funnel, posthog_events)

## Local Development

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .streamlit/secrets.toml with Supabase connection string
mkdir -p .streamlit
echo '[supabase]' > .streamlit/secrets.toml
echo 'connection_string = "postgresql://..."' >> .streamlit/secrets.toml

# Run
streamlit run app.py
# Opens at http://localhost:8501
```

## Architecture

**Data Flow:** PostHog → Supabase → Streamlit Dashboard

1. Events posted to Supabase (via PostHog webhook + batch export)
2. Streamlit queries aggregated views (10-second cache TTL)
3. Plotly visualizations updated automatically

## Features

- Variant comparison stats
- Conversion funnel analysis
- Completion time distribution
- Time series trends
- Statistical summaries

## Tech Stack

- **Framework:** Streamlit
- **Database:** Supabase (PostgreSQL)
- **Viz:** Plotly
- **Analysis:** Pandas
- **ORM:** SQLAlchemy

## Environment

**Deployment:** Fly.io (via `fly.toml`)  
**Region:** sjc  
**Port:** 8501  
**Secrets:** Set via `fly secret set SUPABASE_CONNECTION_STRING=...`

## Database Schema

See `../soma-blog-hugo/supabase-schema.sql` for reference.

Views used:
- `v_variant_stats` - Aggregated stats by variant
- `v_conversion_funnel` - Funnel analysis
- `posthog_events` - Raw events for time series

## Embedded in

SOMA Portfolio (Astro) at https://eeshans.com/projects/ab-test-simulator (iframe embed)

---

**Part of the SOMA project.** See [PROJECT_HISTORY.md](../soma-portfolio/PROJECT_HISTORY.md) for full architecture.
