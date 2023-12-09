from dataclasses import dataclass
from pathlib import Path

# Defining a data class for configuration related to data ingestion
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path