from app.application.dto.reservation_dto import ReservationDTO
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from typing import Dict, Any
from datetime import datetime
from app.enums.payment_status_enum import PaymentStatusEnum
from app.enums.reservation_status_enum import ReservationStatusEnum
from cuid2 import cuid_wrapper


class CreateReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, data: Dict[str, Any]) -> ReservationDTO:
        generate_id = cuid_wrapper()
        reservation = Reservation(
            id=generate_id(),
            userId=data["userId"],
            eventId=data["eventId"],
            termsAccepted=data.get("termsAccepted", False),
            imageRightsAccepted=data.get("imageRightsAccepted", False),
            reservationDate=datetime.now(),
            pastoralLetterUploaded=data.get("pastoralLetterUploaded", False),
            pastoralLetterUploadedAt=self.resolvePasLetUploadedAt(data.get("pastoralLetterUploaded", False)),
            paymentCompletedAt=self.resolvePaymentCompletedAt(data.get("paymentStatus")),
            paymentStatus=data.get("paymentStatus"),
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        reservation.status= self.resolve_status_reservation(reservation.pastoralLetterUploaded, reservation.paymentStatus)
        reservation = await self.reservation_repository.create(reservation)
        return ReservationDTO.from_entity(reservation)

    @staticmethod
    def resolvePasLetUploadedAt(pastoralLetterUploaded):
        if pastoralLetterUploaded:
            return datetime.now()

    @staticmethod
    def resolvePaymentCompletedAt(paymentStatus):
        if paymentStatus == PaymentStatusEnum.COMPLETED:
            return datetime.now()

    @staticmethod
    def resolve_status_reservation(pastoralLetterUploaded, paymentStatus):
        if not pastoralLetterUploaded and paymentStatus == PaymentStatusEnum.PENDING:
            return ReservationStatusEnum.PENDING_BOTH
        elif pastoralLetterUploaded and paymentStatus == PaymentStatusEnum.PENDING:
            return ReservationStatusEnum.PENDING_PAYMENT
        elif not pastoralLetterUploaded and paymentStatus == PaymentStatusEnum.COMPLETED:
            return ReservationStatusEnum.PENDING_PASTORAL_LETTER
        elif pastoralLetterUploaded and paymentStatus == PaymentStatusEnum.COMPLETED:
            return ReservationStatusEnum.COMPLETED
        else:
            raise Exception('Error asignando el status')
