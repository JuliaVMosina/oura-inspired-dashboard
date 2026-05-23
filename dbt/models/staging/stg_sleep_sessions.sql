-- Staging: sleep_sessions
-- One row per user per night.
-- Computes stage percentages for use in downstream models.

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/sleep_sessions.csv')

),

renamed as (

    select
        cast(session_id    as integer)       as session_id,
        cast(user_id       as integer)       as user_id,
        cast(date          as date)          as sleep_date,
        cast(duration_h    as decimal(5,2))  as duration_h,
        cast(deep_sleep_h  as decimal(5,2))  as deep_sleep_h,
        cast(rem_sleep_h   as decimal(5,2))  as rem_sleep_h,
        cast(light_sleep_h as decimal(5,2))  as light_sleep_h,
        cast(awake_h       as decimal(5,2))  as awake_h,
        cast(bedtime_hour  as decimal(4,1))  as bedtime_hour,
        cast(sleep_score   as integer)       as sleep_score,

        -- Stage percentages
        round(deep_sleep_h  / nullif(duration_h, 0) * 100, 1) as deep_pct,
        round(rem_sleep_h   / nullif(duration_h, 0) * 100, 1) as rem_pct,
        round(light_sleep_h / nullif(duration_h, 0) * 100, 1) as light_pct,
        round(awake_h       / nullif(duration_h, 0) * 100, 1) as awake_pct,

        -- Sleep score category
        case
            when sleep_score >= 75 then 'Good'
            when sleep_score >= 50 then 'Medium'
            else 'Low'
        end as sleep_category

    from source

)

select * from renamed
