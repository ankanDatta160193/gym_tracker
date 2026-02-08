import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SERVICE_JSON = json.loads(os.environ["GOOGLE_DRIVE_CREDENTIALS"])
FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

creds = Credentials.from_service_account_info(
    SERVICE_JSON,
    scopes=["https://www.googleapis.com/auth/drive.file"]
)

service = build("drive", "v3", credentials=creds)

file_metadata = {
    "name": "gym_silver.csv",
    "parents": [FOLDER_ID]
}

media = MediaFileUpload(
    "out/gym_silver.csv",
    mimetype="text/csv",
    resumable=False
)

service.files().create(
    body=file_metadata,
    media_body=media,
    fields="id"
).execute()

print("Uploaded to Google Drive")
