import logging
from src.extract.api import Api
from src.transform.transform import Transform
from src.load.db_load import DatabaseLoad
from src.logging_config import setup_logging


def run_pipeline() -> None:
    setup_logging()
    logging.info("Pipeline has begun!")
    try:
        logging.info("Beginning extraction of data")
        api = Api()
        data = api.get_data()
        logging.info("Extraction successful!")
        logging.info("Beginning Transformation - hold onto your...whatever you want :p")
        transform = Transform(data)
        df = transform.transformation()
        logging.info(f"Transform step completed - {len(df)} rows processed")
        logging.info("Loading into the database, oooo spooky :o")
        load = DatabaseLoad()
        load.load_to_sqlite(df)
        logging.info("Data has been loaded successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
