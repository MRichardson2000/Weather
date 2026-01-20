SELECT 
    date,
    temperature_2m AS temperature,
    apparent_temperature,
    comfort_index
FROM weather
ORDER BY temperature_2m DESC
LIMIT 10;
