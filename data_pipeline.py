import requests
import pandas as pd
import sqlite3
import os
from datetime import datetime

API_KEY = os.getenv("de92bbbc41bc4306913ec31e152a2814", "YOUR_FREE_API_KEY_HERE")
BASE_URL = "https://api.football-data.org/v4"
HEADERS  = {"X-Auth-Token": API_KEY}
DB_PATH  = "fifa2026.db"

FIFA2026_TEAMS = [
    "Brazil","France","England","Argentina","Spain","Germany",
    "Portugal","Netherlands","Belgium","Uruguay","Colombia","Morocco",
    "Senegal","Japan","USA","Mexico","Canada","Australia",
    "Croatia","Switzerland","Ecuador","Cameroon","Ghana","South Korea",
    "Serbia","Poland","Denmark","Tunisia","Costa Rica","Iran",
    "Saudi Arabia","Qatar"
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            date TEXT, home_team TEXT, away_team TEXT,
            home_score INTEGER, away_score INTEGER,
            competition TEXT, stage TEXT, fetched_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT, win_probability REAL,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def fetch_world_cup_matches():
    """Fetch FIFA World Cup 2026 matches from football-data.org (competition id=2000)."""
    try:
        r = requests.get(f"{BASE_URL}/competitions/WC/matches", headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"API error {r.status_code}: {r.text[:200]}")
            return []
        matches = r.json().get("matches", [])
        rows = []
        for m in matches:
            hs = m.get("score", {}).get("fullTime", {}).get("home")
            as_ = m.get("score", {}).get("fullTime", {}).get("away")
            rows.append({
                "id":         m["id"],
                "date":       m["utcDate"][:10],
                "home_team":  m["homeTeam"]["name"],
                "away_team":  m["awayTeam"]["name"],
                "home_score": hs,
                "away_score": as_,
                "competition":"FIFA World Cup 2026",
                "stage":      m.get("stage",""),
                "fetched_at": datetime.utcnow().isoformat()
            })
        return rows
    except Exception as e:
        print(f"Fetch error: {e}")
        return []


def fetch_historical_matches():
    """Fetch recent international matches for all WC teams to build training data."""
    all_rows = []
    competitions = ["WC","EC","CA","PD","FL1","BL1","SA","PPL"]
    try:
        r = requests.get(
            f"{BASE_URL}/competitions/WC/matches?season=2022",
            headers=HEADERS, timeout=10
        )
        if r.status_code == 200:
            for m in r.json().get("matches", []):
                hs = m.get("score",{}).get("fullTime",{}).get("home")
                as_ = m.get("score",{}).get("fullTime",{}).get("away")
                if hs is None:
                    continue
                all_rows.append({
                    "id":         m["id"],
                    "date":       m["utcDate"][:10],
                    "home_team":  m["homeTeam"]["name"],
                    "away_team":  m["awayTeam"]["name"],
                    "home_score": hs,
                    "away_score": as_,
                    "competition":"FIFA World Cup 2022",
                    "stage":      m.get("stage",""),
                    "fetched_at": datetime.utcnow().isoformat()
                })
    except Exception as e:
        print(f"Historical fetch error: {e}")
    return all_rows


def save_matches(rows):
    if not rows:
        return 0
    conn = sqlite3.connect(DB_PATH)
    df = pd.DataFrame(rows)
    df.to_sql("matches", conn, if_exists="replace", index=False)
    conn.close()
    return len(rows)


def load_matches():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM matches WHERE home_score IS NOT NULL", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df


def save_predictions(pred_dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM predictions")
    now = datetime.utcnow().isoformat()
    for team, prob in pred_dict.items():
        c.execute("INSERT INTO predictions (team, win_probability, updated_at) VALUES (?,?,?)",
                  (team, round(prob, 4), now))
    conn.commit()
    conn.close()


def load_predictions():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM predictions ORDER BY win_probability DESC", conn)
    except:
        df = pd.DataFrame(columns=["team","win_probability","updated_at"])
    conn.close()
    return df


def run_pipeline():
    print("Initialising database...")
    init_db()
    print("Fetching historical matches (2022 WC)...")
    hist = fetch_historical_matches()
    print(f"Fetching 2026 matches...")
    live = fetch_world_cup_matches()
    all_matches = hist + live
    saved = save_matches(all_matches)
    print(f"Saved {saved} matches to DB")
    return saved


if __name__ == "__main__":
    run_pipeline()
