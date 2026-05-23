-- Staging: activity_sessions
-- One row per user per day.
-- Adds goal_gap (how many steps away from goal) and activity score category.

with source as (

    select * from read_csv_auto('{{ var("data_raw_path") }}/activity_sessions.csv')

),

renamed as (

    select
        cast(activity_id           as integer)      as activity_id,
        cast(user_id               as integer)      as user_id,
        cast(date                  as date)         as activity_date,
        cast(steps                 as integer)      as steps,
        cast(calories_total        as integer)      as calories_total,
        cast(active_minutes        as integer)      as active_minutes,
        cast(goal_steps            as integer)      as goal_steps,
        cast(goal_hit              as boolean)      as goal_hit,
        cast(min_sedentary         as integer)      as min_sedentary,
        cast(min_low               as integer)      as min_low,
        cast(min_medium            as integer)      as min_medium,
        cast(min_high              as integer)      as min_high,
        cast(workout_detected      as boolean)      as workout_detected,
        cast(workout_type          as varchar)      as workout_type,
        cast(workout_duration_min  as integer)      as workout_duration_min,
        cast(workout_calories      as integer)      as workout_calories,

        -- Steps gap to goal
        goal_steps - steps                         as steps_to_goal,

        -- Steps category for bar chart colouring
        case
            when steps >= goal_steps       then 'Good'
            when steps >= goal_steps * 0.7 then 'Medium'
            else 'Low'
        end as steps_category

    from source

)

select * from renamed
