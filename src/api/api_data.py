import requests
from typing import Any


class ApiData:
    def __init__(self) -> None:
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params: dict[str, Any] = {
            "latitude": 53.8679,
            "longitude": -1.9066,
            "hourly": "temperature_2m",
            "timezone": "auto",
        }

    def get_data(self) -> Any:
        response = requests.get(self.url, params=self.params)
        response.raise_for_status()
        data = response.json()
        return data


def main() -> None:
    api = ApiData()
    data = api.get_data()
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    for t, temp in zip(times[:5], temps[:5]):
        print(f"{t}: {temp}°C")


if __name__ == "__main__":
    main()
