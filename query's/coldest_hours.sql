SELECT 
    date,
    temperature_2m AS temperature,
    apparent_temperature,
    is_colder
FROM weather
ORDER BY temperature_2m ASC
LIMIT 10;
