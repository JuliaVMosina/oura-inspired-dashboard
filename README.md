# Oura Health Intelligence Dashboard

> Power BI · DAX · Deneb (Vega-Lite) · DBT · Python · Dark Theme

A health and activity analytics dashboard inspired by the Oura Ring app's visual language.
Built as a BI product — design-first, documented, and Fabric-ready.

---

## Overview

This project demonstrates the full BI product design cycle:
**discovery → UX design → data architecture → development → documentation**

| | |
|---|---|
| **Tool** | Power BI Desktop (Fabric-ready semantic model) |
| **Theme** | Dark — `#1A1A2E` background, gold/amber accents |
| **Data** | Synthetic data generated with Python |
| **Visuals** | Deneb (Vega-Lite) custom visuals |
| **Modeling** | DBT Core (staging → intermediate → marts) |

---

## Dashboard Pages

| # | Page | What it shows |
|---|---|---|
| 1 | **Personal Overview** | Daily readiness, sleep, and activity scores · today's summary vs 7-day avg |
| 2 | **Sleep Analytics** | Sleep stages, duration trends, score distribution, sleep timing |
| 3 | **Activity & Movement** | Steps vs goal, calorie burn, activity zones, workout detection |
| 4 | **Wellbeing Trends** | HRV trend, resting HR, body temperature deviation — long-term patterns |
| 5 | **Engagement Analytics** | Feature usage, goal completion rates, DAU trend · product analytics lens |

---

## Data Architecture

Star schema with `daily_scores` as the central fact table.

| Table | Description |
|---|---|
| `users` | User profiles: age, gender, membership start, device model |
| `daily_scores` | Readiness, sleep, activity scores by day per user |
| `sleep_sessions` | Duration, stages (deep/REM/light/awake), timing, score |
| `activity_sessions` | Steps, calories, active zones, workout sessions |
| `hrv_metrics` | HRV, resting HR, body temperature by day |
| `app_engagement` | Feature views, goal completions, notification interactions |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data generation | Python (pandas, numpy, faker) |
| Data transformation | DBT Core |
| Semantic model | Power BI (star schema, DAX measures) |
| Custom visuals | Deneb (Vega-Lite) |
| Design | Figma (wireframes + custom backgrounds) |
| Theme | Custom Power BI theme JSON |
| Version control | GitHub |

---

## Color Palette

| Color | Hex | Usage |
|---|---|---|
| Background | `#1A1A2E` | Page background |
| Surface | `#16213E` | Card backgrounds |
| Accent gold | `#C8963E` | Primary KPIs, highlights |
| Accent amber | `#E8A838` | Secondary accents |
| Success green | `#4CAF50` | Good scores (≥ 75) |
| Warning orange | `#FF9800` | Medium scores (50–74) |
| Alert red | `#F44336` | Low scores (< 50) |
| Text primary | `#FFFFFF` | Headings |
| Text secondary | `#B0B8C1` | Labels, subtitles |

---

## Project Status

- [x] Discovery & design — personas, user stories, data architecture
- [x] Wireframe specification (Figma)
- [ ] Data generation (`python/generate_data.py`)
- [ ] DBT models
- [ ] Power BI semantic model + DAX
- [ ] Dashboard pages (5)
- [ ] Deneb custom visuals
- [ ] Documentation

---

## Design Principles

- **Design-first:** wireframes in Figma before any Power BI work
- **User-centric:** defined personas and user stories drive visual decisions
- **Custom visuals:** Deneb (Vega-Lite), custom backgrounds, consistent dark theme
- **Documented:** data model diagram, technical design doc, this README
- **Fabric-ready:** semantic model architecture aligned with Microsoft Fabric

---

*Inspired by the Oura Ring app visual language. Not an official Oura product.*
