<div align="center">

# 🚨 India Road Accident Pattern Intelligence
### *Bihar's roads are 10x more deadly than Kerala's. Raw accident counts hide this completely.*
### *This project finds what headline statistics miss.*

<br>

<div align="center">
<table width="100%">
<tr>
<td align="center" width="25%">📅<br><b>6 years</b><br><sub>2019 – 2024</sub></td>
<td align="center" width="25%">🗂️<br><b>15 datasets</b><br><sub>MoRTH · OpenCity · PDF</sub></td>
<td align="center" width="25%">🗄️<br><b>10 SQL tables</b><br><sub>PostgreSQL 16</sub></td>
<td align="center" width="25%">📊<br><b>4 analysis modules</b><br><sub>Maps · Forecast · Stats · BI</sub></td>
</tr>
</table>
</div>

<br>

[![Dashboard](https://img.shields.io/badge/📊%20VIEW%20DASHBOARD-POWER%20BI%20→-FFFFFF?style=for-the-badge&labelColor=1C1C2E&color=FFFFFF)](outputs/Pasted%20image.png) [![Maps](https://img.shields.io/badge/🗺️%20LIVE%20MAPS-GITHUB%20PAGES%20→-FFFFFF?style=for-the-badge&labelColor=E63946&color=FFFFFF)](https://IamShariqMukadam.github.io/India_Road_Accident_Intelligence/outputs/india_risk_map.html)

</div>

<br>

---

## 📸 Dashboard Preview

### 🧠 Intelligence Center — *KPIs, risk ranking, state monitor*
<img src="outputs/dashboard_screenshot.png" width="100%" />

### 🗺️ India Risk Map — *Normalized fatality rate by state*
<img src="outputs/india_risk_map_screenshot.png" width="100%" />

### 📉 Forecast — *Prophet model 2025–2027*
<img src="outputs/forecast_chart.png" width="100%" />

### 🔥 Correlation Matrix — *Statistical relationships*
<img src="outputs/correlation_heatmap.png" width="100%" />

### 📐 Regression Analysis — *OLS scatter plots, all states labeled*
<img src="outputs/regression_scatter.png" width="100%" />

---

## 🗄️ Data Sources

![Source](https://img.shields.io/badge/Source-Government%20Data%20Only-success?style=for-the-badge)
![Kaggle](https://img.shields.io/badge/Kaggle-Not%20Used-red?style=for-the-badge)
![Synthetic](https://img.shields.io/badge/Synthetic%20Data-None-red?style=for-the-badge)

| Dataset | Source | Coverage |
|---|---|---|
| State-wise accidents & fatalities | OpenCity (MoRTH structured) | 36 states, 2019–2023 |
| **2024 state-wise data** | **Manually extracted from MoRTH 2024 PDF — Table 5.1 & 5.6** | 36 states, 2024 |
| **Time-of-day accident slabs** | **Manually extracted from MoRTH 2024 PDF — Table 7.3** | 8 slabs, 2020–2024 |
| Violation type fatalities | OpenCity (MoRTH structured) | 6 categories, 2023 |
| Road user fatalities | OpenCity (MoRTH structured) | 10 categories, 2023 |
| Large cities accident data | OpenCity (MoRTH structured) | 51 cities, 2023 |
| Vehicle & road density | OpenCity (MoRTH structured) | National trend |

> ⚠️ 2024 data was incorporated the **same month** the MoRTH report was publicly released (June 2026) — making this the most current public analysis of India road accidents available.

**Primary source:** Ministry of Road Transport & Highways — *"Road Accidents in India"* reports, 2019–2024. [morth.gov.in](https://morth.gov.in)

---

<div align="center">

## ⚡ The Numbers That Matter

<table>
<tr>
<td align="center" width="12.5%"><h2>4,87,707</h2><b>Accidents in 2024</b><br><sub>+1.5% over 2023</sub></td>
<td align="center" width="12.5%"><h2>1,77,175</h2><b>Fatalities in 2024</b><br><sub>+2.5% over 2023</sub></td>
<td align="center" width="12.5%"><h2>10x</h2><b>Risk gap</b><br><sub>Bihar vs Kerala</sub></td>
<td align="center" width="12.5%"><h2>68.1%</h2><b>Deaths from speeding</b><br><sub>Not drunk driving</sub></td>
</tr>
<tr>
<td align="center"><h2>21.1%</h2><b>Accidents at 18–21hrs</b><br><sub>Deadliest time window</sub></td>
<td align="center"><h2>+31%</h2><b>Post-COVID surge</b><br><sub>2020 → 2024</sub></td>
<td align="center"><h2>0.3633</h2><b>National fatality rate</b><br><sub>Deaths per accident</sub></td>
<td align="center"><h2>2 lakh</h2><b>Projected by 2026–27</b><br><sub>Prophet forecast</sub></td>
</tr>
</table>

</div>

---

## 🔍 6 Findings That Tell the Real Story

### ![01](https://img.shields.io/badge/01-22c55e?style=flat-square) Raw Accident Count Is a Misleading Safety Metric

> Tamil Nadu has 67,526 accidents in 2024 — the most in India. Bihar has only 11,610. So Tamil Nadu is more dangerous, right?

**Wrong.** When we normalize by fatality rate (deaths per accident):

| State | Accidents | Fatality Rate | Risk Rank |
|---|---|---|---|
| Tamil Nadu | 67,526 | 0.2732 | #23 |
| Bihar | 11,610 | **0.8051** | **#1** |
| Kerala | 48,834 | 0.0795 | #36 (safest) |

Bihar kills someone in **8 out of 10 accidents.** Tamil Nadu kills in 3 out of 10. Kerala in less than 1 out of 10.

---

### ![02](https://img.shields.io/badge/02-3b82f6?style=flat-square) The 18:00–21:00 Window Kills More Than Any Other

> One 3-hour window accounts for 1 in 5 of all road accidents in India.

```
06:00–09:00  ████████░░░░░░░░░░░░░░░░░░░░░░  10.1%
09:00–12:00  ████████████░░░░░░░░░░░░░░░░░░  14.0%
12:00–15:00  ████████████░░░░░░░░░░░░░░░░░░  14.6%
15:00–18:00  ██████████████░░░░░░░░░░░░░░░░  17.4%
18:00–21:00  █████████████████░░░░░░░░░░░░░  21.1%  ← PEAK
21:00–24:00  █████████░░░░░░░░░░░░░░░░░░░░░  11.5%
00:00–03:00  ████░░░░░░░░░░░░░░░░░░░░░░░░░░   5.1%
03:00–06:00  ████░░░░░░░░░░░░░░░░░░░░░░░░░░   4.8%  ← SAFEST
```

---

### ![03](https://img.shields.io/badge/03-f59e0b?style=flat-square) The Real Killer Is Speed, Not Drunk Driving

| Cause | Fatalities (2023) | Share |
|---|---|---|
| **Over-speeding** | **1,17,682** | **68.07%** |
| Others | 38,400 | 22.21% |
| Wrong side / Lane indiscipline | 9,432 | 5.46% |
| Drunk driving | 3,674 | 2.13% |
| Mobile phone use | 2,884 | 1.67% |
| Jumping red light | 818 | 0.47% |

Over-speeding kills **32x more people than drunk driving.**

---

### ![04](https://img.shields.io/badge/04-ef4444?style=flat-square) Bihar's Roads Have a Trauma Care Problem, Not Just a Speeding Problem

OLS regression — Log(Accidents) vs fatality rate: **r = -0.086, p = 0.68 — not significant.**
Busier roads are not more dangerous per crash. Bihar's crisis is infrastructure and trauma care access.

**Accidents vs Fatalities: r = 0.816, p < 0.0001 ✓**

---

### ![05](https://img.shields.io/badge/05-a855f7?style=flat-square) COVID Caused a Dip, But India Is Now On a Steeper Trajectory

| Year | Accidents | Fatalities |
|---|---|---|
| 2019 | 4,56,959 | 1,58,984 |
| 2020 | 3,72,181 | 1,38,383 |
| 2021 | 4,12,432 | 1,53,972 |
| 2022 | 4,61,312 | 1,68,491 |
| 2023 | 4,80,583 | 1,72,890 |
| 2024 | **4,87,707** | **1,77,175** |

National fatality rate stuck at ~0.36 for 5 consecutive years.

---

### ![06](https://img.shields.io/badge/06-06b6d4?style=flat-square) India Is On Track to Cross 2 Lakh Fatalities by 2026–27

| Year | Accident Forecast | Fatality Forecast |
|---|---|---|
| 2025 | 5,13,042 [4,69,290–5,55,542] | 1,88,512 [1,78,166–1,98,447] |
| 2026 | 5,28,118 [4,86,715–5,67,928] | **1,94,481 [1,84,033–2,04,429]** |
| 2027 | ~5,43,000 | **~2,00,000** |

---

## 🛠️ Tech Stack

**Languages**

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-FF6F00?style=for-the-badge&logo=postgresql&logoColor=white)

**Data & Analysis**

![Pandas](https://img.shields.io/badge/PANDAS-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SCIPY-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Prophet](https://img.shields.io/badge/PROPHET-FF6F61?style=for-the-badge)

**Geospatial**

![Folium](https://img.shields.io/badge/FOLIUM-77B829?style=for-the-badge)
![GeoPandas](https://img.shields.io/badge/GEOPANDAS-139C5A?style=for-the-badge)

**Database & BI**

![PostgreSQL](https://img.shields.io/badge/POSTGRESQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/POWER%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

---

## 🏗️ How It Was Built

```
📥 RAW DATA            🔧 PYTHON PIPELINE           🗄️ POSTGRESQL         📊 OUTPUT
───────────────        ──────────────────────        ──────────────        ──────────────
15 MoRTH CSVs    →    01_clean_merge.ipynb     →    state_master     →    Power BI Dashboard
PDF (2024 data)  →    02_geospatial_map.ipynb  →    time_of_day      →    India Risk Maps
Time-of-day PDF  →    03_forecasting.ipynb     →    violation_type   →    Forecast Charts
36 states        →    04_correlation.ipynb     →    large_cities     →    Correlation Matrix
6 years          →    5 SQL queries            →    10 tables total  →    Regression Plots
```

### 📁 Project Structure

```
India_Road_Accident_Intelligence/
├── 📂 data/
│   ├── raw/                    ← 15 original source CSVs (MoRTH + PDF extracts)
│   └── cleaned/                ← Processed tables ready for PostgreSQL
├── 📂 notebooks/
│   ├── 01_clean_merge.ipynb
│   ├── 02_geospatial_map.ipynb
│   ├── 03_forecasting.ipynb
│   └── 04_correlation_regression.ipynb
├── 📂 sql/
│   ├── 01_state_risk_ranking.sql
│   ├── 02_yoy_fatality_trend.sql
│   ├── 03_national_trend.sql
│   ├── 04_time_of_day_peak.sql
│   └── 05_violation_fatality_share.sql
├── 📂 outputs/
│   ├── india_risk_map.html
│   ├── india_accidents_map.html
│   ├── forecast_chart.png
│   ├── correlation_heatmap.png
│   ├── regression_scatter.png
│   └── state_fatality_trends.png
└── README.md
```

<details>
<summary><b>⚙️ Reproduce This Project</b></summary>

```bash
git clone https://github.com/IamShariqMukadam/India_Road_Accident_Intelligence
cd India_Road_Accident_Intelligence
python -m venv venv && source venv/bin/activate
pip install pandas numpy matplotlib seaborn sqlalchemy psycopg2-binary \
            folium geopandas requests prophet scipy statsmodels

sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE road_accident_db;"

# Run notebooks in order 01 → 04
# Run SQL queries
psql -U postgres -h localhost -d road_accident_db -f sql/01_state_risk_ranking.sql
```

</details>

---

## 💡 Business Applications

**Insurance (ACKO, Digit, Bajaj Allianz, HDFC Ergo)**
- Bihar/Jharkhand/Punjab flagged as highest-risk for telematics-based premium pricing
- 18:00–21:00 window → time-of-day risk loading for commercial vehicle policies

**Logistics & Fleet (Delhivery, Blue Dart, Porter, Ola, Rapido)**
- Fatality rate normalization identifies true high-risk corridors vs high-volume ones
- YoY trend analysis for proactive fleet safety routing

**Consulting (Deloitte, EY, McKinsey)**
- Prophet forecast supports 2025–2027 road safety budget allocation
- State cluster segmentation for intervention targeting

---

<div align="center">

**Built on Verified Government Data by Shariq Mukadam**
📍 Pune, Maharashtra | BCA Final Year

[![GitHub](https://img.shields.io/badge/GitHub-IamShariqMukadam-181717?style=for-the-badge&logo=github)](https://github.com/IamShariqMukadam)

*If this repo helped you, give it a ⭐*

</div>
