from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.payment import Payment

class PaymentRepository(ABC):
    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_order_id(self, order_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str) -> List[Payment]:
        pass
