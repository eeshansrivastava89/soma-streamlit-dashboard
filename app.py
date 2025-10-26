import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from sqlalchemy import create_engine
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="A/B Test Dashboard - Word Search",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_db_connection():
    """Create database connection from Streamlit secrets"""
    connection_string = st.secrets["supabase"]["connection_string"]
    engine = create_engine(connection_string)
    return engine

# Load data functions
@st.cache_data(ttl=10)  # Cache for 10 seconds (auto-refresh)
def load_variant_stats():
    """Load aggregated variant statistics from v_variant_stats view"""
    engine = get_db_connection()
    query = "SELECT * FROM v_variant_stats ORDER BY variant"
    df = pd.read_sql(query, engine)
    return df

@st.cache_data(ttl=10)
def load_conversion_funnel():
    """Load conversion funnel from v_conversion_funnel view"""
    engine = get_db_connection()
    query = "SELECT * FROM v_conversion_funnel ORDER BY variant"
    df = pd.read_sql(query, engine)
    return df

@st.cache_data(ttl=10)
def load_recent_completions():
    """Load recent puzzle completions"""
    engine = get_db_connection()
    query = """
        SELECT
            variant,
            completion_time_seconds,
            correct_words_count,
            total_guesses_count,
            timestamp,
            user_id
        FROM posthog_events
        WHERE event = 'puzzle_completed'
          AND completion_time_seconds IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT 100
    """
    df = pd.read_sql(query, engine)
    return df

