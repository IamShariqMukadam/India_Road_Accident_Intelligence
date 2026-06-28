-- Top 10 states by fatality rate per accident (2024)
-- Key insight: normalized risk, NOT raw accident count
SELECT
    state,
    accidents,
    fatalities,
    ROUND(fatality_rate_per_accident::NUMERIC, 4) AS fatality_rate,
    RANK() OVER (ORDER BY fatality_rate_per_accident DESC) AS risk_rank
FROM state_master
WHERE year = 2024
  AND accidents > 500
ORDER BY fatality_rate_per_accident DESC
LIMIT 10;