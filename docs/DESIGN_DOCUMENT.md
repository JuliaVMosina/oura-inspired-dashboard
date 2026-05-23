# Oura Health Intelligence Dashboard — Design Document

> This document records design decisions, rejected alternatives, and rationale
> for every significant choice made during the development of this dashboard.
> It exists to show *how* the product was designed, not just *what* was built.

---

## 1. Product Brief

### Problem statement
A health-conscious user wearing an Oura Ring generates data every night and day —
sleep stages, HRV, resting HR, activity, readiness score.
The Oura app shows daily numbers but offers limited analytical depth:
no trend context, no comparative views, no engagement tracking.

**This dashboard answers the questions the app doesn't:**
- Why is my readiness score what it is today?
- Is my HRV improving over the last 90 days?
- Which features do users actually engage with — and which go unused?

### Design goal
Build a BI product, not a report.
Every page answers a specific user question. Every visual earns its place.
The design must be navigable in 3 seconds without reading a single label.

---

## 2. User Personas & Primary Questions Per Page

| Page | Primary user | Primary question |
|---|---|---|
| Personal Overview | Self-Optimizer | *Am I recovering well today — and why?* |
| Sleep Analytics | Self-Optimizer / Health Coach | *How has my sleep quality changed over 30 days?* |
| Activity & Movement | Self-Optimizer | *Am I hitting my activity targets consistently?* |
| Wellbeing Trends | Health Coach | *Are the key physiological markers improving long-term?* |
| Engagement Analytics | Product Analyst | *Which features drive engagement — and where do users drop off?* |

**Design rule derived from this:** Each page has one dominant visual that answers the primary question.
Everything else is supporting context — visually smaller, lower contrast.

---

## 3. Information Architecture Decisions

### Page 1 — Personal Overview

**Hierarchy chosen:**
1. Three headline scores (Readiness / Sleep / Activity) — dominant, large numerals
2. Readiness factor breakdown — explains *why* the readiness score is what it is
3. 7-day trend — provides context: is today an outlier or a pattern?
4. 7-day strip — quick calendar-style scan of the week

**Rejected alternatives:**
- *Gauge chart for readiness score* — rejected. Gauges consume space and add no information beyond a number. A card with status colour communicates the same faster.
- *Radar chart for readiness factors* — rejected. Radar charts are difficult to read accurately and create false impressions of balance. Horizontal bar chart shows magnitude clearly.
- *Line chart as the hero visual* — rejected for this page. Trends are supporting context here; today's state is the primary question.

---

### Page 2 — Sleep Analytics

**Hierarchy chosen:**
1. Four KPI cards (score, avg duration, deep sleep, REM) — today's key numbers
2. 30-day duration bar chart — primary trend view, hero visual
3. Sleep Stages horizontal bar chart — part-of-whole breakdown (supporting); donut rejected, see below
4. Sleep timing scatter + score distribution — diagnostic tools (tertiary)

**Rejected alternatives:**
- *Area chart for sleep duration* — rejected in favour of bars. Bar height is easier to compare night-to-night than area. Goal line on a bar chart is cleaner.
- *Stacked bar for sleep stages over time* — rejected. Stacked bars make it hard to read individual stage trends. Donut for average breakdown + separate trend if needed.
- *Donut chart for sleep stages* — rejected during wireframing in favour of a horizontal bar chart. The four segments (Deep 22% / REM 25% / Light 46% / Awake 7%) are primarily compared against each other — a bar chart gives more accurate magnitude perception than arc length on a donut. Accepted as a deliberate deviation from the initial spec. Stage colours: Deep = `#C8963E` (gold), REM = `#A855C8` (purple — amber `#E8A838` was too close to gold to be distinguishable at bar width; purple is the industry standard for REM in sleep analytics used by Oura and Fitbit), Light = `#4A6FA5` (blue), Awake = `#F44336` (red).
- *Heatmap calendar for sleep scores* — considered, not implemented in v1. Would require Deneb and adds complexity without answering the primary question faster.

---

### Page 3 — Activity & Movement