# Header
st.title("📊 A/B Test Dashboard: Word Search Difficulty")
st.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Load data
try:
    variant_stats = load_variant_stats()
    funnel_data = load_conversion_funnel()
    completions = load_recent_completions()

    # Check if we have data
    if variant_stats.empty:
        st.warning("⏳ No data yet. Play the puzzle game to generate data!")
        st.stop()

    # Summary Stats - Three Columns
    st.header("📈 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    # Control variant (3 words)
    with col1:
        st.subheader("🅰️ Control (3 words)")
        control_stats = variant_stats[variant_stats['variant'] == 'A']

        if not control_stats.empty:
            stats = control_stats.iloc[0]
            st.metric("Total Completions", int(stats['total_completions']))
            st.metric("Unique Users", int(stats['unique_users']))
            st.metric("Avg Completion Time", f"{stats['avg_completion_time']:.2f}s")
            st.metric("Median Time", f"{stats['median_completion_time']:.2f}s")
        else:
            st.info("No data for control variant yet")

    # 4-words variant
    with col2:
        st.subheader("🅱️ Variant (4 words)")
        variant_stats_4words = variant_stats[variant_stats['variant'] == 'B']

        if not variant_stats_4words.empty:
            stats = variant_stats_4words.iloc[0]
            st.metric("Total Completions", int(stats['total_completions']))
            st.metric("Unique Users", int(stats['unique_users']))
            st.metric("Avg Completion Time", f"{stats['avg_completion_time']:.2f}s")
            st.metric("Median Time", f"{stats['median_completion_time']:.2f}s")
        else:
            st.info("No data for 4-words variant yet")

    # Comparison
    with col3:
        st.subheader("⚖️ Comparison")

        if len(variant_stats) >= 2:
            control = variant_stats[variant_stats['variant'] == 'A'].iloc[0]
            variant_b = variant_stats[variant_stats['variant'] == 'B'].iloc[0]

            time_diff = variant_b['avg_completion_time'] - control['avg_completion_time']
            pct_diff = (time_diff / control['avg_completion_time']) * 100

            st.metric(
                "Time Difference",
                f"{time_diff:+.2f}s",
                delta=f"{pct_diff:+.1f}%",
                delta_color="inverse"  # Lower is better
            )

            # Interpretation
            if abs(pct_diff) > 20:
                if pct_diff > 0:
                    st.error("🔴 4-words variant is significantly harder")
                else:
                    st.success("🟢 4-words variant is surprisingly easier")
            elif abs(pct_diff) > 10:
                st.warning("🟡 Moderate difficulty difference")
            else:
                st.info("⚪ Similar difficulty")
        else:
            st.info("Need data from both variants for comparison")

    st.markdown("---")

    # Visualizations
    st.header("📊 Interactive Visualizations")

    # Two columns for charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("⏱️ Completion Time Distribution")

        if not completions.empty:
            # Create KDE (Kernel Density Estimation) curves using Altair
            # Filter out any null values
            completions_clean = completions.dropna(subset=['completion_time_seconds'])
            
            if not completions_clean.empty:
                # Create smooth density curves for each variant
                kde_chart = alt.Chart(completions_clean).transform_density(
                    'completion_time_seconds',
                    as_=['completion_time_seconds', 'density'],
                    groupby=['variant'],
                    bandwidth=0.5  # Adjust smoothness (lower = more detailed, higher = smoother)
                ).mark_line(
                    size=3,
                    opacity=0.8
                ).encode(
                    x=alt.X('completion_time_seconds:Q', title='Completion Time (seconds)'),
                    y=alt.Y('density:Q', title='Probability Density'),
                    color=alt.Color(
                        'variant:N',
                        scale=alt.Scale(
                            domain=['A', 'B'],
                            range=['#636EFA', '#EF553B']
                        ),
                        legend=alt.Legend(title='Variant')
                    ),
                    tooltip=[
                        alt.Tooltip('completion_time_seconds:Q', format='.2f', title='Time (s)'),
                        alt.Tooltip('density:Q', format='.4f', title='Density'),
                        alt.Tooltip('variant:N', title='Variant')
                    ]
                ).properties(
                    height=400,
                    width=600
                ).interactive()
                
                st.altair_chart(kde_chart, use_container_width=True)
                
                st.caption("💡 **Hover over the curves** to see exact time and probability values. Smooth curves show how likely each completion time is for each variant.")
            else:
                st.info("No valid completion time data yet")
        else:
            st.info("No completion data yet")

    with chart_col2:
        st.subheader("🎯 Conversion Funnel")

        if not funnel_data.empty:
            # Create funnel chart
            fig_funnel = go.Figure()

            for idx, row in funnel_data.iterrows():
                variant_name = row['variant']
                display_name = "Control (3 words)" if variant_name == "A" else "Variant (4 words)"
                color = "#636EFA" if variant_name == "A" else "#EF553B"

                fig_funnel.add_trace(go.Funnel(
                    name=display_name,
                    y=["Started", "Completed"],
                    x=[row['started_users'], row['completed_users']],
                    textinfo="value+percent initial",
                    marker={"color": color},
                    connector={"line": {"color": color}}
                ))

            fig_funnel.update_layout(
                height=400,
                showlegend=True,
                hovermode="y"
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.info("No funnel data yet")

    # Time series
    st.subheader("📅 Completion Times Over Time")

    if not completions.empty and len(completions) > 5:
        fig_time = px.scatter(
            completions,
            x="timestamp",
            y="completion_time_seconds",
            color="variant",
            labels={
                "timestamp": "Time",
                "completion_time_seconds": "Completion Time (seconds)",
                "variant": "Variant"
            },
            color_discrete_map={
                "A": "#636EFA",
                "B": "#EF553B"
            }
        )
        fig_time.update_layout(
            height=400,
            hovermode="x unified"
        )
        st.plotly_chart(fig_time, use_container_width=True)

        st.caption("💡 Are users getting faster over time? Watch for patterns in completion times.")
    else:
        st.info("Need more data points for time series analysis")

    # Raw data table
    with st.expander("📋 View Recent Completions"):
        st.dataframe(
            completions[[
                'timestamp', 'variant', 'completion_time_seconds',
                'correct_words_count', 'total_guesses_count'
            ]].head(50),
            use_container_width=True,
            hide_index=True
        )

    # Statistical summary
    with st.expander("📐 Statistical Details"):
        st.subheader("Variant Statistics")

        display_stats = variant_stats[[
            'variant', 'total_completions', 'unique_users',
            'avg_completion_time', 'median_completion_time',
            'min_completion_time', 'max_completion_time',
            'p25_completion_time', 'p75_completion_time',
            'p90_completion_time', 'p95_completion_time'
        ]].copy()

        # Rename columns for display
        display_stats.columns = [
            'Variant', 'Completions', 'Users',
            'Avg (s)', 'Median (s)', 'Min (s)', 'Max (s)',
            'P25 (s)', 'P75 (s)', 'P90 (s)', 'P95 (s)'
        ]

        st.dataframe(display_stats, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("💡 Make sure Supabase connection is configured in Streamlit secrets")

    # Show debug info
    with st.expander("🔍 Debug Information"):
        st.code(str(e))
        st.write("**Connection string format:**")
        st.code('postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres')

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        📊 Data cached for 10 seconds | Powered by PostHog + Supabase + Streamlit
    </div>
""", unsafe_allow_html=True)

# Auto-refresh note
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.8rem; margin-top: 1rem;'>
        Dashboard refreshes when you interact with it (scroll, click, etc.)
    </div>
""", unsafe_allow_html=True)

# Optional: Add a manual refresh button
if st.button("🔄 Refresh Data", type="secondary"):
    st.cache_data.clear()
    st.rerun()
