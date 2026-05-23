-- Staging: hrv_metrics
-- One row per user per day.
-- Adds temp deviation category for body temp diverging bar chart.

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/hrv_metrics.csv')

),

renamed as (

    select
        cast(user_id          as integer)      as user_id,
        cast(date             as date)         as metric_date,
        cast(hrv_ms           as decimal(6,1)) as hrv_ms,
        cast(resting_hr_bpm   as decimal(5,1)) as resting_hr_bpm,
        cast(body_temp_dev_c  as decimal(5,2)) as body_temp_dev_c,

        -- HRV category
        case
            when hrv_ms >= 60 then 'Good'
            when hrv_ms >= 40 then 'Medium'
            else 'Low'
        end as hrv_category,

        -- Temp deviation flag (>0.5°C = elevated)
        case
            when abs(body_temp_dev_c) > 0.5 then 'Elevated'
            else 'Normal'
        end as temp_status

    from source

)

select * from renamed
