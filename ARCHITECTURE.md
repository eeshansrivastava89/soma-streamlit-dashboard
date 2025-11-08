# 🏗️ SOMA Architecture Visual Guide

**Your entire codebase mapped out. Know exactly where to change things.**

---

## 📍 High-Level Overview: The Three Repos

```
┌─────────────────────────────────────────────────────────────────────┐
│                     YOUR THREE REPOSITORIES                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📚 soma-blog-hugo                     🚀 PRODUCTION (LIVE NOW)      │
│  ├─ Hugo static site                                                 │
│  ├─ A/B testing puzzle game                                          │
│  ├─ PostHog + Supabase + Streamlit                                  │
│  ├─ Domain: soma-blog-hugo-shy-bird-7985.fly.dev                   │
│  └─ Status: ✅ Running, all features working                         │
│                                                                      │
│  📊 soma-streamlit-dashboard           🚀 PRODUCTION (Supporting)   │
│  ├─ Streamlit dashboard app                                         │
│  ├─ Queries Supabase views                                          │
│  ├─ Shows: variant stats, funnel, completion times                  │
│  ├─ Embedded in Hugo as iframe                                      │
│  ├─ Domain: soma-app-dashboard-bfabkj7dkvffezprdsnm78.streamlit.app│
│  └─ Status: ✅ Running, auto-refresh every 10s                      │
│                                                                      │
│  🎯 soma-portfolio                     🔄 IN MIGRATION (95% DONE)   │
│  ├─ Astro resume/portfolio site                                     │
│  ├─ Same A/B simulator (from Hugo)                                  │
│  ├─ Same PostHog/Streamlit integration                              │
│  ├─ New: Timeline, Blog, Projects sections                          │
│  ├─ Domain: (will point to custom domain when deployed)             │
│  └─ Status: ⚠️ Built, not deployed yet                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🌐 Data Flow: How Everything Connects

```
USER PLAYS PUZZLE GAME
        │
        ▼
┌──────────────────────────────────────────┐
│   Browser (soma-portfolio or Hugo)       │
│   ├─ Loads /projects/ab-test-simulator   │
│   ├─ Renders puzzle HTML                 │
│   ├─ Runs ab-simulator.js (client-side)  │
│   └─ JavaScript tracks events            │
│        └─ posthog.capture('puzzle_*')    │
└──────┬───────────────────────────────────┘
       │
       ▼ HTTP (REAL-TIME)
┌──────────────────────────────────────────┐
│   PostHog Cloud                          │
│   ├─ Receives: puzzle_started            │
│   ├─ Receives: puzzle_completed          │
│   ├─ Receives: puzzle_failed             │
│   ├─ Assigns: Feature Flag (A or B)      │
│   └─ Sends: Webhook to Supabase          │
└──────┬───────────────────────────────────┘
       │
       ▼ WEBHOOK (<1 second latency)
┌──────────────────────────────────────────┐
│   Supabase Edge Function                 │
│   ├─ Receives webhook payload            │
│   ├─ Parses event data                   │
│   └─ Writes to PostgreSQL table          │
└──────┬───────────────────────────────────┘
       │
       ▼ DATABASE WRITE
┌──────────────────────────────────────────┐
│   Supabase PostgreSQL                    │
│   ├─ posthog_events table (raw data)     │
│   ├─ v_variant_stats (aggregated view)   │
│   ├─ v_conversion_funnel (view)          │
│   └─ v_stats_by_hour (view)              │
└──────┬───────────────────────────────────┘
       │
       ▼ SQL QUERIES (10-second refresh)
┌──────────────────────────────────────────┐
│   Streamlit Dashboard                    │
│   ├─ Queries Supabase views              │
│   ├─ Transforms with Pandas              │
│   ├─ Visualizes with Plotly              │
│   └─ Returns HTML/JSON to browser        │
└──────┬───────────────────────────────────┘
       │
       ▼ IFRAME EMBED
