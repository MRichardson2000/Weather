from pathlib import Path
import json
from typing import Any
from math import ceil, floor

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
        data = self.get_dates()
        return data


    def get_temperature(self) -> list[str]:
        data = self.read_json()
        temp = data["hourly"]["temperature_2m"]
        return temp


def main():
    weather_data = Weather()
    print(weather_data.get_dates())


if __name__ == "__main__":
    main()
