-- National summary 2019-2024 (use for KPI cards in Power BI)
SELECT
    year,
    SUM(accidents)  AS total_accidents,
    SUM(fatalities) AS total_fatalities,
    ROUND(
        (SUM(fatalities) / NULLIF(SUM(accidents), 0))::NUMERIC, 4
    ) AS national_fatality_rate
FROM state_master
GROUP BY year
ORDER BY year;