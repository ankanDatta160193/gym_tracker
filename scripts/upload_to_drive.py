import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CSV_PATH = "out/gym_silver.csv"
FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

creds_dict = json.loads(os.environ["GOOGLE_DRIVE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive = build("drive", "v3", credentials=credentials)

file_metadata = {
    "name": "gym_silver.csv",
    "parents": [FOLDER_ID]
}

media = MediaFileUpload(
    CSV_PATH,
    mimetype="text/csv",
    resumable=False
)

file = drive.files().create(
    body=file_metadata,
    media_body=media,
    fields="id",
    supportsAllDrives=True
).execute()

print(f"Uploaded file ID: {file['id']}")
