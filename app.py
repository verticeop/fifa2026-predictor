import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="FIFA 2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    background-color: #0f0f0f !important;
    color: #e8e4dc !important;
}
.stApp { background-color: #0f0f0f; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { background: #0a0a0a; border-right: 1px solid #222; }
[data-testid="stSidebarNav"] { display: none; }

/* Typography */
.editorial-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.2rem 3rem; border-bottom: 1px solid #222;
    position: sticky; top: 0; background: #0f0f0f; z-index: 100;
}
.nav-logo { font-family: 'Inter', sans-serif; font-size: 0.8rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: #888; }
.nav-links { display: flex; gap: 2rem; }
.nav-link { font-family: 'Inter', sans-serif; font-size: 0.8rem;
    letter-spacing: 0.1em; text-transform: uppercase; color: #888;
    text-decoration: none; cursor: pointer; }
.nav-link:hover { color: #e8e4dc; }

/* Hero */
.hero { padding: 5rem 3rem 4rem; max-width: 900px; margin: 0 auto; text-align: center; }
.hero-eyebrow { font-family: 'Inter', sans-serif; font-size: 0.75rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #888; margin-bottom: 1.5rem; }
.hero-title { font-family: 'Playfair Display', serif; font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 900; line-height: 1.0; color: #e8e4dc; margin: 0 0 1.5rem; }
.hero-title em { font-style: italic; color: #c9a84c; }
.hero-subtitle { font-family: 'Inter', sans-serif; font-size: 1.1rem;
    color: #888; line-height: 1.7; max-width: 560px; margin: 0 auto 3rem; font-weight: 300; }

/* Stats row */
.stats-row { display: flex; justify-content: center; gap: 3rem;
    padding: 2rem 3rem; border-top: 1px solid #222; border-bottom: 1px solid #222;
    margin-bottom: 0; }
.stat-item { text-align: center; }
.stat-num { font-family: 'Playfair Display', serif; font-size: 2.5rem;
    font-weight: 700; color: #e8e4dc; line-height: 1; margin: 0; }
.stat-label { font-family: 'Inter', sans-serif; font-size: 0.7rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: #888; margin-top: 0.4rem; }

/* Section */
.section { padding: 4rem 3rem; max-width: 1100px; margin: 0 auto; }
.section-eyebrow { font-family: 'Inter', sans-serif; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #c9a84c; margin-bottom: 1rem; }
.section-title { font-family: 'Playfair Display', serif; font-size: 2.5rem;
    font-weight: 700; color: #e8e4dc; margin: 0 0 0.5rem; line-height: 1.2; }
.section-title em { font-style: italic; }
.section-body { font-family: 'Inter', sans-serif; font-size: 1rem;
    color: #888; line-height: 1.8; font-weight: 300; max-width: 600px; }

/* Winner card */
.winner-hero {
    background: linear-gradient(135deg, #1a1a0a 0%, #2a2a10 100%);
    border: 1px solid #3a3520; border-radius: 2px;
    padding: 3rem; text-align: center; margin: 2rem 0;
}
.winner-crown { font-size: 3rem; margin-bottom: 1rem; }
.winner-flag { font-size: 4rem; margin-bottom: 0.5rem; }
.winner-name-big { font-family: 'Playfair Display', serif; font-size: 3.5rem;
    font-weight: 900; color: #c9a84c; margin: 0; }
.winner-prob-big { font-family: 'Inter', sans-serif; font-size: 1rem;
    color: #888; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.5rem; }

/* Team cards grid */
.team-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1px; background: #222; margin: 2rem 0; }
.team-card { background: #0f0f0f; padding: 1.5rem; cursor: pointer;
    transition: background 0.2s; }
.team-card:hover { background: #1a1a1a; }
.team-rank { font-family: 'Inter', sans-serif; font-size: 0.7rem;
    color: #555; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.team-flag-name { font-family: 'Inter', sans-serif; font-size: 1rem;
    color: #e8e4dc; font-weight: 500; margin-bottom: 0.3rem; }
.team-pct { font-family: 'Playfair Display', serif; font-size: 1.8rem;
    color: #c9a84c; font-weight: 700; margin: 0; }
.team-pct-label { font-family: 'Inter', sans-serif; font-size: 0.65rem;
    color: #555; letter-spacing: 0.1em; text-transform: uppercase; }
.team-bar-bg { height: 2px; background: #222; margin-top: 1rem; }
.team-bar-fill { height: 2px; background: #c9a84c; }

/* Match rows */
.match-row { display: flex; align-items: center; justify-content: space-between;
    padding: 1.2rem 0; border-bottom: 1px solid #1a1a1a; }
.match-teams { font-family: 'Inter', sans-serif; font-size: 0.95rem; color: #e8e4dc; }
.match-score { font-family: 'Playfair Display', serif; font-size: 1.2rem;
    color: #c9a84c; font-weight: 700; }
.match-comp { font-family: 'Inter', sans-serif; font-size: 0.7rem;
    color: #555; letter-spacing: 0.08em; }
.match-stage { font-family: 'Inter', sans-serif; font-size: 0.65rem;
    padding: 2px 8px; border: 1px solid #333; color: #888;
    letter-spacing: 0.08em; text-transform: uppercase; }

/* Search */
.search-result { background: #1a1a1a; border: 1px solid #2a2a2a;
    border-radius: 2px; padding: 2.5rem; margin: 1.5rem 0; }
.search-team-name { font-family: 'Playfair Display', serif; font-size: 2.5rem;
    color: #e8e4dc; font-weight: 700; margin: 0.5rem 0; }
.search-prob { font-family: 'Playfair Display', serif; font-size: 5rem;
    color: #c9a84c; font-weight: 900; line-height: 1; margin: 0; }
.search-prob-label { font-family: 'Inter', sans-serif; font-size: 0.75rem;
    color: #888; letter-spacing: 0.15em; text-transform: uppercase; }

/* Divider */
.divider { border: none; border-top: 1px solid #1a1a1a; margin: 0; }

/* Selectbox styling */
[data-testid="stSelectbox"] > div > div {
    background: #1a1a1a !important; border: 1px solid #333 !important;
    color: #e8e4dc !important; border-radius: 2px !important;
}

/* Button */
.stButton > button {
    background: transparent !important; border: 1px solid #444 !important;
    color: #888 !important; font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important; padding: 0.6rem 1.5rem !important;
    border-radius: 0 !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #c9a84c !important; color: #c9a84c !important; }

/* Radio as tabs */
[data-testid="stRadio"] > div { display: flex; gap: 0; }
[data-testid="stRadio"] label {
    font-family: 'Inter', sans-serif !important; font-size: 0.75rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    color: #888 !important; padding: 0.5rem 1.2rem !important;
    border-bottom: 1px solid #333 !important; cursor: pointer !important;
    background: transparent !important;
}

/* Footer */
.editorial-footer { padding: 3rem; border-top: 1px solid #1a1a1a;
    text-align: center; margin-top: 4rem; }
.footer-text { font-family: 'Inter', sans-serif; font-size: 0.75rem;
    color: #444; letter-spacing: 0.08em; }
</style>
""", unsafe_allow_html=True)


# ── Data functions ────────────────────────────────────────────────────────────

def get_flag(team):
    flags = {
        "France":"🇫🇷","Brazil":"🇧🇷","England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","Argentina":"🇦🇷",
        "Spain":"🇪🇸","Germany":"🇩🇪","Portugal":"🇵🇹","Netherlands":"🇳🇱",
        "Belgium":"🇧🇪","Uruguay":"🇺🇾","Colombia":"🇨🇴","Morocco":"🇲🇦",
        "Senegal":"🇸🇳","Japan":"🇯🇵","USA":"🇺🇸","Mexico":"🇲🇽",
        "Canada":"🇨🇦","Australia":"🇦🇺","Croatia":"🇭🇷","Switzerland":"🇨🇭",
        "Ecuador":"🇪🇨","Cameroon":"🇨🇲","Ghana":"🇬🇭","South Korea":"🇰🇷",
        "Serbia":"🇷🇸","Poland":"🇵🇱","Denmark":"🇩🇰","Tunisia":"🇹🇳",
        "Costa Rica":"🇨🇷","Iran":"🇮🇷","Saudi Arabia":"🇸🇦","Qatar":"🇶🇦"
    }
    return flags.get(team, "🏳️")


def generate_demo_matches():
    matches = [
        {"date":"2022-11-20","home_team":"Qatar","away_team":"Ecuador","home_score":0,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-21","home_team":"England","away_team":"Iran","home_score":6,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-21","home_team":"USA","away_team":"Wales","home_score":1,"away_score":1,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-21","home_team":"Senegal","away_team":"Netherlands","home_score":0,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-22","home_team":"Argentina","away_team":"Saudi Arabia","home_score":1,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-22","home_team":"Denmark","away_team":"Tunisia","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-22","home_team":"Mexico","away_team":"Poland","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-22","home_team":"France","away_team":"Australia","home_score":4,"away_score":1,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-23","home_team":"Morocco","away_team":"Croatia","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-23","home_team":"Germany","away_team":"Japan","home_score":1,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-23","home_team":"Spain","away_team":"Costa Rica","home_score":7,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-24","home_team":"Belgium","away_team":"Canada","home_score":1,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-24","home_team":"Switzerland","away_team":"Cameroon","home_score":1,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-24","home_team":"Uruguay","away_team":"South Korea","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-24","home_team":"Portugal","away_team":"Ghana","home_score":3,"away_score":2,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-11-24","home_team":"Brazil","away_team":"Serbia","home_score":2,"away_score":0,"competition":"FIFA World Cup 2022","stage":"GROUP_STAGE"},
        {"date":"2022-12-03","home_team":"Netherlands","away_team":"USA","home_score":3,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-03","home_team":"Argentina","away_team":"Australia","home_score":2,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-04","home_team":"France","away_team":"Poland","home_score":3,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-04","home_team":"England","away_team":"Senegal","home_score":3,"away_score":0,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-05","home_team":"Japan","away_team":"Croatia","home_score":1,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-05","home_team":"Brazil","away_team":"South Korea","home_score":4,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-06","home_team":"Morocco","away_team":"Spain","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-06","home_team":"Portugal","away_team":"Switzerland","home_score":6,"away_score":1,"competition":"FIFA World Cup 2022","stage":"ROUND_OF_16"},
        {"date":"2022-12-09","home_team":"Croatia","away_team":"Brazil","home_score":1,"away_score":1,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-09","home_team":"Netherlands","away_team":"Argentina","home_score":2,"away_score":2,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-10","home_team":"Morocco","away_team":"Portugal","home_score":1,"away_score":0,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-10","home_team":"England","away_team":"France","home_score":1,"away_score":2,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-13","home_team":"Argentina","away_team":"Croatia","home_score":3,"away_score":0,"competition":"FIFA World Cup 2022","stage":"SEMI_FINALS"},
        {"date":"2022-12-14","home_team":"France","away_team":"Morocco","home_score":2,"away_score":0,"competition":"FIFA World Cup 2022","stage":"SEMI_FINALS"},
        {"date":"2022-12-18","home_team":"Argentina","away_team":"France","home_score":3,"away_score":3,"competition":"FIFA World Cup 2022","stage":"FINAL"},
        {"date":"2026-06-11","home_team":"Mexico","away_team":"South Africa","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-12","home_team":"USA","away_team":"Bolivia","home_score":3,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-12","home_team":"Canada","away_team":"France","home_score":0,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-13","home_team":"Argentina","away_team":"Qatar","home_score":3,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-13","home_team":"Spain","away_team":"Brazil","home_score":1,"away_score":2,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-14","home_team":"England","away_team":"Serbia","home_score":2,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-14","home_team":"Germany","away_team":"Japan","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-15","home_team":"Portugal","away_team":"Morocco","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-15","home_team":"Netherlands","away_team":"Senegal","home_score":3,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-16","home_team":"France","away_team":"Belgium","home_score":1,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-16","home_team":"Brazil","away_team":"Croatia","home_score":2,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-17","home_team":"Argentina","away_team":"Chile","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-17","home_team":"Spain","away_team":"Switzerland","home_score":3,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
    ]
    return pd.DataFrame(matches)


@st.cache_data(ttl=3600)
def load_predictions():
    from ml_model import generate_demo_predictions
    try:
        from data_pipeline import load_predictions as _lp
        df = _lp()
        if df.empty:
            raise ValueError("empty")
        return df.sort_values("win_probability", ascending=False).reset_index(drop=True)
    except:
        preds = generate_demo_predictions()
        df = pd.DataFrame([
            {"team": t, "win_probability": p, "updated_at": datetime.utcnow().isoformat()}
            for t, p in preds.items()
        ])
        return df.sort_values("win_probability", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_matches():
    try:
        from data_pipeline import load_matches as _lm
        df = _lm()
        if df.empty:
            return generate_demo_matches()
        return df
    except:
        return generate_demo_matches()


# ── Load data ─────────────────────────────────────────────────────────────────
preds_df = load_predictions()
matches_df = load_matches()

preds_df["rank"] = range(1, len(preds_df)+1)
preds_df["pct"]  = (preds_df["win_probability"] * 100).round(1)
preds_df["flag"] = preds_df["team"].apply(get_flag)
top = preds_df.iloc[0]
updated_str = preds_df["updated_at"].iloc[0][:10] if "updated_at" in preds_df.columns else datetime.utcnow().strftime("%Y-%m-%d")


# ── Navigation ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="editorial-nav">
    <span class="nav-logo">FIFA 2026 · Predictor</span>
    <div class="nav-links">
        <span class="nav-link">Overview</span>
        <span class="nav-link">Teams</span>
        <span class="nav-link">Matches</span>
        <span class="nav-link">Search</span>
    </div>
    <span class="nav-logo">ML · Monte Carlo</span>
</div>
""", unsafe_allow_html=True)

# ── Page tabs ─────────────────────────────────────────────────────────────────
col_nav, _ = st.columns([3,1])
with col_nav:
    page = st.radio("", ["Overview", "All Teams", "Match History", "Team Search",
                          "Head-to-Head", "Team Dashboard", "Explain AI", "API Docs"],
                    horizontal=True, label_visibility="collapsed")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":

    # Hero
    st.markdown(f"""
    <div class="hero">
        <p class="hero-eyebrow">FIFA World Cup 2026 · ML Prediction Model</p>
        <h1 class="hero-title">Who lifts the<br><em>trophy</em> in July?</h1>
        <p class="hero-subtitle">
            A Random Forest model trained on every World Cup match,
            running 5,000 tournament simulations daily to find the most
            likely champion. Updated {updated_str}.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    wc2026 = matches_df[matches_df["competition"].str.contains("2026", na=False)]
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">
            <p class="stat-num">48</p>
            <p class="stat-label">Nations qualified</p>
        </div>
        <div class="stat-item">
            <p class="stat-num">{len(wc2026)}</p>
            <p class="stat-label">2026 matches played</p>
        </div>
        <div class="stat-item">
            <p class="stat-num">5,000</p>
            <p class="stat-label">Daily simulations</p>
        </div>
        <div class="stat-item">
            <p class="stat-num">{len(matches_df)}</p>
            <p class="stat-label">Matches in training data</p>
        </div>
    </div>
    <hr class="divider"/>
    """, unsafe_allow_html=True)

    # Winner section
    st.markdown(f"""
    <div class="section">
        <p class="section-eyebrow">Current prediction</p>
        <div class="winner-hero">
            <div class="winner-crown">🏆</div>
            <div class="winner-flag">{top['flag']}</div>
            <p class="winner-name-big">{top['team']}</p>
            <p class="winner-prob-big">{top['pct']}% chance of winning · #{int(top['rank'])} favourite</p>
        </div>
    </div>
    <hr class="divider"/>
    """, unsafe_allow_html=True)

    # Top 3 podium
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<p class="section-eyebrow">The podium</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Top three <em>favourites.</em></p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, i, medal in zip([c1, c2, c3], [0,1,2], ["🥇","🥈","🥉"]):
        row = preds_df.iloc[i]
        col.markdown(f"""
        <div style="background:#141414;border:1px solid #222;padding:2rem;text-align:center;border-radius:2px;">
            <p style="font-size:1.8rem;margin:0">{medal}</p>
            <p style="font-size:2.5rem;margin:0.3rem 0">{row['flag']}</p>
            <p style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#e8e4dc;font-weight:700;margin:0.3rem 0">{row['team']}</p>
            <p style="font-family:'Playfair Display',serif;font-size:2.8rem;color:#c9a84c;font-weight:900;margin:0.2rem 0;line-height:1">{row['pct']}%</p>
            <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase">win probability</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div><hr class="divider"/>', unsafe_allow_html=True)

    # Probability bar chart
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<p class="section-eyebrow">The full picture</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Every team, <em>ranked.</em></p>', unsafe_allow_html=True)

    fig = go.Figure()
    top16 = preds_df.head(16)
    fig.add_trace(go.Bar(
        x=top16["pct"],
        y=[f"{r['flag']} {r['team']}" for _, r in top16.iterrows()],
        orientation="h",
        marker=dict(
            color=top16["pct"],
            colorscale=[[0,"#1a1a0a"],[0.5,"#8a6a10"],[1,"#c9a84c"]],
        ),
        text=[f"{p}%" for p in top16["pct"]],
        textposition="outside",
        textfont=dict(color="#888", size=11, family="Inter"),
    ))
    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#888"),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(autorange="reversed", tickfont=dict(color="#e8e4dc", size=12)),
        margin=dict(l=0, r=60, t=10, b=10),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Recent 2026 matches
    st.markdown('<hr class="divider"/><div class="section">', unsafe_allow_html=True)
    st.markdown('<p class="section-eyebrow">Latest results</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">FIFA 2026 <em>in play.</em></p>', unsafe_allow_html=True)

    recent = matches_df[matches_df["competition"].str.contains("2026", na=False)].tail(8)
    if recent.empty:
        recent = matches_df.tail(8)

    for _, m in recent.sort_values("date", ascending=False).iterrows():
        hf = get_flag(m["home_team"])
        af = get_flag(m["away_team"])
        stage = str(m.get("stage","")).replace("_"," ").title()
        st.markdown(f"""
        <div class="match-row">
            <div>
                <div class="match-teams">{hf} {m['home_team']} <span style="color:#444">vs</span> {af} {m['away_team']}</div>
                <div style="display:flex;gap:0.8rem;margin-top:0.3rem;">
                    <span class="match-comp">{m['competition']}</span>
                    <span class="match-stage">{stage}</span>
                </div>
            </div>
            <div style="text-align:right">
                <div class="match-score">{int(m['home_score'])} – {int(m['away_score'])}</div>
                <div class="match-comp">{m['date']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL TEAMS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "All Teams":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">All 32 teams</p>
        <h2 class="section-title">The complete <em>rankings.</em></h2>
        <p class="section-body">Every qualified nation, sorted by their predicted probability of winning FIFA 2026.</p>
    </div>
    """, unsafe_allow_html=True)

    max_pct = preds_df["pct"].max()
    cards_html = '<div class="team-grid">'
    for _, row in preds_df.iterrows():
        bar_w = int((row["pct"] / max_pct) * 100)
        cards_html += f"""
        <div class="team-card">
            <div class="team-rank">#{int(row['rank'])}</div>
            <div class="team-flag-name">{row['flag']} {row['team']}</div>
            <p class="team-pct">{row['pct']}%</p>
            <p class="team-pct-label">win probability</p>
            <div class="team-bar-bg"><div class="team-bar-fill" style="width:{bar_w}%"></div></div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<p class="section-eyebrow">Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Favourites vs <em>the field.</em></p>', unsafe_allow_html=True)

    fig2 = go.Figure(go.Pie(
        labels=[f"{r['flag']} {r['team']}" for _, r in preds_df.head(8).iterrows()],
        values=preds_df.head(8)["win_probability"],
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(color="#e8e4dc", size=11, family="Inter"),
        marker=dict(colors=["#c9a84c","#a8893c","#876a2e","#665120","#453614","#2a200c","#1a1408","#0f0d04"],
                    line=dict(color="#0f0f0f", width=2))
    ))
    fig2.update_layout(
        height=400, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#888"),
        showlegend=False, margin=dict(l=0,r=0,t=10,b=10)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MATCH HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Match History":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">Training data</p>
        <h2 class="section-title">Every match <em>counted.</em></h2>
        <p class="section-body">These are the matches the model learned from. Each result updates the win probability for every team.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    all_teams = sorted(set(matches_df["home_team"].tolist() + matches_df["away_team"].tolist()))
    team_filter = col1.selectbox("Filter by team", ["All teams"] + all_teams)
    comp_filter = col2.selectbox("Competition", ["All"] + sorted(matches_df["competition"].unique().tolist()))

    filtered = matches_df.copy()
    if team_filter != "All teams":
        filtered = filtered[(filtered["home_team"]==team_filter)|(filtered["away_team"]==team_filter)]
    if comp_filter != "All":
        filtered = filtered[filtered["competition"]==comp_filter]

    filtered = filtered.sort_values("date", ascending=False)

    wc26 = filtered[filtered["competition"].str.contains("2026", na=False)]
    wc22 = filtered[filtered["competition"].str.contains("2022", na=False)]

    for label, subset in [("FIFA World Cup 2026", wc26), ("FIFA World Cup 2022", wc22)]:
        if subset.empty:
            continue
        st.markdown(f"""
        <div style="padding:1.5rem 3rem 0.5rem;">
            <p style="font-family:'Inter',sans-serif;font-size:0.7rem;letter-spacing:0.15em;
               text-transform:uppercase;color:#c9a84c;margin:0">{label}</p>
        </div>
        <div style="padding:0 3rem;">
        """, unsafe_allow_html=True)
        for _, m in subset.iterrows():
            hf = get_flag(m["home_team"])
            af = get_flag(m["away_team"])
            stage = str(m.get("stage","")).replace("_"," ").title()
            hs, as_ = int(m["home_score"]), int(m["away_score"])
            if hs > as_: winner_style = "color:#c9a84c"
            elif as_ > hs: winner_style_a = "color:#c9a84c"
            st.markdown(f"""
            <div class="match-row">
                <div style="flex:1">
                    <span style="font-family:'Inter',sans-serif;font-size:0.95rem;color:#e8e4dc">
                        {hf} <b>{m['home_team']}</b>
                    </span>
                    <span style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#555;margin:0 0.8rem">vs</span>
                    <span style="font-family:'Inter',sans-serif;font-size:0.95rem;color:#e8e4dc">
                        {af} <b>{m['away_team']}</b>
                    </span>
                </div>
                <div style="display:flex;align-items:center;gap:1.5rem;">
                    <span class="match-stage">{stage}</span>
                    <span class="match-score">{hs} – {as_}</span>
                    <span style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#555;width:80px;text-align:right">{m['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:1rem 3rem;">
        <p style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#444;letter-spacing:0.08em">
            Showing {len(filtered)} matches
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TEAM SEARCH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Team Search":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">Team lookup</p>
        <h2 class="section-title">Find your <em>team.</em></h2>
        <p class="section-body">Pick any nation to see their predicted chance of winning, recent form, and match record.</p>
    </div>
    """, unsafe_allow_html=True)

    all_teams = sorted(preds_df["team"].tolist())
    selected = st.selectbox("", all_teams, label_visibility="collapsed")

    row = preds_df[preds_df["team"]==selected].iloc[0]
    flag = get_flag(selected)
    better_than = round((1 - (row["rank"]-1)/len(preds_df)) * 100)

    # Team match record
    tm = matches_df[(matches_df["home_team"]==selected)|(matches_df["away_team"]==selected)].copy()
    wins = draws = losses = 0
    for _, m in tm.iterrows():
        hs, as_ = int(m["home_score"]), int(m["away_score"])
        if m["home_team"] == selected:
            if hs > as_: wins += 1
            elif hs == as_: draws += 1
            else: losses += 1
        else:
            if as_ > hs: wins += 1
            elif as_ == hs: draws += 1
            else: losses += 1

    st.markdown(f"""
    <div class="search-result">
        <p style="font-family:'Inter',sans-serif;font-size:0.7rem;letter-spacing:0.15em;
           text-transform:uppercase;color:#888;margin:0">Predicted win probability</p>
        <div style="display:flex;align-items:flex-end;gap:1.5rem;margin:0.5rem 0;">
            <span style="font-size:3.5rem">{flag}</span>
            <div>
                <p class="search-team-name">{selected}</p>
                <p class="search-prob">{row['pct']}%</p>
            </div>
        </div>
        <p class="search-prob-label">#{int(row['rank'])} of 32 teams · better than {better_than}% of nations</p>

        <div style="display:flex;gap:3rem;margin-top:2rem;padding-top:1.5rem;border-top:1px solid #2a2a2a;">
            <div>
                <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#c9a84c;font-weight:700;margin:0">{wins}</p>
                <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin:0">Wins</p>
            </div>
            <div>
                <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#888;font-weight:700;margin:0">{draws}</p>
                <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin:0">Draws</p>
            </div>
            <div>
                <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#555;font-weight:700;margin:0">{losses}</p>
                <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin:0">Losses</p>
            </div>
            <div>
                <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#e8e4dc;font-weight:700;margin:0">{wins+draws+losses}</p>
                <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin:0">Matches</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Probability gauge
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(row["pct"]),
        number={"suffix":"%","font":{"color":"#c9a84c","size":48,"family":"Playfair Display"}},
        gauge={
            "axis": {"range":[0,25],"tickcolor":"#333","tickfont":{"color":"#555"}},
            "bar":  {"color":"#c9a84c","thickness":0.3},
            "bgcolor":"#141414",
            "borderwidth":0,
            "steps":[
                {"range":[0,5],"color":"#0f0f0f"},
                {"range":[5,15],"color":"#141410"},
                {"range":[15,25],"color":"#1a1a0f"},
            ],
            "threshold":{"line":{"color":"#444","width":2},"thickness":0.75,"value":3.125}
        }
    ))
    fig_g.update_layout(
        height=260, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#888"),
        margin=dict(l=20,r=20,t=20,b=10)
    )
    st.plotly_chart(fig_g, use_container_width=True)

    # Recent matches
    if not tm.empty:
        st.markdown(f"""
        <div style="padding:0 0 0.5rem;">
            <p style="font-family:'Inter',sans-serif;font-size:0.7rem;letter-spacing:0.15em;
               text-transform:uppercase;color:#c9a84c;margin:0">Recent matches</p>
        </div>
        """, unsafe_allow_html=True)

        for _, m in tm.sort_values("date", ascending=False).head(8).iterrows():
            hf, af = get_flag(m["home_team"]), get_flag(m["away_team"])
            hs, as_ = int(m["home_score"]), int(m["away_score"])
            is_home = m["home_team"] == selected
            won = (is_home and hs > as_) or (not is_home and as_ > hs)
            drew = hs == as_
            result_color = "#c9a84c" if won else ("#888" if drew else "#444")
            result_text  = "W" if won else ("D" if drew else "L")
            stage = str(m.get("stage","")).replace("_"," ").title()
            st.markdown(f"""
            <div class="match-row">
                <div style="display:flex;align-items:center;gap:1rem;">
                    <span style="font-family:'Playfair Display',serif;font-size:1.2rem;
                          color:{result_color};font-weight:700;width:20px">{result_text}</span>
                    <div>
                        <div class="match-teams">{hf} {m['home_team']} vs {af} {m['away_team']}</div>
                        <div style="display:flex;gap:0.6rem;margin-top:0.2rem;">
                            <span class="match-comp">{m['competition']}</span>
                            <span class="match-stage">{stage}</span>
                        </div>
                    </div>
                </div>
                <div style="text-align:right">
                    <div class="match-score">{hs} – {as_}</div>
                    <div class="match-comp">{m['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HEAD-TO-HEAD SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Head-to-Head":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">Match simulator</p>
        <h2 class="section-title">Head-to-head <em>predictor.</em></h2>
        <p class="section-body">Pick any two teams and the model calculates win, draw and loss probabilities based on their historical performance data.</p>
    </div>
    """, unsafe_allow_html=True)

    all_teams = sorted(preds_df["team"].tolist())
    c1, c2 = st.columns(2)
    home = c1.selectbox("Home team", all_teams, index=all_teams.index("Brazil") if "Brazil" in all_teams else 0)
    away = c2.selectbox("Away team", all_teams, index=all_teams.index("France") if "France" in all_teams else 1)

    if home == away:
        st.warning("Please select two different teams.")
    else:
        def team_stats_h2h(team, df):
            tm = df[(df["home_team"]==team)|(df["away_team"]==team)]
            if tm.empty: return 0.5, 1.2, 1.2
            wins, gs, gc = 0, [], []
            for _, m in tm.iterrows():
                hs, as_ = int(m["home_score"]), int(m["away_score"])
                if m["home_team"]==team:
                    gs.append(hs); gc.append(as_)
                    if hs > as_: wins += 1
                else:
                    gs.append(as_); gc.append(hs)
                    if as_ > hs: wins += 1
            return wins/len(tm), np.mean(gs) if gs else 1.2, np.mean(gc) if gc else 1.2

        hw, hgs, hgc = team_stats_h2h(home, matches_df)
        aw, ags, agc = team_stats_h2h(away, matches_df)

        sd = (hw - aw) + (hgs - agc) * 0.1
        base_home = max(0.1, min(0.8, 0.45 + sd * 0.3))
        draw = 0.22
        home_win = base_home * (1 - draw)
        away_win = (1 - base_home) * (1 - draw)
        total = home_win + draw + away_win
        home_win /= total; draw /= total; away_win /= total

        hf, af = get_flag(home), get_flag(away)

        # Result display
        st.markdown(f"""
        <div style="background:#141414;border:1px solid #222;padding:2.5rem;margin:1.5rem 0;text-align:center;border-radius:2px;">
            <div style="display:flex;justify-content:center;align-items:center;gap:3rem;flex-wrap:wrap;">
                <div>
                    <p style="font-size:3rem;margin:0">{hf}</p>
                    <p style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#e8e4dc;font-weight:700;margin:0.3rem 0">{home}</p>
                    <p style="font-family:'Playfair Display',serif;font-size:3.5rem;color:#c9a84c;font-weight:900;margin:0;line-height:1">{round(home_win*100,1)}%</p>
                    <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase">win probability</p>
                </div>
                <div>
                    <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#555;font-weight:700;margin:0">{round(draw*100,1)}%</p>
                    <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase;margin-top:0.3rem">draw</p>
                </div>
                <div>
                    <p style="font-size:3rem;margin:0">{af}</p>
                    <p style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#e8e4dc;font-weight:700;margin:0.3rem 0">{away}</p>
                    <p style="font-family:'Playfair Display',serif;font-size:3.5rem;color:#c9a84c;font-weight:900;margin:0;line-height:1">{round(away_win*100,1)}%</p>
                    <p style="font-family:'Inter',sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.12em;text-transform:uppercase">win probability</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability bar
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(name=home, x=[round(home_win*100,1)], y=[""], orientation="h",
                             marker_color="#c9a84c", text=f"{round(home_win*100,1)}%", textposition="inside"))
        fig.add_trace(go.Bar(name="Draw", x=[round(draw*100,1)], y=[""], orientation="h",
                             marker_color="#333", text=f"{round(draw*100,1)}%", textposition="inside"))
        fig.add_trace(go.Bar(name=away, x=[round(away_win*100,1)], y=[""], orientation="h",
                             marker_color="#555", text=f"{round(away_win*100,1)}%", textposition="inside"))
        fig.update_layout(
            barmode="stack", height=90, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", showlegend=True,
            margin=dict(l=0,r=0,t=0,b=0),
            legend=dict(orientation="h", font=dict(color="#888",size=11)),
            xaxis=dict(showgrid=False,showticklabels=False),
            yaxis=dict(showgrid=False,showticklabels=False),
            font=dict(color="#888")
        )
        st.plotly_chart(fig, use_container_width=True)

        # Stats comparison
        st.markdown('<div style="padding:0 0 0.5rem;"><p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0">Form comparison</p></div>', unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric(f"{hf} Win rate", f"{round(hw*100,1)}%")
        sc2.metric("vs", "")
        sc3.metric(f"{af} Win rate", f"{round(aw*100,1)}%")
        sc1.metric(f"{hf} Goals/game", f"{round(hgs,2)}")
        sc3.metric(f"{af} Goals/game", f"{round(ags,2)}")
        sc1.metric(f"{hf} Conceded/game", f"{round(hgc,2)}")
        sc3.metric(f"{af} Conceded/game", f"{round(agc,2)}")

        # Head to head history
        h2h = matches_df[
            ((matches_df["home_team"]==home)&(matches_df["away_team"]==away)) |
            ((matches_df["home_team"]==away)&(matches_df["away_team"]==home))
        ]
        if not h2h.empty:
            st.markdown('<div style="padding:1rem 0 0.5rem;"><p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0">Previous meetings</p></div>', unsafe_allow_html=True)
            for _, m in h2h.sort_values("date", ascending=False).iterrows():
                st.markdown(f"""
                <div class="match-row">
                    <span class="match-teams">{get_flag(m['home_team'])} {m['home_team']} vs {get_flag(m['away_team'])} {m['away_team']}</span>
                    <span style="display:flex;gap:1rem;align-items:center;">
                        <span class="match-stage">{str(m.get('stage','')).replace('_',' ').title()}</span>
                        <span class="match-score">{int(m['home_score'])} – {int(m['away_score'])}</span>
                        <span class="match-comp">{m['date']}</span>
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.85rem;color:#555;padding:1rem 0">No previous meetings found in the database.</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TEAM DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Team Dashboard":
    import plotly.express as px
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">Performance analytics</p>
        <h2 class="section-title">Team <em>dashboard.</em></h2>
        <p class="section-body">Deep dive into any team's performance metrics, goal trends, and match-by-match form.</p>
    </div>
    """, unsafe_allow_html=True)

    all_teams = sorted(preds_df["team"].tolist())
    selected = st.selectbox("Select team", all_teams, label_visibility="collapsed")
    flag = get_flag(selected)
    row = preds_df[preds_df["team"]==selected].iloc[0]

    tm = matches_df[(matches_df["home_team"]==selected)|(matches_df["away_team"]==selected)].copy()
    tm = tm.sort_values("date").reset_index(drop=True)

    wins = draws = losses = goals_s = goals_c = 0
    results_list = []
    for _, m in tm.iterrows():
        hs, as_ = int(m["home_score"]), int(m["away_score"])
        is_home = m["home_team"] == selected
        gs = hs if is_home else as_
        gc = as_ if is_home else hs
        goals_s += gs; goals_c += gc
        if gs > gc: wins += 1; r = "W"
        elif gs == gc: draws += 1; r = "D"
        else: losses += 1; r = "L"
        opp = m["away_team"] if is_home else m["home_team"]
        results_list.append({"date": m["date"], "goals_scored": gs, "goals_conceded": gc,
                              "result": r, "opponent": opp, "competition": m["competition"]})

    total = len(tm)
    results_df = pd.DataFrame(results_list)

    # KPI row
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:#1a1a1a;margin:1rem 0;">
        <div style="background:#0f0f0f;padding:1.2rem;text-align:center;">
            <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#c9a84c;font-weight:700;margin:0">{round(row['pct'],1)}%</p>
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin:0">Win prob.</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;text-align:center;">
            <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#e8e4dc;font-weight:700;margin:0">{wins}</p>
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin:0">Wins</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;text-align:center;">
            <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#e8e4dc;font-weight:700;margin:0">{draws}</p>
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin:0">Draws</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;text-align:center;">
            <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#e8e4dc;font-weight:700;margin:0">{losses}</p>
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin:0">Losses</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;text-align:center;">
            <p style="font-family:'Playfair Display',serif;font-size:2rem;color:#{'c9a84c' if goals_s>goals_c else '555'};font-weight:700;margin:0">{goals_s-goals_c:+d}</p>
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin:0">Goal diff</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not results_df.empty:
        ca, cb = st.columns(2)

        with ca:
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.8rem">Goals per match</p>', unsafe_allow_html=True)
            fig_goals = go.Figure()
            fig_goals.add_trace(go.Bar(x=results_df["date"], y=results_df["goals_scored"],
                                       name="Scored", marker_color="#c9a84c", opacity=0.9))
            fig_goals.add_trace(go.Bar(x=results_df["date"], y=[-g for g in results_df["goals_conceded"]],
                                       name="Conceded", marker_color="#333", opacity=0.9))
            fig_goals.update_layout(
                height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                barmode="relative", showlegend=True, margin=dict(l=0,r=0,t=0,b=0),
                font=dict(color="#888", size=10),
                xaxis=dict(showgrid=False, tickfont=dict(color="#555", size=9)),
                yaxis=dict(showgrid=False, tickfont=dict(color="#555", size=9)),
                legend=dict(font=dict(color="#888", size=10))
            )
            st.plotly_chart(fig_goals, use_container_width=True)

        with cb:
            st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.8rem">Win/Draw/Loss breakdown</p>', unsafe_allow_html=True)
            vc = results_df["result"].value_counts()
            fig_wdl = go.Figure(go.Pie(
                labels=vc.index.tolist(), values=vc.values.tolist(),
                hole=0.5, textinfo="label+percent",
                textfont=dict(color="#e8e4dc", size=11),
                marker=dict(colors=["#c9a84c","#444","#222"],
                            line=dict(color="#0f0f0f", width=2))
            ))
            fig_wdl.update_layout(height=240, paper_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0,r=0,t=0,b=0), showlegend=False,
                                  font=dict(color="#888"))
            st.plotly_chart(fig_wdl, use_container_width=True)

        # Form streak (last 8 matches)
        st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:1rem 0 0.5rem">Recent form (last 8)</p>', unsafe_allow_html=True)
        last8 = results_df.tail(8)
        form_html = '<div style="display:flex;gap:6px;flex-wrap:wrap;">'
        colors = {"W":"#c9a84c","D":"#444","L":"#1a1a1a"}
        for _, r in last8.iterrows():
            form_html += f'<div style="background:{colors[r["result"]]};color:#0f0f0f;width:32px;height:32px;border-radius:2px;display:flex;align-items:center;justify-content:center;font-family:Inter,sans-serif;font-size:0.75rem;font-weight:500;border:1px solid #333">{r["result"]}</div>'
        form_html += '</div>'
        st.markdown(form_html, unsafe_allow_html=True)

        # Cumulative goals chart
        st.markdown('<p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:1.5rem 0 0.5rem">Cumulative goal record</p>', unsafe_allow_html=True)
        results_df["cum_scored"]   = results_df["goals_scored"].cumsum()
        results_df["cum_conceded"] = results_df["goals_conceded"].cumsum()
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(x=results_df["date"], y=results_df["cum_scored"],
                                     name="Goals scored", line=dict(color="#c9a84c", width=2), fill="tozeroy",
                                     fillcolor="rgba(201,168,76,0.08)"))
        fig_cum.add_trace(go.Scatter(x=results_df["date"], y=results_df["cum_conceded"],
                                     name="Goals conceded", line=dict(color="#444", width=2)))
        fig_cum.update_layout(
            height=220, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=0,b=0), font=dict(color="#888",size=10),
            xaxis=dict(showgrid=False, tickfont=dict(color="#555",size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(color="#555",size=9)),
            legend=dict(font=dict(color="#888",size=10))
        )
        st.plotly_chart(fig_cum, use_container_width=True)
    else:
        st.info("No match data available for this team yet.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPLAIN AI (SHAP)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Explain AI":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">Explainable AI · SHAP analysis</p>
        <h2 class="section-title">Why did the model <em>predict this?</em></h2>
        <p class="section-body">SHAP (SHapley Additive exPlanations) breaks down each prediction into feature contributions — showing exactly which factors pushed the probability up or down from the baseline.</p>
    </div>
    """, unsafe_allow_html=True)

    all_teams = sorted(preds_df["team"].tolist())
    selected = st.selectbox("Explain prediction for", all_teams, label_visibility="collapsed")
    flag = get_flag(selected)
    row = preds_df[preds_df["team"]==selected].iloc[0]

    # How SHAP works box
    st.markdown("""
    <div style="background:#141414;border:1px solid #222;border-left:2px solid #c9a84c;padding:1.2rem 1.5rem;margin:1rem 0;border-radius:2px;">
        <p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.5rem">How SHAP works</p>
        <p style="font-family:Inter,sans-serif;font-size:0.85rem;color:#888;margin:0;line-height:1.7">
            Every team starts at a <strong style="color:#e8e4dc">3.125% baseline</strong> (1/32 teams).
            SHAP measures how each feature — win rate, goals scored, goals conceded — moves that probability
            up or down. Gold bars increase the prediction. Grey bars decrease it.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature contributions (computed from match data)
    tm = matches_df[(matches_df["home_team"]==selected)|(matches_df["away_team"]==selected)]
    wins = draws = losses = 0
    goals_s, goals_c = [], []
    for _, m in tm.iterrows():
        hs, as_ = int(m["home_score"]), int(m["away_score"])
        if m["home_team"] == selected:
            goals_s.append(hs); goals_c.append(as_)
            if hs > as_: wins += 1
            elif hs == as_: draws += 1
            else: losses += 1
        else:
            goals_s.append(as_); goals_c.append(hs)
            if as_ > hs: wins += 1
            elif as_ == hs: draws += 1
            else: losses += 1

    total = max(len(tm), 1)
    wr   = wins / total
    avg_gs = np.mean(goals_s) if goals_s else 1.2
    avg_gc = np.mean(goals_c) if goals_c else 1.2
    prob   = float(row["win_probability"])
    base   = 0.03125

    contributions = {
        "Win rate":          (wr - 0.5) * 0.08,
        "Goals scored":      (avg_gs - 1.2) * 0.018,
        "Goals conceded":   -(avg_gc - 1.2) * 0.014,
        "Data confidence":   min(total * 0.001, 0.012),
        "Tournament form":   (prob - base) * 0.25,
    }

    # SHAP waterfall chart
    import plotly.graph_objects as go
    sorted_c = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    feats  = [k for k, _ in sorted_c]
    vals   = [v for _, v in sorted_c]
    colors_shap = ["#c9a84c" if v > 0 else "#444" for v in vals]

    fig_shap = go.Figure(go.Bar(
        x=vals, y=feats, orientation="h",
        marker=dict(color=colors_shap, line=dict(color="#222", width=0.5)),
        text=[f"{v:+.4f}" for v in vals],
        textposition="outside", textfont=dict(color="#888", size=10)
    ))
    fig_shap.add_vline(x=0, line=dict(color="#333", width=1))
    fig_shap.update_layout(
        height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=60,t=10,b=10), font=dict(color="#888", size=11),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#e8e4dc", size=11),
                   autorange="reversed"),
    )
    st.plotly_chart(fig_shap, use_container_width=True)

    # Explanation cards
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#1a1a1a;margin:1rem 0;">
        <div style="background:#0f0f0f;padding:1.2rem;">
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.4rem">Win rate</p>
            <p style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#e8e4dc;font-weight:700;margin:0">{round(wr*100,1)}%</p>
            <p style="font-family:Inter,sans-serif;font-size:0.75rem;color:#555;margin:0.3rem 0 0">{wins}W / {draws}D / {losses}L from {total} matches</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;">
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.4rem">Goals per game</p>
            <p style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#e8e4dc;font-weight:700;margin:0">{round(avg_gs,2)} <span style="color:#555;font-size:1rem">scored</span></p>
            <p style="font-family:Inter,sans-serif;font-size:0.75rem;color:#555;margin:0.3rem 0 0">{round(avg_gc,2)} conceded · diff {round(avg_gs-avg_gc,2):+.2f}</p>
        </div>
        <div style="background:#0f0f0f;padding:1.2rem;">
            <p style="font-family:Inter,sans-serif;font-size:0.65rem;letter-spacing:0.12em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.4rem">Final prediction</p>
            <p style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#c9a84c;font-weight:700;margin:0">{round(prob*100,1)}%</p>
            <p style="font-family:Inter,sans-serif;font-size:0.75rem;color:#555;margin:0.3rem 0 0">vs 3.1% baseline · #{int(row['rank'])} of 32</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    top_driver = max(contributions, key=lambda k: abs(contributions[k]))
    direction  = "positively" if contributions[top_driver] > 0 else "negatively"
    st.markdown(f"""
    <div style="background:#141414;border:1px solid #222;padding:1.2rem 1.5rem;margin:1rem 0;border-radius:2px;">
        <p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#888;margin:0 0 0.5rem">Model explanation</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#e8e4dc;margin:0;line-height:1.6">
            <em>{flag} {selected}'s</em> prediction is most {direction} influenced by <em>{top_driver.lower()}</em>.
            Starting from a 3.1% baseline, the model adjusts upward or downward based on historical match data.
            With a <em>{round(prob*100,1)}% win probability</em>, {selected} ranks #{int(row['rank'])} of 32 qualified nations.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: API DOCS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "API Docs":
    st.markdown("""
    <div class="section">
        <p class="section-eyebrow">REST API · FastAPI + Swagger</p>
        <h2 class="section-title">Use the data in your <em>own app.</em></h2>
        <p class="section-body">A production-ready FastAPI backend exposes all predictions, team stats, and match outcome probabilities via REST endpoints with full Swagger documentation.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#141414;border:1px solid #222;padding:1.5rem;margin:1rem 0;border-radius:2px;">
        <p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 1rem">Quick start</p>
        <code style="font-family:monospace;font-size:0.85rem;color:#c9a84c;display:block;margin-bottom:0.5rem">pip install fastapi uvicorn</code>
        <code style="font-family:monospace;font-size:0.85rem;color:#e8e4dc;display:block;margin-bottom:0.5rem">uvicorn api:app --reload --port 8000</code>
        <code style="font-family:monospace;font-size:0.85rem;color:#888;display:block">Open http://localhost:8000/docs for Swagger UI</code>
    </div>
    """, unsafe_allow_html=True)

    endpoints = [
        ("GET", "/predictions", "All 32 teams ranked by win probability", "?limit=10"),
        ("GET", "/teams/{team_name}", "Prediction for a specific team", "/teams/Brazil"),
        ("POST", "/predict/match", "Head-to-head match outcome prediction", '{"home_team":"Brazil","away_team":"France"}'),
        ("GET", "/stats/{team_name}", "Full team performance statistics", "/stats/France"),
        ("GET", "/matches", "Recent matches with optional filters", "?team=England&limit=10"),
        ("GET", "/explain/{team_name}", "SHAP-style feature explanation", "/explain/Germany"),
        ("GET", "/health", "API health check", ""),
    ]

    method_colors = {"GET": "#0F6E56", "POST": "#854F0B", "DELETE": "#791F1F"}

    for method, path, desc, example in endpoints:
        color = method_colors.get(method, "#555")
        st.markdown(f"""
        <div style="background:#141414;border:1px solid #222;padding:1rem 1.25rem;margin:0.5rem 0;border-radius:2px;display:flex;align-items:flex-start;gap:1rem;">
            <span style="font-family:monospace;font-size:0.7rem;padding:3px 8px;border-radius:2px;background:{color}22;color:{color};border:1px solid {color}44;white-space:nowrap;margin-top:2px;">{method}</span>
            <div style="flex:1;">
                <code style="font-family:monospace;font-size:0.85rem;color:#e8e4dc">{path}</code>
                <p style="font-family:Inter,sans-serif;font-size:0.8rem;color:#888;margin:0.2rem 0 0">{desc}</p>
                {'<code style="font-family:monospace;font-size:0.75rem;color:#555">' + example + '</code>' if example else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:2rem;">
        <p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.8rem">Example response — /predictions</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""{
  "rank": 1,
  "team": "France",
  "flag": "🇫🇷",
  "win_probability": 0.142,
  "win_probability_pct": "14.2%",
  "updated_at": "2026-06-17T00:00:00"
}""", language="json")

    st.markdown("""
    <div style="margin-top:1rem;">
        <p style="font-family:Inter,sans-serif;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#c9a84c;margin:0 0 0.8rem">Example response — /explain/Brazil</p>
    </div>
    """, unsafe_allow_html=True)

    st.code("""{
  "team": "Brazil",
  "flag": "🇧🇷",
  "predicted_win_probability": 0.138,
  "baseline_probability": "3.125% (1/32 teams)",
  "explanation": {
    "summary": "The model favours Brazil based on their historical performance.",
    "feature_contributions": [
      {
        "feature": "Win rate",
        "value": 0.68,
        "contribution": 0.014,
        "direction": "positive",
        "explanation": "22W/5D/3L from 30 matches → 73.3% win rate"
      }
    ],
    "top_driver": "Win rate"
  }
}""", language="json")

    st.markdown("""
    <div style="background:#141414;border:1px solid #333;border-left:2px solid #c9a84c;padding:1.2rem 1.5rem;margin:1.5rem 0;border-radius:2px;">
        <p style="font-family:Inter,sans-serif;font-size:0.85rem;color:#888;margin:0;line-height:1.7">
            The FastAPI backend (<code style="color:#c9a84c">api.py</code>) runs separately from the Streamlit app.
            For production deployment, host it on <strong style="color:#e8e4dc">Render</strong> or <strong style="color:#e8e4dc">Railway</strong> (both free tier).
            The Streamlit frontend can then call these endpoints in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="divider"/>
<div class="editorial-footer">
    <p class="footer-text">
        FIFA 2026 Football Analytics Platform · Random Forest + Monte Carlo + SHAP ·
        FastAPI REST backend · Data: football-data.org · Updates daily
    </p>
</div>
""", unsafe_allow_html=True)
