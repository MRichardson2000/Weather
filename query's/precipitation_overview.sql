SELECT
    SUM(is_rain) AS rain_hours,
    SUM(is_snow) AS snow_hours,
    SUM(precipitation) AS total_precipitation
FROM weather;
