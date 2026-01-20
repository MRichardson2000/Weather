from __future__ import annotations
import logging
import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
from typing import Any, cast
from datetime import datetime, timedelta, UTC


class Api:
    def __init__(
        self, latitude: float = 52.52, longitude: float = 13.41, days_ahead: int = 1
    ) -> None:
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        session = cast(requests.Session, retry_session)
        self.client = openmeteo_requests.Client(session=session)  # type: ignore
        self.url = "https://api.open-meteo.com/v1/forecast"
        today = datetime.now(UTC).date()
        self.params: dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "dew_point_2m",
                "apparent_temperature",
                "precipitation_probability",
                "precipitation",
                "snow_depth",
                "weather_code",
                "pressure_msl",
                "surface_pressure",
                "cloud_cover",
                "visibility",
                "vapour_pressure_deficit",
                "evapotranspiration",
                "et0_fao_evapotranspiration",
                "wind_speed_180m",
                "wind_direction_180m",
                "wind_gusts_10m",
                "temperature_180m",
                "soil_temperature_54cm",
                "soil_moisture_27_to_81cm",
            ],
            "timezone": "auto",
            "start_date": today.isoformat(),
            "end_date": (today + timedelta(days=days_ahead)).isoformat(),
        }

    def get_data(self) -> dict[str, Any]:
        try:
            responses = self.client.weather_api(self.url, params=self.params)
            if not responses:
                raise RuntimeError("No response from Open-Meteo API")
            response = responses[0]
            hourly = response.Hourly()
            start_time = datetime.fromtimestamp(hourly.Time(), UTC)
            end_time = datetime.fromtimestamp(hourly.TimeEnd(), UTC)
            interval = timedelta(seconds=hourly.Interval())
            dates: list[str] = []
            current = start_time
            while current < end_time:
                dates.append(current.isoformat())
                current += interval
            hourly_data: dict[str, Any] = {"date": dates}
            steps: int = len(dates)
            for i, var in enumerate(self.params["hourly"]):
                values = [hourly.Variables(i).Values(j) for j in range(steps)]
                hourly_data[var] = values
            return {
                "coordinates": {
                    "latitude": response.Latitude(),
                    "longitude": response.Longitude(),
                    "elevation": response.Elevation(),
                    "utc_offset_seconds": response.UtcOffsetSeconds(),
                },
                "hourly": hourly_data,
            }
        except Exception as e:
            logging.error(f"Extract step failed: {e}")
            raise


def main() -> None:
    api = Api()
    data = api.get_data()
    print(data)


if __name__ == "__main__":
    main()
