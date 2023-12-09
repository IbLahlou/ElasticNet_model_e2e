from WineX.config.configuration import ConfigurationManager
from WineX.components.data_ingestion import DataIngestion
from WineX import logger
import os

# Set your Google Cloud Storage credentials (replace with your actual credentials)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../../credentials.json"

# Replace with your Google Cloud Storage bucket and file path
bucket_name = "wine_data_buckets"
file_path = "winequality-data.zip"
local_file_path = "../../../artifacts/data_ingestion/winequality-data.zip"



STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
