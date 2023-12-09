
# Importing necessary modules
import os
import urllib.request as request
import zipfile
from dataclasses import dataclass
from pathlib import Path

# Importing logger and utility function from WineX package
from WineX import logger
from WineX.utils.common import get_size

from WineX.entity.config_entity import DataIngestionConfig


# Class for handling data ingestion operations
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    # Method to download the data file
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            # Downloading the file using urllib
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded! with the following info:\n{headers}")
        else:
            # Logging if the file already exists
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    # Method to extract the zip file
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        # Creating the unzip directory if it doesn't exist
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            # Extracting the contents of the zip file
            zip_ref.extractall(unzip_path)