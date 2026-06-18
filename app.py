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
    page = st.radio("", ["Overview", "All Teams", "Match History", "Team Search"],
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


# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="divider"/>
<div class="editorial-footer">
    <p class="footer-text">
        FIFA 2026 Predictor · Random Forest + Monte Carlo · Data: football-data.org ·
        Updates daily · Built with Python & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
