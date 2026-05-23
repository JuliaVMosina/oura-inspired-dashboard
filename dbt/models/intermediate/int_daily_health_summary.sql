-- Intermediate: daily health summary
-- Joins scores + HRV + sleep + activity into one wide row per user per day.
-- This is the main building block for all health-related mart tables.

with scores as (
    select * from {{ ref('stg_daily_scores') }}
),

hrv as (
    select * from {{ ref('stg_hrv_metrics') }}
),

sleep as (
    select * from {{ ref('stg_sleep_sessions') }}
),

activity as (
    select * from {{ ref('stg_activity_sessions') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

joined as (

    select
        -- Keys
        s.user_id,
        s.score_date                            as date,
        u.segment,

        -- Daily scores
        s.readiness_score,
        s.sleep_score,
        s.activity_score,
        s.readiness_category,

        -- Readiness factors
        s.hrv_balance,
        s.recovery_index,
        s.sleep_balance,
        s.activity_balance,
        s.body_temp_score,

        -- HRV metrics
        h.hrv_ms,
        h.resting_hr_bpm,
        h.body_temp_dev_c,
        h.hrv_category,
        h.temp_status,

        -- Sleep
        sl.duration_h,
        sl.deep_sleep_h,
        sl.rem_sleep_h,
        sl.light_sleep_h,
        sl.awake_h,
        sl.deep_pct,
        sl.rem_pct,
        sl.bedtime_hour,
        sl.sleep_category,

        -- Activity
        a.steps,
        a.calories_total,
        a.active_minutes,
        a.goal_steps,
        a.goal_hit,
        a.steps_category,
        a.workout_detected,
        a.workout_type,
        a.workout_duration_min,
        a.workout_calories

    from scores s
    left join hrv      h  on s.user_id = h.user_id and s.score_date = h.metric_date
    left join sleep    sl on s.user_id = sl.user_id and s.score_date = sl.sleep_date
    left join activity a  on s.user_id = a.user_id and s.score_date = a.activity_date
    left join users    u  on s.user_id = u.user_id

)

select * from joined
