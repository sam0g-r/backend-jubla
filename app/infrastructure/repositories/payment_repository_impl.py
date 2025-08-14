from app.domain.entities.payment import Payment
from app.domain.repositories.payment_repository import PaymentRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import Optional, List

class PaymentRepositoryImpl(PaymentRepository):
    def _to_entity(self, db_payment) -> Payment:
        return Payment(
            id=db_payment.id,
            userId=db_payment.userId,
            amount=db_payment.amount,
            currency=db_payment.currency,
            paymentMethod=db_payment.paymentMethod,
            createdAt=db_payment.createdAt,
            updatedAt=db_payment.updatedAt,
            status=db_payment.status,
            financialMovement=[],
            paymentDetails=None,
            reservationsPayments=[]
        )

    async def create(self, payment: Payment) -> Payment:
        async with prisma_client as client:
            db_payment = await client.client.payment.create(data=payment.__dict__)
        return self._to_entity(db_payment)

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        async with prisma_client as client:
            db_payment = await client.client.payment.find_unique(where={"id": payment_id})
            if db_payment:
                return self._to_entity(db_payment)
            return None

    async def get_by_order_id(self, order_id: str) -> Optional[Payment]:
        async with prisma_client as client:
            db_payment = await client.client.payment.find_first(where={"orderId": order_id})
            if db_payment:
                return self._to_entity(db_payment)
            return None

    async def list_by_user(self, user_id: str) -> List[Payment]:
        async with prisma_client as client:
            db_payments = await client.client.payment.find_many(where={"userId": user_id})
        return [self._to_entity(p) for p in db_payments]
