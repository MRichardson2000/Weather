from __future__ import annotations
import logging
import pandas as pd
import sqlite3


class DatabaseLoad:
    def __init__(self) -> None:
        pass

    def load_to_sqlite(
        self,
        df: pd.DataFrame,
        db_name: str = "db/weather.db",
        table_name: str = "weather",
    ) -> None:
        try:
            conn = sqlite3.connect(db_name)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            conn.close()
        except Exception as e:
            logging.error(f"Load step failed: {e}")
            raise
