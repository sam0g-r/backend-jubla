from decimal import Decimal
import json
from typing import Any
from datetime import date, datetime
from app.domain.entities.reservation import Reservation
from app.domain.repositories.reservation_repository import ReservationRepository
from app.enums.reservation_status_enum import ReservationStatusEnum
from app.infrastructure.adapters.data_transformer import DataTransformer
from app.infrastructure.services.paypal_detail_service import PayPalDetailService
from app.infrastructure.database.prisma_client import prisma_client

class ReservationRepositoryImpl(ReservationRepository):
    def __init__(self):
        self._transformer = DataTransformer()
        self._paypal_service = PayPalDetailService(prisma_client)
        
    def _to_entity(self, db_reservation: Any) -> Reservation:
        return Reservation(
            id=db_reservation.id,
            userId=db_reservation.userId,
            eventId=db_reservation.eventId,
            termsAccepted=db_reservation.termsAccepted,
            imageRightsAccepted=db_reservation.imageRightsAccepted,
            privacyAccepted=db_reservation.privacyAccepted,
            reservationDate=db_reservation.reservationDate,
            pastoralLetterUploaded=db_reservation.pastoralLetterUploaded,
            pastoralLetterUploadedAt=db_reservation.pastoralLetterUploadedAt,
            pastorContact=db_reservation.pastorContact,
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
            "privacyAccepted": reservation.privacyAccepted,
            "pastorContact": reservation.pastorContact,
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
            "termsAccepted",
            "imageRightsAccepted",
            "privacyAccepted",
            "pastorContact",
            "pastoralLetter",
            "paypalOrderId",
            "transferReceipt"
        ]
        data = {k: v for k, v in updates.items() if k in allowed_fields}
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
                                        reservation_payload: dict,
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

            # crear reserva
            reservation_db = await tx.reservations.create(data=reservation_payload)

            files_record = None
            if file_metadata:
                files_payload = file_metadata.copy()
                files_payload.update({'uploadedById': user_db.id, 'fileableId': user_db.id})
                files_record = await tx.files.create(data=files_payload)
                await tx.reservations.update(where={'id': reservation_db.id}, data={'pastoralLetterUploaded': True, 
                                                                                    'pastoralLetterUploadedAt': datetime.now(), 
                                                                                    'status': ReservationStatusEnum.PENDING_PAYMENT})

            payment_db = None
            paypal_detail_db = None
            if payment_payload is not None:
                # copy payload and attach user id
                payment_payload = payment_payload.copy()
                payment_payload['userId'] = user_db.id

                # paypal_raw may contain the raw order; extract it and remove non-Payment fields
                paypal_raw = payment_payload.pop('paypal_raw', None)
                # payer fields are not columns in Payment model; extract them first
                payer_id = payment_payload.pop('payer_id', None)
                payer_email = payment_payload.pop('payer_email', None)

                # create Payment with allowed fields only
                payment_db = await tx.payment.create(data=payment_payload)

                # create PaypalPaymentDetail if we have raw data
                if paypal_raw:
                    # ensure rawData is a JSON-serializable Python object
                    raw_data = paypal_raw
                    if isinstance(raw_data, str):
                        raw_data = json.loads(raw_data)

                    raw_data = self.json_ready(raw_data)  # dict/array JSON-safe

                    # extract order id
                    order_id = None
                    if isinstance(raw_data, dict):
                        order_id = raw_data.get('id')
                    
                    # only create detail if we have an order id (schema requires orderId and paymentId)
                    if order_id:
                        paypal_detail_db = await tx.paypalpaymentdetail.create(
                            data={
                                'orderId': order_id,
                                'captureId': None,
                                'payerId': payer_id,
                                'payerEmail': payer_email,
                                'rawData': json.dumps(raw_data),
                                'payment': {'connect': {'id': str(payment_db.id)}},
                            }
                        )
                    else:
                        # no order id found: skip creating paypal detail to avoid schema errors
                        paypal_detail_db = None

            if payment_db is not None:
                await tx.reservationspayments.create(data={'reservationId': reservation_db.id, 'paymentId': payment_db.id})
                await tx.payment.update(where={'id': payment_db.id}, data={'status': 'COMPLETED'})
                await tx.reservations.update(where={'id': reservation_db.id}, data={'paymentStatus': 'COMPLETED', 
                                                                                    'status': ReservationStatusEnum.COMPLETED.value if files_record 
                                                                                    else ReservationStatusEnum.PENDING_PASTORAL_LETTER.value, 
                                                                                    'paymentCompletedAt': datetime.now()})

            results['reservation'] = reservation_db
            results['files'] = files_record
            results['payment'] = payment_db
            results['paypal_detail'] = paypal_detail_db

        return results

    def json_ready(self, obj):
        def _default(o):
            if isinstance(o, (datetime, date)):
                return o.isoformat()
            if isinstance(o, Decimal):
                return float(o)
            return str(o)  # último recurso
        return json.loads(json.dumps(obj, default=_default))

    async def create_file_for_reservation(self, reservationId: str, file_metadata: dict, is_pastoral: bool) -> dict:
        """Crear registro de files y actualizar reservation si corresponde. Devuelve {'files': files_record, 'reservation': reservation_db}"""
        results = {'files': None, 'reservation': None}
        async with prisma_client.client.tx() as tx:
            reservation_db = await tx.reservations.find_unique(where={'id': reservationId})
            if not reservation_db:
                raise Exception('Reserva no encontrada')

            files_payload = file_metadata.copy()
            files_payload.update({'uploadedById': reservation_db.userId, 'fileableId': reservation_db.userId})
            files_record = await tx.files.create(data=files_payload)

            if is_pastoral:
                await tx.reservations.update(where={'id': reservation_db.id}, data={
                    'pastoralLetterUploaded': True,
                    'pastoralLetterUploadedAt': datetime.now(),
                    'status': ReservationStatusEnum.PENDING_PAYMENT
                })

            results['files'] = files_record
            results['reservation'] = reservation_db
        return results

    async def create_payment_for_reservation(self, reservationId: str, payment_payload: dict, paypal_raw: dict | None = None) -> dict:
        """Crear payment, paypal detail y reservationspayments dentro de tx; actualizar status/paymentStatus."""
        results = {'payment': None, 'paypal_detail': None, 'reservation': None}
        async with prisma_client.client.tx() as tx:
            reservation_db = await tx.reservations.find_unique(where={'id': reservationId})
            if not reservation_db:
                raise Exception('Reserva no encontrada')

            payment_copy = payment_payload.copy()
            payment_copy['userId'] = reservation_db.userId

            # remove paypal_raw, payer fields from payload if present
            paypal_raw_value = payment_copy.pop('paypal_raw', paypal_raw)
            payer_id = payment_copy.pop('payer_id', None)
            payer_email = payment_copy.pop('payer_email', None)

            payment_db = await tx.payment.create(data=payment_copy)

            paypal_detail_db = None
            raw_data = paypal_raw_value
            if raw_data:
                if isinstance(raw_data, str):
                    try:
                        raw_data = json.loads(raw_data)
                    except Exception:
                        pass

                raw_data = self.json_ready(raw_data)
                order_id = None
                if isinstance(raw_data, dict):
                    order_id = raw_data.get('id')

                if order_id:
                    paypal_detail_db = await tx.paypalpaymentdetail.create(data={
                        'orderId': order_id,
                        'captureId': None,
                        'payerId': payer_id,
                        'payerEmail': payer_email,
                        'rawData': json.dumps(raw_data),
                        'payment': {'connect': {'id': payment_db.id}},
                    })

            await tx.reservationspayments.create(data={'reservationId': reservation_db.id, 'paymentId': payment_db.id})
            await tx.payment.update(where={'id': payment_db.id}, data={'status': 'COMPLETED'})

            # Decide new reservation status based on whether pastoral letter exists
            new_status = reservation_db.status
            if reservation_db.pastoralLetterUploaded:
                if reservation_db.status == ReservationStatusEnum.PENDING_BOTH.value:
                    new_status = ReservationStatusEnum.PENDING_PASTORAL_LETTER.value
                elif reservation_db.status == ReservationStatusEnum.PENDING_PAYMENT.value:
                    new_status = ReservationStatusEnum.COMPLETED.value
            else:
                if reservation_db.status == ReservationStatusEnum.PENDING_BOTH.value:
                    new_status = ReservationStatusEnum.PENDING_PASTORAL_LETTER.value
                elif reservation_db.status == ReservationStatusEnum.PENDING_PAYMENT.value:
                    new_status = ReservationStatusEnum.COMPLETED.value

            await tx.reservations.update(where={'id': reservation_db.id}, data={
                'paymentStatus': 'COMPLETED',
                'paymentCompletedAt': datetime.now(),
                'status': new_status
            })

            results['payment'] = payment_db
            results['paypal_detail'] = paypal_detail_db
            results['reservation'] = reservation_db

        return results
