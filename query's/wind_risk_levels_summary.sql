SELECT
    CASE 
        WHEN wind_risk < 0.3 THEN 'Low'
        WHEN wind_risk < 0.6 THEN 'Moderate'
        ELSE 'High'
    END AS risk_level,
    COUNT(*) AS observations
FROM weather
GROUP BY risk_level
ORDER BY observations DESC;
