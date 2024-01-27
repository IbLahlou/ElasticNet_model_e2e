from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
import json
from google.cloud import storage
import pandas as pd
import zipfile
from io import BytesIO
import json
    
default_args = {
     'owner': 'Macmillan',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'upload_csv_to_gcs',
    default_args=default_args,
    description='A simple DAG to do updates to google cloud daily',
    schedule_interval=timedelta(days=1),  # You can adjust the interval as needed
    
)

def upload_csv_to_gcs(**kwargs):
    # Load CSV data (replace 'your_file.csv' with your actual file path)
    csv_data = pd.read_csv('/opt/airflow/dags/winequality-red.csv')
    
    remote_file_name = 'winequality-red1'
    
    bucket_name = 'wine_data_buckets'

    # Convert DataFrame to CSV string

    csv_file_path = '/opt/airflow/dags/output_file.csv'

    csv_buffer = BytesIO()

    # Export the DataFrame to CSV and write to the BytesIO buffer
    csv_data.to_csv(csv_buffer, index=False)

    # Create a zip file
    zip_file_path = '/opt/airflow/dags/winequality-red1.zip'

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        # Add the CSV data to the zip file
        zipf.writestr('winequality-red1.csv', csv_buffer.getvalue())

    # Optionally, you can close the BytesIO buffer
    csv_buffer.close()

    credentials_file_path = '/opt/airflow/config/credentials.json'

    with open(credentials_file_path, 'r') as f:
        credentials = json.load(f)
     # Create a client using the credentials

    client = storage.Client.from_service_account_info(credentials)

    # Get a reference to the bucket

    bucket = client.get_bucket(bucket_name)

    # Replace 'local-file.txt' with the path to the file on your local machine that you want to upload
    local_file_path = '/opt/airflow/dags/winequality-red1.zip'

    # Upload the file to the bucket
    blob = bucket.blob(remote_file_name)

    blob.upload_from_filename(local_file_path)

    print(f"File {local_file_path} uploaded to {bucket_name}/{remote_file_name}")


upload_csv_to_gcs= PythonOperator(
    task_id='upload_csv_to_gcs',
    python_callable=upload_csv_to_gcs,
    dag=dag,
)

# Define the end task (DummyOperator in this case)
end = DummyOperator(task_id='end', dag=dag)


upload_csv_to_gcs >> end
