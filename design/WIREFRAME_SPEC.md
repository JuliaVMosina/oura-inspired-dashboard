# Oura Health Intelligence Dashboard — Wireframe Specification
## Figma Blueprint · All 5 Pages

> Use this document as a blueprint when building wireframes in Figma.
> Canvas size: **1280 × 720 px** (16:9, Power BI default)
> Grid: 24px margin all sides, 16px gutters between components

---

## Global Layout System

```
┌──────────────────────────────────────────────────────────┐
│  HEADER BAR (height: 60px)                               │
│  [Logo / Page Title]              [Filters / Date range] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  CONTENT AREA (height: 636px)                            │
│  — varies per page —                                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Color tokens (Figma styles to define)
| Token | Hex | Usage |
|---|---|---|
| `bg/page` | `#1A1A2E` | Page background |
| `bg/card` | `#16213E` | Card backgrounds |
| `bg/card-hover` | `#1E2A4A` | Card hover state |
| `accent/gold` | `#C8963E` | Primary KPIs, highlights |
| `accent/amber` | `#E8A838` | Secondary accents |
| `status/good` | `#4CAF50` | Score ≥ 75 |
| `status/medium` | `#FF9800` | Score 50–74 |
| `status/low` | `#F44336` | Score < 50 |
| `text/primary` | `#FFFFFF` | Headings, KPI values |
| `text/secondary` | `#B0B8C1` | Labels, subtitles |
| `border/subtle` | `#2A3550` | Card borders |

### Typography
| Style | Font | Size | Weight | Color |
|---|---|---|---|---|
| Page title | Segoe UI | 18px | SemiBold | `#FFFFFF` |
| Section label | Segoe UI | 11px | Regular | `#B0B8C1` uppercase |
| KPI value | Segoe UI | 36px | Bold | `#C8963E` |
| KPI label | Segoe UI | 12px | Regular | `#B0B8C1` |
| Body | Segoe UI | 13px | Regular | `#FFFFFF` |
| Chart axis | Segoe UI | 11px | Regular | `#B0B8C1` |

### Reusable components (create as Figma components)
- **KPI Card**: 200×100px · bg/card · 8px radius · gold value + label + optional delta badge
- **Section Header**: label text + thin gold underline (2px, 40px wide)
- **Chart Container**: bg/card · 8px radius · 12px internal padding
- **Filter Pill**: 120×32px · bg/card · border/subtle · text/secondary
- **Status Badge**: 48×20px · rounded · status color background

---

## Page 1 — Personal Overview

**Purpose:** Daily readiness summary — today's headline scores at a glance.

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
│ [⬡ Oura] Personal Overview          [User: Julia ▼] [Today ▼] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ READINESS    │  │ SLEEP        │  │ ACTIVITY     │          │
│  │   82         │  │   76         │  │   91         │          │
│  │ ↑ +5 vs avg  │  │ → same       │  │ ↑ +12 vs avg │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌─────────────────────────────┐  ┌────────────────────────┐   │
│  │ READINESS FACTORS           │  │ 7-DAY SCORE TREND      │   │
│  │ HRV Balance      ████ 85    │  │                        │   │
│  │ Recovery Index   ███  72    │  │  [sparkline ×3 lines]  │   │
│  │ Sleep Balance    ████ 78    │  │  Readiness / Sleep /   │   │
│  │ Activity Balance ██   65    │  │  Activity              │   │
│  │ Body Temp        ████ 80    │  │                        │   │
│  └─────────────────────────────┘  └────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ LAST 7 DAYS                                             │   │
│  │  Mon   Tue   Wed   Thu   Fri   Sat   Sun                │   │
│  │  [82]  [75]  [88]  [71]  [65]  [90]  [82]              │   │
│  │  color-coded dots: green / orange / red                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Header bar** — logo left, user selector + date filter right
2. **3 × KPI Card** (top row) — Readiness / Sleep / Activity · value + vs-avg delta
3. **Readiness Factors** (bottom-left) — horizontal bar chart, 5 factors, color-coded bars
4. **7-Day Trend** (bottom-right) — line chart · 3 series · legend
5. **7-Day Strip** (full-width bottom) — 7 score badges, color-coded by status

**Key design notes:**
- The 3 KPI cards are the dominant visual — large gold numerals, prominent
- Readiness score has the biggest card (slightly wider) — it's the primary metric
- Delta arrows: green ↑ / grey → / red ↓

---

## Page 2 — Sleep Analytics

