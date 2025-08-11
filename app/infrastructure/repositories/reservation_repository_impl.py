from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.infrastructure.database.prisma_client import prisma_client

class ReservationRepositoryImpl(ReservationRepository):
    def _to_entity(self, db_reservation) -> Reservation:
        return Reservation(
            id=db_reservation.id,
            userId=db_reservation.userId,
            eventId=db_reservation.eventId,
            termsAccepted=db_reservation.termsAccepted,
            imageRightsAccepted=db_reservation.imageRightsAccepted,
            reservationDate=db_reservation.reservationDate,
            pastoralLetterUploaded=db_reservation.pastoralLetterUploaded,
            pastoralLetterUploadedAt=db_reservation.pastoralLetterUploadedAt,
            paymentCompletedAt=db_reservation.paymentCompletedAt,
            paymentStatus=db_reservation.paymentStatus,
            status=db_reservation.status,
            createdAt=db_reservation.createdAt,
            updatedAt=db_reservation.updatedAt,
        )

    async def create(self, reservation: Reservation) -> Reservation:
        async with prisma_client as client:
            db_reservation = await client.client.reservations.create(
                data = {
                    "id": reservation.id,
                    "userId": reservation.userId,
                    "eventId": reservation.eventId,
                    "termsAccepted": reservation.termsAccepted,
                    "imageRightsAccepted": reservation.imageRightsAccepted,
                    "reservationDate": reservation.reservationDate,
                    "pastoralLetterUploaded": reservation.pastoralLetterUploaded,
                    "pastoralLetterUploadedAt": reservation.pastoralLetterUploadedAt,
                    "paymentCompletedAt": reservation.paymentCompletedAt,
                    "paymentStatus": reservation.paymentStatus.value,
                    "status": reservation.status.value,
                    "createdAt": reservation.createdAt,
                    "updatedAt": reservation.updatedAt,
                }
            )
        return self._to_entity(db_reservation)

    async def query(self, filters: dict = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        prisma_filters = {}
        # Map filters to prisma query
        for key, value in filters.items():
            if value is not None:
                prisma_filters[key] = value
        async with prisma_client as client:
            total = await client.client.reservations.count(where=prisma_filters)
            db_reservations = await client.client.reservations.find_many(
                where=prisma_filters,
                skip=skip,
                take=limit,
                order={"createdAt": "desc"}
            )
        return [self._to_entity(r) for r in db_reservations], total

    async def update(self, reservation_id: str, updates: dict) -> Reservation:
        allowed_fields = [
            "pastoralLetterUploaded",
            "pastoralLetterUploadedAt",
            "paymentCompletedAt",
            "paymentStatus",
            "status",
            "updatedAt"
        ]
        data = {k: v for k, v in updates.items() if k in allowed_fields}
        if "paymentStatus" in data and hasattr(data["paymentStatus"], "value"):
            data["paymentStatus"] = data["paymentStatus"].value
        if "status" in data and hasattr(data["status"], "value"):
            data["status"] = data["status"].value
        async with prisma_client as client:
            db_reservation = await client.client.reservations.update(
                where={"id": reservation_id},
                data=data
            )
        return self._to_entity(db_reservation)