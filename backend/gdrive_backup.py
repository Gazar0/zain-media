#!/usr/bin/env python3
"""
Google Drive auto-backup for Zain Media database.
Backs up the SQLite database to Google Drive using a service account.

Setup:
1. Go to https://console.cloud.google.com/
2. Create a new project → "Zain Media Backup"
3. Enable "Google Drive API"
4. Go to "Credentials" → "Create Credentials" → "Service Account"
5. Name it "zain-backup" → Click "Done"
6. Click on the service account → "Keys" → "Add Key" → "JSON"
7. Download the JSON file and save as backend/service-account.json
8. Create a folder in your Google Drive named "ZainMedia Backups"
9. Share that folder with the service account email (from the JSON file)
"""

import os
import json
import pickle
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BACKEND_DIR, "zainmedia.db")
TOKEN_PATH = os.path.join(BACKEND_DIR, "gdrive_token.pickle")
CREDS_PATH = os.path.join(BACKEND_DIR, "gdrive_credentials.json")
BACKUP_FOLDER_NAME = "ZainMedia Backups"


def get_drive_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(CREDS_PATH):
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            return None

        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)


def find_or_create_folder(service):
    response = service.files().list(
        q=f"name='{BACKUP_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        spaces="drive", fields="files(id, name)"
    ).execute()
    folders = response.get("files", [])
    if folders:
        return folders[0]["id"]
    file_metadata = {"name": BACKUP_FOLDER_NAME, "mimeType": "application/vnd.google-apps.folder"}
    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]


def upload_backup():
    if not os.path.exists(DB_PATH):
        print("Database file not found")
        return False

    service = get_drive_service()
    if not service:
        print("Google Drive not configured. Create gdrive_credentials.json first.")
        return False

    try:
        folder_id = find_or_create_folder(service)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"zainmedia_backup_{timestamp}.db"

        # Delete old backups (keep last 5)
        results = service.files().list(
            q=f"'{folder_id}' in parents and name contains 'zainmedia_backup' and trashed=false",
            spaces="drive", fields="files(id, name, createdTime)",
            orderBy="createdTime asc"
        ).execute()
        files = results.get("files", [])
        while len(files) >= 5:
            oldest = files.pop(0)
            service.files().delete(fileId=oldest["id"]).execute()

        media = MediaFileUpload(DB_PATH, mimetype="application/octet-stream")
        file_metadata = {"name": filename, "parents": [folder_id]}
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"Backup uploaded: {filename}")
        return True
    except Exception as e:
        print(f"Backup error: {e}")
        return False


if __name__ == "__main__":
    upload_backup()
