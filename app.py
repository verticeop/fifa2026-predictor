import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="FIFA 2026 Predictor",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
.big-title { font-size:2.2rem; font-weight:700; color:#1a1a2e; margin:0; }
.subtitle  { color:#666; font-size:1rem; margin-bottom:1.5rem; }
.winner-card {
    background: linear-gradient(135deg, #1a6b3c, #2d9e5e);
    color: white; border-radius:12px; padding:1.5rem;
    text-align:center; margin-bottom:1rem;
}
.winner-name { font-size:1.8rem; font-weight:700; margin:0; }
.winner-prob { font-size:1.1rem; opacity:0.9; margin:0.3rem 0 0; }
.updated-badge {
    background:#E1F5EE; color:#085041;
    padding:4px 12px; border-radius:20px;
    font-size:0.8rem; font-weight:600;
    display:inline-block; margin-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_predictions():
    from data_pipeline import load_predictions as _lp
    from ml_model import generate_demo_predictions as demo_preds
    try:
        df = _lp()
        if df.empty:
            preds = demo_preds()
            df = pd.DataFrame([
                {"team": t, "win_probability": p, "updated_at": datetime.utcnow().isoformat()}
                for t, p in preds.items()
            ])
        return df
    except:
        preds = demo_preds()
        return pd.DataFrame([
            {"team": t, "win_probability": p, "updated_at": datetime.utcnow().isoformat()}
            for t, p in preds.items()
        ])


def generate_demo_matches():
    """Generate realistic demo match data for display when no API key is set."""
    matches = [
        # 2022 World Cup Group Stage
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
        # Round of 16
        {"date":"2022-12-03","home_team":"Netherlands","away_team":"USA","home_score":3,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-03","home_team":"Argentina","away_team":"Australia","home_score":2,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-04","home_team":"France","away_team":"Poland","home_score":3,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-04","home_team":"England","away_team":"Senegal","home_score":3,"away_score":0,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-05","home_team":"Japan","away_team":"Croatia","home_score":1,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-05","home_team":"Brazil","away_team":"South Korea","home_score":4,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-06","home_team":"Morocco","away_team":"Spain","home_score":0,"away_score":0,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        {"date":"2022-12-06","home_team":"Portugal","away_team":"Switzerland","home_score":6,"away_score":1,"competition":"FIFA World Cup 2022","stage":"LAST_16"},
        # Quarter finals
        {"date":"2022-12-09","home_team":"Croatia","away_team":"Brazil","home_score":1,"away_score":1,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-09","home_team":"Netherlands","away_team":"Argentina","home_score":2,"away_score":2,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-10","home_team":"Morocco","away_team":"Portugal","home_score":1,"away_score":0,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        {"date":"2022-12-10","home_team":"England","away_team":"France","home_score":1,"away_score":2,"competition":"FIFA World Cup 2022","stage":"QUARTER_FINALS"},
        # Semi finals
        {"date":"2022-12-13","home_team":"Argentina","away_team":"Croatia","home_score":3,"away_score":0,"competition":"FIFA World Cup 2022","stage":"SEMI_FINALS"},
        {"date":"2022-12-14","home_team":"France","away_team":"Morocco","home_score":2,"away_score":0,"competition":"FIFA World Cup 2022","stage":"SEMI_FINALS"},
        # Final
        {"date":"2022-12-18","home_team":"Argentina","away_team":"France","home_score":3,"away_score":3,"competition":"FIFA World Cup 2022","stage":"FINAL"},
        # FIFA 2026 matches played so far
        {"date":"2026-06-11","home_team":"Mexico","away_team":"USA","home_score":0,"away_score":2,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-12","home_team":"Canada","away_team":"France","home_score":0,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-12","home_team":"Argentina","away_team":"Qatar","home_score":3,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-13","home_team":"Spain","away_team":"Brazil","home_score":1,"away_score":2,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-13","home_team":"England","away_team":"Serbia","home_score":2,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-14","home_team":"Germany","away_team":"Japan","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-14","home_team":"Portugal","away_team":"Morocco","home_score":2,"away_score":1,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-15","home_team":"Netherlands","away_team":"Senegal","home_score":3,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-15","home_team":"France","away_team":"Belgium","home_score":1,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
        {"date":"2026-06-16","home_team":"Brazil","away_team":"Croatia","home_score":2,"away_score":0,"competition":"FIFA World Cup 2026","stage":"GROUP_STAGE"},
    ]
    return pd.DataFrame(matches)


@st.cache_data(ttl=3600)
def load_matches():
    from data_pipeline import load_matches as _lm
    try:
        df = _lm()
        if df.empty:
            return generate_demo_matches()
        return df
    except:
        return generate_demo_matches()


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
    return flags.get(team, "")


with st.sidebar:
    st.markdown("### FIFA 2026 Predictor")
    st.markdown("---")
    page = st.radio("", ["Overview","Team search","Match history","About"], label_visibility="collapsed")

    st.markdown("---")

    if st.button("Refresh predictions", use_container_width=True):
        from data_pipeline import run_pipeline
        from ml_model import train_model, predict_tournament_winner
        with st.spinner("Fetching latest data..."):
            run_pipeline()
            model, df = train_model()
            if model:
                predict_tournament_winner(model, df)
            else:
                from ml_model import generate_demo_predictions
                generate_demo_predictions()
        st.cache_data.clear()
        st.success("Updated!")

    st.markdown("---")
    st.caption("Data: football-data.org")
    st.caption("Model: Random Forest + Monte Carlo simulation")
    st.caption("Updates: daily at midnight")


preds_df = load_predictions()
matches_df = load_matches()

if preds_df.empty:
    st.error("No predictions available. Click 'Refresh predictions' in the sidebar.")
    st.stop()

preds_df = preds_df.sort_values("win_probability", ascending=False).reset_index(drop=True)
preds_df["rank"] = preds_df.index + 1
preds_df["pct"] = (preds_df["win_probability"] * 100).round(1)
preds_df["flag"] = preds_df["team"].apply(get_flag)
preds_df["display"] = preds_df["flag"] + " " + preds_df["team"]


if page == "Overview":
    st.markdown('<p class="big-title">FIFA World Cup 2026 Predictor</p>', unsafe_allow_html=True)
    try:
        updated = preds_df["updated_at"].iloc[0][:16].replace("T"," ")
        st.markdown(f'<span class="updated-badge">Last updated: {updated} UTC</span>', unsafe_allow_html=True)
    except:
        pass

    top = preds_df.iloc[0]
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.markdown(f"""
        <div class="winner-card">
            <p style="font-size:2rem;margin:0">{top['flag']}</p>
            <p class="winner-name">{top['team']}</p>
            <p class="winner-prob">Predicted winner · {top['pct']}% chance</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        r2 = preds_df.iloc[1]
        st.metric(f"{r2['flag']} {r2['team']}", f"{r2['pct']}%", "2nd favourite")
    with c3:
        r3 = preds_df.iloc[2]
        st.metric(f"{r3['flag']} {r3['team']}", f"{r3['pct']}%", "3rd favourite")

    st.divider()

    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        st.subheader("Win probability — all 32 teams")
        top16 = preds_df.head(16)
        fig = px.bar(
            top16, x="pct", y="display",
            orientation="h",
            color="pct",
            color_continuous_scale=["#E6F1FB","#185FA5"],
            labels={"pct":"Win probability (%)","display":""},
            text="pct"
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(
            height=520, showlegend=False,
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
            margin=dict(l=0,r=40,t=10,b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("Full rankings")
        display_df = preds_df[["rank","display","pct"]].copy()
        display_df.columns = ["Rank","Team","Win %"]
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=520)

    st.divider()
    st.subheader("Probability distribution")
    fig2 = px.pie(
        preds_df.head(8),
        values="win_probability", names="display",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig2.update_layout(height=350, margin=dict(l=0,r=0,t=10,b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)


elif page == "Team search":
    st.markdown('<p class="big-title">Team search</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Search any team to see their winning chances and match record</p>',
                unsafe_allow_html=True)

    all_teams = sorted(preds_df["team"].tolist())
    selected = st.selectbox("Search for a team", all_teams, index=0)

    row = preds_df[preds_df["team"]==selected].iloc[0]
    flag = get_flag(selected)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Win probability", f"{row['pct']}%")
    c2.metric("World ranking", f"#{int(row['rank'])}")
    better_than = round((1 - row["rank"]/32) * 100)
    c3.metric("Better than", f"{better_than}% of teams")

    if not matches_df.empty:
        team_matches = matches_df[
            (matches_df["home_team"]==selected) | (matches_df["away_team"]==selected)
        ]
        c4.metric("Matches in DB", len(team_matches))
    else:
        c4.metric("Matches in DB", "0")

    st.divider()

    gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=float(row["pct"]),
        title={"text": f"{flag} {selected} — Win probability"},
        delta={"reference": 3.125, "valueformat": ".1f"},
        gauge={
            "axis": {"range": [0, 30]},
            "bar": {"color": "#185FA5"},
            "steps": [
                {"range": [0, 5],  "color": "#E6F1FB"},
                {"range": [5, 15], "color": "#B5D4F4"},
                {"range": [15,30], "color": "#85B7EB"},
            ],
            "threshold": {
                "line": {"color": "#E24B4A", "width": 3},
                "thickness": 0.75,
                "value": 3.125
            }
        }
    ))
    gauge.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(gauge, use_container_width=True)

    if not matches_df.empty:
        st.subheader(f"Recent matches — {selected}")
        team_matches = matches_df[
            (matches_df["home_team"]==selected) | (matches_df["away_team"]==selected)
        ].copy().tail(10)

        if not team_matches.empty:
            def result_label(row):
                if row["home_team"] == selected:
                    if row["home_score"] > row["away_score"]: return "Win"
                    if row["home_score"] == row["away_score"]: return "Draw"
                    return "Loss"
                else:
                    if row["away_score"] > row["home_score"]: return "Win"
                    if row["away_score"] == row["home_score"]: return "Draw"
                    return "Loss"

            team_matches["Result"] = team_matches.apply(result_label, axis=1)
            team_matches["Score"] = team_matches["home_score"].astype(str) + " - " + \
                                    team_matches["away_score"].astype(str)
            team_matches["Opponent"] = team_matches.apply(
                lambda r: r["away_team"] if r["home_team"]==selected else r["home_team"], axis=1
            )
            show = team_matches[["date","Opponent","Score","Result","competition"]].copy()
            show.columns = ["Date","Opponent","Score","Result","Competition"]

            def colour_result(val):
                if val=="Win":  return "background-color:#E1F5EE; color:#085041"
                if val=="Loss": return "background-color:#FCEBEB; color:#791F1F"
                return "background-color:#FAEEDA; color:#633806"

            st.dataframe(
                show.style.applymap(colour_result, subset=["Result"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No match history found for this team in the database yet.")


elif page == "Match history":
    st.markdown('<p class="big-title">Match history</p>', unsafe_allow_html=True)

    if matches_df.empty:
        st.info("No match data yet. Click 'Refresh predictions' in the sidebar to fetch data from the API.")
    else:
        c1, c2 = st.columns(2)
        all_teams = sorted(set(matches_df["home_team"].tolist() + matches_df["away_team"].tolist()))
        team_filter = c1.selectbox("Filter by team (optional)", ["All teams"] + all_teams)

        filtered = matches_df.copy()
        if team_filter != "All teams":
            filtered = filtered[
                (filtered["home_team"]==team_filter) | (filtered["away_team"]==team_filter)
            ]

        filtered["Score"] = filtered["home_score"].astype(str) + " - " + filtered["away_score"].astype(str)
        show = filtered[["date","home_team","Score","away_team","competition","stage"]].copy()
        show.columns = ["Date","Home","Score","Away","Competition","Stage"]
        st.dataframe(show.sort_values("Date", ascending=False),
                     use_container_width=True, hide_index=True, height=500)

        st.caption(f"Showing {len(filtered)} of {len(matches_df)} matches")


elif page == "About":
    st.markdown('<p class="big-title">How it works</p>', unsafe_allow_html=True)

    st.markdown("""
    ### Data source
    Live match data is fetched daily from [football-data.org](https://football-data.org) — a free API
    that provides real FIFA World Cup fixtures and results.

    ### ML model
    - **Algorithm:** Random Forest Classifier (200 trees)
    - **Features:** Team win rate (last 10 games), goals scored, goals conceded, win rate differential
    - **Training:** Every match in the database is used to train the model daily
    - **Prediction:** 5,000 Monte Carlo tournament simulations are run to estimate each team's winning probability

    ### How to get your free API key
    1. Go to [football-data.org](https://www.football-data.org/client/register)
    2. Register for a free account
    3. Copy your API token
    4. Set it as an environment variable: `FOOTBALL_API_KEY=your_token_here`
    5. On Streamlit Cloud: add it under Settings → Secrets as `FOOTBALL_API_KEY = "your_token"`

    ### Daily updates
    The scheduler (`scheduler.py`) runs automatically every day at midnight:
    1. Fetches latest match results from the API
    2. Retrains the Random Forest model on all available data
    3. Runs 5,000 new tournament simulations
    4. Updates the predictions database

    ### Project files
    ```
    fifa2026/
    ├── app.py            — Streamlit web app (this page)
    ├── data_pipeline.py  — API fetching + SQLite database
    ├── ml_model.py       — Feature engineering + Random Forest + Monte Carlo
    ├── scheduler.py      — Daily auto-update (run separately)
    └── requirements.txt  — All dependencies
    ```
    """)
