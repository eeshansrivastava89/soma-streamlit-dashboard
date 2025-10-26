# SOMA Blog - A/B Test Dashboard

Real-time Streamlit dashboard for analyzing word search puzzle A/B test results.

## Features

- 📊 Live statistics updating every 10 seconds
- ⚖️ Variant comparison (Control vs 4-words)
- ⏱️ Completion time distribution
- 🎯 Conversion funnel analysis
- 📅 Time series trends
- 📐 Statistical summaries

## Architecture

```
PostHog Events → Supabase (PostgreSQL) → Streamlit Dashboard → Embedded in Hugo
```

**Data Flow:**
1. User plays puzzle on Hugo blog
2. PostHog tracks events in real-time
3. Webhook delivers events to Supabase (< 1 second latency)
4. Streamlit queries Supabase views for aggregated stats
5. Dashboard auto-refreshes with new data

## Tech Stack

- **Streamlit** - Python dashboard framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **SQLAlchemy** - Database connection
- **Supabase** - PostgreSQL database

## Local Development

### Prerequisites

- Python 3.9+
- Supabase account with connection credentials

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eeshansrivastava89/soma-streamlit-dashboard.git
cd soma-streamlit-dashboard
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml`:
```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

5. Add Supabase connection string to `.streamlit/secrets.toml`:
```toml
[supabase]
connection_string = "postgresql://postgres:[YOUR-PASSWORD]@[YOUR-PROJECT].supabase.co:5432/postgres"
```

Replace `[YOUR-PASSWORD]` and `[YOUR-PROJECT]` with your actual Supabase credentials.

6. Run the app:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Database Schema

The dashboard queries these Supabase views:

- `v_variant_stats` - Aggregated statistics by variant
- `v_conversion_funnel` - Start → Complete → Fail funnel
- `posthog_events` - Raw event data for time series

See [supabase-schema.sql](https://github.com/eeshansrivastava89/soma-blog-hugo/blob/main/supabase-schema.sql) for complete schema.

## Deployment

### Streamlit Community Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select this repository
5. Set main file: `app.py`
6. Add secrets in "Advanced settings":
   ```toml
   [supabase]
   connection_string = "postgresql://..."
   ```
7. Click "Deploy"

Deployment takes ~2 minutes. Your app will be live at `https://YOUR-APP-NAME.streamlit.app`

## Embedded in Hugo

This dashboard is embedded in the SOMA blog A/B testing simulator:

🔗 [View Live Dashboard](https://soma-blog-hugo-shy-bird-7985.fly.dev/experiments/ab-test-simulator/)

## Data Privacy

This dashboard displays anonymized experiment data:
- No personally identifiable information (PII)
- Only aggregate statistics and completion metrics
- Session IDs are hashed by PostHog

## Contributing

This is a personal project for demonstrating modern data analytics workflows. Feel free to fork and adapt for your own use cases.

## License

MIT License - feel free to use and modify.

## Links

- [Main Blog](https://soma-blog-hugo-shy-bird-7985.fly.dev/)
- [PostHog Documentation](https://posthog.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
