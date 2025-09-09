import os
from typing import Optional, Dict, Any
import httpx

RESEND_API_URL = "https://api.resend.com"  # base URL


class ResendService:
    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None):
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.from_email = from_email or os.getenv("RESEND_FROM_EMAIL")
        if not self.api_key:
            raise RuntimeError("RESEND_API_KEY is not set")

    async def send_email(self, to: str, subject: str, html: str, text: Optional[str] = None) -> Dict[str, Any]:
        """Send an email via Resend. Returns the API response as dict.

        This is a minimal wrapper. See https://resend.com/docs for more options.
        """
        payload = {
            "from": self.from_email,
            "to": [to],
            "subject": subject,
            "html": html,
        }
        if text:
            payload["text"] = text

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{RESEND_API_URL}/emails", json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
