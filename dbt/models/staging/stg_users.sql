-- Staging: users
-- One row per user. Casts types, renames nothing (source names are already clean).

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/users.csv')

),

renamed as (

    select
        cast(user_id          as integer)   as user_id,
        cast(segment          as varchar)   as segment,
        cast(age              as integer)   as age,
        cast(gender           as varchar)   as gender,
        cast(device_model     as varchar)   as device_model,
        cast(membership_start as date)      as membership_start,
        cast(step_goal        as integer)   as step_goal,
        cast(sleep_goal_hours as decimal(4,1)) as sleep_goal_hours

    from source

)

select * from renamed
