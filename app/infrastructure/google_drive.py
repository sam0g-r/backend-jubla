from typing import Optional, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
import os

# Mirrors api/src/lib/google-drive.ts behaviour
def upload_pdf_to_drive(file_name: str, buffer: bytes, folder_id: Optional[str] = None) -> Optional[Dict[str, str]]:
    sa_b64 = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    if not sa_b64:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT env var not set")

    # Service account JSON is base64-encoded in env (same as JS project)
    import base64, json
    credentials_info = json.loads(base64.b64decode(sa_b64).decode('utf-8'))
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=["https://www.googleapis.com/auth/drive"])

    drive_service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaIoBaseUpload(BytesIO(buffer), mimetype='application/pdf')

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    return file
