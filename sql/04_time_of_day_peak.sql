-- Accident peak by time slab 2024 (differentiator insight)
SELECT
    time_interval,
    time_type,
    "2024_accidents",
    "2024_pct",
    RANK() OVER (ORDER BY "2024_accidents" DESC) AS danger_rank
FROM time_of_day
WHERE time_interval != 'Unknown'
ORDER BY "2024_accidents" DESC;