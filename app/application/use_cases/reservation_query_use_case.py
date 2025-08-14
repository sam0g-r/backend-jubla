from typing import Any, Dict, List, Optional, Tuple
from app.application.dto.reservation_dto import ReservationDTO
from app.domain.repositories.reservation_repository import ReservationRepository

class QueryReservationsUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> Tuple[List[ReservationDTO], int]:
        reservations, total = await self.reservation_repository.query(filters, skip, limit)
        return [ReservationDTO.from_entity(r) for r in reservations], total
