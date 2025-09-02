from typing import Dict, Optional
from prisma import Prisma

class PayPalDetailService:
    def __init__(self, prisma_client: Prisma):
        self._prisma = prisma_client

    async def create_payment_detail(
        self,
        tx: Prisma,
        payment_id: str,
        raw_data: Dict,
        payer_id: Optional[str] = None,
        payer_email: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Crea un PaypalPaymentDetail si los datos son válidos.
        
        Args:
            tx: Transacción Prisma activa
            payment_id: ID del pago relacionado
            raw_data: Datos crudos de PayPal (debe contener 'id' para orderId)
            payer_id: ID opcional del pagador
            payer_email: Email opcional del pagador
            
        Returns:
            El registro creado o None si no hay orderId
        """
        if not isinstance(raw_data, dict) or 'id' not in raw_data:
            return None
            
        return await tx.paypalpaymentdetail.create(
            data={
                'orderId': raw_data['id'],
                'captureId': None,
                'payerId': payer_id,
                'payerEmail': payer_email,
                'rawData': raw_data,
                'payment': {'connect': {'id': payment_id}},
            }
        )
