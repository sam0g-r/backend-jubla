from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository

class UpdateReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, reservation_id: str, updates: dict) -> Reservation:
        return await self.reservation_repository.update_reservation(reservation_id, updates)
