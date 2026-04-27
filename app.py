"""
Sri Lanka Sustainability Data Dashboard
World Bank – World Development Indicators
"""

import os
import subprocess
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sri Lanka Sustainability Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 50%, #0d1b2a 100%);
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background: rgba(15, 20, 35, 0.9);
    border-right: 1px solid rgba(99, 179, 237, 0.15);
    backdrop-filter: blur(12px);
}

.kpi-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(99, 179, 237, 0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    backdrop-filter: blur(10px);
}

.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #63b3ed, #76e4f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.kpi-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

.kpi-delta {
    font-size: 0.85rem;
    margin-top: 0.4rem;
}

.kpi-delta.up { color: #68d391; }
.kpi-delta.down { color: #fc8181; }

.section-header {
    font-size: 1.05rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-left: 3px solid #63b3ed;
    padding-left: 0.8rem;
    margin-bottom: 1rem;
}

.hero-banner {
    background: linear-gradient(135deg,
        rgba(99,179,237,0.15) 0%,
        rgba(118,228,247,0.08) 50%,
        rgba(159,122,234,0.12) 100%);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff, #63b3ed, #76e4f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.5rem;
}

.insight-box {
    background: rgba(99,179,237,0.07);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-top: 0.8rem;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.75);
    line-height: 1.6;
}

.insight-box strong {
    color: #63b3ed;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Plotly layout
# ─────────────────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
    font=dict(family="Inter", color="rgba(255,255,255,0.85)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True, zeroline=False),
    margin=dict(t=40, b=40, l=10, r=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
    ),
)

COLORS = [
    "#63b3ed", "#76e4f7", "#9f7aea", "#68d391",
    "#f6ad55", "#fc8181", "#b794f4", "#4fd1c5",
]

# ─────────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LKA_CSV = os.path.join(BASE_DIR, "cleaned_lka.csv")
ALL_CSV = os.path.join(BASE_DIR, "cleaned_all.csv")


def ensure_cleaned():
    """Run data_prep.py if cleaned CSV files do not exist."""
    if not os.path.exists(LKA_CSV) or not os.path.exists(ALL_CSV):
        subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "data_prep.py")],
            check=True
        )


@st.cache_data(show_spinner=False)
def load_lka() -> pd.DataFrame:
    ensure_cleaned()
    return pd.read_csv(LKA_CSV)


@st.cache_data(show_spinner=False)
def load_all() -> pd.DataFrame:
    ensure_cleaned()
    return pd.read_csv(ALL_CSV)


with st.spinner("Loading data..."):
    lka_df = load_lka()
    all_df = load_all()

