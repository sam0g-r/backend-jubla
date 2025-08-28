from typing import Optional, Dict, Any
from app.infrastructure.paypal_service import PaypalService


class PaypalAdapter:
    """Normalize PayPal order details for the application layer."""
    def __init__(self):
        self._svc = PaypalService()

    async def get_order_summary(self, order_id: str) -> Optional[Dict[str, Any]]:
        if not order_id:
            return None
        order = await self._svc.get_order_details(order_id)
        if not order:
            return None

        amount = 0.0
        currency = 'USD'
        try:
            purchase_unit = order.get('purchase_units', [])[0]
            amount_info = purchase_unit.get('amount', {})
            amount = float(amount_info.get('value', 0.0))
            currency = amount_info.get('currency_code', 'USD')
        except Exception:
            pass

        return {
            'raw': order,
            'amount': amount,
            'currency': currency,
            'order_id': order.get('id'),
            'payer_id': order.get('payer', {}).get('payer_id'),
            'payer_email': order.get('payer', {}).get('email_address'),
        }
