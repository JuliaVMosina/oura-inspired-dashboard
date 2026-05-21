# Oura-inspired: Health & Activity Analytics Dashboard
## Project Plan & Context

> *This document serves as the persistent context for multi-session work on this project.
> Update status after each work session.*

---

## Strategic Purpose

This project is designed to demonstrate the **BI Product Designer** skill set —
not just technical BI delivery, but the full product design cycle:
discovery → UX design → data architecture → development → documentation.

**Target role this project is built for:**
KONE BI Product Designer, Business Intelligence (Espoo, hybrid)
- Requires: Power BI + Fabric, DBT, SQL, DAX, Python, UX principles in BI, data modeling, documentation
- Requires: PL-300 (in progress) + DP-600/DP-605 (Fabric — to be pursued)
- Julia has a referral contact at KONE

**Why Oura:**
- Julia's BBA thesis is about a wearable health tracking app (same domain)
- Oura is a Helsinki-based target company on Julia's watchlist
- Distinctive dark UI → opportunity for custom/non-standard design
- Strong narrative: "I built a framework for this domain in my thesis, now I visualize it"

---

## Design Philosophy

This is NOT a standard drag-and-drop Power BI report.
It is a **BI product** — designed like a designer, built like an engineer.

Principles:
- **Design-first:** wireframe in Figma/PowerPoint before any Power BI work
- **User-centric:** defined personas, user stories, acceptance criteria
- **Custom visuals:** Deneb (Vega-Lite), custom backgrounds, dark theme
- **Documented:** technical design doc, data model diagram, README as product spec
- **Fabric-ready:** semantic model architecture aligned with Microsoft Fabric

---

## Target Dashboard

