"""
PSEO Earnings Dashboard
Run with: streamlit run dashboard.py
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PSEO Earnings Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Light theme CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .main, .block-container {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        font-family: "IBM Plex Sans", "Inter", "Helvetica Neue", sans-serif !important;
    }
    section[data-testid="stSidebar"] { display: none !important; }

    .block-container {
        padding: 2.5rem 3rem !important;
        max-width: 1600px !important;
    }

    /* Research question */
    h1.rq {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1a1a1a;
        border-left: 3px solid #bbbbbb;
        padding-left: 0.75rem;
        margin: 0 0 0.2rem 0;
        line-height: 1.5;
        letter-spacing: 0.01em;
    }

    /* Chart section title */
    h2.chart-title {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #555555;
        margin: 0 0 0.6rem 0;
        border-bottom: 1px solid #dddddd;
        padding-bottom: 0.4rem;
    }

    /* Filter label */
    .f-label {
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #777777;
        margin-bottom: 0.2rem;
    }

    /* Warning box */
    .warn-box {
        background: #fff8e1;
        border: 1px solid #e6a800;
        border-radius: 2px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #7a5c00;
        font-weight: 500;
    }

    /* Footer */
    .footer-val { font-size: 0.85rem; color: #444444; margin-top: 0.1rem; }
    .meta-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
                  text-transform: uppercase; color: #888888; }

    /* Divider */
    hr { border-color: #e0e0e0 !important; margin: 2rem 0 !important; }
    hr.section-break {
        border-color: #cccccc !important;
        margin: 3.5rem 0 !important;
        border-width: 2px !important;
    }

    /* All Streamlit text inputs light */
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #dddddd !important;
    }
    div[data-baseweb="option"]:hover { background-color: #f0f0f0 !important; }
    span[data-baseweb="tag"] {
        background-color: #e8e8e8 !important;
        color: #1a1a1a !important;
    }
    label, .stRadio label, .stSelectbox label, .stMultiSelect label {
        color: #1a1a1a !important;
    }
    .stRadio > div { gap: 0.4rem; }
    p { color: #1a1a1a !important; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffffff !important;
        border-bottom: 1px solid #dddddd !important;
        gap: 0.25rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #888888 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        padding: 0.55rem 1.2rem !important;
        border-radius: 0 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1a1a1a !important;
        border-bottom: 2px solid #1a1a1a !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff !important;
        padding-top: 1.5rem !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Plotly light palette ───────────────────────────────────────────────────────
BG_PLOT  = "#ffffff"
BG_PAPER = "#ffffff"
TEXT_CLR = "#1a1a1a"
GRID_CLR = "#e8e8e8"
LINE_CLR = "#cccccc"
AXIS_CLR = "#666666"

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_FILE      = "Usage_Data/pseo_state_cohort_trends_agg34_deg5_cip11_13_51_clean.csv"
FLOW_DATA_FILE = "Usage_Data/pseof_agg178_deg5_cip11_13_51_clean.csv"

CIP_MAP   = {11: "Computer Science (CIP 11)", 13: "Education (CIP 13)", 51: "Healthcare (CIP 51)"}
CIP_SHORT = {11: "CS", 13: "Education", 51: "Healthcare"}
CIP_LABEL = {"11": "Computer Science", "13": "Education", "51": "Health Professions"}

YEAR_COLS = {
    1:  {"p25": "y1_p25_earnings",  "p50": "y1_p50_earnings",  "p75": "y1_p75_earnings"},
    5:  {"p25": "y5_p25_earnings",  "p50": "y5_p50_earnings",  "p75": "y5_p75_earnings"},
    10: {"p25": "y10_p25_earnings", "p50": "y10_p50_earnings", "p75": "y10_p75_earnings"},
}
YEARS_LABEL = {1: "1 Yr Post-Grad", 5: "5 Yrs Post-Grad", 10: "10 Yrs Post-Grad"}

FLOW_EMP_COLS = {
    1:  "y1_grads_emp",
    5:  "y5_grads_emp",
    10: "y10_grads_emp",
}
FLOW_NME_COLS = {
    1:  "y1_grads_nme",
    5:  "y5_grads_nme",
    10: "y10_grads_nme",
}
FLOW_GRANULAR_FILE = "Intermediary_Cleaned/pseo_sankey_granular.csv"
INSTATE_COLOR = "#0a8f4f"
FLOW_COUNT_COLS = {1: "y1_count", 5: "y5_count", 10: "y10_count"}

MAJOR_PALETTES = {
    11: ["#6baed6", "#2171b5", "#084594"],
    13: ["#74c476", "#238b45", "#00441b"],
    51: ["#fc8d59", "#d7301f", "#7f0000"],
}
MAJOR_COLOR = {11: "#4a9fd4", 13: "#41ab5d", 51: "#f16913"}

PCT_OPTIONS = {"25th Percentile": "p25", "50th Percentile (Median)": "p50", "75th Percentile": "p75"}
PCT_LABELS  = {"p25": "25th Pctl.", "p50": "50th Pctl. (Median)", "p75": "75th Pctl."}

# 20 high-contrast industry colors (one per NAICS sector)
INDUSTRY_COLORS = {
    "Agriculture, Forestry, Fishing and Hunting":                          "#4e9a6e",
    "Mining, Quarrying, and Oil and Gas Extraction":                       "#b5a642",
    "Utilities":                                                            "#e07b39",
    "Construction":                                                         "#c0392b",
    "Manufacturing":                                                        "#8e44ad",
    "Wholesale Trade":                                                      "#2980b9",
    "Retail Trade":                                                         "#16a085",
    "Transportation and Warehousing":                                       "#d35400",
    "Information":                                                          "#2471a3",
    "Finance and Insurance":                                                "#1abc9c",
    "Real Estate and Rental and Leasing":                                  "#7d3c98",
    "Professional, Scientific, and Technical Services":                    "#117a65",
    "Management of Companies and Enterprises":                             "#6e2f80",
    "Administrative and Support and Waste Management and Remediation Services": "#935116",
    "Educational Services":                                                 "#1a5276",
    "Health Care and Social Assistance":                                    "#922b21",
    "Arts, Entertainment, and Recreation":                                  "#7b241c",
    "Accommodation and Food Services":                                      "#784212",
    "Other Services (except Public Administration)":                        "#515a5a",
    "Public Administration":                                                "#1f618d",
}
NME_COLOR    = "#bbbbbb"
MAJOR_NODE_COLORS = {
    "Computer Science":  "#4a9fd4",
    "Education":         "#41ab5d",
    "Health Professions":"#f16913",
}
DIVISION_COLORS = [
    "#0288d1","#0277bd","#01579b","#039be5",
    "#1565c0","#0d47a1","#1976d2","#1e88e5","#2196f3",
]


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

@st.cache_data
def load_flow_data():
    df = pd.read_csv(
        FLOW_DATA_FILE,
        dtype={
            "cipcode": str, "degree_level": str,
            "geography": str, "industry": str,
            "institution": str,
        },
    )
    # Ensure state_name column exists (fallback if notebook hasn't been re-run)
    if "state_name" not in df.columns:
        try:
            fips = pd.read_csv("Labels/label_fipsnum.csv", dtype={"geography": str})
            fips = fips.rename(columns={"label": "state_name"})[["geography", "state_name"]]
            df["_fips"] = df["institution"].astype(str).str.zfill(2)
            df = df.merge(fips, left_on="_fips", right_on="geography", how="left", suffixes=("", "_fips"))
            df = df.drop(columns=["_fips", "geography_fips"], errors="ignore")
        except Exception:
            df["state_name"] = df["institution"]
    return df

@st.cache_data
def load_flow_granular():
    """Load expanded In-State / Out-of-State Sankey dataset (notebook Step 6)."""
    for path in (FLOW_GRANULAR_FILE, "pseo_sankey_granular.csv"):
        try:
            return pd.read_csv(
                path,
                dtype={"cipcode": str, "geography": str,
                       "industry": str, "institution": str},
            )
        except FileNotFoundError:
            continue
    return None


@st.cache_data
def load_regression_coefficients():
    """Load OLS regression coefficients (β premiums vs Agriculture baseline)."""
    df = pd.read_csv("Regression/regression_coefficients.csv")
    # Map numeric year labels to integers  (y1→1, y5→5, y10→10)
    df["year_after"] = df["Year_Label"].str.replace("y", "").astype(int)
    return df

df        = load_data()
df_flow   = load_flow_data()
df_flow_g = load_flow_granular()
df_coef   = load_regression_coefficients()

all_states       = sorted(df["state_name"].dropna().unique().tolist())
all_cohorts      = sorted(df["grad_cohort_label"].dropna().unique().tolist())
flow_states      = sorted(df_flow["state_name"].dropna().unique().tolist())
flow_cohorts     = sorted(df_flow["grad_cohort_label"].dropna().unique().tolist())


# ── Shared helpers ─────────────────────────────────────────────────────────────
def apply_filters(base_df, cips, state, cohort):
    out = base_df[base_df["cipcode"].isin(cips)].copy()
    if state  != "All States Combined":  out = out[out["state_name"]        == state]
    if cohort != "All Cohorts Combined": out = out[out["grad_cohort_label"] == cohort]
    return out


PLOTLY_CONFIG = {
    "toImageButtonOptions": {
        "format": "png",
        "scale": 4,
    },
}


def base_layout(title, subtitle):
    return dict(
        plot_bgcolor=BG_PLOT,
        paper_bgcolor=BG_PAPER,
        font=dict(family="IBM Plex Sans, Inter, sans-serif", color=TEXT_CLR, size=16),
        title=dict(
            text=(
                f"<b style='color:{TEXT_CLR}'>{title}</b>"
                f"<br><sup><span style='color:#777777'>{subtitle}</span></sup>"
            ),
            font=dict(size=22, color=TEXT_CLR),
            x=0, xanchor="left", pad=dict(b=18),
        ),
        xaxis=dict(
            tickfont=dict(size=16, color=TEXT_CLR),
            title_font=dict(size=16, color="#555555"),
            showgrid=False, showline=True,
            linecolor=LINE_CLR, ticks="outside",
            ticklen=5, tickcolor=AXIS_CLR, zeroline=False,
        ),
        yaxis=dict(
            tickformat="$,.0f",
            tickfont=dict(size=15, color=TEXT_CLR),
            title_font=dict(size=16, color="#555555"),
            showgrid=True, gridcolor=GRID_CLR, gridwidth=1,
            showline=True, linecolor=LINE_CLR,
            ticks="outside", ticklen=5, tickcolor=AXIS_CLR, zeroline=False,
        ),
        legend=dict(
            font=dict(size=15, color=TEXT_CLR),
            bgcolor="#f8f8f8", bordercolor="#dddddd", borderwidth=1,
            orientation="v", x=1.01, xanchor="left", y=1.0, yanchor="top",
        ),
        hoverlabel=dict(
            bgcolor="#ffffff", bordercolor="#cccccc",
            font=dict(color=TEXT_CLR, size=15),
        ),
        margin=dict(l=90, r=220, t=110, b=80),
        height=750,
    )


# ── Sankey builder ─────────────────────────────────────────────────────────────
def build_sankey(dff: pd.DataFrame, year: int, title: str,
                 mode: str = "full") -> go.Figure:
    """
    Multi-mode Sankey with optional In-State / Out-of-State granularity.

    Modes
    -----
    "industry"  : Major → Industry  (2-tier)
    "geography" : Major → Geography (2-tier, In-State / Division targets)
    "full"      : Major → Industry → Geography (3-tier)

    Accepts both the *granular* dataset (target_node + y*_count columns) and
    the legacy flow file (division_label + y*_grads_emp).  NME nodes are added
    per major for graduates with no / marginal employment.
    """
    is_granular = "target_node" in dff.columns
    count_col = FLOW_COUNT_COLS[year] if is_granular else FLOW_EMP_COLS[year]
    nme_col   = FLOW_NME_COLS[year]
    geo_col   = "target_node" if is_granular else "division_label"

    majors     = sorted(dff["major_label"].dropna().unique().tolist())
    industries = sorted(dff["industry_label"].dropna().unique().tolist())
    geo_values = sorted(dff[geo_col].dropna().unique().tolist())

    # ── Node registry ─────────────────────────────────────────────────────────
    node_labels: list[str] = []
    node_colors: list[str] = []

    maj_idx: dict[str, int] = {}
    for m in majors:
        maj_idx[m] = len(node_labels)
        node_labels.append(m)
        node_colors.append(MAJOR_NODE_COLORS.get(m, "#888888"))

    nme_idx: dict[str, int] = {}
    for m in majors:
        nme_idx[m] = len(node_labels)
        node_labels.append(f"{m} — Not Observed / Marginal")
        node_colors.append(NME_COLOR)

    # Industry nodes (modes: industry, full)
    ind_idx: dict[str, int] = {}
    if mode in ("industry", "full"):
        if mode == "full":
            # Sort by volume to reduce visual tangling in the 3-tier layout
            vol = (dff.groupby("industry_label")[count_col]
                   .sum(min_count=1).fillna(0)
                   .sort_values(ascending=False))
            ordered_ind = vol.index.tolist()
        else:
            ordered_ind = industries
        for ind in ordered_ind:
            ind_idx[ind] = len(node_labels)
            node_labels.append(ind)
            node_colors.append(INDUSTRY_COLORS.get(ind, "#888888"))

    # Geography / target nodes (modes: geography, full)
    geo_idx: dict[str, int] = {}
    if mode in ("geography", "full"):
        unique_divs = sorted(dff["division_label"].dropna().unique().tolist())
        div_clr = {d: DIVISION_COLORS[i % len(DIVISION_COLORS)]
                   for i, d in enumerate(unique_divs)}

        def _geo_key(n: str) -> tuple:
            if "(In-State)" in n:
                return (0, n)
            if n.startswith("Other "):
                return (2, n)
            return (1, n)

        for gn in sorted(geo_values, key=_geo_key):
            geo_idx[gn] = len(node_labels)
            node_labels.append(gn)
            if "(In-State)" in gn:
                node_colors.append(INSTATE_COLOR)
            else:
                base_div = gn.replace("Other ", "", 1) if gn.startswith("Other ") else gn
                base = div_clr.get(base_div, "#888888")
                if gn.startswith("Other "):
                    r = int(int(base[1:3], 16) * 0.6)
                    g = int(int(base[3:5], 16) * 0.6)
                    b = int(int(base[5:7], 16) * 0.6)
                    node_colors.append(f"#{r:02x}{g:02x}{b:02x}")
                else:
                    node_colors.append(base)

    sources:    list[int]            = []
    targets:    list[int]            = []
    values:     list[float]          = []
    customdata: list[str | None]     = []

    # ── Tier-1 links ──────────────────────────────────────────────────────────
    if mode in ("industry", "full"):
        agg = (dff.groupby(["major_label", "industry_label"])[count_col]
               .sum(min_count=1).reset_index().dropna(subset=[count_col]))
        for _, row in agg.iterrows():
            v = float(row[count_col])
            if v <= 0:
                continue
            sources.append(maj_idx[row["major_label"]])
            targets.append(ind_idx[row["industry_label"]])
            values.append(v)
            customdata.append(None)

    elif mode == "geography":
        agg = (dff.groupby(["major_label", geo_col])[count_col]
               .sum(min_count=1).reset_index().dropna(subset=[count_col]))
        for _, row in agg.iterrows():
            v = float(row[count_col])
            if v <= 0:
                continue
            sources.append(maj_idx[row["major_label"]])
            targets.append(geo_idx[row[geo_col]])
            values.append(v)
            customdata.append(None)

    # ── Major → NME (deduplicated per institution × major × cohort) ───────────
    nme_keys = [c for c in ("institution", "major_label", "grad_cohort")
                if c in dff.columns]
    nme_dd = (dff[nme_keys + [nme_col]]
              .drop_duplicates(subset=nme_keys)
              .dropna(subset=[nme_col]))
    nme_agg = (nme_dd.groupby("major_label")[nme_col]
               .sum(min_count=1).reset_index().dropna(subset=[nme_col]))
    for _, row in nme_agg.iterrows():
        m, v = row["major_label"], float(row[nme_col])
        if v <= 0 or m not in maj_idx:
            continue
        sources.append(maj_idx[m])
        targets.append(nme_idx[m])
        values.append(v)
        customdata.append(None)

    # ── Back-fill percentage hover text for tier-1 + NME links ────────────────
    out_tot: dict[str, float] = {}
    for s, v in zip(sources, values):
        lbl = node_labels[s]
        out_tot[lbl] = out_tot.get(lbl, 0) + v
    for i in range(len(customdata)):
        if customdata[i] is None:
            sl, tl = node_labels[sources[i]], node_labels[targets[i]]
            v   = values[i]
            tot = out_tot.get(sl, 0)
            pct = (v / tot * 100) if tot > 0 else 0.0
            customdata[i] = f"{sl} → {tl}<br>Count: {v:,.0f}<br>Share: {pct:.1f}%"

    # ── Tier-2 links (full mode): Industry → Geography ────────────────────────
    if mode == "full":
        agg2 = (dff.groupby(["industry_label", geo_col])[count_col]
                .sum(min_count=1).reset_index().dropna(subset=[count_col]))
        ind_tot = agg2.groupby("industry_label")[count_col].sum().to_dict()
        for _, row in agg2.iterrows():
            v = float(row[count_col])
            if v <= 0:
                continue
            ind, gn = row["industry_label"], row[geo_col]
            tot = float(ind_tot.get(ind, 0))
            pct = (v / tot * 100) if tot > 0 else 0.0
            sources.append(ind_idx[ind])
            targets.append(geo_idx[gn])
            values.append(v)
            customdata.append(
                f"{ind} → {gn}<br>Count: {v:,.0f}<br>Share: {pct:.1f}%")

    if not sources:
        return None

    # ── Link colors (inherit source node color, translucent) ──────────────────
    link_colors = []
    for s in sources:
        c = node_colors[s]
        if c.startswith("rgba"):
            link_colors.append(c)
        else:
            link_colors.append(
                f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.35)")

    mode_subtitle = {
        "industry":  "Major → Industry",
        "geography": "Major → Geography (In-State / Division)",
        "full":      "Major → Industry → Geography (In-State / Division)",
    }

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=18, thickness=22,
            line=dict(color="#000000", width=0.5),
            label=node_labels, color=node_colors,
            hovertemplate="%{label}<br>Total flow: %{value:,.0f}<extra></extra>",
        ),
        link=dict(
            source=sources, target=targets, value=values,
            color=link_colors, customdata=customdata,
            hovertemplate="%{customdata}<extra></extra>",
        ),
    ))

    fig.update_layout(
        paper_bgcolor=BG_PAPER, plot_bgcolor=BG_PAPER,
        font=dict(family="IBM Plex Sans, Inter, sans-serif",
                  color=TEXT_CLR, size=13),
        title=dict(
            text=(
                f"<b style='color:{TEXT_CLR}'>{title}</b>"
                f"<br><sup><span style='color:#777777'>"
                f"{mode_subtitle.get(mode, '')} · "
                f"Agg 178, Degree 05, CIP 11/13/51"
                f"</span></sup>"
            ),
            font=dict(size=20, color=TEXT_CLR),
            x=0, xanchor="left", pad=dict(b=12),
        ),
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#cccccc",
                        font=dict(color=TEXT_CLR, size=14)),
        margin=dict(l=20, r=20, t=100, b=20),
        height=800,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Page header
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<h1 class="rq">What are the 1-year, 5-year, and 10-year post-graduation average salaries '
    "for Computer Science, Education, and Healthcare majors?</h1>",
    unsafe_allow_html=True,
)
st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:0.78rem;color:#888888;margin:0'>PSEO — U.S. Census Bureau &nbsp;·&nbsp; "
    "Aggregation level 34 / 178, Degree level 5 &nbsp;·&nbsp; CIP 11 / 13 / 51</p>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tabs
# ══════════════════════════════════════════════════════════════════════════════
tab_earnings, tab_flows, tab_reg = st.tabs(["Earnings", "Employment Flows", "Economic Returns"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Earnings
# ══════════════════════════════════════════════════════════════════════════════
with tab_earnings:

    # ── FIGURE 1 — Bar chart ──────────────────────────────────────────────────
    st.markdown('<h2 class="chart-title">Figure 1 &nbsp;·&nbsp; Earnings Distribution by Major</h2>',
                unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns([2, 2, 2, 2])
    with fc1:
        st.markdown('<div class="f-label">Major</div>', unsafe_allow_html=True)
        b_majors = st.multiselect(
            "b_major", options=list(CIP_SHORT.values()),
            default=list(CIP_SHORT.values()), label_visibility="collapsed", key="b_major"
        )
    with fc2:
        st.markdown('<div class="f-label">Years Post-Graduation</div>', unsafe_allow_html=True)
        b_year_lbl = st.radio(
            "b_year", options=["1 Year", "5 Years", "10 Years"],
            index=0, label_visibility="collapsed", horizontal=True, key="b_year"
        )
        b_year = {"1 Year": 1, "5 Years": 5, "10 Years": 10}[b_year_lbl]
    with fc3:
        st.markdown('<div class="f-label">State</div>', unsafe_allow_html=True)
        b_state = st.selectbox(
            "b_state", options=["All States Combined"] + all_states,
            index=0, label_visibility="collapsed", key="b_state"
        )
    with fc4:
        st.markdown('<div class="f-label">Graduation Cohort</div>', unsafe_allow_html=True)
        b_cohort = st.selectbox(
            "b_cohort", options=["All Cohorts Combined"] + all_cohorts,
            index=0, label_visibility="collapsed", key="b_cohort"
        )

    if not b_majors:
        st.markdown(
            '<div class="warn-box">⚠&nbsp; At least one major must be chosen.</div>',
            unsafe_allow_html=True,
        )
    else:
        b_cips = [k for k, v in CIP_SHORT.items() if v in b_majors]
        dff_b  = apply_filters(df, b_cips, b_state, b_cohort)
        cols_b = YEAR_COLS[b_year]
        agg_b  = (
            dff_b.groupby("cipcode")[list(cols_b.values())].mean().reset_index()
            .rename(columns={cols_b["p25"]: "P25", cols_b["p50"]: "P50", cols_b["p75"]: "P75"})
        )

        PCTL_LABEL = {"P25": "25th Pctl.", "P50": "50th Pctl. (Median)", "P75": "75th Pctl."}
        fig_bar = go.Figure()
        for cip in sorted(b_cips):
            row = agg_b[agg_b["cipcode"] == cip]
            if row.empty:
                continue
            pal   = MAJOR_PALETTES[cip]
            short = CIP_SHORT[cip]
            for i, pct in enumerate(["P25", "P50", "P75"]):
                val = float(row[pct].values[0]) if not row[pct].isna().all() else 0.0
                fig_bar.add_trace(go.Bar(
                    name=f"{short} — {PCTL_LABEL[pct]}",
                    x=[CIP_MAP[cip]], y=[val],
                    marker_color=pal[i],
                    marker_line_color=BG_PLOT, marker_line_width=1.5,
                    legendgroup=f"{cip}_{pct}",
                    text=[f"${val:,.0f}"],
                    textposition="inside",
                    textfont=dict(size=14, color="#ffffff"),
                    insidetextanchor="middle",
                    hovertemplate=f"<b>{short}</b><br>{PCTL_LABEL[pct]}<br><b>${val:,.0f}</b><extra></extra>",
                ))

        b_major_str = " · ".join(CIP_SHORT[c] for c in sorted(b_cips))
        b_title = f"{b_year_lbl} Post-Grad  |  {b_major_str}  |  {b_state}  |  Cohort: {b_cohort}"
        b_sub   = f"Mean 25th, 50th & 75th percentile earnings · {b_state} · Cohort: {b_cohort}"

        layout_b = base_layout(b_title, b_sub)
        layout_b["barmode"] = "group"
        layout_b["bargap"]  = 0.15
        layout_b["bargroupgap"] = 0.04
        layout_b["xaxis"]["title"] = dict(text="Field of Study (CIP Category)",
                                          font=dict(size=16, color="#555555"))
        layout_b["yaxis"]["title"] = dict(text="Mean Annual Earnings (USD)",
                                          font=dict(size=16, color="#555555"))
        y_max = agg_b[["P25", "P50", "P75"]].max().max()
        layout_b["yaxis"]["range"] = [0, y_max * 1.25]
        layout_b["legend"]["title"] = dict(text="Major — Percentile",
                                           font=dict(size=14, color="#555555"))
        fig_bar.update_layout(**layout_b)
        st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(f'<div class="meta-label">Rows in view</div>'
                        f'<div class="footer-val">{len(dff_b):,}</div>', unsafe_allow_html=True)
        with mc2:
            st.markdown(f'<div class="meta-label">States in view</div>'
                        f'<div class="footer-val">{dff_b["state_name"].nunique()}</div>', unsafe_allow_html=True)
        with mc3:
            st.markdown(f'<div class="meta-label">Cohorts in view</div>'
                        f'<div class="footer-val">{dff_b["grad_cohort_label"].nunique()}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<hr class='section-break'>", unsafe_allow_html=True)
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── FIGURE 2 — Line chart: trajectory ────────────────────────────────────
    st.markdown('<h2 class="chart-title">Figure 2 &nbsp;·&nbsp; Earnings Trajectory Across Post-Graduation Years</h2>',
                unsafe_allow_html=True)

    lc1, lc2, lc3, lc4 = st.columns([2, 2, 2, 2])
    with lc1:
        st.markdown('<div class="f-label">Major</div>', unsafe_allow_html=True)
        l_majors = st.multiselect(
            "l_major", options=list(CIP_SHORT.values()),
            default=list(CIP_SHORT.values()), label_visibility="collapsed", key="l_major"
        )
    with lc2:
        st.markdown('<div class="f-label">Percentile</div>', unsafe_allow_html=True)
        l_pct_lbl = st.radio(
            "l_pct", options=list(PCT_OPTIONS.keys()),
            index=1, label_visibility="collapsed", horizontal=False, key="l_pct"
        )
        l_pct = PCT_OPTIONS[l_pct_lbl]
    with lc3:
        st.markdown('<div class="f-label">State</div>', unsafe_allow_html=True)
        l_state = st.selectbox(
            "l_state", options=["All States Combined"] + all_states,
            index=0, label_visibility="collapsed", key="l_state"
        )
    with lc4:
        st.markdown('<div class="f-label">Graduation Cohort</div>', unsafe_allow_html=True)
        l_cohort = st.selectbox(
            "l_cohort", options=["All Cohorts Combined"] + all_cohorts,
            index=0, label_visibility="collapsed", key="l_cohort"
        )

    if not l_majors:
        st.markdown(
            '<div class="warn-box">⚠&nbsp; At least one major must be chosen.</div>',
            unsafe_allow_html=True,
        )
    else:
        l_cips = [k for k, v in CIP_SHORT.items() if v in l_majors]
        dff_l  = apply_filters(df, l_cips, l_state, l_cohort)

        records = []
        for yr in [1, 5, 10]:
            col_name = YEAR_COLS[yr][l_pct]
            grp = dff_l.groupby("cipcode")[col_name].mean().reset_index()
            grp["year"] = yr
            grp.rename(columns={col_name: "value"}, inplace=True)
            records.append(grp)
        line_df = pd.concat(records, ignore_index=True)

        x_labels = {1: "1 Yr Post-Grad", 5: "5 Yrs Post-Grad", 10: "10 Yrs Post-Grad"}

        TRAJ_TEXT_POS = {11: "top center", 13: "top center", 51: "bottom center"}

        fig_line = go.Figure()
        for cip in sorted(l_cips):
            sub = line_df[line_df["cipcode"] == cip].sort_values("year")
            if sub.empty or sub["value"].isna().all():
                continue
            short  = CIP_SHORT[cip]
            color  = MAJOR_COLOR[cip]
            xs     = [x_labels[y] for y in sub["year"]]
            ys     = sub["value"].tolist()
            labels = [f"${v:,.0f}" for v in ys]
            fig_line.add_trace(go.Scatter(
                name=short,
                x=xs, y=ys,
                mode="lines+markers+text",
                line=dict(color=color, width=2.5),
                marker=dict(color=color, size=8, symbol="circle",
                            line=dict(color=BG_PLOT, width=1.5)),
                text=labels,
                textposition=TRAJ_TEXT_POS.get(cip, "top center"),
                textfont=dict(size=12, color=color),
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{short}</b><br>"
                    f"{PCT_LABELS[l_pct]}<br>"
                    "%{x}<br><b>$%{y:,.0f}</b><extra></extra>"
                ),
            ))

        l_major_str = " · ".join(CIP_SHORT[c] for c in sorted(l_cips))
        l_title = (
            f"Earnings Trajectory — {PCT_LABELS[l_pct]}  |  {l_major_str}  |  "
            f"{l_state}  |  Cohort: {l_cohort}"
        )
        l_sub = f"{PCT_LABELS[l_pct]} earnings at 1, 5, and 10 years · {l_state} · Cohort: {l_cohort}"

        layout_l = base_layout(l_title, l_sub)
        layout_l["xaxis"]["title"] = dict(text="Years Post-Graduation",
                                          font=dict(size=11, color="#555555"))
        layout_l["xaxis"]["categoryorder"] = "array"
        layout_l["xaxis"]["categoryarray"] = ["1 Yr Post-Grad", "5 Yrs Post-Grad", "10 Yrs Post-Grad"]
        layout_l["yaxis"]["title"] = dict(text="Mean Annual Earnings (USD)",
                                          font=dict(size=11, color="#555555"))
        layout_l["legend"]["title"] = dict(text="Field of Study",
                                           font=dict(size=10, color="#555555"))

        all_vals = line_df["value"].dropna()
        if not all_vals.empty:
            y_lo, y_hi = all_vals.min(), all_vals.max()
            span = y_hi - y_lo
            if span > 0:
                layout_l["yaxis"]["range"] = [y_lo - span * 0.25, y_hi + span * 0.25]
                layout_l["yaxis"]["dtick"] = 5000

        fig_line.update_layout(**layout_l)
        st.plotly_chart(fig_line, use_container_width=True, config=PLOTLY_CONFIG)

        lm1, lm2, lm3 = st.columns(3)
        with lm1:
            st.markdown(f'<div class="meta-label">Rows in view</div>'
                        f'<div class="footer-val">{len(dff_l):,}</div>', unsafe_allow_html=True)
        with lm2:
            st.markdown(f'<div class="meta-label">States in view</div>'
                        f'<div class="footer-val">{dff_l["state_name"].nunique()}</div>', unsafe_allow_html=True)
        with lm3:
            st.markdown(f'<div class="meta-label">Cohorts in view</div>'
                        f'<div class="footer-val">{dff_l["grad_cohort_label"].nunique()}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<hr class='section-break'>", unsafe_allow_html=True)
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── FIGURE 3 — Line chart: cohorts ────────────────────────────────────────
    st.markdown(
        '<h2 class="chart-title">Figure 3 &nbsp;·&nbsp; Earnings by Graduation Cohort</h2>',
        unsafe_allow_html=True,
    )

    cc1, cc2, cc3, cc4 = st.columns([2, 2, 1.4, 2])
    with cc1:
        st.markdown('<div class="f-label">Major</div>', unsafe_allow_html=True)
        c_majors = st.multiselect(
            "c_major", options=list(CIP_SHORT.values()),
            default=list(CIP_SHORT.values()), label_visibility="collapsed", key="c_major",
        )
    with cc2:
        st.markdown('<div class="f-label">Percentile</div>', unsafe_allow_html=True)
        c_pct_lbl = st.radio(
            "c_pct", options=list(PCT_OPTIONS.keys()),
            index=1, label_visibility="collapsed", horizontal=False, key="c_pct",
        )
        c_pct = PCT_OPTIONS[c_pct_lbl]
    with cc3:
        st.markdown('<div class="f-label">Years Post-Grad</div>', unsafe_allow_html=True)
        c_years_sel = st.multiselect(
            "c_years",
            options=["1 Year", "5 Years", "10 Years"],
            default=["1 Year", "5 Years", "10 Years"],
            label_visibility="collapsed", key="c_years",
        )
        c_years_map = {"1 Year": 1, "5 Years": 5, "10 Years": 10}
        c_years = [c_years_map[y] for y in c_years_sel]
    with cc4:
        st.markdown('<div class="f-label">State</div>', unsafe_allow_html=True)
        c_state = st.selectbox(
            "c_state", options=["All States Combined"] + all_states,
            index=0, label_visibility="collapsed", key="c_state",
        )

    _warn_c = []
    if not c_majors:
        _warn_c.append("at least one major")
    if not c_years:
        _warn_c.append("at least one post-grad year")

    if _warn_c:
        st.markdown(
            f'<div class="warn-box">⚠&nbsp; Please select {" and ".join(_warn_c)}.</div>',
            unsafe_allow_html=True,
        )
    else:
        c_cips = [k for k, v in CIP_SHORT.items() if v in c_majors]
        dff_c = df[df["cipcode"].isin(c_cips)].copy()
        if c_state != "All States Combined":
            dff_c = dff_c[dff_c["state_name"] == c_state]

        cohort_order = sorted(dff_c["grad_cohort_label"].dropna().unique().tolist())

        DASH_STYLES = {1: "solid", 5: "dash", 10: "dot"}
        YEAR_LABEL  = {1: "1 Yr", 5: "5 Yrs", 10: "10 Yrs"}

        MAJOR_YEAR_COLORS = {
            (11, 1):  "#6baed6",
            (11, 5):  "#2171b5",
            (11, 10): "#08306b",
            (13, 1):  "#74c476",
            (13, 5):  "#238b45",
            (13, 10): "#00441b",
            (51, 1):  "#fc8d59",
            (51, 5):  "#d7301f",
            (51, 10): "#67000d",
        }

        COHORT_POS_CYCLE = [
            "top center", "bottom center", "top right",
            "bottom right", "top left", "bottom left",
            "middle right", "middle left", "top center",
        ]

        fig_coh = go.Figure()
        _trace_idx = 0

        for cip in sorted(c_cips):
            sub_cip = dff_c[dff_c["cipcode"] == cip]
            short   = CIP_SHORT[cip]
            for yr in sorted(c_years):
                col_name = YEAR_COLS[yr][c_pct]
                agg_c = (
                    sub_cip.groupby("grad_cohort_label")[col_name]
                    .mean()
                    .reindex(cohort_order)
                    .reset_index()
                    .rename(columns={col_name: "value", "grad_cohort_label": "cohort"})
                )
                if agg_c["value"].isna().all():
                    continue
                color = MAJOR_YEAR_COLORS.get((cip, yr), MAJOR_COLOR[cip])
                labels = [f"${v:,.0f}" if pd.notna(v) else "" for v in agg_c["value"]]
                tpos = COHORT_POS_CYCLE[_trace_idx % len(COHORT_POS_CYCLE)]
                _trace_idx += 1
                fig_coh.add_trace(go.Scatter(
                    name=f"{short} — {YEAR_LABEL[yr]}",
                    x=agg_c["cohort"],
                    y=agg_c["value"],
                    mode="lines+markers+text",
                    line=dict(color=color, width=2, dash=DASH_STYLES[yr]),
                    marker=dict(color=color, size=6, symbol="circle",
                                line=dict(color=BG_PLOT, width=1)),
                    text=labels,
                    textposition=tpos,
                    textfont=dict(size=10, color=color),
                    cliponaxis=False,
                    hovertemplate=(
                        f"<b>{short} · {YEAR_LABEL[yr]} Post-Grad</b><br>"
                        f"{PCT_LABELS[c_pct]}<br>"
                        "Cohort: %{x}<br><b>$%{y:,.0f}</b><extra></extra>"
                    ),
                ))

        c_major_str = " · ".join(CIP_SHORT[c] for c in sorted(c_cips))
        c_years_str = " / ".join(YEAR_LABEL[y] for y in sorted(c_years))
        c_title = (
            f"Cohort Earnings — {PCT_LABELS[c_pct]}  |  {c_major_str}  |  "
            f"{c_years_str} Post-Grad  |  {c_state}"
        )
        c_sub = (
            f"{PCT_LABELS[c_pct]} mean earnings by graduation cohort · "
            f"{c_state} · {c_years_str} post-graduation"
        )

        layout_c = base_layout(c_title, c_sub)
        layout_c["xaxis"]["title"] = dict(text="Graduation Cohort",
                                          font=dict(size=11, color="#555555"))
        layout_c["xaxis"]["tickangle"] = -40
        layout_c["xaxis"]["tickfont"]  = dict(size=9, color=TEXT_CLR)
        layout_c["yaxis"]["title"] = dict(text="Mean Annual Earnings (USD)",
                                          font=dict(size=11, color="#555555"))
        layout_c["legend"]["title"] = dict(text="Major — Post-Grad Year",
                                           font=dict(size=10, color="#555555"))
        layout_c["height"] = 750
        layout_c["margin"]["b"] = 90

        fig_coh.update_layout(**layout_c)
        st.plotly_chart(fig_coh, use_container_width=True, config=PLOTLY_CONFIG)

        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.markdown(f'<div class="meta-label">Rows in view</div>'
                        f'<div class="footer-val">{len(dff_c):,}</div>', unsafe_allow_html=True)
        with cm2:
            st.markdown(f'<div class="meta-label">States in view</div>'
                        f'<div class="footer-val">{dff_c["state_name"].nunique()}</div>', unsafe_allow_html=True)
        with cm3:
            st.markdown(f'<div class="meta-label">Cohorts in view</div>'
                        f'<div class="footer-val">{len(cohort_order)}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<hr class='section-break'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.68rem;color:#aaaaaa;text-align:center;margin:0'>"
        "Post-Secondary Employment Outcomes (PSEO) · U.S. Census Bureau · "
        "CIP 11 Computer Science · CIP 13 Education · CIP 51 Healthcare"
        "</p>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Employment Flows
# ══════════════════════════════════════════════════════════════════════════════
with tab_flows:

    _use_granular = df_flow_g is not None

    st.markdown(
        '<h2 class="chart-title">Employment Flows</h2>',
        unsafe_allow_html=True,
    )

    # ── View Mode toggle (only when granular data is available) ───────────────
    if _use_granular:
        st.markdown('<div class="f-label">View Mode</div>', unsafe_allow_html=True)
        _view_mode = st.radio(
            "view_mode",
            options=["Industry Only", "Geography Only", "Full Hierarchy (Both)"],
            index=2,
            label_visibility="collapsed",
            horizontal=True,
            key="view_mode",
        )
        s_mode = {"Industry Only": "industry", "Geography Only": "geography",
                  "Full Hierarchy (Both)": "full"}[_view_mode]
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    else:
        s_mode = "full"

    # ── Filters ───────────────────────────────────────────────────────────────
    sf1, sf2, sf3, sf4 = st.columns([2, 2, 2, 2])

    with sf1:
        st.markdown('<div class="f-label">Source State</div>', unsafe_allow_html=True)
        s_state = st.selectbox(
            "s_state",
            options=["All States"] + flow_states,
            index=0,
            label_visibility="collapsed",
            key="s_state",
        )

    with sf2:
        st.markdown('<div class="f-label">Majors</div>', unsafe_allow_html=True)
        s_majors = st.multiselect(
            "s_majors",
            options=["Computer Science", "Education", "Health Professions"],
            default=["Computer Science", "Education", "Health Professions"],
            label_visibility="collapsed",
            key="s_majors",
        )

    with sf3:
        st.markdown('<div class="f-label">Graduation Cohort</div>', unsafe_allow_html=True)
        s_cohort = st.selectbox(
            "s_cohort",
            options=["All Cohorts"] + flow_cohorts,
            index=len(flow_cohorts),
            label_visibility="collapsed",
            key="s_cohort",
        )

    with sf4:
        st.markdown('<div class="f-label">Time Milestone</div>', unsafe_allow_html=True)
        s_year_lbl = st.radio(
            "s_year",
            options=["1 Year", "5 Years", "10 Years"],
            index=1,
            label_visibility="collapsed",
            horizontal=True,
            key="s_year",
        )
        s_year = {"1 Year": 1, "5 Years": 5, "10 Years": 10}[s_year_lbl]

    # ── Select & filter data source ───────────────────────────────────────────
    dff_s = (df_flow_g if _use_granular else df_flow).copy()

    _collapsed_to_division = False
    if s_state != "All States":
        dff_s = dff_s[dff_s["state_name"] == s_state]
    elif _use_granular:
        dff_s["target_node"] = dff_s["division_label"]
        _collapsed_to_division = True
    if s_majors:
        dff_s = dff_s[dff_s["major_label"].isin(s_majors)]
    if s_cohort != "All Cohorts":
        dff_s = dff_s[dff_s["grad_cohort_label"] == s_cohort]

    # ── Render ────────────────────────────────────────────────────────────────
    if not s_majors:
        st.markdown(
            '<div class="warn-box">⚠&nbsp; At least one major must be chosen.</div>',
            unsafe_allow_html=True,
        )
    elif dff_s.empty:
        st.markdown(
            '<div class="warn-box">⚠&nbsp; No data available for the selected filters.</div>',
            unsafe_allow_html=True,
        )
    else:
        _count_col = FLOW_COUNT_COLS[s_year] if _use_granular else FLOW_EMP_COLS[s_year]
        if not dff_s[_count_col].notna().any():
            st.markdown(
                f'<div class="warn-box">⚠&nbsp; All employment counts are suppressed '
                f'for {s_year_lbl} post-graduation with the current filters.</div>',
                unsafe_allow_html=True,
            )
        else:
            maj_str  = " · ".join(s_majors)
            sk_title = (f"{s_year_lbl} Post-Grad  |  {maj_str}  |  "
                        f"{s_state}  |  Cohort: {s_cohort}")

            fig_sk = build_sankey(dff_s, s_year, sk_title, mode=s_mode)
            if fig_sk is None:
                st.markdown(
                    '<div class="warn-box">⚠&nbsp; Insufficient non-zero flow data '
                    'to render diagram.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.plotly_chart(fig_sk, use_container_width=True, config=PLOTLY_CONFIG)

            sm1, sm2, sm3, sm4 = st.columns(4)
            with sm1:
                st.markdown(f'<div class="meta-label">Rows in view</div>'
                            f'<div class="footer-val">{len(dff_s):,}</div>',
                            unsafe_allow_html=True)
            with sm2:
                st.markdown(f'<div class="meta-label">States in view</div>'
                            f'<div class="footer-val">{dff_s["state_name"].nunique()}</div>',
                            unsafe_allow_html=True)
            with sm3:
                st.markdown(f'<div class="meta-label">Industries</div>'
                            f'<div class="footer-val">{dff_s["industry_label"].nunique()}</div>',
                            unsafe_allow_html=True)
            with sm4:
                if _use_granular and not _collapsed_to_division:
                    _geo_label = "Target Nodes"
                    _geo_col   = "target_node"
                else:
                    _geo_label = "Census Divisions"
                    _geo_col   = "division_label"
                st.markdown(f'<div class="meta-label">{_geo_label}</div>'
                            f'<div class="footer-val">{dff_s[_geo_col].nunique()}</div>',
                            unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.68rem;color:#aaaaaa;text-align:center;margin:0'>"
        "Post-Secondary Employment Outcomes (PSEO) · U.S. Census Bureau · "
        "Agg Level 178 · CIP 11 Computer Science · CIP 13 Education · CIP 51 Healthcare"
        "</p>",
        unsafe_allow_html=True,
    )


with tab_reg:

    # ── Constants for this tab ────────────────────────────────────────────────
    REG_CIP_LABEL = {"11": "Computer Science", "13": "Education", "51": "Nursing"}
    REG_CIP_COLORS = {
        "Computer Science": "#0077b6",
        "Education":        "#d32f2f",
        "Nursing":          "#2e7d32",
    }
    BASELINE_COLOR = "#aaaaaa"
    REG_PCT_OPTIONS = {
        "p25 (Low-End)":   "p25",
        "p50 (Median)":    "p50",
        "p75 (Top-Tier)":  "p75",
    }
    REG_PCT_LABELS = {"p25": "25th Percentile", "p50": "50th Percentile", "p75": "75th Percentile"}

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        "<h2 style='font-size:1.6rem; font-weight:700; color:#1a1a1a; margin-bottom:0.2rem;'>"
        "The Career-Span Gap: Regression-Adjusted Premiums</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#555555; font-size:0.92rem; margin-top:0; margin-bottom:1.8rem;'>"
        "By controlling for geography and graduation cohort, we isolate the pure market "
        "value of each degree across a 10-year career horizon.</p>",
        unsafe_allow_html=True,
    )

    # ── Local filter ──────────────────────────────────────────────────────────
    filt_col, chart_col = st.columns([1, 5])

    with filt_col:
        st.markdown('<div class="f-label">Earnings Percentile</div>', unsafe_allow_html=True)
        reg_pct_lbl = st.selectbox(
            "reg_pct",
            options=list(REG_PCT_OPTIONS.keys()),
            index=1,   # default to Median
            label_visibility="collapsed",
            key="reg_pct",
        )
        reg_pct = REG_PCT_OPTIONS[reg_pct_lbl]

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # # ── Insight text ──────────────────────────────────────────────────────
        # st.markdown(
        #     "<div style='border-left:3px solid #00d4ff; padding-left:0.75rem; margin-bottom:1.2rem;'>"
        #     "<p style='font-size:0.82rem; color:#cccccc; font-weight:600; margin-bottom:0.3rem;'>"
        #     "The Scissors Effect</p>"
        #     "<p style='font-size:0.78rem; color:#999999; line-height:1.55;'>"
        #     "Observe how technical premiums (CS / Nursing) <b style='color:#e8e8e8;'>accelerate</b> "
        #     "with experience. In contrast, Education exhibits "
        #     "<b style='color:#ff4b4b;'>Compressed Returns</b> — where the market fails to reward "
        #     "10 years of experience with a significant wage increase.</p>"
        #     "</div>",
        #     unsafe_allow_html=True,
        # )
        # st.markdown(
        #     "<div style='border-left:3px solid #888; padding-left:0.75rem;'>"
        #     "<p style='font-size:0.82rem; color:#cccccc; font-weight:600; margin-bottom:0.3rem;'>"
        #     "Statistical Rigor</p>"
        #     "<p style='font-size:0.78rem; color:#999999; line-height:1.55;'>"
        #     "P-values for STEM premiums are consistently "
        #     "<b style='color:#00ff88;'>&lt; 0.001</b>, while the Education premium "
        #     "often fails to reach statistical significance "
        #     "(<span style='color:#ff4b4b;'>p &gt; 0.05</span>).</p>"
        #     "</div>",
        #     unsafe_allow_html=True,
        # )

    with chart_col:
        dff_reg = df_coef[df_coef["Percentile"] == reg_pct].copy()
        dff_reg["major"] = dff_reg["Major_Code"].astype(str).map(REG_CIP_LABEL)

        YEAR_SYMBOLS = {1: "circle", 5: "diamond", 10: "circle"}
        YEAR_SIZES   = {1: 12, 5: 10, 10: 18}
        major_order  = ["Education", "Nursing", "Computer Science"]

        fig_reg = go.Figure()

        for major_name in major_order:
            sub = dff_reg[dff_reg["major"] == major_name].sort_values("year_after")
            if sub.empty:
                continue
            color    = REG_CIP_COLORS[major_name]
            premiums = sub["Premium_USD"].tolist()
            years    = sub["year_after"].tolist()
            pvals    = sub["P_Value"].tolist()

            fig_reg.add_trace(go.Scatter(
                x=premiums,
                y=[major_name] * len(premiums),
                mode="lines",
                line=dict(color=color, width=6),
                showlegend=False,
                hoverinfo="skip",
            ))

            for i, yr in enumerate(years):
                prem, pval = premiums[i], pvals[i]
                sig = ("***" if pval < 0.001
                       else "**" if pval < 0.01
                       else "*" if pval < 0.05
                       else "n.s.")

                show_label = yr in (1, 10)
                text_val   = f"${prem:+,.0f}" if show_label else ""
                tpos       = "top center" if yr == 10 else "bottom center"

                marker_opacity = 1.0 if yr != 5 else 0.7

                fig_reg.add_trace(go.Scatter(
                    x=[prem],
                    y=[major_name],
                    mode="markers+text",
                    marker=dict(
                        color=color, size=YEAR_SIZES[yr],
                        symbol=YEAR_SYMBOLS[yr],
                        opacity=marker_opacity,
                        line=dict(color=BG_PLOT, width=2),
                    ),
                    text=[text_val],
                    textposition=tpos,
                    textfont=dict(size=13, color=color, family="IBM Plex Sans, Inter, sans-serif"),
                    cliponaxis=False,
                    showlegend=False,
                    hovertemplate=(
                        f"<b>{major_name}</b> | Year {yr}<br>"
                        f"Premium: <b>${prem:+,.0f}</b><br>"
                        f"p = {pval:.2e} ({sig})<br>"
                        f"{REG_PCT_LABELS[reg_pct]}"
                        f"<extra></extra>"
                    ),
                ))

        pct_title  = REG_PCT_LABELS[reg_pct]
        all_prems  = dff_reg["Premium_USD"].dropna().tolist() + [0]
        x_lo, x_hi = min(all_prems), max(all_prems)
        x_span     = x_hi - x_lo
        x_range    = [x_lo - x_span * 0.12, x_hi + x_span * 0.18]

        fig_reg.update_layout(
            plot_bgcolor=BG_PLOT,
            paper_bgcolor=BG_PAPER,
            font=dict(family="IBM Plex Sans, Inter, sans-serif", color=TEXT_CLR, size=16),
            title=dict(
                text=(
                    f"<b style='color:{TEXT_CLR}'>Wage Premium vs. Agriculture (CIP 01) — {pct_title}</b>"
                    f"<br><sup><span style='color:#777777'>OLS β · State & cohort FE · "
                    f"763 obs &nbsp;·&nbsp; ● Yr 1 &nbsp; ◆ Yr 5 &nbsp; ● Yr 10</span></sup>"
                ),
                font=dict(size=20, color=TEXT_CLR),
                x=0, xanchor="left", pad=dict(b=18),
            ),
            xaxis=dict(
                title=dict(text="Wage Premium over Agriculture (USD)",
                           font=dict(size=14, color="#555555")),
                tickformat="$+,.0f",
                tickfont=dict(size=14, color=TEXT_CLR),
                showgrid=True, gridcolor=GRID_CLR, gridwidth=1,
                showline=True, linecolor=LINE_CLR,
                ticks="outside", ticklen=5, tickcolor=AXIS_CLR,
                zeroline=True, zerolinecolor="#999999", zerolinewidth=1.5,
                range=x_range,
            ),
            yaxis=dict(
                tickfont=dict(size=16, color=TEXT_CLR),
                showgrid=False,
                showline=False,
                categoryorder="array",
                categoryarray=major_order,
            ),
            hoverlabel=dict(
                bgcolor="#ffffff", bordercolor="#cccccc",
                font=dict(color=TEXT_CLR, size=14),
            ),
            showlegend=False,
            margin=dict(l=180, r=60, t=110, b=80),
            height=420,
        )

        fig_reg.add_annotation(
            x=0, y=-0.5, xref="x", yref="y",
            text="▲ Agriculture baseline ($0)",
            showarrow=False,
            font=dict(size=10, color="#999999",
                      family="IBM Plex Sans, Inter, sans-serif"),
            xanchor="center", yanchor="top",
        )

        st.plotly_chart(fig_reg, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Footer meta row ───────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)

    rm1, rm2, rm3, rm4 = st.columns(4)
    with rm1:
        st.markdown(
            '<div class="meta-label">Model Type</div>'
            '<div class="footer-val">Multiple OLS Regression</div>',
            unsafe_allow_html=True,
        )
    with rm2:
        st.markdown(
            '<div class="meta-label">Controls</div>'
            '<div class="footer-val">State & Cohort Fixed Effects</div>',
            unsafe_allow_html=True,
        )
    with rm3:
        st.markdown(
            '<div class="meta-label">Data N</div>'
            '<div class="footer-val">763 Observations (Level 34)</div>',
            unsafe_allow_html=True,
        )
    with rm4:
        st.markdown(
            '<div class="meta-label">Baseline</div>'
            '<div class="footer-val">Agriculture (CIP 01)</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.68rem;color:#aaaaaa;text-align:center;margin:0'>"
        "Post-Secondary Employment Outcomes (PSEO) · U.S. Census Bureau · "
        "OLS coefficients with State & Cohort suppression · "
        "CIP 01 Agriculture (Baseline) · CIP 11 Computer Science · "
        "CIP 13 Education · CIP 51 Nursing"
        "</p>",
        unsafe_allow_html=True,
    )

    #git check
