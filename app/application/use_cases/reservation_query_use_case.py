from typing import Any, Dict, List, Optional, Tuple
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository

class QueryReservationsUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> Tuple[List[Reservation], int]:
        return self.reservation_repository.query_reservations(filters, skip, limit)
