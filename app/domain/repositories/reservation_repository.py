from abc import ABC, abstractmethod
from app.domain.entities.reservation import Reservation
from typing import Optional
from datetime import datetime

class ReservationRepository(ABC):
    @abstractmethod
    async def create(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    async def query(self, filters: Optional[dict] = None, skip: int = 0, limit: int = 10):
        """Query reservations with filters and pagination."""
        pass

    @abstractmethod
    async def update(self, reservation_id: str, updates: dict) -> Reservation:
        """Actualiza solo los campos permitidos de una reserva."""
        pass
