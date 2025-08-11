from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from typing import Dict, Any
from uuid import uuid4
from datetime import datetime


class CreateReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    def execute(self, data: Dict[str, Any]) -> Reservation:
        reservation = Reservation(
            id=str(uuid4()),
            userId=data["userId"],
            eventId=data["eventId"],
            termsAccepted=data.get("termsAccepted", False),
            imageRightsAccepted=data.get("imageRightsAccepted", False),
            reservationDate=datetime.now(),
            pastoralLetterUploaded=data.get("pastoralLetterUploaded", False),
            pastoralLetterUploadedAt=data.get("pastoralLetterUploadedAt"),
            paymentCompletedAt=None,
            paymentStatus=data.get("paymentStatus"),
            status=data.get("status"),
            createdAt=datetime.now(),
            updatedAt=None,
        )
        return self.reservation_repository.create(reservation)
