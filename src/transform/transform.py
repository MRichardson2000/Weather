from __future__ import annotations
import logging
import pandas as pd
from typing import Any
from src.extract.api import Api

api = Api()


class Transform:
    def __init__(self, data: dict[str, Any] = api.get_data()) -> None:
        self.data = data

    def create_df(self, data) -> pd.DataFrame:
        return pd.DataFrame(data["hourly"])

    def clean_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = df["date"].dt.tz_localize(None)
        return df

    def round_columns(self, df: pd.DataFrame, round_num: int = 1) -> pd.DataFrame:
        df["temperature_2m"] = df["temperature_2m"].round(round_num)
        df["dew_point_2m"] = df["dew_point_2m"].round(round_num)
        df["apparent_temperature"] = df["apparent_temperature"].round(round_num)
        df["pressure_msl"] = df["pressure_msl"].round(round_num)
        df["surface_pressure"] = df["surface_pressure"].round(round_num)
        df["vapour_pressure_deficit"] = df["vapour_pressure_deficit"].round(round_num)
        df["et0_fao_evapotranspiration"] = df["et0_fao_evapotranspiration"].round(
            round_num
        )
        df["wind_speed_180m"] = df["wind_speed_180m"].round(round_num)
        df["wind_direction_180m"] = df["wind_direction_180m"].round(round_num)
        df["wind_gusts_10m"] = df["wind_gusts_10m"].round(round_num)
        df["temperature_180m"] = df["temperature_180m"].round(round_num)
        df["soil_temperature_54cm"] = df["soil_temperature_54cm"].round(round_num)
        df["soil_moisture_27_to_81cm"] = df["soil_moisture_27_to_81cm"].round(round_num)
        return df

    def get_temperature_average(self, df: pd.DataFrame, hour: int = 3) -> pd.DataFrame:
        df[f"temp_{hour}_hour_average"] = df["temperature_2m"].rolling(hour).mean()
        return df

    def get_humidity_average(self, df: pd.DataFrame, hour: int = 6) -> pd.DataFrame:
        df[f"humidity_{hour}_hour_average"] = (
            df["relative_humidity_2m"].rolling(hour).mean()
        )
        return df

    def get_temp_deltas(self, df: pd.DataFrame) -> pd.DataFrame:
        df["temp_change"] = df["temperature_2m"].diff()
        return df

    def get_day_or_night(self, df: pd.DataFrame) -> pd.DataFrame:
        df["hour"] = df["date"].dt.hour
        df["is_daytime"] = df["hour"].between(6, 18).astype(int)
        df["is_nighttime"] = ((df["hour"] >= 19) | (df["hour"] <= 5)).astype(int)
        return df

    def cold_or_warm_temp(self, df: pd.DataFrame) -> pd.DataFrame:
        df["is_colder"] = df["apparent_temperature"] < df["temperature_2m"].astype(int)
        df["is_warmer"] = df["apparent_temperature"] > df["temperature_2m"].astype(int)
        return df

    def wind_direction_options(self, deg: float) -> str:
        directions: list[str] = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        ix: int = int((deg + 22.5) // 45) % 8
        return directions[ix]

    def get_wind_direction(self, df: pd.DataFrame) -> pd.DataFrame:
        df["wind_direction"] = df["wind_direction_180m"].apply(
            self.wind_direction_options
        )
        return df

    def get_wind_risk_index(self, df: pd.DataFrame) -> pd.DataFrame:
        df["wind_risk"] = (
            df["wind_speed_180m"] * 0.6 + df["wind_gusts_10m"] * 0.4
        ).round(1)
        return df

    def get_precipitation_flag(self, df: pd.DataFrame) -> pd.DataFrame:
        df["is_rain"] = (df["precipitation"] > 0).astype(int)
        df["is_snow"] = (df["snow_depth"] > 0).astype(int)
        return df

    def get_comfort_index(self, df: pd.DataFrame) -> pd.DataFrame:
        df["comfort_index"] = (
            (df["temperature_2m"] * -0.1).round(1)
            + (df["relative_humidity_2m"] * -0.03).round(1)
            + (df["wind_speed_180m"] * -0.02).round(1)
        )
        return df

    def visibility(self, df: pd.DataFrame) -> pd.DataFrame:
        df["visibility_norm"] = (df["visibility"] - df["visibility"].min()) / (
            df["visibility"].max() - df["visibility"].min()
        )
        df["visibility_norm"] = df["visibility_norm"].round(1)
        return df

    def daily_aggregations(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.resample("D", on="date").agg(
            {
                "temperature_2m": ["mean", "max", "min"],
                "precipitation": "sum",
                "wind_speed_180m": "mean",
                "relative_humidity_2m": "mean",
            }
        )

    def transformation(self) -> pd.DataFrame:
        try:
            df = self.create_df(self.data)
            df = self.clean_dates(df)
            df = self.round_columns(df)
            df = self.get_temperature_average(df)
            df = self.get_humidity_average(df)
            df = self.get_temp_deltas(df)
            df = self.get_day_or_night(df)
            df = self.cold_or_warm_temp(df)
            df = self.get_wind_direction(df)
            df = self.get_wind_risk_index(df)
            df = self.get_precipitation_flag(df)
            df = self.get_comfort_index(df)
            df = self.visibility(df)
            return df
        except Exception as e:
            logging.error(f"Transform step failed: {e}")
            raise


def main() -> None:
    transform = Transform()
    df = transform.transformation()
    print("Transformation Complete!")
    print(df.head())


if __name__ == "__main__":
    main()
