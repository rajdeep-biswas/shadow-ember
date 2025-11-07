import requests
import datetime
import json
import os

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

# TODO Ensure ../data_dumps exists (os.makedirs(..., exist_ok=True)). Avoids “file not found” errors on first run.
JSON_PATH = "../data_dumps"
fully_formed_path = os.path.join(JSON_PATH, str(datestamp) + ".json")

# TODO if I am gonna continue using this Python code in Cloud Functions and / or Airflow, I'll have to dump this into a GCP Bucket instead of writing a local file
with open(fully_formed_path, 'w') as json_dump_file:
    json.dump(json_return, json_dump_file)

# TODO Replace print() with the logging module. Integrates better with Airflow or Cloud Functions logs.
print("✅ Wrote to:", fully_formed_path)