┌──────────────────────────────────────────┐
│   Portfolio / Blog Page                  │
│   ├─ Displays live dashboard             │
│   ├─ Updates every 10 seconds            │
│   └─ User sees real-time experiment data │
└──────────────────────────────────────────┘
```

---

## 📂 File Structure: Where Things Live

### 🟦 soma-portfolio (Astro) - NEW PORTFOLIO SITE

```
soma-portfolio/
│
├── 🟩 ROOT LEVEL (Config & Deploy)
│   ├── astro.config.mjs              ← Build config, integrations
│   ├── fly.toml                      ← Fly.io deployment config
│   ├── package.json                  ← Dependencies, scripts
│   ├── tsconfig.json                 ← TypeScript settings
│   ├── tailwind.config.js            ← Tailwind CSS config
│   ├── .env                          ← 🔐 PostHog credentials (DO NOT COMMIT)
│   └── HUGO_TO_ASTRO_MIGRATION.md    ← Migration tracking doc
│
├── 🟦 src/
│   │
│   ├── ✨ PAGES (Routes - what users see)
│   │   ├── index.astro               ← Homepage (hero, about, posts, timeline, projects)
│   │   ├── blog/
│   │   │   ├── [slug].astro          ← Individual blog post page
│   │   │   └── [...page].astro       ← Blog listing with pagination
│   │   └── projects/
│   │       └── ab-test-simulator.astro  ← 🎮 A/B SIMULATOR PAGE (KEY FILE)
│   │
│   ├── 🎨 COMPONENTS (Reusable UI pieces)
│   │   ├── BaseHead.astro            ← 🔐 PostHog initialization goes here
│   │   ├── Button.astro              ← Reusable button component
│   │   ├── Card.astro                ← Card layout component
│   │   ├── ProjectCard.astro         ← Project showcase card
│   │   ├── Label.astro               ← Label styling
│   │   ├── Timeline.tsx              ← ⏱️ ANIMATED TIMELINE (React component)
│   │   ├── Paginator.astro           ← Pagination component
│   │   ├── FormattedDate.astro       ← Date formatter
│   │   ├── SkillLayout.astro         ← Skills section layout
│   │   ├── Section.astro             ← Generic section wrapper
│   │   ├── ThemeProvider.astro       ← Dark/light theme toggle
│   │   ├── blog/
│   │   │   └── Post.astro            ← Blog post template
│   │   └── layout/
│   │       ├── Header.astro          ← Navigation bar
│   │       ├── Footer.astro          ← Footer
│   │       └── BaseLayout.astro      ← Main layout wrapper
│   │
│   ├── 📄 LAYOUTS (Page templates)
│   │   └── BaseLayout.astro          ← Wraps all pages (header, footer, etc)
│   │
│   ├── 📝 CONTENT (Blog posts & data)
│   │   ├── config.ts                 ← Content collection config
│   │   ├── post/
│   │   │   └── first-post.md         ← Example blog post (Markdown)
│   │   └── ...                       ← More blog posts here
│   │
│   ├── 📊 DATA (YAML/JSON data files)
│   │   └── timeline.yaml             ← 📍 YOUR WORK HISTORY (7 companies)
│   │
│   ├── 🎨 STYLES (Global CSS)
│   │   ├── app.css                   ← Global Tailwind styles
│   │   └── variables.css             ← CSS custom properties
│   │
│   ├── 🛠️ UTILS (Helper functions)
│   │   ├── date.ts                   ← Date formatting helpers
│   │   └── remarkReadingTime.ts      ← Reading time calculator
│   │
│   ├── 🎭 ICONS (SVG icons)
│   │   └── various.tsx               ← Icon components
│   │
│   ├── 🖼️ ASSETS (Images - Astro optimizes these)
│   │   ├── about-astro.png           ← Profile image
│   │   ├── coming-soon.png           ← Placeholder images
│   │   └── ...
│   │
│   ├── site.config.ts                ← Site metadata (title, author, description)
│   ├── types.ts                      ← TypeScript type definitions
│   └── env.d.ts                      ← Astro environment types
│
├── 🟫 public/ (Static files - NOT processed by Astro)
│   ├── 📁 logos/                     ← Company logos for timeline
│   │   ├── amazon.png
│   │   ├── overstock.png
│   │   └── ...
│   │
│   ├── 📁 css/
│   │   └── ab-simulator.css          ← 🎮 SIMULATOR STYLING (from Hugo)
│   │
│   ├── 📁 js/
│   │   └── ab-simulator.js           ← 🎮 SIMULATOR LOGIC (from Hugo)
│   │
│   ├── 📁 favicon/                   ← Favicon files
│   │   ├── apple-touch-icon.png
│   │   ├── favicon-32x32.png
│   │   └── site.webmanifest
│   │
│   ├── 📁 fonts/                     ← Web fonts (if any)
│   └── social-card.png               ← Social media preview image
│
└── .vercel/ (Generated on build - ignore)
```

---

### 🟫 soma-blog-hugo (Hugo) - PRODUCTION BLOG (LIVE NOW)

```
soma-blog-hugo/
│
├── 🟩 ROOT LEVEL (Config & Deploy)
│   ├── hugo.toml                     ← Hugo configuration
│   ├── fly.toml                      ← Fly.io deployment config
│   ├── Dockerfile                    ← Container build instructions
│   ├── .env                          ← 🔐 PostHog & Supabase keys
│   ├── MIGRATION_SUMMARY.md          ← PostHog/Supabase/Streamlit setup docs
│   ├── posthog-streamlit-migration-plan.md  ← Detailed integration guide
│   └── README.md                     ← Project overview
│
├── 📝 content/ (Your blog posts)
│   ├── posts/                        ← Blog articles (Markdown)
│   │   ├── post-1.md
│   │   └── post-2.md
│   ├── about/                        ← About page
│   │   └── _index.md
│   └── search.md                     ← Search page
│
├── 🎨 layouts/ (Hugo templates)
│   ├── _default/
│   │   ├── baseof.html               ← 🔐 PostHog script init (CRITICAL)
│   │   ├── single.html               ← Blog post template
│   │   └── list.html                 ← List template
│   ├── about/
│   │   └── single.html               ← About page template
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── sidebar.html
│   └── shortcodes/
│       ├── ab-simulator-puzzle.html   ← 🎮 PUZZLE HTML
│       ├── ab-simulator-dashboard.html ← 📊 DASHBOARD EMBED
│       └── ab-simulator-code.html     ← Code display
│
├── 🟫 static/ (Non-processed assets)
│   ├── css/
│   │   ├── custom.css                ← Site-wide styling
│   │   └── ab-simulator.css          ← 🎮 SIMULATOR STYLING
│   ├── js/
│   │   └── ab-simulator.js           ← 🎮 SIMULATOR LOGIC
│   └── images/
│       └── ...
│
├── 📊 data/
│   └── timeline.yaml                 ← Work history (same as Astro copy)
│
├── 📦 themes/
│   └── rusty-typewriter/             ← Hugo theme (not modified)
│
└── public/ (Generated build output - ignore)
```

---

### 🟪 soma-streamlit-dashboard (Python) - ANALYTICS DASHBOARD

```
soma-streamlit-dashboard/
│
├── 🟩 ROOT LEVEL
│   ├── app.py                        ← 🎯 MAIN APP FILE (all logic here)
│   ├── requirements.txt               ← Python dependencies
│   ├── README.md                     ← Setup & deployment guide
│   └── .gitignore
│
├── .streamlit/
│   └── secrets.toml                  ← 🔐 Supabase credentials (NOT in git)
│
└── .github/
    └── workflows/
        └── deploy.yml                ← Auto-deploy on push
