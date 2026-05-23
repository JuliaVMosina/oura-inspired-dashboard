-- Staging: daily_scores
-- Central fact table. One row per user per day.
-- Adds score_date as proper date type; keeps all readiness factor columns.

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/daily_scores.csv')

),

renamed as (

    select
        cast(user_id          as integer)  as user_id,
        cast(date             as date)     as score_date,
        cast(readiness_score  as integer)  as readiness_score,
        cast(sleep_score      as integer)  as sleep_score,
        cast(activity_score   as integer)  as activity_score,

        -- Readiness factor breakdown (used on Page 1 — Personal Overview)
        cast(hrv_balance       as integer) as hrv_balance,
        cast(recovery_index    as integer) as recovery_index,
        cast(sleep_balance     as integer) as sleep_balance,
        cast(activity_balance  as integer) as activity_balance,
        cast(body_temp_score   as integer) as body_temp_score,

        -- Derived: overall wellness category
        case
            when readiness_score >= 75 then 'Good'
            when readiness_score >= 50 then 'Medium'
            else 'Low'
        end as readiness_category

    from source

)

select * from renamed
