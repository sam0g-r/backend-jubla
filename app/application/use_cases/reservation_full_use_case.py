from typing import Dict, Any, List
from app.application.dto.user_dto import CreateUserDTO
from app.application.use_cases.event_use_cases import EventUseCases
from app.application.use_cases.reservation_use_cases import CreateReservationUseCase
from app.application.use_cases.user_medical_information_use_cases import CreateUserMedicalInformationUseCase
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.user_medical_information_repository import UserMedicalInformationRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.entities.reservation import Reservation
from app.enums.payment_status_enum import PaymentStatusEnum
from app.enums.reservation_status_enum import ReservationStatusEnum
from datetime import datetime, date
import base64
from uuid import uuid4
from typing import Optional
import os
import asyncio

from app.infrastructure.paypal_service import PaypalService
from app.infrastructure.database.prisma_client import prisma_client
from app.infrastructure.google_drive import upload_pdf_to_drive


class CreateFullReservationUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        medical_repo: UserMedicalInformationRepository,
        event_repo: EventRepository,
        reservation_repo: ReservationRepository,
    ):
        self.user_repo = user_repo
        self.medical_repo = medical_repo
        self.event_repo = event_repo
        self.reservation_repo = reservation_repo

    async def execute(self, data: Dict[str, Any]) -> Reservation:
        # 1. Validar evento
        event = await self.validate_event(data['paymentData']['slug'])

        # Ejecutar las operaciones de escritura en la DB dentro de una sola transacción Prisma
        # Las operaciones externas (Google Drive, PayPal API calls) seguirán fuera o antes según corresponda,
        # pero los writes que dependan del DB se ejecutan en la transacción.
        from passlib.context import CryptContext
        from cuid2 import cuid_wrapper

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        generate_id = cuid_wrapper()

        # Normalize incoming date fields that may be python date objects (Prisma expects serializable values)
        personal_data = data.get('personalData', {})
        bd = personal_data.get('birthdate')
        def _to_iso_datetime(val):
            if val is None:
                return None
            if isinstance(val, datetime) and not isinstance(val, date):
                # naive datetime -> append Z
                try:
                    if val.tzinfo is None:
                        return val.strftime('%Y-%m-%dT%H:%M:%SZ')
                    return val.isoformat()
                except Exception:
                    return val.isoformat()
            if isinstance(val, date) and not isinstance(val, datetime):
                # date -> midnight UTC with Z suffix
                return datetime.combine(val, datetime.min.time()).strftime('%Y-%m-%dT%H:%M:%SZ')
            return val

        if bd is not None:
            personal_data['birthdate'] = _to_iso_datetime(bd)
            data['personalData'] = personal_data

        # variables para uso fuera de la transacción (por ejemplo upload a Drive)
        files_record = None
        pastoral_b64 = data['churchData'].get('pastoralLetter')

        # Obtener datos de pago (detalles se pedirán a PayPal antes de la transacción si es necesario)
        payment_data = data.get('paymentData') or {}
        paypal_order_id = payment_data.get('orderId') or payment_data.get('paypalOrderId')
        paypal_order = None
        if paypal_order_id:
            # obtener detalles del pedido fuera de la transacción (no afecta ACID)
            paypal = PaypalService()
            paypal_order = await paypal.get_order_details(paypal_order_id)

        async with prisma_client as client:
            # usar la API de transacción del cliente Prisma (tx() es la API correcta)
            async with client.client.tx() as tx:
                # 2. Crear usuario
                user_id = generate_id()
                hashed_password = pwd_context.hash(data['personalData']['password'])

                # construir payload de creación de usuario y transformar countryId/stateId a relaciones connect
                user_create_data = {
                    'id': user_id,
                    'email': data['personalData']['email'],
                    'firstname': data['personalData']['firstname'],
                    'lastname': data['personalData']['lastname'],
                    'birthdate': data['personalData']['birthdate'],
                    'phone': data['personalData'].get('phone'),
                    'password': hashed_password,
                    'church': data['churchData']['church'],
                }

                if data['personalData'].get('countryId'):
                    user_create_data['country'] = {'connect': {'id': data['personalData']['countryId']}}
                if data['personalData'].get('stateId'):
                    user_create_data['state'] = {'connect': {'id': data['personalData']['stateId']}}

                user_db = await tx.user.create(
                    data=user_create_data
                )

                # 3. Crear información médica
                med_db = await tx.usermedicalinformation.create(
                    data={
                        'id': str(uuid4()),
                        'user': {'connect': {'id': user_db.id}},
                        'emergencyContactName': data['medicalData']['emergencyContactName'],
                        'emergencyContactPhone': data['medicalData']['emergencyContactPhone'],
                        'emergencyContactRelationship': data['medicalData']['emergencyContactRelationship'],
                        'emergencyContactEmail': data['medicalData']['emergencyContactEmail'],
                        'hasPatologies': data['medicalData'].get('hasPatologies', False),
                        'hasMedication': data['medicalData'].get('hasMedication', False),
                        'hasAllergies': data['medicalData'].get('hasAllergies', False),
                        'hasMedicationAllergies': data['medicalData'].get('hasMedicationAllergies', False),
                        'hasSurgeryHistory': data['medicalData'].get('hasSurgeryHistory', False),
                        'hasDaietaryRestrictions': data['medicalData'].get('hasDaietaryRestrictions', False),
                        'patologies': data['medicalData'].get('patologies'),
                        'medication': data['medicalData'].get('medication'),
                        'allergies': data['medicalData'].get('allergies'),
                        'medicationAllergies': data['medicalData'].get('medicationAllergies'),
                        'surgeryHistory': data['medicalData'].get('surgeryHistory'),
                        'dietaryRestrictions': data['medicalData'].get('dietaryRestrictions'),
                        'createdAt': datetime.now(),
                    }
                )

                # 4.a Crear registro de archivo si viene la carta pastoral
                if pastoral_b64:
                    file_name = f"pastoral_letter_{uuid4()}.pdf"
                    files_record = await tx.files.create(
                        data={
                            'name': file_name,
                            'mimeType': 'application/pdf',
                            'driveFileId': '',
                            'url': '',
                            'uploadedById': user_db.id,
                            'fileableId': user_db.id,
                            'fileableType': 'USER',
                        }
                    )

                # 4.b Crear registro de payment y detalle paypal si aplica
                payment_db = None
                paypal_detail_db = None
                if paypal_order is not None:
                    # intentar extraer amount/currency
                    amount = 0.0
                    currency = 'USD'
                    try:
                        purchase_unit = paypal_order.get('purchase_units', [])[0]
                        amount_info = purchase_unit.get('amount', {})
                        amount = float(amount_info.get('value', 0.0))
                        currency = amount_info.get('currency_code', 'USD')
                    except Exception:
                        pass

                    payment_db = await tx.payment.create(
                        data={
                            'userId': user_db.id,
                            'amount': amount,
                            'currency': currency,
                            'paymentMethod': 'PAYPAL',
                            'status': 'PENDING',
                        }
                    )

                    paypal_detail_db = await tx.paypalpaymentdetail.create(
                        data={
                            'paymentId': payment_db.id,
                            'orderId': paypal_order.get('id'),
                            'captureId': None,
                            'payerId': paypal_order.get('payer', {}).get('payer_id'),
                            'payerEmail': paypal_order.get('payer', {}).get('email_address'),
                            'rawData': paypal_order,
                        }
                    )

                # 5. Crear reserva
                reservation_id = generate_id()
                reservation_db = await tx.reservations.create(
                    data={
                        'id': reservation_id,
                        'termsAccepted': data['personalData']['terms'],
                        'imageRightsAccepted': data['personalData']['imageTerms'],
                        'reservationDate': datetime.now(),
                        'pastoralLetterUploaded': bool(pastoral_b64),
                        'pastoralLetterUploadedAt': datetime.now() if pastoral_b64 else None,
                        'paymentCompletedAt': None,
                        'paymentStatus': PaymentStatusEnum.PENDING.value,
                        'status': ReservationStatusEnum.PENDING_BOTH.value,
                        'createdAt': datetime.now(),
                        # 'updatedAt': None,  # removed: let Prisma manage @updatedAt
                        'userId': user_db.id,
                        'eventId': event.id,
                    }
                )

                # 6. Si hubo payment, enlazar y actualizar dentro de la misma transacción
                if payment_db is not None:
                    await tx.reservationspayments.create(
                        data={
                            'reservationId': reservation_db.id,
                            'paymentId': payment_db.id,
                        }
                    )

                    await tx.payment.update(
                        where={'id': payment_db.id},
                        data={'status': 'COMPLETED'}
                    )

                    await tx.reservations.update(
                        where={'id': reservation_db.id},
                        data={
                            'paymentStatus': 'COMPLETED',
                            'status': ReservationStatusEnum.COMPLETED.value,
                            'paymentCompletedAt': datetime.now(),
                        }
                    )

        # FIN transacción

        # Subir el PDF a Google Drive después de que la transacción haya sido confirmada
        if pastoral_b64 and files_record:
            try:
                raw = base64.b64decode(pastoral_b64.split(',')[-1] if ',' in pastoral_b64 else pastoral_b64)
                folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
                drive_resp = await asyncio.to_thread(upload_pdf_to_drive, files_record.name, raw, folder_id)
                if drive_resp:
                    async with prisma_client as client:
                        await client.client.files.update({
                            'where': {'id': files_record.id},
                            'data': {
                                'driveFileId': drive_resp.get('id', ''),
                                'url': drive_resp.get('webViewLink', ''),
                            },
                        })
            except Exception:
                # fallo en upload: registrar y continuar; la transacción DB ya fue comprometida
                pass

        # Mapear a la entidad de dominio Reservation y devolver
        from app.domain.entities.reservation import Reservation as ReservationEntity

        def to_datetime(val):
            if val is None:
                return None
            if isinstance(val, datetime):
                return val
            if isinstance(val, date):
                return datetime.combine(val, datetime.min.time())
            return val

        return ReservationEntity(
            id=reservation_db.id,
            userId=reservation_db.userId,
            eventId=reservation_db.eventId,
            termsAccepted=reservation_db.termsAccepted,
            imageRightsAccepted=reservation_db.imageRightsAccepted,
            reservationDate=to_datetime(reservation_db.reservationDate),
            pastoralLetterUploaded=reservation_db.pastoralLetterUploaded,
            pastoralLetterUploadedAt=to_datetime(reservation_db.pastoralLetterUploadedAt),
            paymentCompletedAt=to_datetime(reservation_db.paymentCompletedAt),
            paymentStatus=reservation_db.paymentStatus,
            status=reservation_db.status,
            createdAt=to_datetime(reservation_db.createdAt),
            updatedAt=to_datetime(reservation_db.updatedAt),
        )

    async def validate_event(self, slug: str):
        event_use_case = EventUseCases(self.event_repo)
        event = await event_use_case.get_by_slug(slug)
        if not event:
            raise Exception('Evento no existente')
        if not event.isActive:
            raise Exception('Evento no disponible')
        if not event.title or not event.startDate or not event.endDate:
            raise Exception('El evento no tiene todos los datos requeridos configurados')
        if event.maxCapacity:
            currentReservations = await self.reservation_repo.count_by_event(eventId=event.id)
            if currentReservations >= event.maxCapacity:
                raise Exception('El evento ha alcanzado su capacidad máxima')
        return event

    async def _rollback(self, created_ids: List[Dict[str, str]]):
        # intentar eliminar en orden inverso los recursos creados
        try:
            async with prisma_client as client:
                for item in reversed(created_ids):
                    if 'paypal_payment_detail' in item:
                        await client.paypalpaymentdetail.delete(where={ 'id': item['paypal_payment_detail'] })
                    if 'payment' in item:
                        await client.payment.delete(where={ 'id': item['payment'] })
                    if 'files' in item:
                        await client.files.delete(where={ 'id': item['files'] })
                    if 'reservation' in item:
                        await client.reservations.delete(where={ 'id': item['reservation'] })
        except Exception:
            # No podemos hacer más si falla la limpieza
            pass
