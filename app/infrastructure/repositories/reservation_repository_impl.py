from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.enums.reservation_status_enum import ReservationStatusEnum
from app.infrastructure.database.prisma_client import prisma_client
from datetime import datetime

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
        prisma_data = {
            "id": reservation.id,
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
            "user": {
                "connect": {"id": reservation.userId}
            },
            "event": {
                "connect": {"id": reservation.eventId}
            }
        }
        db_reservation = await prisma_client.client.reservations.create(data=prisma_data)
        return self._to_entity(db_reservation)

    async def query(self, filters: dict = None, skip: int = 0, limit: int = 10):
        filters = filters or {}
        prisma_filters = {}
        # Map filters to prisma query
        for key, value in filters.items():
            if value is not None:
                prisma_filters[key] = value
        total = await prisma_client.client.reservations.count(where=prisma_filters)
        db_reservations = await prisma_client.client.reservations.find_many(
            where=prisma_filters,
            skip=skip,
            take=limit,
            order={"createdAt": "desc"}
        )
        return [self._to_entity(r) for r in db_reservations], total

    async def update(self, reservationId: str, updates: dict) -> Reservation:
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
        db_reservation = await prisma_client.client.reservations.update(
            where={"id": reservationId},
            data=data
        )
        return self._to_entity(db_reservation)
    
    async def count_by_event(self, eventId) -> int:
        return await prisma_client.client.reservations.count(
            where={
                'eventId': eventId,
                'status': {
                    'not': ReservationStatusEnum.CANCELLED.value
                }
            })
    
    async def create_full_transactional(self, *,
                                        user_payload: dict,
                                        medical_payload: dict,
                                        eventId: str,
                                        payment_payload: dict | None = None,
                                        file_metadata: dict | None = None) -> dict:
        """Encapsula la transacción que crea user, medical, optional payment/paypal detail, file record y reservation.
        Devuelve un dict con keys: reservation, files, payment, paypal_detail (cuando existan).
        """
        results = {'reservation': None, 'files': None, 'payment': None, 'paypal_detail': None}
        async with prisma_client.client.tx() as tx:
            # crear user
            user_db = await tx.user.create(data=user_payload)

            # crear medical vinculando al user
            medical_payload['user'] = {'connect': {'id': user_db.id}}
            med_db = await tx.usermedicalinformation.create(data=medical_payload)

            files_record = None
            if file_metadata:
                files_payload = file_metadata.copy()
                files_payload.update({'uploadedById': user_db.id, 'fileableId': user_db.id})
                files_record = await tx.files.create(data=files_payload)

            payment_db = None
            paypal_detail_db = None
            if payment_payload is not None:
                payment_payload = payment_payload.copy()
                payment_payload['userId'] = user_db.id
                paypal_raw = payment_payload.pop('paypal_raw', None)
                payment_db = await tx.payment.create(data=payment_payload)
                if paypal_raw:
                    paypal_detail_db = await tx.paypalpaymentdetail.create(
                        data={
                            'paymentId': payment_db.id,
                            'orderId': paypal_raw.get('id'),
                            'captureId': None,
                            'payerId': payment_payload.get('payer_id'),
                            'payerEmail': payment_payload.get('payer_email'),
                            'rawData': paypal_raw,
                        }
                    )

            # crear reserva
            reservation_payload = {
                'id': user_payload.get('id') + '_res' if 'id' in user_payload else None,
                'termsAccepted': True,
                'imageRightsAccepted': True,
                'reservationDate': datetime.now(),
                'pastoralLetterUploaded': bool(files_record),
                'pastoralLetterUploadedAt': datetime.now() if files_record else None,
                'paymentCompletedAt': None,
                'paymentStatus': 'PENDING',
                'status': ReservationStatusEnum.PENDING_BOTH.value,
                'createdAt': datetime.now(),
                'userId': user_db.id,
                'eventId': eventId,
            }
            reservation_db = await tx.reservations.create(data=reservation_payload)

            if payment_db is not None:
                await tx.reservationspayments.create(data={'reservationId': reservation_db.id, 'paymentId': payment_db.id})
                await tx.payment.update(where={'id': payment_db.id}, data={'status': 'COMPLETED'})
                await tx.reservations.update(where={'id': reservation_db.id}, data={'paymentStatus': 'COMPLETED', 'status': ReservationStatusEnum.COMPLETED.value, 'paymentCompletedAt': datetime.now()})

            results['reservation'] = reservation_db
            results['files'] = files_record
            results['payment'] = payment_db
            results['paypal_detail'] = paypal_detail_db

        return results
