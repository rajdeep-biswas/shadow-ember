import requests
import datetime
import json
import os

from google.cloud import storage

config = {
    "use_bucket": True
}

GCS_BUCKET_NAME = "dummy_lake_cloud"

# TODO Check "⚙️ What could be improved for “production-ready” section in https://chatgpt.com/c/690ddafa-74d4-8322-8e23-3ba0daf5bdf1 for improvements

# Figuring out date 5 years ago today because NASA's funding got cut
now = datetime.datetime.now() # TODO You already handle this well, but consider datetime.date.today() for readability. Cleaner intent when time-of-day isn’t needed.

years = 5
days_per_year = 365.24
five_years_ago = datetime.timedelta(days=(years*days_per_year))

datestamp = (now - five_years_ago).date()

# TODO Move hardcoded paths and URLs to environment variables or config file. Makes it portable and CI/CD-friendly.
# https://epic.gsfc.nasa.gov/about/api
URL = f"https://epic.gsfc.nasa.gov/api/enhanced/date/{datestamp}"

json_return = requests.get(URL).json()

if not config['use_bucket']:
    # TODO Ensure ../data_dumps exists (os.makedirs(..., exist_ok=True)). Avoids “file not found” errors on first run.
    JSON_PATH = "../data_dumps"
    fully_formed_path = os.path.join(JSON_PATH, str(datestamp) + ".json")

    # TODO if I am gonna continue using this Python code in Cloud Functions and / or Airflow, I'll have to dump this into a GCP Bucket instead of writing a local file
    with open(fully_formed_path, 'w') as json_dump_file:
        json.dump(json_return, json_dump_file)

    # TODO Replace print() with the logging module. Integrates better with Airflow or Cloud Functions logs.
    print(f"✅ Wrote JSON to local dir:", fully_formed_path)

else:
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    gcs_object = f"{datestamp}.json"
    blob = bucket.blob(gcs_object)
    
    json_string = json.dumps(json_return)

    # TODO this probably could use some improvement. source: https://docs.cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.blob.Blob#google_cloud_storage_blob_Blob_upload_from_string
    # Chat suggested to just change to content_type="application/json" // https://chatgpt.com/c/690ddafa-74d4-8322-8e23-3ba0daf5bdf1
    # He says - text/plain works fine, but "application/json" is the semantically correct MIME type, and tools that inspect the bucket later (like BigQuery or Cloud Functions triggers) will infer it as JSON automatically. So it’s not just “tidier” — it’s metadata-correct.
    blob.upload_from_string(json_string, content_type="text/plain")

    # Section "⚙️ Second: how does your Python code “magically” know which project you’re writing to?" in above linked Chat is pretty cool. For later, though.
    gcs_source_uri = f"gs://{GCS_BUCKET_NAME}/{gcs_object}"

    # TODO Replace print() with the logging module. Integrates better with Airflow or Cloud Functions logs.
    print(f"✅ Dumped JSON to GCS: {gcs_source_uri}")