from pathlib import Path
from typing import Any
from math import ceil, floor
from dateutil import parser
import json

JSON_DATA = Path(__file__).parent / "data.json"


class Weather:
    def __init__(self, json_file: Path = JSON_DATA) -> None:
        self.json_file = json_file

    def read_json(self) -> dict[str, Any]:
        with open(self.json_file, "r", encoding="utf-8", newline="") as f:
            data = json.load(f)
            return data

    def get_coordinates(self) -> dict[str, Any]:
        data = self.read_json()
        cords = data.get("coordinates")
        if cords is not None:
            return cords
        else:
            return {}

    def set_coordinates(self) -> list[float]:
        lst: list[float] = []
        data = self.get_coordinates()
        exclusions = ["elevation", "utc_offset_seconds"]
        for k, v in data.items():
            if k not in exclusions:
                if v + 0.5 > 53:
                    lst.append(ceil(v))
                else:
                    lst.append(floor(v))
        return lst

    def get_dates(self) -> list[str]:
        data = self.read_json()
        date = data["hourly"]["date"]
        return date

    def set_dates(self) -> list[str]:
        dates = []
        data = self.get_dates()
        for x in data:
            d = parser.parse(x)
            dates.append(d.strftime("%Y-%m-%d %H:%M%S").replace(":0000", ":00:00"))
        return dates

    def get_temperature(self) -> list[str]:
        data = self.read_json()
        temp = data["hourly"]["temperature_2m"]
        return temp

    def set_temperature(self) -> list[str]:
        temps = []
        data = self.get_temperature()
        for x in data:
            temps.append(round(x, 2))
        return temps

    def find_date_of_first_0_temp(self) -> str:
        data = self.set_temperature()
        index_val = data.index(-0.1)
        date = self.set_dates()
        return date[index_val]

    def get_wind_speeds(self) -> list[str]:
        tidied_speeds = []
        data = self.read_json()
        wind_speeds = [x for x in data["hourly"]["wind_speed_180m"]]
        for x in wind_speeds:
            tidied_speeds.append(round(x, 2))
        return tidied_speeds


def main():
    weather_data = Weather()
    print(weather_data.get_wind_speeds())


if __name__ == "__main__":
    main()