**Purpose:** Deep-dive into sleep quality, duration, and stage patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
│ [⬡ Oura] Sleep Analytics           [User ▼] [Last 30 days ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │ SLEEP     │  │ AVG DUR.  │  │ DEEP SLEEP│  │ REM SLEEP │   │
│  │ SCORE 76  │  │ 7h 24m    │  │ 1h 42m    │  │ 1h 58m    │   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
│                                                                 │
│  ┌───────────────────────────┐  ┌───────────────────────────┐  │
│  │ 30-DAY SLEEP DURATION     │  │ SLEEP STAGES BREAKDOWN    │  │
│  │                           │  │                           │  │
│  │  [bar chart - daily       │  │  [donut chart]            │  │
│  │   duration bars with      │  │  Deep / REM /             │  │
│  │   color by score, goal    │  │  Light / Awake            │  │
│  │   line at 8h]             │  │                           │  │
│  │                           │  │  Deep  22%  ████          │  │
│  │                           │  │  REM   25%  █████         │  │
│  │                           │  │  Light 46%  █████████     │  │
│  │                           │  │  Awake  7%  █             │  │
│  └───────────────────────────┘  └───────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────┐  ┌───────────────────────────┐  │
│  │ SLEEP TIMING              │  │ SCORE DISTRIBUTION        │  │
│  │ [scatter: bedtime vs      │  │ [histogram: 0-100 range,  │  │
│  │  wake time, 30 days]      │  │  bell curve shape]        │  │
│  └───────────────────────────┘  └───────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
1. **4 × KPI Card** — Sleep Score / Avg Duration / Deep Sleep / REM Sleep
2. **30-Day Bar Chart** — daily sleep duration, bars colored by score, 8h goal line
3. **Stage Donut** — 4 segments + legend with % labels
4. **Sleep Timing Scatter** — bedtime (y-axis, inverted) vs wake time, 30 points
5. **Score Distribution** — histogram showing score frequency across 0–100

**Key design notes:**
- Duration bars use status colors (green/orange/red) based on score threshold
- Donut colors: deep = gold, REM = amber, light = #4A6FA5, awake = #F44336

---

## Page 3 — Activity & Movement

**Purpose:** Step tracking, calorie burn, activity zones, goal achievement.

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
│ [⬡ Oura] Activity & Movement       [User ▼] [Last 30 days ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│  │ TODAY'S STEPS │  │ CALORIES  │  │ ACTIVE MIN│  │ GOAL %  │ │
│  │  9,847        │  │ 2,340     │  │  62       │  │  82%    │ │
│  │ Goal: 10,000  │  │           │  │           │  │ ▓▓▓▓▓▒  │ │
│  └───────────────┘  └───────────┘  └───────────┘  └─────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────┐  ┌───────────────┐  │
│  │ DAILY STEPS — LAST 30 DAYS            │  │ ACTIVITY ZONES│  │
│  │                                       │  │               │  │
│  │  [bar chart with goal line at 10,000] │  │ [horizontal   │  │
│  │  bars colored: green = hit goal       │  │  stacked bar] │  │
│  │              orange = close           │  │  Sedentary    │  │
│  │              red = far below          │  │  Low          │  │
│  │                                       │  │  Medium       │  │
│  │                                       │  │  High         │  │
│  └───────────────────────────────────────┘  └───────────────┘  │
│                                                                 │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐ │
│  │ CALORIE TREND (30 days) │  │ WORKOUT SESSIONS DETECTED    │ │
│  │ [area chart]            │  │ [table: date / type /        │ │
│  │                         │  │  duration / calories]        │ │
│  └─────────────────────────┘  └──────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
1. **4 × KPI Card** — Steps / Calories / Active Minutes / Goal %
2. **Daily Steps Bar Chart** — 30 bars, color-coded vs goal, goal line
3. **Activity Zones** — stacked horizontal bar (sedentary / low / medium / high)
4. **Calorie Trend** — area chart, 30 days, gold fill with opacity
5. **Workout Table** — last 5–10 detected workouts with type icon

**Key design notes:**
- Goal % card has mini progress bar (visual, not chart) inside the card
- Steps bars: green if ≥ 10k, orange if 7k–9.9k, red if < 7k
- Activity zones use a distinct 4-color palette (not status colors)

---

## Page 4 — Wellbeing Trends

**Purpose:** Long-term HRV, resting HR, and body temperature patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
│ [⬡ Oura] Wellbeing Trends          [User ▼] [Last 90 days ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────────┐ │
│  │ AVG HRV        │  │ RESTING HR     │  │ BODY TEMPERATURE  │ │
│  │ 58 ms          │  │ 52 bpm         │  │ +0.2°C deviation  │ │
│  │ ↑ trend: +3ms  │  │ ↓ improving    │  │ → normal          │ │
│  └────────────────┘  └────────────────┘  └───────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ HRV TREND — 90 DAYS                                     │   │
│  │                                                         │   │
│  │  [line chart · single series · rolling 7-day avg        │   │
│  │   as secondary dashed line · gold primary line]         │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌───────────────────────────┐  ┌───────────────────────────┐  │
│  │ RESTING HR TREND          │  │ BODY TEMP DEVIATION       │  │
│  │ [line chart, 90 days]     │  │ [bar chart, deviation     │  │
│  │ lower = better (invert    │  │  from baseline:           │  │
│  │ annotation)               │  │  bars above/below 0      │  │
│  │                           │  │  green = normal,          │  │
│  │                           │  │  red = elevated]          │  │
│  └───────────────────────────┘  └───────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
1. **3 × KPI Card** — Avg HRV / Resting HR / Body Temp deviation
2. **HRV Trend Line** — full-width, 90 days, primary line + dashed 7-day rolling avg
3. **Resting HR Line** — 90 days, annotation "lower is better"
4. **Body Temp Bar** — deviation from personal baseline, above/below zero axis

**Key design notes:**
- HRV chart is the hero visual on this page — full width, prominent
- Body temp deviation chart uses diverging color: green bars (normal) / red bars (elevated)
- Resting HR: downward trend should appear as improvement (annotation label)

---

## Page 5 — Engagement Analytics

**Purpose:** Product analyst view — feature usage, goal completion, user engagement patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
│ [⬡ Oura] Engagement Analytics      [Segment ▼] [Last 30d ▼]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  │
│  │ DAU        │  │ GOAL COMP. │  │ AVG SESSION│  │ NOTIF    │  │
│  │ 847        │  │ 68%        │  │ 4.2 min    │  │ CTR 34%  │  │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘  │
│                                                                 │
│  ┌──────────────────────────────┐  ┌──────────────────────────┐ │
│  │ FEATURE USAGE — TOP 8        │  │ GOAL COMPLETION BY       │ │
│  │                              │  │ USER SEGMENT             │ │
│  │ [horizontal bar chart]       │  │                          │ │
│  │ Readiness Score   ████████   │  │ [grouped bar chart:      │ │
│  │ Sleep Score       ███████    │  │  Self-Optimizer /        │ │
│  │ Activity Ring     ██████     │  │  Health Coach /          │ │
│  │ HRV Chart         █████      │  │  Casual User]            │ │
│  │ Sleep Stages      ████       │  │                          │ │
│  │ Trends            ███        │  │                          │ │
│  │ Goals             ██         │  │                          │ │
│  │ Notifications     █          │  │                          │ │
│  └──────────────────────────────┘  └──────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ DAILY ACTIVE USERS — 30-DAY TREND                       │   │
│  │ [area chart · gold fill · 30 days]                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
1. **4 × KPI Card** — DAU / Goal Completion % / Avg Session / Notification CTR
2. **Feature Usage Bar** — horizontal, sorted descending, top 8 features
3. **Goal Completion Grouped Bar** — 3 user segments × completion rate
4. **DAU Trend Area** — 30-day line with gold fill

**Key design notes:**
- This page has a different tone — data-dense, product analytics style
- Segment filter at top changes all visuals
- Feature usage bars use gradient from gold (top) to amber (bottom)

---

## Figma Setup Checklist

### Before you start
- [ ] Canvas: Frame · 1280 × 720 · bg/page `#1A1A2E`
- [ ] Define all color styles (tokens table above)
- [ ] Define all text styles (typography table above)
- [ ] Create reusable components: KPI Card, Section Header, Chart Container, Filter Pill

### Per page
- [ ] Duplicate frame (⌘D) · rename to page name
- [ ] Place header bar first · lock it
- [ ] Block out zones with rectangles (no details yet — just layout proportions)
- [ ] Add text labels for each zone
- [ ] Fill in KPI card values (representative numbers, not real data)
- [ ] Replace chart placeholder rects with rough chart sketches (lines/bars as shapes)

### Final
- [ ] Export each frame as PNG (1x) to `design/wireframes/` folder
- [ ] Push PNGs to GitHub
- [ ] Share Figma link in PROJECT_PLAN.md

---

## Recommended Figma Layout: Start with Page 1

**Sequence:** Page 1 → Page 2 → Page 3 → Page 4 → Page 5

Page 1 establishes all the reusable components. Once you build the KPI cards and header for Page 1, you can copy them to every other page — saves 80% of setup time.

**Time estimate per page:** 30–45 min in Figma once components are built.