```

---

## 🎯 What Changes Where? (Quick Reference)

### "I want to change the **BLOG CONTENT**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Add new blog post | **Both repos** | Markdown | Create `.md` file in `soma-portfolio/src/content/post/` AND `soma-blog-hugo/content/posts/` |
| Change blog post title | **Both repos** | Markdown frontmatter | Edit `title:` field in `.md` |
| Change blog CSS styling | **Astro only** | CSS | Edit `src/styles/app.css` in soma-portfolio |
| Change post layout | **Astro only** | Astro | Modify `src/components/blog/Post.astro` |

**💡 NOTE:** During migration, edit soma-portfolio first. After cutover, delete soma-blog-hugo.

---

### "I want to change the **HOMEPAGE**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Change hero text/image | **Astro** | Astro | Edit `src/pages/index.astro` (hero section) |
| Change about section | **Astro** | Astro | Edit `src/pages/index.astro` (about section) |
| Change projects shown | **Astro** | Astro | Edit `src/pages/index.astro` (projects section) |
| Change timeline companies | **Astro** | YAML | Edit `src/data/timeline.yaml` |
| Change timeline logo | **Astro** | PNG files | Replace files in `public/logos/` |
| Change colors/fonts | **Astro** | Config | Edit `tailwind.config.js` or `src/styles/app.css` |

**📍 CRITICAL FILE:** `src/pages/index.astro` (all homepage sections in one file)

---

### "I want to change the **A/B SIMULATOR**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Change puzzle words | **Both** | JavaScript | Edit `ab-simulator.js` (PUZZLE_CONFIG object) |
| Change timer length | **Both** | JavaScript | Edit `ab-simulator.js` (change 60000 to new milliseconds) |
| Change CSS styling | **Both** | CSS | Edit `ab-simulator.css` |
| Change puzzle HTML | **Astro** | Astro | Edit `src/pages/projects/ab-test-simulator.astro` |
| Track new event type | **Both** | JavaScript | Add `posthog.capture()` call in `ab-simulator.js` |
| Change variant A/B logic | **Both** | JavaScript | Edit feature flag logic in `ab-simulator.js` |

**📍 CRITICAL FILES:**
- `public/js/ab-simulator.js` - Game logic & PostHog tracking
- `public/css/ab-simulator.css` - Styling
- `src/pages/projects/ab-test-simulator.astro` - HTML container (Astro only)

---

### "I want to change **POSTHOG INTEGRATION**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Add new event tracking | **Astro** | JavaScript | Add `posthog.capture()` in `ab-simulator.js` |
| Change PostHog API key | **Astro** | .env file | Update `PUBLIC_POSTHOG_KEY` in `.env` |
| Change experiment flag name | **Astro** | JavaScript | Edit feature flag key in `ab-simulator.js` |
| Initialize PostHog | **Astro** | Astro | Edit `src/components/BaseHead.astro` |
| Add PostHog UI customization | **Astro** | Astro/JS | Modify `BaseHead.astro` script config |

**🔐 CREDENTIALS:**
- Location: `soma-portfolio/.env`
- Keys used: `PUBLIC_POSTHOG_KEY`, `PUBLIC_POSTHOG_HOST`
- Same keys as Hugo (so they share analytics)

---

### "I want to change the **ANALYTICS DASHBOARD**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Add new chart | **Streamlit** | Python | Edit `app.py`, add `st.plotly_chart()` or `st.write()` |
| Change Supabase query | **Streamlit** | SQL/Python | Edit query string in `app.py` |
| Change refresh interval | **Streamlit** | Python | Edit `@st.cache_data(ttl=X)` decorator in `app.py` |
| Change colors/theme | **Streamlit** | Config | Edit `.streamlit/config.toml` |
| Deploy dashboard | **Streamlit** | Git | Push to GitHub, Streamlit auto-deploys |

**📍 CRITICAL FILE:** `soma-streamlit-dashboard/app.py` (all logic in one file)

**🔐 CREDENTIALS:**
- Location: `soma-streamlit-dashboard/.streamlit/secrets.toml` (NOT in git)
- Needed: Supabase connection string

---

### "I want to change the **DATABASE SCHEMA**"

| What | Where | File Type | How |
|------|-------|-----------|-----|
| Add new table | **Supabase** | SQL | Run in Supabase SQL Editor, use `supabase-schema.sql` as reference |
| Add new view | **Supabase** | SQL | Create view, query in `soma-streamlit-dashboard/app.py` |
| Add new column | **Supabase** | SQL | Alter table, update views if needed |
| See current schema | **Reference** | SQL | Check `soma-blog-hugo/supabase-schema.sql` |

**📍 NOTE:** Schema changes affect both Hugo analytics AND Astro analytics (same database)

---

## 🔐 Secrets & Credentials Management

```
┌─────────────────────────────────────────────────────┐
│              WHERE CREDENTIALS LIVE                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  PostHog API Key                                   │
│  ├─ Astro:     soma-portfolio/.env                │
│  │             PUBLIC_POSTHOG_KEY=phc_...         │
│  ├─ Hugo:      layouts/_default/baseof.html       │
│  │             (hardcoded in script)              │
│  └─ Status:    BOTH USE SAME KEY                  │
│                                                     │
│  Supabase Connection                               │
│  ├─ Hugo:      .env (URL pooler format)           │
│  ├─ Streamlit: .streamlit/secrets.toml            │
│  └─ Status:    Same database, different protocols │
│                                                     │
│  ⚠️  NEVER commit .env or secrets.toml            │
│  ⚠️  Use .gitignore to exclude sensitive files    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