indicators = sorted(lka_df["Indicator Name"].dropna().unique())
all_countries = sorted(all_df["Country Name"].dropna().unique())

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 0.5rem 0 1.5rem;'>
            <div style='font-size:2rem;'>🌿</div>
            <div style='font-size:1rem; font-weight:700; color:#63b3ed; letter-spacing:0.04em;'>
                LKA Dashboard
            </div>
            <div style='font-size:0.72rem; color:rgba(255,255,255,0.4); margin-top:0.25rem;'>
                World Bank · Development Indicators
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🗂 Navigation")
    page = st.radio(
        "Go to",
        [
            "🏠 Overview",
            "📈 Trend Analysis",
            "🔬 Bivariate Analysis",
            "🌍 Global Comparison",
            "📊 Statistical Summary",
            "📋 Raw Data",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Filters")

    selected_indicators = st.multiselect(
        "Indicators",
        indicators,
        default=indicators[:1] if indicators else [],
        help="Choose one or more indicators to analyse",
    )

    all_years = sorted(lka_df["Year"].dropna().unique())
    year_min, year_max = int(min(all_years)), int(max(all_years))

    year_range = st.slider(
        "Year range",
        year_min,
        year_max,
        (year_min, year_max),
    )

    st.markdown("---")
    st.markdown("### 🌍 Comparison Countries")

    compare_countries = st.multiselect(
        "Compare with",
        [c for c in all_countries if c != "Sri Lanka"],
        default=["India", "Bangladesh", "Thailand"]
        if all(c in all_countries for c in ["India", "Bangladesh", "Thailand"])
        else [],
        max_selections=5,
    )

    st.markdown("---")
    st.caption("Data: World Bank WDI · Last Updated 2026-04-08")


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def get_filtered(indicator: str | None = None) -> pd.DataFrame:
    mask = (lka_df["Year"] >= year_range[0]) & (lka_df["Year"] <= year_range[1])

    if indicator:
        mask &= lka_df["Indicator Name"] == indicator
    elif selected_indicators:
        mask &= lka_df["Indicator Name"].isin(selected_indicators)

    return lka_df[mask].copy()


def fmt(val, decimals=2, suffix=""):
    if pd.isna(val):
        return "N/A"
    return f"{val:,.{decimals}f}{suffix}"


# ─────────────────────────────────────────────────────────────────────────────
# Overview
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.markdown(
        """
        <div class='hero-banner'>
            <div class='hero-title'>🌿 Sri Lanka Sustainability Dashboard</div>
            <div class='hero-sub'>
                Interactive exploration of World Bank Development Indicators · Data spans 1960 – 2025
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not selected_indicators:
        st.info("Select at least one indicator from the sidebar.")
    else:
        ind = selected_indicators[0]
        df_ind = get_filtered(ind)

        if df_ind.empty:
            st.info("No data available for the selected filters.")
        else:
            latest_year = df_ind["Year"].max()
            earliest_year = df_ind["Year"].min()

            latest_val = df_ind.loc[df_ind["Year"] == latest_year, "Value"].values[0]
            earliest_val = df_ind.loc[df_ind["Year"] == earliest_year, "Value"].values[0]

            pct_change = (
                ((latest_val - earliest_val) / abs(earliest_val)) * 100
                if earliest_val != 0
                else 0
            )

            avg_val = df_ind["Value"].mean()
            peak_year = df_ind.loc[df_ind["Value"].idxmax(), "Year"]
            peak_val = df_ind["Value"].max()

            col1, col2, col3, col4 = st.columns(4)

            cards = [
                (
                    col1,
                    fmt(latest_val),
                    f"Latest ({latest_year})",
                    f"{'▲' if pct_change >= 0 else '▼'} {abs(pct_change):.1f}% vs {earliest_year}",
                    "up" if pct_change >= 0 else "down",
                ),
                (
                    col2,
                    fmt(avg_val),
                    "Period Average",
                    f"Years {year_range[0]}–{year_range[1]}",
                    "",
                ),
                (
                    col3,
                    fmt(peak_val),
                    "Peak Value",
                    f"Recorded in {peak_year}",
                    "up",
                ),
                (
                    col4,
                    str(len(df_ind)),
                    "Data Points",
                    f"Across {year_range[1] - year_range[0] + 1} years",
                    "",
                ),
            ]

            for col, val, label, delta, cls in cards:
                with col:
                    delta_html = f"<div class='kpi-delta {cls}'>{delta}</div>" if delta else ""
                    st.markdown(
                        f"""
                        <div class='kpi-card'>
                            <div class='kpi-value'>{val}</div>
                            <div class='kpi-label'>{label}</div>
                            {delta_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>📈 Quick Trend</div>", unsafe_allow_html=True)

            fig = px.area(
                df_ind,
                x="Year",
                y="Value",
                title=f"{ind} — Sri Lanka ({year_range[0]}–{year_range[1]})",
                color_discrete_sequence=[COLORS[0]],
            )

            fig.update_traces(
                line=dict(width=2.5),
                fillcolor="rgba(99,179,237,0.12)",
                hovertemplate="<b>%{x}</b><br>%{y:.2f}<extra></extra>",
            )

            fig.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

            trend_word = "upward" if pct_change > 0 else "downward"

            st.markdown(
                f"""
                <div class='insight-box'>
                    📌 <strong>Key Insight:</strong> The selected indicator shows an overall
                    <strong>{trend_word} trend</strong> of <strong>{abs(pct_change):.1f}%</strong>
                    between {earliest_year} and {latest_year}. The peak value was
                    <strong>{fmt(peak_val)}</strong> in <strong>{peak_year}</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📂 Dataset Overview</div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Total Indicators", len(indicators))

    with col_b:
        st.metric("Year Range", f"{year_min} – {year_max}")

    with col_c:
        st.metric("Total Sri Lanka Records", len(lka_df))

    st.markdown(
        f"""
        <div class='insight-box'>
            🗂️ <strong>About this Dataset</strong><br>
            Source: <strong>World Bank – World Development Indicators</strong>.
            The dataset covers Sri Lanka across <strong>{len(indicators)}</strong>
            indicators from <strong>{year_min}</strong> to <strong>{year_max}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Trend Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📈 Trend Analysis":
    st.markdown(
        "<div class='section-header'>📈 Trend Analysis — Sri Lanka</div>",
        unsafe_allow_html=True,
    )

    if not selected_indicators:
        st.warning("Please select at least one indicator from the sidebar.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(
        ["📉 Line / Area", "📊 Bar Chart", "🔢 Year-over-Year Change"]
    )

    with tab1:
        df_multi = get_filtered()

        if df_multi.empty:
            st.info("No data for the selected filters.")
        else:
            viz_type = st.radio(
                "Chart Type",
                ["Line", "Area"],
                horizontal=True,
                key="line_area",
            )

            fig = go.Figure()

            for i, ind in enumerate(selected_indicators):
                sub = df_multi[df_multi["Indicator Name"] == ind]

                if sub.empty:
                    continue

                color = COLORS[i % len(COLORS)]

                if viz_type == "Area":
                    fig.add_trace(
                        go.Scatter(
                            x=sub["Year"],
                            y=sub["Value"],
                            name=ind,
                            fill="tozeroy",
                            mode="lines",
                            line=dict(color=color, width=2),
                        )
                    )
                else:
                    fig.add_trace(
                        go.Scatter(
                            x=sub["Year"],
                            y=sub["Value"],
                            name=ind,
                            mode="lines+markers",
                            line=dict(color=color, width=2.5),
                            marker=dict(size=5),
                        )
                    )

            fig.update_layout(
                **PLOT_LAYOUT,
                title="Indicator Trends Over Time",
                xaxis_title="Year",
                yaxis_title="Value",
                hovermode="x unified",
            )

            st.plotly_chart(fig, use_container_width=True)

            if len(selected_indicators) == 1:
                show_ma = st.checkbox("Show 5-year moving average", value=True)

                if show_ma:
                    ind = selected_indicators[0]
                    sub = df_multi[df_multi["Indicator Name"] == ind].sort_values("Year")
                    sub["MA5"] = sub["Value"].rolling(5, min_periods=3).mean()

                    fig2 = go.Figure()

                    fig2.add_trace(
                        go.Scatter(
                            x=sub["Year"],
                            y=sub["Value"],
                            name="Actual",
                            mode="lines+markers",
                            line=dict(color=COLORS[0], width=2),
                            marker=dict(size=4),
                        )
                    )

                    fig2.add_trace(
                        go.Scatter(
                            x=sub["Year"],
                            y=sub["MA5"],
                            name="5-Year Moving Average",
                            mode="lines",
                            line=dict(color=COLORS[1], width=2.5, dash="dash"),
                        )
                    )

                    fig2.update_layout(
                        **PLOT_LAYOUT,
                        title=f"{ind} with 5-Year Moving Average",
                        xaxis_title="Year",
                        yaxis_title="Value",
                    )

                    st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        df_multi = get_filtered()
        ind_sel = st.selectbox("Select Indicator", selected_indicators, key="bar_ind")

        sub = df_multi[df_multi["Indicator Name"] == ind_sel]

        if sub.empty:
            st.info("No data.")
        else:
            fig = px.bar(
                sub,
                x="Year",
                y="Value",
                color="Value",
                color_continuous_scale=[
                    [0, "#1a365d"],
                    [0.5, "#63b3ed"],
                    [1, "#76e4f7"],
                ],
                title=f"{ind_sel} — Annual Values",
            )

            fig.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        df_multi = get_filtered()
        ind_sel = st.selectbox("Select Indicator", selected_indicators, key="yoy_ind")

        sub = df_multi[df_multi["Indicator Name"] == ind_sel].sort_values("Year").copy()

        if len(sub) < 2:
            st.info("Not enough data points for YoY change.")
        else:
            sub["YoY Change"] = sub["Value"].diff()
            sub["YoY % Change"] = sub["Value"].pct_change() * 100
            sub = sub.dropna(subset=["YoY Change"])

            col_left, col_right = st.columns(2)

            with col_left:
                fig = px.bar(
                    sub,
                    x="Year",
                    y="YoY Change",
                    color="YoY Change",
                    color_continuous_scale=[
                        [0, "#fc8181"],
                        [0.5, "#f6ad55"],
                        [1, "#68d391"],
                    ],
                    title="Year-over-Year Absolute Change",
                )

                fig.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                fig2 = px.bar(
                    sub,
                    x="Year",
                    y="YoY % Change",
                    color="YoY % Change",
                    color_continuous_scale=[
                        [0, "#fc8181"],
                        [0.5, "#f6ad55"],
                        [1, "#68d391"],
                    ],
                    title="Year-over-Year Percentage Change",
                )

                fig2.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
                st.plotly_chart(fig2, use_container_width=True)

            stats = sub[["Year", "Value", "YoY Change", "YoY % Change"]].copy()
            stats["YoY Change"] = stats["YoY Change"].round(3)
            stats["YoY % Change"] = stats["YoY % Change"].round(2)

            st.dataframe(stats.set_index("Year"), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# Bivariate Analysis
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔬 Bivariate Analysis":
    st.markdown(
        "<div class='section-header'>🔬 Bivariate & Multivariate Analysis</div>",
        unsafe_allow_html=True,
    )

    available_indicators = sorted(lka_df["Indicator Name"].dropna().unique())

    if len(available_indicators) < 1:
        st.warning(
            "Bivariate Analysis requires at least 2 different indicators. "
            "Your current dataset only contains one indicator, so correlation/scatter analysis cannot be created."
        )
        st.stop()

    tab1, tab2, tab3 = st.tabs(
        ["🔵 Scatter / Correlation", "🌡 Heatmap", "📦 Distribution"]
    )

    with tab1:
    st.info(
        "This dataset has one main indicator, so the scatter plot uses a derived variable: "
        "current year value vs previous year value."
    )

    indicator_name = available_indicators[0]

    sub = lka_df[
        (lka_df["Indicator Name"] == indicator_name)
        & (lka_df["Year"] >= year_range[0])
        & (lka_df["Year"] <= year_range[1])
    ].copy()

    sub = sub.sort_values("Year")

    # Create derived second variable
    sub["Previous Year Value"] = sub["Value"].shift(1)

    # Remove first row because previous year value is empty
    sub = sub.dropna(subset=["Previous Year Value"])

    merged = sub.rename(
        columns={
            "Value": "X",
            "Previous Year Value": "Y",
        }
    )

    if merged.empty:
        st.info("Not enough yearly data to create the derived bivariate analysis.")
    else:
        x_ind = "Current Year Value"
        y_ind = "Previous Year Value"

        corr = merged["X"].corr(merged["Y"])

        if corr > 0.7:
            corr_text = "Strong positive relationship"
        elif corr > 0.3:
            corr_text = "Moderate positive relationship"
        elif corr < -0.7:
            corr_text = "Strong negative relationship"
        elif corr < -0.3:
            corr_text = "Moderate negative relationship"
        else:
            corr_text = "Weak relationship"

        st.markdown(
            f"""
            <div class='insight-box'>
                📐 <strong>Pearson Correlation:</strong>
                <strong>{corr:.4f}</strong> — {corr_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig = px.scatter(
            merged,
            x="X",
            y="Y",
            color="Year",
            color_continuous_scale="Teal",
            trendline="ols",
            labels={
                "X": x_ind,
                "Y": y_ind,
                "Year": "Year",
            },
            title=f"Derived Bivariate Analysis: {x_ind} vs {y_ind}",
            hover_data={"Year": True},
        )

        fig.update_traces(marker=dict(size=8, opacity=0.85))
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("Select indicators for the correlation matrix:")

        heat_inds = st.multiselect(
            "Indicators for heatmap",
            available_indicators,
            default=available_indicators[:min(6, len(available_indicators))],
            key="heat_inds",
        )

        if len(heat_inds) < 2:
            st.info("Select at least 2 indicators.")
        else:
            pivot = (
                lka_df[
                    lka_df["Indicator Name"].isin(heat_inds)
                    & (lka_df["Year"] >= year_range[0])
                    & (lka_df["Year"] <= year_range[1])
                ]
                .pivot_table(index="Year", columns="Indicator Name", values="Value")
                .dropna(how="all", axis=1)
            )

            if pivot.shape[1] < 2:
                st.info("Not enough overlapping data to compute correlation matrix.")
            else:
                corr_mat = pivot.corr()

                fig = px.imshow(
                    corr_mat,
                    color_continuous_scale=[
                        [0, "#fc8181"],
                        [0.5, "#2d3748"],
                        [1, "#68d391"],
                    ],
                    zmin=-1,
                    zmax=1,
                    text_auto=".2f",
                    title="Correlation Matrix",
                )

                fig.update_layout(**PLOT_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        dist_ind = st.selectbox(
            "Indicator for distribution",
            available_indicators,
            key="dist_ind",
        )

        sub = lka_df[
            (lka_df["Indicator Name"] == dist_ind)
            & (lka_df["Year"] >= year_range[0])
            & (lka_df["Year"] <= year_range[1])
        ]["Value"].dropna()

        if sub.empty:
            st.info("No data.")
        else:
            col_l, col_r = st.columns(2)

            with col_l:
                fig = px.histogram(
                    sub,
                    nbins=15,
                    color_discrete_sequence=[COLORS[0]],
                    title="Distribution Histogram",
                )

                fig.update_layout(**PLOT_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

            with col_r:
                fig2 = go.Figure()

                fig2.add_trace(
                    go.Box(
                        y=sub,
                        name=dist_ind[:30],
                        boxpoints="all",
                        marker_color=COLORS[1],
                        line_color=COLORS[0],
                    )
                )

                fig2.update_layout(
                    **PLOT_LAYOUT,
                    title="Box Plot",
                    yaxis_title=dist_ind,
                )

                st.plotly_chart(fig2, use_container_width=True)

            desc = sub.describe()

            st.markdown(
                "<div class='section-header'>📊 Descriptive Statistics</div>",
                unsafe_allow_html=True,
            )

            cols = st.columns(4)

            for i, (stat, val) in enumerate(desc.items()):
                with cols[i % 4]:
                    st.metric(stat.capitalize(), f"{val:.3f}")


# ─────────────────────────────────────────────────────────────────────────────
# Global Comparison
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🌍 Global Comparison":
    st.markdown(
        "<div class='section-header'>🌍 Global Comparison</div>",
        unsafe_allow_html=True,
    )

    comp_ind = st.selectbox(
        "Indicator to compare",
        selected_indicators if selected_indicators else indicators,
        key="comp_ind",
    )

    countries_to_plot = ["Sri Lanka"] + compare_countries

    comp_df = all_df[
        (all_df["Country Name"].isin(countries_to_plot))
        & (all_df["Indicator Name"] == comp_ind)
        & (all_df["Year"] >= year_range[0])
        & (all_df["Year"] <= year_range[1])
    ].copy()

    if comp_df.empty:
        st.info("No data for the selected indicator or countries.")
    else:
        tab1, tab2, tab3 = st.tabs(
            ["📉 Time Series", "📊 Latest Comparison", "📋 Ranking Table"]
        )

        with tab1:
            fig = px.line(
                comp_df,
                x="Year",
                y="Value",
                color="Country Name",
                title=f"{comp_ind} — Country Comparison",
                color_discrete_sequence=COLORS,
                markers=True,
            )

            for trace in fig.data:
                if trace.name == "Sri Lanka":
                    trace.line.width = 3.5
                    trace.marker.size = 7

            fig.update_layout(**PLOT_LAYOUT, hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            latest_year_avail = comp_df["Year"].max()

            latest_bar = comp_df[
                comp_df["Year"] == latest_year_avail
            ].sort_values("Value", ascending=True)

            fig = px.bar(
                latest_bar,
                x="Value",
                y="Country Name",
                orientation="h",
                color="Country Name",
                color_discrete_sequence=COLORS,
                title=f"{comp_ind} — Latest Year ({latest_year_avail})",
            )

            fig.update_layout(**PLOT_LAYOUT, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            pivot_tab = (
                comp_df.pivot_table(
                    index="Country Name",
                    columns="Year",
                    values="Value",
                )
                .round(2)
            )

            pivot_tab.columns = [str(c) for c in pivot_tab.columns]

            st.dataframe(
                pivot_tab.style.background_gradient(cmap="Blues", axis=None),
                use_container_width=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# Statistical Summary
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📊 Statistical Summary":
    st.markdown(
        "<div class='section-header'>📊 Statistical Summary</div>",
        unsafe_allow_html=True,
    )

    if not selected_indicators:
        st.warning("Please select at least one indicator from the sidebar.")
        st.stop()

    rows = []

    for ind in selected_indicators:
        sub = lka_df[
            (lka_df["Indicator Name"] == ind)
            & (lka_df["Year"] >= year_range[0])
            & (lka_df["Year"] <= year_range[1])
        ]["Value"].dropna()

        if sub.empty:
            continue

        rows.append(
            {
                "Indicator": ind[:60],
                "N": int(len(sub)),
                "Min": round(sub.min(), 3),
                "Max": round(sub.max(), 3),
                "Mean": round(sub.mean(), 3),
                "Median": round(sub.median(), 3),
                "Std Dev": round(sub.std(), 3),
                "25th %ile": round(sub.quantile(0.25), 3),
                "75th %ile": round(sub.quantile(0.75), 3),
                "Skewness": round(sub.skew(), 3),
                "Kurtosis": round(sub.kurtosis(), 3),
            }
        )

    if not rows:
        st.info("No data for selected filters.")
    else:
        summary_df = pd.DataFrame(rows).set_index("Indicator")

        st.dataframe(summary_df, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div class='section-header'>📈 Violin / Distribution Comparison</div>",
            unsafe_allow_html=True,
        )

        fig = go.Figure()

        for i, ind in enumerate(selected_indicators):
            sub = lka_df[
                (lka_df["Indicator Name"] == ind)
                & (lka_df["Year"] >= year_range[0])
                & (lka_df["Year"] <= year_range[1])
            ]["Value"].dropna()

            if sub.empty:
                continue

            fig.add_trace(
                go.Violin(
                    y=sub,
                    name=ind[:30] + ("…" if len(ind) > 30 else ""),
                    box_visible=True,
                    meanline_visible=True,
                    line_color=COLORS[i % len(COLORS)],
                )
            )

        fig.update_layout(
            **PLOT_LAYOUT,
            title="Value Distribution by Indicator",
            yaxis_title="Value",
        )

        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# Raw Data
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📋 Raw Data":
    st.markdown(
        "<div class='section-header'>📋 Raw Data Explorer</div>",
        unsafe_allow_html=True,
    )

    raw_show = st.radio(
        "Dataset",
        ["Sri Lanka Only", "All Countries"],
        horizontal=True,
    )

    if raw_show == "Sri Lanka Only":
        source_df = get_filtered()
    else:
        source_df = all_df[
            (all_df["Year"] >= year_range[0])
            & (all_df["Year"] <= year_range[1])
        ]

    search_q = st.text_input("🔍 Filter rows", "")

    if search_q:
        mask = source_df.apply(
            lambda col: col.astype(str).str.contains(search_q, case=False)
        ).any(axis=1)

        source_df = source_df[mask]

    st.caption(f"Showing **{len(source_df):,}** rows")
    st.dataframe(source_df, use_container_width=True, height=480)

    csv_bytes = source_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download as CSV",
        data=csv_bytes,
        file_name="sri_lanka_dashboard_export.csv",
        mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <hr style='border-color:rgba(255,255,255,0.08); margin-top:2rem;'>
    <div style='text-align:center; font-size:0.75rem; color:rgba(255,255,255,0.3); padding:0.5rem;'>
        Sri Lanka Sustainability Dashboard · Data: World Bank World Development Indicators · Built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)