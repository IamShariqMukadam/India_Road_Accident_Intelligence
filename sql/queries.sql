-- ================================================================
-- ROAD ACCIDENT INTELLIGENCE — SQL Queries
-- Run in pgAdmin or DBeaver after Day 1 pipeline completes
-- NOTE: Adjust column names if your print output showed different names
-- ================================================================

-- 1. States with highest fatality rate per accident (2024) — your key insight
--    This is NOT the same as states with highest raw accidents
SELECT 
    state,
    accidents,
    fatalities,
    ROUND(fatality_rate_per_accident::NUMERIC, 4) AS fatality_rate,
    RANK() OVER (ORDER BY fatality_rate_per_accident DESC) AS risk_rank
FROM state_master
WHERE year = 2024 AND accidents > 500  -- exclude tiny UTs with noisy rates
ORDER BY fatality_rate_per_accident DESC
LIMIT 10;

-- 2. YoY fatality change per state (window function) — who improved, who worsened
SELECT 
    state,
    year,
    fatalities,
    fatalities - LAG(fatalities) OVER (PARTITION BY state ORDER BY year) AS yoy_change,
    ROUND(
        100.0 * (fatalities - LAG(fatalities) OVER (PARTITION BY state ORDER BY year))
        / NULLIF(LAG(fatalities) OVER (PARTITION BY state ORDER BY year), 0), 2
    ) AS yoy_pct_change
FROM state_master
WHERE year BETWEEN 2020 AND 2024
ORDER BY state, year;

-- 3. National trend summary 2019-2024 (use in KPI cards)
SELECT 
    year,
    SUM(accidents) AS total_accidents,
    SUM(fatalities) AS total_fatalities,
    ROUND(SUM(fatalities)::NUMERIC / NULLIF(SUM(accidents), 0), 4) AS national_fatality_rate
FROM state_master
GROUP BY year
ORDER BY year;

-- 4. Time of day peak analysis — your differentiator (uses 2024 data from PDF)
SELECT 
    time_interval,
    time_type,
    "2024_accidents",
    "2024_pct",
    RANK() OVER (ORDER BY "2024_accidents" DESC) AS danger_rank
FROM time_of_day
WHERE time_interval != 'Unknown'
ORDER BY "2024_accidents" DESC;

-- 5. Top 15 cities by accidents 2023 with killed ranking comparison
SELECT 
    "City",
    "2023 Accidents",
    "2023 Killed",
    "2023 Ranking Accidents",
    "2023 Ranking Killed",
    -- Gap between accident rank and fatality rank: positive = more deadly than accident count suggests
    "2023 Ranking Accidents" - "2023 Ranking Killed" AS rank_gap
FROM large_cities
ORDER BY "2023 Accidents" DESC
LIMIT 15;

-- 6. Violation type contribution to fatalities 2023 (window for %)
SELECT 
    "Category",
    "2023-Killed",
    ROUND(100.0 * "2023-Killed" / SUM("2023-Killed") OVER (), 2) AS pct_of_total_fatalities
FROM violation_type
ORDER BY "2023-Killed" DESC;
