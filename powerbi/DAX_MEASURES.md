# DAX Measures — Oura Health Intelligence Dashboard

> Copy each measure into Power BI via Modeling → New Measure.
> Organise into display folders as shown.

---

## Display Folder: // Scores

```dax
Readiness Score =
AVERAGE(mart_daily_scores[readiness_score])
```

```dax
Sleep Score =
AVERAGE(mart_daily_scores[sleep_score])
```

```dax
Activity Score =
AVERAGE(mart_daily_scores[activity_score])
```

```dax
Readiness Score 7D Avg =
CALCULATE(
    AVERAGE(mart_daily_scores[readiness_score]),
    DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -7, DAY)
)
```

```dax
Readiness vs 7D Avg =
[Readiness Score] - [Readiness Score 7D Avg]
```

```dax
Readiness vs 7D Avg Label =
VAR diff = [Readiness vs 7D Avg]
RETURN
    IF(diff > 0, "↑ +" & FORMAT(diff, "0") & " vs avg",
    IF(diff < 0, "↓ " & FORMAT(diff, "0") & " vs avg",
    "→ same"))
```

```dax
Sleep vs 7D Avg =
CALCULATE(AVERAGE(mart_daily_scores[sleep_score]),
    DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -7, DAY))
- [Sleep Score]
```

```dax
Sleep vs 7D Avg Label =
VAR diff = [Sleep vs 7D Avg] * -1
RETURN
    IF(diff > 0, "↑ +" & FORMAT(diff, "0") & " vs avg",
    IF(diff < 0, "↓ " & FORMAT(diff, "0") & " vs avg",
    "→ same"))
```

---

## Display Folder: // Sleep

```dax
Avg Sleep Duration (h) =
AVERAGE(mart_daily_scores[duration_h])
```

```dax
Avg Deep Sleep (h) =
AVERAGE(mart_daily_scores[deep_sleep_h])
```

```dax
Avg REM Sleep (h) =
AVERAGE(mart_daily_scores[rem_sleep_h])
```

```dax
Deep Sleep % =
DIVIDE(
    SUM(mart_daily_scores[deep_sleep_h]),
    SUM(mart_daily_scores[duration_h])
) * 100
```

```dax
REM Sleep % =
DIVIDE(
    SUM(mart_daily_scores[rem_sleep_h]),
    SUM(mart_daily_scores[duration_h])
) * 100
```

```dax
Light Sleep % =
DIVIDE(
    SUM(mart_daily_scores[light_sleep_h]),
    SUM(mart_daily_scores[duration_h])
) * 100
```

```dax
Awake % =
DIVIDE(
    SUM(mart_daily_scores[awake_h]),
    SUM(mart_daily_scores[duration_h])
) * 100
```

```dax
Sleep Goal Hours =
SELECTEDVALUE(dim_users[sleep_goal_hours], 8)
```

---

## Display Folder: // Activity

```dax
Total Steps =
SUM(mart_daily_scores[steps])
```

```dax
Avg Daily Steps =
AVERAGE(mart_daily_scores[steps])
```

```dax
Total Calories =
SUM(mart_daily_scores[calories_total])
```

```dax
Avg Active Minutes =
AVERAGE(mart_daily_scores[active_minutes])
```

```dax
Goal Hit Rate % =
DIVIDE(
    COUNTROWS(FILTER(mart_daily_scores, mart_daily_scores[goal_hit] = TRUE())),
    COUNTROWS(mart_daily_scores)
) * 100
```

```dax
Steps vs Goal =
AVERAGE(mart_daily_scores[steps]) - AVERAGE(mart_daily_scores[goal_steps])
```

```dax
Workout Days =
COUNTROWS(FILTER(mart_daily_scores, mart_daily_scores[workout_detected] = TRUE()))
```

---

## Display Folder: // Wellbeing

```dax
Avg HRV (ms) =
AVERAGE(mart_daily_scores[hrv_ms])
```

```dax
Avg Resting HR (bpm) =
AVERAGE(mart_daily_scores[resting_hr_bpm])
```