**Name:** Oura Health Intelligence Dashboard
**Theme:** Dark (#1A1A2E background, gold/amber accents #C8963E, white text)
**Tool:** Power BI Desktop (Fabric-ready semantic model)
**Inspired by:** Oura Ring app visual language — NOT an official Oura product

### Pages (planned)
| # | Page | Focus |
|---|---|---|
| 1 | **Personal Overview** | Daily readiness score, sleep, activity — today's summary |
| 2 | **Sleep Analytics** | Sleep stages, duration trends, score distribution |
| 3 | **Activity & Movement** | Steps, calories, activity zones, workout detection |
| 4 | **Wellbeing Trends** | HRV, resting HR, body temperature, long-term patterns |
| 5 | **Engagement Analytics** | Feature usage, app engagement, goal completion (product lens) |

---

## Data Architecture

### Tables (to be generated)
| Table | Description |
|---|---|
| `users` | User profiles: age, gender, membership start, device model |
| `daily_scores` | Readiness, sleep, activity scores by day per user |
| `sleep_sessions` | Sleep session details: duration, stages, timing, score |
| `activity_sessions` | Steps, calories, active zones, workout sessions |
| `hrv_metrics` | HRV, resting HR, body temperature by day |
| `app_engagement` | Feature views, goal completions, notification interactions |

### Schema
Star schema: `daily_scores` as central fact table, dimensions: `users`, `DateTable`

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data generation | Python (pandas, numpy, faker) |
| Data transformation | DBT Core (staging → intermediate → marts) |
| Semantic model | Power BI (star schema, DAX measures) |
| Custom visuals | Deneb (Vega-Lite inside Power BI) |
| Design | Figma or PowerPoint for wireframes + custom backgrounds |
| Theme | Custom Power BI theme JSON (dark, Oura palette) |
| Documentation | Markdown (this file + README + data model diagram) |
| Version control | GitHub |

---

## Oura Color Palette

| Color | Hex | Usage |
|---|---|---|
| Background dark | `#1A1A2E` | Page background |
| Surface | `#16213E` | Card backgrounds |
| Accent gold | `#C8963E` | Primary KPIs, highlights |
| Accent amber | `#E8A838` | Secondary accents |
| Success green | `#4CAF50` | Good scores |
| Warning orange | `#FF9800` | Medium scores |
| Alert red | `#F44336` | Low scores |
| Text primary | `#FFFFFF` | Headings |
| Text secondary | `#B0B8C1` | Labels, subtitles |

---

## User Personas

### Persona 1 — The Self-Optimizer (primary)
- 28-40 years old, uses Oura daily
- Wants to understand patterns: why is my readiness low today?
- Needs: quick daily summary + trend context

### Persona 2 — The Health Coach
- Reviews client data weekly
- Wants: comparative trends, anomaly detection, sleep quality patterns
- Needs: multi-week view, clear scoring

### Persona 3 — Oura Product Analyst (internal)
- Tracks engagement and feature adoption
- Needs: DAU, feature usage, goal completion rates

---

## User Stories (Draft)

**Page 1 — Personal Overview**
- As a user, I want to see today's readiness, sleep, and activity scores at a glance
- As a user, I want to know if today is better or worse than my 7-day average
- As a user, I want to see which factor is dragging my readiness score down

**Page 2 — Sleep Analytics**
- As a user, I want to see my sleep duration and score trend over the last 30 days
- As a user, I want to understand my sleep stage breakdown (deep, REM, light, awake)
- As a health coach, I want to see which nights had poor sleep and why

**Page 3 — Activity**
- As a user, I want to see my daily step count vs. my goal
- As a user, I want to see which days I hit activity targets
- As a user, I want to understand my calorie burn trend

**Page 4 — Wellbeing Trends**
- As a user, I want to track my HRV trend over time
- As a user, I want to see if my resting HR is improving
- As a health coach, I want to identify concerning trends early

**Page 5 — Engagement (Product Analytics)**
- As a product analyst, I want to see which features users engage with most
- As a product analyst, I want to track goal completion rates by user segment

---

## Work Phases & Status

### Phase 1 — Discovery & Design
- [x] Define strategic purpose and target role
- [x] Define user personas
- [x] Draft user stories
- [x] Define data architecture
- [ ] Create wireframes (Figma or PowerPoint) for all 5 pages
- [ ] Finalize acceptance criteria per page

### Phase 2 — Data Generation
- [ ] Write `python/generate_data.py`
- [ ] Generate: users, daily_scores, sleep_sessions, activity_sessions, hrv_metrics, app_engagement
- [ ] Validate data quality and realism

### Phase 3 — Data Modeling (optional DBT layer)
- [ ] DBT staging models
- [ ] DBT intermediate models
- [ ] DBT mart models
- [ ] DBT tests and documentation

### Phase 4 — Power BI Development
- [ ] Create custom theme JSON (dark, Oura palette)
- [ ] Design custom background (Figma → PNG)
- [ ] Build semantic model (star schema, relationships)
- [ ] Create DAX measures
- [ ] Build Page 1 — Personal Overview
- [ ] Build Page 2 — Sleep Analytics
- [ ] Build Page 3 — Activity & Movement
- [ ] Build Page 4 — Wellbeing Trends
- [ ] Build Page 5 — Engagement Analytics
- [ ] Add Deneb custom visuals
- [ ] Performance optimization

### Phase 5 — Documentation & Publishing
- [ ] Write README (product spec style)
- [ ] Create data model diagram
- [ ] Write technical design doc
- [ ] Take screenshots of all pages
- [ ] Push to GitHub
- [ ] Add to LinkedIn Featured
- [ ] Update portfolio projects-plan.md

---

## Certifications to Pursue in Parallel

| Cert | Why | Priority |
|---|---|---|
| PL-300: Power BI Data Analyst | Already in progress | 🔴 High |
| DP-605: Develop Reports with Power BI | Required for KONE BI Product Designer | 🟡 Medium |
| DP-600: Fabric Analytics Engineer | Required for KONE BI Product Designer | 🟡 Medium |

---

## Session Log

| Date | What was done |
|---|---|
| 21.05.2026 | Project created. Strategic context defined. Personas, user stories, data architecture, phases documented. |

---

## Notes for Next Session

**Start here:** Phase 1 → wireframes.
Options:
1. Sketch wireframes in PowerPoint (quick, shareable)
2. Use Figma (more realistic, shows UX skill)

Then move to Phase 2 — `generate_data.py`.