**Hierarchy chosen:**
1. Four KPI cards (steps vs goal, calories, active minutes, goal %) — status at a glance
2. Daily steps bar chart (30 days, goal line) — the core accountability visual
3. Activity zones stacked bar — how time is distributed across intensity levels
4. Calorie trend area chart + workout table — supporting detail

**Rejected alternatives:**
- *Ring / donut for goal completion* — rejected. Looks like Oura branding which this project deliberately avoids replicating. Progress card with % is cleaner.
- *Scatter plot for steps vs calories* — rejected for primary view. Correlation is not the primary question on this page; consistency vs goal is.

---

### Page 4 — Wellbeing Trends

**Hierarchy chosen:**
1. Three KPI cards (avg HRV, resting HR, body temp deviation) — current state
2. HRV line chart (90 days) — full-width hero visual, primary trend
3. Resting HR trend + body temp deviation chart — secondary trends, half-width

**Rejected alternatives:**
- *Combining all three metrics in one chart* — rejected. Different units (ms, bpm, °C) and different directionalities (HRV higher = better, HR lower = better) make a combined chart misleading. Separate charts, clear annotation.
- *90-day bar chart for HRV* — rejected. HRV is a continuous physiological signal; line chart correctly implies continuity. Bar chart implies discrete events.
- *Box plots for distribution* — considered for v2. Shows variability better than a line, but adds interpretation complexity for non-technical users.

---

### Page 5 — Engagement Analytics

**Hierarchy chosen:**
1. Four KPI cards (DAU, goal completion %, avg session, notification CTR)
2. Feature usage horizontal bar (sorted descending) — what users actually use
3. Goal completion by segment (grouped bar) — who completes goals
4. DAU trend area chart — engagement over time

**Rejected alternatives:**
- *Treemap for feature usage* — rejected. Treemaps require reading area, which is imprecise. Sorted horizontal bar is faster and more accurate.
- *Funnel chart for feature engagement* — rejected for primary view. Not all features are sequential; a funnel implies a conversion path that doesn't exist here.

---

## 4. Visual Design Decisions

### Dark theme rationale
Oura Ring app uses a deep navy/black background. This is not aesthetic preference — it serves a function:
- Health data is viewed at night (before sleep, after waking)
- Dark UI reduces eye strain in low-light conditions
- High-contrast gold/white numerals on dark background maximise pre-attentive processing of KPI values

**Challenge:** Dark backgrounds require higher contrast than light UI. 
`#B0B8C1` (secondary text) is used only for labels and axis text — never for data values. 
Data values always use `#FFFFFF` or `#C8963E`.

### Colour system decisions

| Decision | Rationale |
|---|---|
| Gold `#C8963E` for primary KPIs only | Gold draws the eye first. If everything is gold, nothing is. Reserved for the single most important number per page. |
| Status colours for scores only | Green/orange/red is a semantic system — it means "good/ok/bad". Using it for non-score data (e.g., category labels) corrupts the semantic meaning. |
| Maximum 4 colours per chart | Beyond 4, legend lookup becomes mandatory. Mandatory legend = cognitive load = slower insight. |
| No gradient fills on bars | Gradients add visual noise without adding data. Flat colour bars with status-colour encoding are faster to read. |

### Typography decisions
- Segoe UI throughout — consistent with Power BI's default, no custom font loading required
- KPI values at 36px bold — large enough to read from 60cm without leaning in
- Section labels in uppercase, 11px — clearly distinguishable from data labels without size increase

---

## 5. Semantic Model Design

### Why star schema

The star schema with `daily_scores` as the central fact table was chosen because:
- Most user questions are answered by filtering scores by date and user
- Dimension tables (`users`, `DateTable`) are stable and reusable across all pages
- DirectLake mode in Microsoft Fabric performs optimally with star schema (minimal join complexity)

### Measures organisation (display folders)

| Folder | Measures |
|---|---|
| `// Scores` | Readiness Score, Sleep Score, Activity Score, 7-Day Avg Readiness |
| `// Sleep` | Avg Sleep Duration, Deep Sleep %, REM %, Sleep Timing Variance |
| `// Activity` | Total Steps, Goal Achievement %, Active Minutes, Calorie Burn |
| `// Wellbeing` | Avg HRV, Avg Resting HR, Temp Deviation, HRV 7-Day Trend |
| `// Engagement` | DAU, Feature Usage Count, Goal Completion Rate, Notification CTR |
| `// Utility` | Selected User, Date Context, Period Label |

