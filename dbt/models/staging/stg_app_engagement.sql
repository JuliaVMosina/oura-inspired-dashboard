-- Staging: app_engagement
-- One row per feature view per session.
-- Notification CTR derived here for use in engagement marts.

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/app_engagement.csv')

),

renamed as (

    select
        cast(engagement_id   as integer)      as engagement_id,
        cast(user_id         as integer)      as user_id,
        cast(date            as date)         as engagement_date,
        cast(session_min     as decimal(5,1)) as session_min,
        cast(feature_viewed  as varchar)      as feature_viewed,
        cast(goal_completed  as boolean)      as goal_completed,
        cast(notif_sent      as boolean)      as notif_sent,
        cast(notif_clicked   as boolean)      as notif_clicked

    from source

)

select * from renamed
