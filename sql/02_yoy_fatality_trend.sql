-- Year-over-year fatality change per state (2019-2024)
-- Shows who improved and who worsened
SELECT
    state,
    year,
    fatalities,
    fatalities - LAG(fatalities) OVER (PARTITION BY state ORDER BY year) AS yoy_change,
    ROUND(
        (100.0 * (fatalities - LAG(fatalities) OVER (PARTITION BY state ORDER BY year))
        / NULLIF(LAG(fatalities) OVER (PARTITION BY state ORDER BY year), 0))::NUMERIC, 2
    ) AS yoy_pct_change
FROM state_master
WHERE year BETWEEN 2020 AND 2024
ORDER BY state, year;