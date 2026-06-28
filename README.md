<div align="center">

<br>

# 🚗💥 India Road Accident Intelligence
## *487,707 accidents. 177,175 deaths. One year. Most analysts just counted them.*
### *This project asked why some states kill 10x more people per crash than others.*

<br>

[![Live Maps](https://img.shields.io/badge/🗺️_OPEN_INTERACTIVE_MAP-IamShariqMukadam.github.io-E63946?style=for-the-badge)](https://IamShariqMukadam.github.io/India_Road_Accident_Intelligence/outputs/india_risk_map.html) [![Dashboard](https://img.shields.io/badge/📊_VIEW_DASHBOARD-Power_BI_Intelligence_Center-1C1C2E?style=for-the-badge)](#)

<br>

> **Data:** MoRTH 2019–2024 (Official Government Reports, not Kaggle)
> **Updated:** June 2026 — 2024 data added the month it was released

</div>

---

<br>

## The Insight That Started Everything

```
Tamil Nadu   → 67,526 accidents → 18,449 deaths   → rate: 0.27
Bihar        → 11,610 accidents →  9,347 deaths   → rate: 0.81
Kerala       → 48,834 accidents →  3,880 deaths   → rate: 0.08
```

**Tamil Nadu has 6x more accidents than Bihar. Bihar kills nearly as many people.**
**Kerala has 4x more accidents than Bihar. Kerala kills less than half as many.**

Raw accident counts — the metric every news article uses — rank Tamil Nadu as India's most dangerous state. Normalized fatality rate reveals Bihar is **10x more dangerous per crash than Kerala.** That's the gap this project is built to find.

<br>

---

## 🗺️ What It Looks Like

*Two maps. Same country. Completely different stories.*

| Fatality Rate Map *(what actually matters)* | Raw Accident Count Map *(what everyone shows)* |
|---|---|
| [![Risk Map](outputs/india_risk_map_screenshot.png)](https://IamShariqMukadam.github.io/India_Road_Accident_Intelligence/outputs/india_risk_map.html) | [![Accidents Map](outputs/india_accidents_map_screenshot.png)](https://IamShariqMukadam.github.io/India_Road_Accident_Intelligence/outputs/india_accidents_map.html) |

*Hover any state for live stats → click maps to open full interactive version*

<br>

**Power BI Intelligence Center**
<img src="outputs/dashboard_screenshot.png" width="100%" />

<br>

---

## 🔬 What The Data Actually Says

<br>

**① The time you drive matters more than where you drive**

One 3-hour window. 21% of all accidents.

```
03:00–06:00  ██░░░░░░░░░░░░░░  4.8%   ← safest
18:00–21:00  █████████████████ 21.1%  ← 102,897 accidents
```
Evening commute + low light + fatigue. Insurance companies pricing flat rates across the day are missing this.

<br>

**② Everyone blames drunk driving. The data doesn't.**

| What kills | How much |
|---|---|
| 🚗 Speeding | **68.1%** of all fatalities |
| 🍺 Drunk driving | 2.1% |
| 📱 Mobile phone | 1.7% |

Speeding kills 32x more people than drunk driving. Awareness campaigns are focused on the wrong problem.

<br>

**③ The Bihar problem is infrastructure, not behaviour**

Statistical test: does accident volume predict fatality rate per crash?

```
r = -0.086  |  p = 0.68  |  ✗ NOT SIGNIFICANT
```

Busier roads are **not** more deadly per crash. Bihar's 0.81 rate vs Kerala's 0.08 is explained by trauma care access and road quality — not driver behaviour. This matters for policy targeting.

<br>

**④ COVID was a pause, not a turning point**

```
2020  ▼ 372,181 accidents    (lockdown dip)
2021  ▲ 412,432              (bounce back)
2022  ▲ 461,312
2023  ▲ 480,583
2024  ▲ 487,707              (+31% from 2020)
```

Fatality rate unchanged at ~0.36 for 5 consecutive years. Road safety spend went up. Outcomes didn't move.

<br>

**⑤ Where it's heading**

*Prophet model · 6 years of training data · 80% confidence*

```
2024 →  177,175 fatalities  (actual)
2025 →  188,512 forecasted  [178,166 – 198,447]
2026 →  194,481 forecasted  [184,033 – 204,429]
2027 →  ~200,000            ← crosses 2 lakh
```

<img src="outputs/forecast_chart.png" width="100%" />

<br>

---

## 📐 Statistical Layer

*Not just charts — actual hypothesis testing*

<img src="outputs/correlation_heatmap.png" width="100%" />
<img src="outputs/regression_scatter.png" width="100%" />

| Test | Result | What it means |
|---|---|---|
| Accidents ↔ Fatalities | r=0.816, p<0.0001 ✓ | Volume drives deaths at state level |
| Log(Accidents) ↔ Fatality Rate | r=-0.086, p=0.68 ✗ | Busy roads ≠ more dangerous per crash |
| YoY Accidents ↔ YoY Fatalities | r=0.533, p=0.006 ✓ | Rising accidents predict rising deaths |
| OLS slope | 0.2652 deaths/accident | Each additional accident adds 0.27 fatalities |

<br>

---

## 🏗️ Pipeline

```
MoRTH PDFs + OpenCity CSVs
        ↓
   Python cleaning
   (15 files, 6 years, 36 states)
        ↓
   PostgreSQL 16
   (10 tables, window functions, CTEs)
        ↓
        ├── Folium → 2 interactive India maps
        ├── Prophet → fatality forecast 2025–2027
        ├── scipy + statsmodels → correlation + OLS regression
        └── Power BI → Intelligence Center dashboard
```

```
India_Road_Accident_Intelligence/
├── notebooks/
│   ├── 01_clean_merge.ipynb          ← data pipeline
│   ├── 02_geospatial_map.ipynb       ← folium maps
│   ├── 03_forecasting.ipynb          ← prophet model
│   └── 04_correlation_regression.ipynb
├── sql/
│   ├── 01_state_risk_ranking.sql
│   ├── 02_yoy_fatality_trend.sql
│   ├── 03_national_trend.sql
│   ├── 04_time_of_day_peak.sql
│   └── 05_violation_fatality_share.sql
├── data/raw/                         ← 15 MoRTH source files
└── outputs/                          ← maps, charts, dashboard
```

<details>
<summary>Run it yourself</summary>

```bash
git clone https://github.com/IamShariqMukadam/India_Road_Accident_Intelligence
cd India_Road_Accident_Intelligence
pip install pandas numpy matplotlib seaborn folium geopandas \
            prophet scipy statsmodels sqlalchemy psycopg2-binary

# PostgreSQL setup
sudo -u postgres psql -c "CREATE DATABASE road_accident_db;"

# Run notebooks 01 → 04 in order
```

</details>

<br>

---

## Who This Is For

This project targets the exact domain where most DA hiring happens in India:

**Insurance** — ACKO, Digit, Bajaj Allianz, HDFC Ergo → risk pricing, telematics, UBI products

**Logistics & Rideshare** — Delhivery, Ola, Porter, Rapido → fleet safety, route risk scoring

**Consulting** — Deloitte, EY, McKinsey → government road safety mandates, BFSI clients

<br>

---

<div align="center">

**Shariq Mukadam** · Pune · BCA Final Year

[![GitHub](https://img.shields.io/badge/GitHub-IamShariqMukadam-181717?style=flat-square&logo=github)](https://github.com/IamShariqMukadam)

*All data sourced from official MoRTH government publications. No Kaggle. No synthetic data.*

⭐ Star if useful

</div>
