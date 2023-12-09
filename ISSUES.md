# ISSUES ABOUT THE PROJECT


#### Data Ingestion From GOOGLE CLOUD STORAGE

- Google Cloud Storage needs Key and credentials whichs not very useful and important in our case.

- You can use this code to ingest data from Google Cloud Storage

```python
from google.cloud import storage
import requests
import os


# Set your Google Cloud Storage credentials (replace with your actual credentials)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Replace with your Google Cloud Storage bucket and file path
bucket_name = "wine_data_buckets"
file_path = "winequality-data.zip"
local_file_path = "artifacts/data_ingestion/winequality-data.zip"

def download_from_gcs(bucket_name, file_path, local_file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    # Download the file to a local path
    blob.download_to_filename(local_file_path)
    print(f"File downloaded to {local_file_path}")

# Download the file from Google Cloud Storage
download_from_gcs(bucket_name, file_path, local_file_path)
```