All measures have descriptions filled in the Power BI model.

### Row-level security

Two roles defined:
- `Individual User` — sees only their own data (filters `users[user_id] = USERPRINCIPALNAME()`)
- `Health Coach` — sees all users (no filter)

This mirrors a real-world deployment where coaches review client data.

### Fabric-ready architecture

| Layer | Current (local) | Fabric equivalent |
|---|---|---|
| Raw data | CSV files in `/data/raw/` | Lakehouse Files (OneLake) |
| Transformed data | DBT models → CSV in `/data/marts/` | Lakehouse Tables (Delta) |
| Semantic model | Power BI Desktop (.pbix) | Fabric Semantic Model (DirectLake) |
| Reports | Power BI Desktop | Power BI Service (Fabric workspace) |

DirectLake mode would be the target deployment: semantic model reads directly from Delta tables in OneLake, no import or DirectQuery overhead.

---

## 6. DBT Layer Design

### Model structure rationale

```
models/
├── staging/          -- 1:1 with source tables, type casting, rename only
│   ├── stg_users.sql
│   ├── stg_daily_scores.sql
│   ├── stg_sleep_sessions.sql
│   ├── stg_activity_sessions.sql
│   ├── stg_hrv_metrics.sql
│   └── stg_app_engagement.sql
├── intermediate/     -- business logic, joins, derived fields
│   ├── int_daily_health_summary.sql    -- joins scores + hrv + activity per day
│   └── int_user_engagement_summary.sql -- aggregates engagement per user per day
└── marts/            -- final tables consumed by Power BI
    ├── mart_daily_scores.sql
    ├── mart_sleep_analytics.sql
    ├── mart_activity_analytics.sql
    ├── mart_wellbeing_trends.sql
    └── mart_engagement_analytics.sql
```

**Why this separation:**
- Staging models are a stable interface layer — if the source schema changes, only staging changes
- Intermediate models contain the complex joins; if logic changes, marts don't need to be rewritten
- Power BI reads only from marts — clean, pre-aggregated, named consistently

### Tests implemented

| Test | Table | What it catches |
|---|---|---|
| `not_null` | `daily_scores.user_id`, `daily_scores.date` | Missing FK or date |
| `unique` | `daily_scores.[user_id, date]` | Duplicate daily records |
| `accepted_values` | `daily_scores.readiness_score` (0–100) | Out-of-range generated data |
| `relationships` | `daily_scores.user_id` → `users.user_id` | Orphaned fact records |

---

## 7. Deneb / Vega-Lite Usage

Deneb is used where Power BI native visuals cannot deliver the required design:

| Visual | Page | Why Deneb, not native |
|---|---|---|
| HRV trend with rolling avg overlay | Wellbeing Trends | Native line chart cannot render a calculated rolling average as a dashed secondary series without a separate DAX column |
| Sleep stage area chart (stacked, time-series) | Sleep Analytics | Native stacked area requires unpivoted data structure; Deneb handles wide format directly |
| Body temp deviation (diverging bar) | Wellbeing Trends | Native bar chart cannot colour bars individually above/below zero without complex conditional formatting |

All other visuals use native Power BI charts. Deneb is not used for decoration.

---

## 8. What Was Deliberately Not Built

| Feature | Reason not included |
|---|---|
| Animated transitions between pages | Adds no analytical value. Distracts from data. |
| 3D visuals of any kind | 3D distorts magnitude perception. Never appropriate in BI. |
| More than 5 pages | Depth beats breadth. 5 well-documented pages > 8 surface-level pages. |
| Real Oura API data | Would create a privacy dependency. Synthetic data with realistic distributions is sufficient for a portfolio project and avoids legal complexity. |
| Mobile layout | Power BI mobile layout is a separate design task. Not in scope for v1. |

---

*Last updated: 21.05.2026*
*Status: in progress — updated as each phase is completed*
