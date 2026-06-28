-- Violation type contribution to fatalities 2023
-- Shows overspeeding vs drunk driving vs other causes
SELECT
    "Category",
    "2023-Killed",
    ROUND(
        100.0 * "2023-Killed" / SUM("2023-Killed") OVER (), 2
    ) AS pct_of_total_fatalities,
    RANK() OVER (ORDER BY "2023-Killed" DESC) AS rank
FROM violation_type
ORDER BY "2023-Killed" DESC;