```dax
Avg Body Temp Deviation =
AVERAGE(mart_daily_scores[body_temp_dev_c])
```

```dax
HRV 7D Rolling Avg =
CALCULATE(
    AVERAGE(mart_daily_scores[hrv_ms]),
    DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -7, DAY)
)
```

```dax
HRV Trend Label =
VAR current  = [Avg HRV (ms)]
VAR baseline = CALCULATE(
    AVERAGE(mart_daily_scores[hrv_ms]),
    DATESINPERIOD(DateTable[Date], FIRSTDATE(DateTable[Date]), 30, DAY)
)
VAR diff = current - baseline
RETURN
    IF(diff > 0, "↑ trend: +" & FORMAT(diff, "0.0") & "ms",
    IF(diff < 0, "↓ trend: " & FORMAT(diff, "0.0") & "ms",
    "→ stable"))
```

```dax
Resting HR Trend Label =
VAR current  = [Avg Resting HR (bpm)]
VAR baseline = CALCULATE(
    AVERAGE(mart_daily_scores[resting_hr_bpm]),
    DATESINPERIOD(DateTable[Date], FIRSTDATE(DateTable[Date]), 30, DAY)
)
VAR diff = current - baseline
RETURN
    IF(diff < 0, "↓ improving",
    IF(diff > 0, "↑ worsening",
    "→ stable"))
```

---

## Display Folder: // Engagement

```dax
DAU =
DISTINCTCOUNT(mart_engagement_analytics[date])
```

```dax
Goal Completion % =
AVERAGE(mart_engagement_analytics[goal_completion_pct])
```

```dax
Avg Session (min) =
AVERAGE(mart_engagement_analytics[avg_session_min])
```

```dax
Notification CTR % =
AVERAGE(mart_engagement_analytics[notif_ctr_pct])
```

---

## Display Folder: // Utility

```dax
Selected User =
SELECTEDVALUE(dim_users[user_id], "All users")
```

```dax
Selected Segment =
SELECTEDVALUE(dim_users[segment], "All segments")
```

```dax
Date Range Label =
FORMAT(MIN(DateTable[Date]), "DD MMM") & " – " & FORMAT(MAX(DateTable[Date]), "DD MMM YYYY")
```

```dax
Days in Selection =
DATEDIFF(MIN(DateTable[Date]), MAX(DateTable[Date]), DAY) + 1
```

---

## Conditional Formatting Colours

Use these in Format → Data colors → Conditional formatting → Field value

```dax
Score Color =
VAR s = SELECTEDVALUE(mart_daily_scores[readiness_score])
RETURN
    SWITCH(TRUE(),
        s >= 75, "#4CAF50",
        s >= 50, "#FF9800",
        "#F44336"
    )
```

```dax
Steps Color =
VAR steps = SELECTEDVALUE(mart_daily_scores[steps])
VAR goal  = SELECTEDVALUE(mart_daily_scores[goal_steps], 10000)
RETURN
    SWITCH(TRUE(),
        steps >= goal,        "#4CAF50",
        steps >= goal * 0.7,  "#FF9800",
        "#F44336"
    )
```

---

## DateTable (create via Modeling → New Table)

```dax
DateTable =
CALENDAR(
    DATE(2026, 2, 21),
    DATE(2026, 5, 21)
)
```

Add columns to DateTable:

```dax
-- Year
Year = YEAR(DateTable[Date])
```

```dax
-- Month number
Month Num = MONTH(DateTable[Date])
```

```dax
-- Month name
Month Name = FORMAT(DateTable[Date], "MMM YYYY")
```

```dax
-- Day of week
Day of Week = WEEKDAY(DateTable[Date], 2)
```

```dax
-- Week number
Week = WEEKNUM(DateTable[Date], 2)
```

---

## Relationships (set in Model view)

| From table | Column | To table | Column | Cardinality |
|---|---|---|---|---|
| `mart_daily_scores` | `user_id` | `dim_users` | `user_id` | Many → One |
| `mart_daily_scores` | `date` | `DateTable` | `Date` | Many → One |
| `mart_engagement_analytics` | `date` | `DateTable` | `Date` | Many → One |
