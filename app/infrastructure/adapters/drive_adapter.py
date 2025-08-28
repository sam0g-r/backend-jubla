from typing import Dict, Any
from app.infrastructure.google_drive import upload_pdf_to_drive
import os
import asyncio


class DriveAdapter:
    """Adapter around Google Drive upload helper to return normalized result."""
    def __init__(self):
        pass

    async def upload_pdf(self, filename: str, raw_bytes: bytes) -> Dict[str, Any]:
        folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        # upload_pdf_to_drive is synchronous in the infra; run in thread
        drive_resp = await asyncio.to_thread(upload_pdf_to_drive, filename, raw_bytes, folder_id)
        return drive_resp or {}
