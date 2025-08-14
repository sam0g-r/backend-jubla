from datetime import datetime
from app.application.dto.reservation_dto import ReservationDTO
from app.domain.repositories.reservation_repository import ReservationRepository

class UpdateReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, reservation_id: str, updates: dict) -> ReservationDTO:
        updates['updatedAt'] = datetime.now()
        reservation = await self.reservation_repository.update(reservation_id, updates)
        return ReservationDTO.from_entity(reservation)
