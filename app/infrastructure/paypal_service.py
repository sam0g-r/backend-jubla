import os
import httpx
from typing import Any, Dict, Optional
from app.shared.config.settings import settings


class PaypalService:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.mode = settings.PAYPAL_MODE or "sandbox"
        self.base = "https://api-m.paypal.com" if self.mode == "live" else "https://api-m.sandbox.paypal.com"

    async def _get_access_token(self) -> str:
        url = f"{self.base}/v1/oauth2/token"
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, data={"grant_type": "client_credentials"}, auth=(self.client_id, self.client_secret))
            resp.raise_for_status()
            data = resp.json()
            return data["access_token"]

    async def get_order_details(self, order_id: str) -> Dict[str, Any]:
        token = await self._get_access_token()
        url = f"{self.base}/v2/checkout/orders/{order_id}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
