# Importing constants and utility functions from the WineX package
from WineX.constants import *
from WineX.utils.common import read_yaml, create_directories
from WineX.entity.config_entity import DataIngestionConfig


# ConfigurationManager class for managing configurations
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        # Reading configuration, parameters, and schema from YAML files
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        # Creating necessary directories
        create_directories([self.config.artifacts_root])

    # Method to get the data ingestion configuration
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        # Creating necessary directories
        create_directories([config.root_dir])

        # Creating a DataIngestionConfig object
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config