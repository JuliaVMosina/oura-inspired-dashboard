-- Mart: engagement_analytics
-- Powers Page 5 — Engagement Analytics.
-- Three aggregation levels: daily DAU, feature usage, segment breakdown.

with daily as (
    select * from {{ ref('int_user_engagement_summary') }}
),

feature_raw as (
    select * from {{ ref('stg_app_engagement') }}
),

users as (
    select user_id, segment from {{ ref('stg_users') }}
),

-- DAU by date
dau_by_date as (

    select
        date,
        sum(is_dau)                                     as dau,
        round(avg(session_min), 1)                      as avg_session_min,
        round(avg(cast(goal_completed as integer)) * 100, 1) as goal_completion_pct,
        sum(notif_sent)                                 as notif_sent,
        sum(notif_clicked)                              as notif_clicked,
        round(
            sum(notif_clicked) * 1.0 / nullif(sum(notif_sent), 0) * 100, 1
        )                                               as notif_ctr_pct

    from daily
    group by date

),

-- Feature usage counts (all time, for ranking)
feature_usage as (

    select
        feature_viewed,
        count(*)                                        as view_count

    from feature_raw
    group by feature_viewed
    order by view_count desc

),

-- Goal completion by segment
segment_goals as (

    select
        u.segment,
        round(avg(cast(d.goal_completed as integer)) * 100, 1) as goal_completion_pct,
        count(distinct d.user_id)                       as users_in_segment

    from daily d
    left join users u on d.user_id = u.user_id
    group by u.segment

)

-- Power BI will use each of these as a separate query / table
-- Final output: DAU daily (primary output for this mart)
select
    d.date,
    d.dau,
    d.avg_session_min,
    d.goal_completion_pct,
    d.notif_ctr_pct

from dau_by_date d
order by d.date
