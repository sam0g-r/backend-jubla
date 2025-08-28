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
    async def update(self, reservationId: str, updates: dict) -> Reservation:
        """Actualiza solo los campos permitidos de una reserva."""
        pass

    @abstractmethod
    async def count_by_event(self, eventId) -> int:
        """Centa el total de registros activos de reserva."""
        pass

    @abstractmethod
    async def create_full_transactional(self, *,
                                        user_payload: dict,
                                        medical_payload: dict,
                                        eventId: str,
                                        payment_payload: dict | None = None,
                                        file_metadata: dict | None = None) -> dict:
        """Crear usuario, medical info, payment, reservation y archivos dentro de una transacción.
        Devuelve un dict con los objetos DB creados mínimos: reservation, files (if any), payment, paypal_detail.
        """
        pass
