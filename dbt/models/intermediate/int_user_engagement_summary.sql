-- Intermediate: user engagement summary
-- Aggregates app_engagement to one row per user per day.
-- Computes DAU flag, feature counts, goal completion, notification CTR.

with engagement as (
    select * from {{ ref('stg_app_engagement') }}
),

users as (
    select user_id, segment from {{ ref('stg_users') }}
),

daily_agg as (

    select
        user_id,
        engagement_date                             as date,
        count(distinct engagement_id)               as feature_views,
        count(distinct feature_viewed)              as unique_features_viewed,
        max(session_min)                            as session_min,
        max(cast(goal_completed as integer))        as goal_completed,
        max(cast(notif_sent as integer))            as notif_sent,
        max(cast(notif_clicked as integer))         as notif_clicked,
        1                                           as is_dau

    from engagement
    group by user_id, engagement_date

),

with_segment as (

    select
        d.*,
        u.segment,

        -- Notification CTR flag (clicked / sent)
        case
            when d.notif_sent = 1 and d.notif_clicked = 1 then 1
            else 0
        end as notif_ctr

    from daily_agg d
    left join users u on d.user_id = u.user_id

)

select * from with_segment
