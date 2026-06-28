SELECT 
    "City",
    "2023 Accidents" AS accidents_2023,
    "2023 Killed" AS killed_2023,
    ROUND(
        "2023 Killed"::NUMERIC / NULLIF("2023 Accidents"::NUMERIC, 0), 4
    ) AS fatality_rate,
    "2023 Ranking Accidents" AS accident_rank,
    "2023 Ranking Killed" AS fatality_rank,
    "2023 Ranking Killed" - "2023 Ranking Accidents" AS rank_gap
FROM large_cities
WHERE "2023 Accidents" > 200
ORDER BY fatality_rate DESC
LIMIT 10;