```
┌───────────────────────────────────────────────────────────┐
│              DEPLOYMENT TARGETS                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  soma-portfolio (Astro) → Fly.io                         │
│  ├─ Command: npm run build                              │
│  ├─ Output: .vercel/output/ (Vercel adapter)            │
│  ├─ Deploy: fly deploy                                  │
│  ├─ Status: Ready (Phase 7)                             │
│  └─ URL: (will be soma-blog-hugo or custom domain)      │
│                                                           │
│  soma-blog-hugo (Hugo) → Fly.io                          │
│  ├─ Command: hugo (builds to public/)                   │
│  ├─ Docker: Alpine + nginx                              │
│  ├─ Deploy: fly deploy                                  │
│  ├─ Status: Currently live                              │
│  └─ URL: soma-blog-hugo-shy-bird-7985.fly.dev          │
│                                                           │
│  soma-streamlit-dashboard → Streamlit Community Cloud   │
│  ├─ Command: streamlit run app.py                       │
│  ├─ Deploy: git push origin main (auto)                │
│  ├─ Status: Currently live                              │
│  └─ URL: soma-app-dashboard-*.streamlit.app             │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 Data Ownership: Who Uses What

```
┌─────────────────────────────────────────┐
│          soma-portfolio (Astro)         │
├─────────────────────────────────────────┤
│ Reads:                                  │
│  ✓ Blog posts from src/content/post/   │
│  ✓ Timeline from src/data/timeline.yaml│
│  ✓ Logos from public/logos/            │
│  ✓ PostHog feature flags               │
│  ✓ Streamlit dashboard (iframe)        │
│                                         │
│ Writes:                                 │
│  ✓ Events to PostHog                   │
│  ✓ Leaderboard to localStorage         │
│  ✗ NOT Supabase (only Hugo does)       │
│                                         │
│ Config:                                 │
│  ✓ .env (PostHog credentials)          │
│  ✓ astro.config.mjs                    │
│  ✓ tailwind.config.js                  │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│        soma-blog-hugo (Hugo)            │
├─────────────────────────────────────────┤
│ Reads:                                  │
│  ✓ Blog posts from content/posts/      │
│  ✓ Timeline from data/timeline.yaml    │
│  ✓ Logos from static/images/           │
│  ✓ PostHog feature flags               │
│  ✓ Streamlit dashboard (iframe)        │
│                                         │
│ Writes:                                 │
│  ✓ Events to PostHog                   │
│  ✓ Leaderboard to localStorage         │
│  ✓ Events to Supabase (webhook)        │
│                                         │
│ Config:                                 │
│  ✓ .env (all keys)                     │
│  ✓ hugo.toml                           │
│  ✓ fly.toml                            │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     soma-streamlit-dashboard (Python)   │
├─────────────────────────────────────────┤
│ Reads:                                  │
│  ✓ Events from Supabase                │
│  ✓ Views from Supabase                 │
│                                         │
│ Writes:                                 │
│  ✓ HTML/JSON to browser                │
│  ✗ Does NOT write to Supabase          │
│                                         │
│ Config:                                 │
│  ✓ .streamlit/secrets.toml (creds)     │
│  ✓ requirements.txt (deps)             │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│        Supabase (PostgreSQL)            │
├─────────────────────────────────────────┤
│ Receives:                               │
│  ✓ PostHog webhook (puzzle events)     │
│  ✓ PostHog batch export (backup)       │
│                                         │
│ Stores:                                 │
│  ✓ posthog_events table                │
│  ✓ Multiple views (aggregations)       │
│                                         │
│ Serves:                                 │
│  ✓ Queries to Streamlit                │
│  ✓ Queries to Hugo (if needed)         │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎯 Decision Tree: "Where Do I Make This Change?"

