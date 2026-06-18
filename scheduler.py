"""
Run this once — it schedules daily data fetch + model retrain at midnight.
Keep this running in background: python scheduler.py
"""
import schedule
import time
from datetime import datetime
from data_pipeline import run_pipeline
from ml_model import train_model, predict_tournament_winner


def daily_update():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Running daily update...")
    saved = run_pipeline()
    print(f"Fetched {saved} matches")
    model, df = train_model()
    if model:
        preds = predict_tournament_winner(model, df)
        top3 = sorted(preds.items(), key=lambda x: -x[1])[:3]
        print("Top 3 after update:", [(t, f"{p*100:.1f}%") for t,p in top3])
    print("Daily update complete.")


schedule.every().day.at("00:00").do(daily_update)

print("Scheduler started. Running first update now...")
daily_update()

print("Waiting for next scheduled run at midnight...")
while True:
    schedule.run_pending()
    time.sleep(60)
