-- Mart: daily_scores
-- Power BI central fact table (star schema hub).
-- One row per user per day. All KPIs and factors for Pages 1–4.

select
    user_id,
    date,
    segment,

    -- Core scores
    readiness_score,
    sleep_score,
    activity_score,
    readiness_category,

    -- Readiness factors (Page 1 — horizontal bar chart)
    hrv_balance,
    recovery_index,
    sleep_balance,
    activity_balance,
    body_temp_score,

    -- HRV & physiology (Page 4)
    hrv_ms,
    resting_hr_bpm,
    body_temp_dev_c,
    hrv_category,
    temp_status,

    -- Sleep summary (Page 2)
    duration_h,
    deep_sleep_h,
    rem_sleep_h,
    light_sleep_h,
    awake_h,
    deep_pct,
    rem_pct,
    bedtime_hour,
    sleep_category,

    -- Activity summary (Page 3)
    steps,
    calories_total,
    active_minutes,
    goal_steps,
    goal_hit,
    steps_category,
    workout_detected,
    workout_type

from {{ ref('int_daily_health_summary') }}