```
START: I want to change something
│
├─ Is it BLOG CONTENT (posts, articles)?
│  ├─ YES → Edit src/content/post/*.md in soma-portfolio
│  └─ (Also update soma-blog-hugo temporarily if live)
│
├─ Is it HOMEPAGE (hero, about, timeline)?
│  ├─ YES → Edit src/pages/index.astro in soma-portfolio
│  └─ (Or data/timeline.yaml if changing companies)
│
├─ Is it SIMULATOR LOGIC (puzzle words, timer)?
│  ├─ YES → Edit public/js/ab-simulator.js in soma-portfolio
│  └─ (Also in soma-blog-hugo while both are live)
│
├─ Is it SIMULATOR STYLING (colors, fonts)?
│  ├─ YES → Edit public/css/ab-simulator.css in soma-portfolio
│  └─ (Also in soma-blog-hugo while both are live)
│
├─ Is it SIMULATOR HTML STRUCTURE?
│  ├─ YES → Edit src/pages/projects/ab-test-simulator.astro
│  └─ (Astro only, no Hugo equivalent)
│
├─ Is it ANALYTICS DASHBOARD VISUALIZATION?
│  ├─ YES → Edit soma-streamlit-dashboard/app.py
│  └─ Deploy via git push
│
├─ Is it POSTHOG EVENT TRACKING?
│  ├─ YES → Edit public/js/ab-simulator.js (posthog.capture calls)
│  └─ (Also depends on where game runs)
│
├─ Is it SITE THEME/COLORS/FONTS?
│  ├─ YES → Edit tailwind.config.js or src/styles/app.css
│  └─ (Astro only)
│
├─ Is it NAVIGATION/HEADER?
│  ├─ YES → Edit src/components/layout/Header.astro
│  └─ (Astro only)
│
├─ Is it DATABASE SCHEMA?
│  ├─ YES → Run SQL in Supabase dashboard
│  └─ Reference: soma-blog-hugo/supabase-schema.sql
│
└─ Is it DEPLOYMENT CONFIG?
   ├─ YES → Edit fly.toml or astro.config.mjs
   └─ (Site-wide infrastructure changes)
```

