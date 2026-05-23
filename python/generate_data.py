"""
Oura Health Intelligence Dashboard — Synthetic Data Generator
=============================================================
Generates realistic health tracking data for 6 tables:
  users, daily_scores, sleep_sessions, activity_sessions,
  hrv_metrics, app_engagement

Output: CSV files in ../data/raw/

Design decisions:
- 15 users, 90 days of history
- Users belong to 3 segments: Self-Optimizer, Health Coach, Casual User
- Scores are correlated (sleep affects readiness, HRV affects readiness)
- Each user has a personal baseline so data feels individual, not random
- Trends are embedded: HRV slightly improving, HR slightly decreasing over time
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

# ── Config ──────────────────────────────────────────────────────────────────

N_USERS      = 15
N_DAYS       = 90
END_DATE     = date(2026, 5, 21)
START_DATE   = END_DATE - timedelta(days=N_DAYS - 1)
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

os.makedirs(OUTPUT_DIR, exist_ok=True)

DATES = [START_DATE + timedelta(days=i) for i in range(N_DAYS)]

# ── User segments ────────────────────────────────────────────────────────────
# Each segment has a baseline that shapes all downstream metrics

SEGMENTS = {
    "Self-Optimizer": {
        "count": 6,
        "hrv_base": (62, 8),        # (mean, std)
        "rhr_base": (50, 4),
        "sleep_dur_base": (7.8, 0.5),
        "steps_base": (10500, 1500),
        "readiness_bonus": 5,
        "engagement_level": "high",
    },
    "Health Coach": {
        "count": 4,
        "hrv_base": (55, 7),
        "rhr_base": (54, 5),
        "sleep_dur_base": (7.2, 0.6),
        "steps_base": (8500, 2000),
        "readiness_bonus": 0,
        "engagement_level": "medium",
    },
    "Casual User": {
        "count": 5,
        "hrv_base": (45, 10),
        "rhr_base": (60, 6),
        "sleep_dur_base": (6.8, 0.8),
        "steps_base": (7000, 2500),
        "readiness_bonus": -5,
        "engagement_level": "low",
    },
}

DEVICE_MODELS = ["Oura Ring 3", "Oura Ring 4", "Oura Ring 4 Horizon"]
GENDERS       = ["female", "male", "non-binary"]
FEATURES      = [
    "Readiness Score", "Sleep Score", "Activity Ring",
    "HRV Chart", "Sleep Stages", "Trends", "Goals", "Notifications",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def score(val, lo=0, hi=100):
    return int(round(clamp(val, lo, hi)))

def clip_normal(mean, std, lo, hi):
    return clamp(np.random.normal(mean, std), lo, hi)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 1 — users
# ══════════════════════════════════════════════════════════════════════════════

def build_users():
    rows = []
    uid  = 1
    for seg_name, cfg in SEGMENTS.items():
        for _ in range(cfg["count"]):
            membership_start = START_DATE - timedelta(days=np.random.randint(30, 730))
            rows.append({
                "user_id":          uid,
                "segment":          seg_name,
                "age":              int(clip_normal(33, 8, 22, 55)),
                "gender":           np.random.choice(GENDERS, p=[0.55, 0.40, 0.05]),
                "device_model":     np.random.choice(DEVICE_MODELS, p=[0.2, 0.5, 0.3]),
                "membership_start": membership_start.isoformat(),
                "step_goal":        10000,
                "sleep_goal_hours": round(clip_normal(8.0, 0.3, 7.0, 9.0), 1),
            })
            uid += 1
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 2 — hrv_metrics  (generate first — other tables depend on it)
# ══════════════════════════════════════════════════════════════════════════════

def build_hrv_metrics(users_df):
    rows = []
    for _, user in users_df.iterrows():
        seg   = SEGMENTS[user["segment"]]
        hrv_m, hrv_s = seg["hrv_base"]
        rhr_m, rhr_s = seg["rhr_base"]

        # Personal baseline varies by individual
        personal_hrv_offset = np.random.normal(0, 4)
        personal_rhr_offset = np.random.normal(0, 2)

        for i, d in enumerate(DATES):
            # Gradual trend over 90 days: HRV +3ms, RHR -3bpm
            trend_factor = i / (N_DAYS - 1)
            hrv_trend    = trend_factor * 3
            rhr_trend    = -trend_factor * 3

            # Weekly cycle: HRV dips on Monday (weekend recovery disruption)
            weekly_dip   = -3 if d.weekday() == 0 else 0

            hrv  = clip_normal(hrv_m + personal_hrv_offset + hrv_trend + weekly_dip, hrv_s, 20, 120)
            rhr  = clip_normal(rhr_m + personal_rhr_offset + rhr_trend, rhr_s, 40, 90)
            temp = round(np.random.normal(0, 0.25), 2)   # deviation from baseline °C

            # Occasional "sick day" — spike in temp, drop in HRV
            if np.random.random() < 0.03:
                temp += round(np.random.uniform(0.4, 1.2), 2)
                hrv  *= 0.85

            rows.append({
                "user_id":          int(user["user_id"]),
                "date":             d.isoformat(),
                "hrv_ms":           round(hrv, 1),
                "resting_hr_bpm":   round(rhr, 1),
                "body_temp_dev_c":  temp,
            })
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 3 — sleep_sessions
# ══════════════════════════════════════════════════════════════════════════════

def build_sleep_sessions(users_df, hrv_df):
    rows = []
    sid = 1
    hrv_lookup = hrv_df.set_index(["user_id", "date"])

    for _, user in users_df.iterrows():
        seg = SEGMENTS[user["segment"]]
        dur_m, dur_s = seg["sleep_dur_base"]

        for d in DATES:
            hrv_row  = hrv_lookup.loc[(int(user["user_id"]), d.isoformat())]
            hrv_val  = hrv_row["hrv_ms"]
            temp_dev = hrv_row["body_temp_dev_c"]

            # Duration influenced by HRV (good recovery = better sleep)
            hrv_influence = (hrv_val - 50) * 0.02
            duration_h    = clip_normal(dur_m + hrv_influence, dur_s, 4.0, 10.0)

            # Sleep stages — proportions vary with sleep quality
            # More deep/REM when sleep is longer and HRV is good
            quality = clamp((hrv_val - 30) / 70, 0, 1)     # 0–1
            deep_pct  = clamp(np.random.normal(0.17 + quality * 0.08, 0.03), 0.10, 0.30)
            rem_pct   = clamp(np.random.normal(0.20 + quality * 0.07, 0.04), 0.12, 0.32)
            awake_pct = clamp(np.random.normal(0.06, 0.02), 0.02, 0.12)
            light_pct = 1 - deep_pct - rem_pct - awake_pct

            deep_h  = round(duration_h * deep_pct, 2)
            rem_h   = round(duration_h * rem_pct, 2)
            light_h = round(duration_h * light_pct, 2)
            awake_h = round(duration_h * awake_pct, 2)

            # Sleep timing (bedtime hour, 22–01)
            bedtime_hour = clip_normal(23.0, 0.8, 21.0, 26.0) % 24

            # Sleep score (0–100): driven by duration, deep%, REM%, HRV
            sleep_score = (
                  duration_h / user["sleep_goal_hours"] * 40   # 40 pts for duration
                + deep_pct   / 0.25 * 25                        # 25 pts for deep
                + rem_pct    / 0.25 * 20                        # 20 pts for REM
                + quality    * 15                               # 15 pts for HRV quality
                - (temp_dev  * 5)                               # penalise fever
            )

            rows.append({
                "session_id":       sid,
                "user_id":          int(user["user_id"]),
                "date":             d.isoformat(),
                "duration_h":       round(duration_h, 2),
                "deep_sleep_h":     deep_h,
                "rem_sleep_h":      rem_h,
                "light_sleep_h":    light_h,
                "awake_h":          awake_h,
                "bedtime_hour":     round(bedtime_hour, 1),
                "sleep_score":      score(sleep_score),
            })
            sid += 1
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 4 — activity_sessions
# ══════════════════════════════════════════════════════════════════════════════

def build_activity_sessions(users_df, hrv_df):
    rows = []
    aid = 1
    hrv_lookup = hrv_df.set_index(["user_id", "date"])

    ZONES = ["Sedentary", "Low", "Medium", "High"]

    for _, user in users_df.iterrows():
        seg = SEGMENTS[user["segment"]]
        steps_m, steps_s = seg["steps_base"]

        for d in DATES:
            hrv_val = hrv_lookup.loc[(int(user["user_id"]), d.isoformat())]["hrv_ms"]

            # Rest days: ~15% chance (fewer for Self-Optimizer)
            rest_prob = 0.05 if user["segment"] == "Self-Optimizer" else 0.18
            is_rest   = np.random.random() < rest_prob
            hrv_boost = (hrv_val - 50) * 10  # more steps when HRV is high

            steps    = int(clip_normal(steps_m + hrv_boost, steps_s, 500, 25000)) if not is_rest else int(clip_normal(2500, 500, 500, 4000))
            calories = int(steps * clip_normal(0.045, 0.005, 0.03, 0.06) + clip_normal(1500, 100, 1200, 1800))

            # Active minutes scales with steps
            active_min = int(clip_normal(steps / 130, 10, 0, 180))

            # Activity zone distribution (minutes in 1440-min day)
            if user["segment"] == "Self-Optimizer":
                zone_dist = [0.50, 0.20, 0.18, 0.12]
            elif user["segment"] == "Health Coach":
                zone_dist = [0.60, 0.22, 0.12, 0.06]
            else:
                zone_dist = [0.70, 0.18, 0.09, 0.03]

            zone_minutes = {z: int(1440 * p + np.random.normal(0, 10)) for z, p in zip(ZONES, zone_dist)}

            # Workout detection (separate row if workout happened)
            had_workout = steps > 9000 and np.random.random() < 0.6

            rows.append({
                "activity_id":          aid,
                "user_id":              int(user["user_id"]),
                "date":                 d.isoformat(),
                "steps":                steps,
                "calories_total":       calories,
                "active_minutes":       active_min,
                "goal_steps":           user["step_goal"],
                "goal_hit":             int(steps >= user["step_goal"]),
                "min_sedentary":        zone_minutes["Sedentary"],
                "min_low":              zone_minutes["Low"],
                "min_medium":           zone_minutes["Medium"],
                "min_high":             zone_minutes["High"],
                "workout_detected":     int(had_workout),
                "workout_type":         np.random.choice(["Run", "Strength", "Yoga", "Cycling", "Walk"], p=[0.3, 0.25, 0.15, 0.2, 0.1]) if had_workout else None,
                "workout_duration_min": int(clip_normal(45, 15, 20, 90)) if had_workout else None,
                "workout_calories":     int(clip_normal(350, 80, 150, 700)) if had_workout else None,
            })
            aid += 1
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 5 — daily_scores  (central fact table)
# ══════════════════════════════════════════════════════════════════════════════

def build_daily_scores(users_df, sleep_df, activity_df, hrv_df):
    rows = []
    sleep_lookup    = sleep_df.set_index(["user_id", "date"])
    activity_lookup = activity_df.set_index(["user_id", "date"])
    hrv_lookup      = hrv_df.set_index(["user_id", "date"])

    for _, user in users_df.iterrows():
        uid = int(user["user_id"])
        seg = SEGMENTS[user["segment"]]

        for d in DATES:
            d_str = d.isoformat()
            sl  = sleep_lookup.loc[(uid, d_str)]
            act = activity_lookup.loc[(uid, d_str)]
            hrv = hrv_lookup.loc[(uid, d_str)]

            sleep_score    = int(sl["sleep_score"])
            hrv_val        = hrv["hrv_ms"]
            steps          = int(act["steps"])
            goal_steps     = int(act["goal_steps"])

            # Activity score
            activity_score = score(
                  (steps / goal_steps) * 50
                + (act["min_medium"] + act["min_high"] * 1.5) / 6
                + act["goal_hit"] * 10
                + seg["readiness_bonus"]
                + np.random.normal(0, 3)
            )

            # HRV score (component of readiness)
            hrv_score = score((hrv_val - 30) / 90 * 100)

            # Readiness = weighted blend
            readiness_score = score(
                  sleep_score  * 0.35
                + hrv_score    * 0.35
                + activity_score * 0.20
                + seg["readiness_bonus"]
                + np.random.normal(0, 2)
            )

            # Individual readiness factors (for Page 1 chart)
            hrv_balance        = score(hrv_score + np.random.normal(0, 3))
            recovery_index     = score(sleep_score * 0.7 + hrv_score * 0.3 + np.random.normal(0, 3))
            sleep_balance      = score(sleep_score + np.random.normal(0, 3))
            activity_balance   = score(activity_score + np.random.normal(0, 3))
            body_temp_score    = score(100 - abs(hrv["body_temp_dev_c"]) * 40 + np.random.normal(0, 2))

            rows.append({
                "user_id":              uid,
                "date":                 d_str,
                "readiness_score":      readiness_score,
                "sleep_score":          sleep_score,
                "activity_score":       activity_score,
                "hrv_balance":          hrv_balance,
                "recovery_index":       recovery_index,
                "sleep_balance":        sleep_balance,
                "activity_balance":     activity_balance,
                "body_temp_score":      body_temp_score,
            })
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 6 — app_engagement
# ══════════════════════════════════════════════════════════════════════════════

ENGAGEMENT_PROFILE = {
    "high":   {"session_prob": 0.95, "features_per_session": (4, 2), "notif_ctr": 0.45},
    "medium": {"session_prob": 0.75, "features_per_session": (3, 1), "notif_ctr": 0.32},
    "low":    {"session_prob": 0.50, "features_per_session": (2, 1), "notif_ctr": 0.18},
}

FEATURE_WEIGHTS = {
    "Readiness Score": 0.95,
    "Sleep Score":     0.88,
    "Activity Ring":   0.80,
    "HRV Chart":       0.60,
    "Sleep Stages":    0.55,
    "Trends":          0.45,
    "Goals":           0.38,
    "Notifications":   0.25,
}

def build_app_engagement(users_df, daily_scores_df):
    rows = []
    eid  = 1
    scores_lookup = daily_scores_df.set_index(["user_id", "date"])

    for _, user in users_df.iterrows():
        uid     = int(user["user_id"])
        seg     = SEGMENTS[user["segment"]]
        profile = ENGAGEMENT_PROFILE[seg["engagement_level"]]

        for d in DATES:
            d_str = d.isoformat()

            # Did user open the app today?
            if np.random.random() > profile["session_prob"]:
                continue

            readiness = int(scores_lookup.loc[(uid, d_str)]["readiness_score"])

            # Session length influenced by readiness (curious when scores change)
            novelty_boost = 1 + abs(readiness - 75) / 100
            session_min   = round(clip_normal(
                profile["features_per_session"][0] * novelty_boost,
                profile["features_per_session"][1], 0.5, 20
            ), 1)

            # Which features were viewed (weighted random)
            n_features = max(1, int(clip_normal(profile["features_per_session"][0], profile["features_per_session"][1], 1, 8)))
            weights    = list(FEATURE_WEIGHTS.values())
            total_w    = sum(weights)
            probs      = [w / total_w for w in weights]
            viewed     = np.random.choice(FEATURES, size=min(n_features, len(FEATURES)), replace=False, p=probs).tolist()

            # Goal completion
            goal_completed = int(np.random.random() < (0.65 if seg["engagement_level"] == "high" else 0.45 if seg["engagement_level"] == "medium" else 0.28))

            # Notification interaction
            notif_sent     = int(np.random.random() < 0.8)
            notif_clicked  = int(notif_sent and np.random.random() < profile["notif_ctr"])

            for feature in viewed:
                rows.append({
                    "engagement_id":    eid,
                    "user_id":          uid,
                    "date":             d_str,
                    "session_min":      session_min,
                    "feature_viewed":   feature,
                    "goal_completed":   goal_completed,
                    "notif_sent":       notif_sent,
                    "notif_clicked":    notif_clicked,
                })
                eid += 1

    return pd.DataFrame(rows)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Generating synthetic Oura data...")
    print(f"  Users: {N_USERS} | Days: {N_DAYS} | Period: {START_DATE} to {END_DATE}")
    print()

    print("  [1/6] users...")
    users = build_users()
    users.to_csv(os.path.join(OUTPUT_DIR, "users.csv"), index=False)
    print(f"        {len(users)} rows")

    print("  [2/6] hrv_metrics...")
    hrv = build_hrv_metrics(users)
    hrv.to_csv(os.path.join(OUTPUT_DIR, "hrv_metrics.csv"), index=False)
    print(f"        {len(hrv)} rows")

    print("  [3/6] sleep_sessions...")
    sleep = build_sleep_sessions(users, hrv)
    sleep.to_csv(os.path.join(OUTPUT_DIR, "sleep_sessions.csv"), index=False)
    print(f"        {len(sleep)} rows")

    print("  [4/6] activity_sessions...")
    activity = build_activity_sessions(users, hrv)
    activity.to_csv(os.path.join(OUTPUT_DIR, "activity_sessions.csv"), index=False)
    print(f"        {len(activity)} rows")

    print("  [5/6] daily_scores...")
    scores = build_daily_scores(users, sleep, activity, hrv)
    scores.to_csv(os.path.join(OUTPUT_DIR, "daily_scores.csv"), index=False)
    print(f"        {len(scores)} rows")

    print("  [6/6] app_engagement...")
    engagement = build_app_engagement(users, scores)
    engagement.to_csv(os.path.join(OUTPUT_DIR, "app_engagement.csv"), index=False)
    print(f"        {len(engagement)} rows")

    print()
    print("Done! Files saved to data/raw/")
    print()

    # Quick validation
    print("--- Validation ---")
    print(f"  Readiness score range:  {scores['readiness_score'].min()}–{scores['readiness_score'].max()}")
    print(f"  Sleep score range:      {scores['sleep_score'].min()}–{scores['sleep_score'].max()}")
    print(f"  Activity score range:   {scores['activity_score'].min()}–{scores['activity_score'].max()}")
    print(f"  Avg HRV:                {hrv['hrv_ms'].mean():.1f} ms")
    print(f"  Avg resting HR:         {hrv['resting_hr_bpm'].mean():.1f} bpm")
    print(f"  Goal hit rate:          {activity['goal_hit'].mean()*100:.1f}%")
    print(f"  Avg daily steps:        {activity['steps'].mean():.0f}")
    print(f"  App sessions generated: {engagement['engagement_id'].max()}")
    print(f"  Null workout types:     {activity['workout_type'].isna().sum()} (expected ~{int(N_USERS*N_DAYS*0.4)})")


if __name__ == "__main__":
    main()
