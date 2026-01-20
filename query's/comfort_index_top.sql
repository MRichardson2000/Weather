SELECT
    date,
    temperature_2m,
    relative_humidity_2m,
    comfort_index
FROM weather
ORDER BY comfort_index DESC
LIMIT 10;