---

## 📋 Quick Checklists

### When Adding a New Blog Post

```
☐ Write post in Markdown
☐ Add frontmatter (title, date, tags, description)
☐ Save to src/content/post/[slug].md
☐ Test locally: npm run dev → check blog page
☐ Build test: npm run build → should succeed
☐ Git add, commit, push
☐ Deploy to Fly.io
```

### When Changing Simulator Logic

```
☐ Edit public/js/ab-simulator.js
☐ Test locally: npm run dev → load simulator
☐ Play game → verify logic works
☐ Open browser console → check for errors
☐ npm run build → should succeed
☐ Git add, commit, push
☐ Deploy to Fly.io
☐ Verify PostHog receives events
☐ Verify Supabase stores events
☐ Verify Streamlit shows updated data
```

### When Deploying to Production

```
☐ Run npm run build locally
☐ Verify no TypeScript errors
☐ Test npm run preview locally
☐ Test all major features:
  ☐ Homepage loads
  ☐ Blog posts render
  ☐ Timeline shows
  ☐ Simulator is playable
  ☐ Events track to PostHog
  ☐ Streamlit dashboard embedded
☐ Git add, commit, push
☐ Deploy: fly deploy
☐ Test live site
☐ Verify all features work on deployed version
☐ Monitor PostHog for events
```

---

## 🎓 Key Takeaways

| Concept | What It Means | Where It Matters |
|---------|---------------|-----------------|
| **Content Layer** | Blog posts, project descriptions | `src/content/post/` in Astro |
| **Styling Layer** | CSS, colors, fonts, layout | `tailwind.config.js`, `src/styles/`, `public/css/` |
| **Logic Layer** | JavaScript game code, tracking | `public/js/ab-simulator.js` |
| **Infrastructure** | Deployment, environment, config | `fly.toml`, `.env`, `astro.config.mjs` |
| **Analytics Layer** | Event tracking, dashboards, data | PostHog → Supabase → Streamlit |
| **Database Layer** | Tables, views, schema | Supabase PostgreSQL |

---

## ✨ Tips for Success

1. **Always test locally first** - `npm run dev` before pushing
2. **Build passes locally?** - Then it'll pass on Fly.io
3. **Changing JS?** - Test simulator gameplay immediately
4. **Changing styles?** - Check mobile AND desktop
5. **Adding tracking?** - Check PostHog dashboard 30 seconds later
6. **Not seeing new data?** - Clear browser cache and localStorage
7. **Domain issues?** - Check Fly.io DNS settings and SSL certificates

---

**This guide is your map. Bookmark it.** 🗺️

