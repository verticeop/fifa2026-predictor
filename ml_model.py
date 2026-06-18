import pandas as pd
import numpy as np
import sqlite3
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from data_pipeline import load_matches, save_predictions, FIFA2026_TEAMS

MODEL_PATH = "fifa_model.pkl"
ENC_PATH   = "team_encoder.pkl"


def build_features(df):
    """Engineer features from raw match data."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    rows = []
    for _, row in df.iterrows():
        ht, at = row["home_team"], row["away_team"]
        hs, as_ = int(row["home_score"]), int(row["away_score"])

        home_history = df[(df["date"] < row["date"]) &
                          ((df["home_team"]==ht)|(df["away_team"]==ht))].tail(10)
        away_history = df[(df["date"] < row["date"]) &
                          ((df["home_team"]==at)|(df["away_team"]==at))].tail(10)

        def team_stats(hist, team):
            if hist.empty:
                return 0.5, 0.0, 0.0
            wins = ((hist["home_team"]==team) & (hist["home_score"]>hist["away_score"])) | \
                   ((hist["away_team"]==team) & (hist["away_score"]>hist["home_score"]))
            goals_scored = np.where(hist["home_team"]==team,
                                    hist["home_score"], hist["away_score"]).mean()
            goals_conceded = np.where(hist["home_team"]==team,
                                      hist["away_score"], hist["home_score"]).mean()
            return wins.mean(), goals_scored, goals_conceded

        hw, hgs, hgc = team_stats(home_history, ht)
        aw, ags, agc = team_stats(away_history, at)

        if hs > as_:   result = 2
        elif hs == as_: result = 1
        else:          result = 0

        rows.append({
            "home_win_rate":    hw,
            "home_goals_scored":hgs,
            "home_goals_conceded":hgc,
            "away_win_rate":    aw,
            "away_goals_scored":ags,
            "away_goals_conceded":agc,
            "win_rate_diff":    hw - aw,
            "goals_diff":       hgs - agc,
            "result":           result,
            "home_team":        ht,
            "away_team":        at,
        })
    return pd.DataFrame(rows)


def train_model():
    df = load_matches()
    if df.empty or len(df) < 10:
        print("Not enough match data to train. Run data_pipeline.py first.")
        return None, None

    print(f"Training on {len(df)} matches...")
    features_df = build_features(df)

    FEATURES = ["home_win_rate","home_goals_scored","home_goals_conceded",
                "away_win_rate","away_goals_scored","away_goals_conceded",
                "win_rate_diff","goals_diff"]

    X = features_df[FEATURES].fillna(0.5)
    y = features_df["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(y)>10 else None
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model accuracy: {acc:.3f}")
    print(classification_report(y_test, model.predict(X_test),
                                 target_names=["Away win","Draw","Home win"]))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return model, features_df


def predict_tournament_winner(model=None, df=None):
    """Monte Carlo simulation: simulate the tournament 10,000 times."""
    if model is None:
        if not os.path.exists(MODEL_PATH):
            print("No model found. Training first...")
            model, df = train_model()
        else:
            model = joblib.load(MODEL_PATH)

    match_data = load_matches()
    if match_data.empty:
        return generate_demo_predictions()

    features_df = build_features(match_data)

    def predict_match(home, away, features_df, model):
        """Predict win probabilities for a single match."""
        FEATURES = ["home_win_rate","home_goals_scored","home_goals_conceded",
                    "away_win_rate","away_goals_scored","away_goals_conceded",
                    "win_rate_diff","goals_diff"]

        def get_team_stats(team):
            h = features_df[features_df["home_team"]==team]["home_win_rate"].mean()
            hgs = features_df[features_df["home_team"]==team]["home_goals_scored"].mean()
            hgc = features_df[features_df["home_team"]==team]["home_goals_conceded"].mean()
            if np.isnan(h): h, hgs, hgc = 0.5, 1.2, 1.2
            return h, hgs, hgc

        hw, hgs, hgc = get_team_stats(home)
        aw, ags, agc = get_team_stats(away)

        X = pd.DataFrame([{
            "home_win_rate": hw, "home_goals_scored": hgs, "home_goals_conceded": hgc,
            "away_win_rate": aw, "away_goals_scored": ags, "away_goals_conceded": agc,
            "win_rate_diff": hw - aw, "goals_diff": hgs - agc
        }])
        probs = model.predict_proba(X[FEATURES].fillna(0.5))[0]
        classes = model.classes_
        p_home = probs[list(classes).index(2)] if 2 in classes else 0.4
        p_draw = probs[list(classes).index(1)] if 1 in classes else 0.2
        p_away = probs[list(classes).index(0)] if 0 in classes else 0.4
        total = p_home + p_draw + p_away
        return p_home/total, p_draw/total, p_away/total

    N_SIMS = 5000
    win_counts = {team: 0 for team in FIFA2026_TEAMS}

    for _ in range(N_SIMS):
        remaining = FIFA2026_TEAMS.copy()
        np.random.shuffle(remaining)

        while len(remaining) > 1:
            next_round = []
            for i in range(0, len(remaining)-1, 2):
                home, away = remaining[i], remaining[i+1]
                ph, pd_, pa = predict_match(home, away, features_df, model)
                r = np.random.random()
                if r < ph:
                    winner = home
                elif r < ph + pd_:
                    winner = home if np.random.random() > 0.5 else away
                else:
                    winner = away
                next_round.append(winner)
            if len(remaining) % 2 == 1:
                next_round.append(remaining[-1])
            remaining = next_round

        if remaining:
            win_counts[remaining[0]] += 1

    total_sims = sum(win_counts.values())
    predictions = {team: count/total_sims for team, count in win_counts.items()}
    save_predictions(predictions)
    return predictions


def generate_demo_predictions():
    """Fallback demo predictions based on FIFA rankings when no API data available."""
    demo = {
        "France": 0.142, "Brazil": 0.138, "England": 0.118,
        "Argentina": 0.112, "Spain": 0.098, "Germany": 0.087,
        "Portugal": 0.062, "Netherlands": 0.048, "Belgium": 0.031,
        "Uruguay": 0.022, "Colombia": 0.019, "Morocco": 0.018,
        "Senegal": 0.012, "Japan": 0.011, "USA": 0.010,
        "Mexico": 0.008, "Canada": 0.007, "Australia": 0.006,
        "Croatia": 0.005, "Switzerland": 0.005, "Ecuador": 0.004,
        "Cameroon": 0.004, "Ghana": 0.003, "South Korea": 0.003,
        "Serbia": 0.003, "Poland": 0.002, "Denmark": 0.003,
        "Tunisia": 0.002, "Costa Rica": 0.002, "Iran": 0.002,
        "Saudi Arabia": 0.001, "Qatar": 0.001,
    }
    save_predictions(demo)
    return demo


if __name__ == "__main__":
    model, df = train_model()
    if model:
        preds = predict_tournament_winner(model, df)
        print("\nTop 10 predicted winners:")
        for team, prob in sorted(preds.items(), key=lambda x: -x[1])[:10]:
            print(f"  {team}: {prob*100:.1f}%")
