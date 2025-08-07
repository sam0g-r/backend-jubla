from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.registration import Registration, PaymentStatus

class RegistrationRepository(ABC):
    @abstractmethod
    async def create(self, registration: Registration) -> Registration:
        pass
    
    @abstractmethod
    async def get_by_id(self, registration_id: str) -> Optional[Registration]:
        pass
    
    @abstractmethod
    async def get_by_user_and_event(self, user_id: str, event_id: str) -> Optional[Registration]:
        pass
    
    @abstractmethod
    async def update(self, registration: Registration) -> Registration:
        pass
    
    @abstractmethod
    async def delete(self, registration_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_by_event(self, event_id: str, skip: int = 0, limit: int = 100) -> List[Registration]:
        pass
    
    @abstractmethod
    async def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Registration]:
        pass
    
    @abstractmethod
    async def list_by_payment_status(self, status: PaymentStatus, skip: int = 0, limit: int = 100) -> List[Registration]:
        pass
    
    @abstractmethod
    async def count_by_event(self, event_id: str) -> int:
        pass 