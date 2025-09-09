from typing import Dict, Any, List
from app.application.use_cases.event_use_cases import EventUseCases
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.user_medical_information_repository import UserMedicalInformationRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.reservation_repository import ReservationRepository
from app.domain.entities.reservation import Reservation
from datetime import datetime, date
import base64

from app.enums.reservation_status_enum import ReservationStatusEnum
from app.infrastructure.database.prisma_client import prisma_client
from app.infrastructure.google_drive import upload_pdf_to_drive
from app.shared.exceptions.user_exceptions import UserAlreadyExistsError, UserValidationError
from app.infrastructure.repositories.country_repository_impl import CountryRepositoryImpl
from app.infrastructure.repositories.state_repository_impl import StateRepositoryImpl


class CreateFullReservationUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        medical_repo: UserMedicalInformationRepository,
        event_repo: EventRepository,
        reservation_repo: ReservationRepository,
        file_repo=None,
    ):
        self.user_repo = user_repo
        self.medical_repo = medical_repo
        self.event_repo = event_repo
        self.reservation_repo = reservation_repo
        self.file_repo = file_repo

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

        # Validaciones previas a la transacción
        # 1) email no debe existir
        existing_user = await self.user_repo.get_by_email(data['personalData']['email'])
        if existing_user:
            # Requerimiento: retornar 404 cuando el email ya existe
            raise UserAlreadyExistsError(f"El email {data['personalData']['email']} ya está registrado")

        # 2) password y confirmPassword deben coincidir
        if data['personalData'].get('password') != data['personalData'].get('confirmPassword'):
            raise UserValidationError('Las contraseñas no coinciden')

        # 3) validar countryId / stateId existen en la BD (si fueron provistos)
        country_repo = CountryRepositoryImpl()
        state_repo = StateRepositoryImpl()
        country_id = data['personalData'].get('countryId')
        state_id = data['personalData'].get('stateId')
        if country_id:
            country = await country_repo.get_by_id(country_id)
            if not country:
                raise UserValidationError('El countryId proporcionado no existe')
        if state_id:
            state = await state_repo.get_by_id(state_id)
            if not state:
                raise UserValidationError('El stateId proporcionado no existe')

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
        transfer_receipt = None

        # Obtener datos de pago (detalles se pedirán a PayPal antes de la transacción si es necesario)
        # use adapter to normalize PayPal info
        from app.infrastructure.adapters.paypal_adapter import PaypalAdapter
        from app.infrastructure.adapters.drive_adapter import DriveAdapter
        from app.infrastructure.email.resend_service import ResendService

        payment_data = data.get('paymentData') or {}
        if payment_data.get('paymentMethod') == 'paypal':
            paypal_order_id = payment_data.get('paypalOrderId')
            paypal_summary = None
            if paypal_order_id:
                paypal_adapter = PaypalAdapter()
                paypal_summary = await paypal_adapter.get_order_summary(paypal_order_id)
        elif payment_data.get('paymentMethod') == 'transferencia':
            transfer_receipt = payment_data.get('transferReceipt')

        # construir payloads a pasar al repositorio transaccional
        userId = generate_id()
        hashed_password = pwd_context.hash(data['personalData']['password'])

        user_create_data = {
            'id': userId,
            'email': data['personalData']['email'],
            'firstname': data['personalData']['firstname'],
            'lastname': data['personalData']['lastname'],
            'birthdate': data['personalData']['birthdate'],
            'phone': data['personalData'].get('phone'),
            'gender': data['personalData'].get('gender'),
            'documentId': data['personalData'].get('documentId'),
            'profession': data['personalData'].get('profession'),
            'instagramProfile': data['personalData'].get('instagramProfile'),
            'password': hashed_password,
            'church': data['churchData']['church'],
            'birthCountry': data['personalData']['birthCountry'],
            'country': {'connect': {'id': data['personalData']['countryId']}},
            'state': {'connect': {'id': data['personalData']['stateId']}}
        }

        med_payload = {
            'id': generate_id(),
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

        file_metadata = None
        if pastoral_b64:
            file_name = f"pastoral_letter_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            file_metadata = {
                'name': file_name,
                'mimeType': 'application/pdf',
                'driveFileId': '',
                'url': '',
                'fileableType': 'USER',
            }
        if transfer_receipt:
            file_name = f"transfer_receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            file_metadata = {
                'name': file_name,
                'mimeType': 'application/pdf',
                'driveFileId': '',
                'url': '',
                'fileableType': 'USER',
            }

        payment_payload = None
        if paypal_summary is not None:
            payment_payload = {
                'amount': paypal_summary['amount'],
                'currency': paypal_summary['currency'],
                'paymentMethod': 'PAYPAL',
                'status': 'PENDING',
                'paypal_raw': paypal_summary['raw'],
                'payer_id': paypal_summary.get('payer_id'),
                'payer_email': paypal_summary.get('payer_email'),
            }

        
        reservation_payload = {
            'id': generate_id(),
            'termsAccepted': data['personalData']['terms'],
            'imageRightsAccepted': data['personalData']['imageTerms'],
            'privacyAccepted': data['personalData']['privacyAccepted'],
            'pastorContact':data['churchData']['pastorContact'],
            'reservationDate': datetime.now(),
            'pastoralLetterUploaded': False,
            'pastoralLetterUploadedAt': None,
            'paymentCompletedAt': None,
            'paymentStatus': 'PENDING',
            'status': ReservationStatusEnum.PENDING_BOTH.value,
            'createdAt': datetime.now(),
            'userId': userId,
            'eventId': event.id,
        }

        # llamar al repositorio transaccional
        created = await self.reservation_repo.create_full_transactional(
            user_payload=user_create_data,
            medical_payload=med_payload,
            reservation_payload=reservation_payload,
            payment_payload=payment_payload,
            file_metadata=file_metadata,
        )

        # FIN transacción

        files_record = created.get('files')
        payment_db = created.get('payment')
        reservation_db = created.get('reservation')

        # Subir el PDF a Google Drive después de que la transacción haya sido confirmada
        if pastoral_b64 and files_record:
            try:
                raw = base64.b64decode(pastoral_b64.split(',')[-1] if ',' in pastoral_b64 else pastoral_b64)
                drive_adapter = DriveAdapter()
                drive_resp = await drive_adapter.upload_pdf(files_record.name, raw)
                if drive_resp:
                    if self.file_repo:
                        await self.file_repo.update(files_record.id, {
                            'driveFileId': drive_resp.get('id', ''),
                            'url': drive_resp.get('webViewLink', ''),
                        })
                    else:
                        await prisma_client.client.files.update(
                            where={'id': files_record.id},
                            data={
                                'driveFileId': drive_resp.get('id', ''),
                                'url': drive_resp.get('webViewLink', ''),
                            },
                        )
            except Exception:
                # fallo en upload: registrar y continuar; la transacción DB ya fue comprometida
                pass

        # Si se proporcionó un comprobante de transferencia (transfer_receipt), subirlo igual que la carta pastoral
        # Nota: el repositorio transaccional crea un único registro de archivo usando el `file_metadata` enviado.
        # La lógica aquí asume que `files_record` referencia el archivo creado para el comprobante actual.
        if transfer_receipt and files_record:
            try:
                raw_tr = base64.b64decode(transfer_receipt.split(',')[-1] if ',' in transfer_receipt else transfer_receipt)
                drive_adapter = DriveAdapter()
                drive_resp = await drive_adapter.upload_pdf(files_record.name, raw_tr)
                if drive_resp:
                    if self.file_repo:
                        await self.file_repo.update(files_record.id, {
                            'driveFileId': drive_resp.get('id', ''),
                            'url': drive_resp.get('webViewLink', ''),
                        })
                    else:
                        await prisma_client.client.files.update(
                            where={'id': files_record.id},
                            data={
                                'driveFileId': drive_resp.get('id', ''),
                                'url': drive_resp.get('webViewLink', ''),
                            },
                        )
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

        # Construir la entidad que vamos a retornar
        reservation_entity = ReservationEntity(
            id=reservation_db.id,
            userId=reservation_db.userId,
            eventId=reservation_db.eventId,
            termsAccepted=reservation_db.termsAccepted,
            imageRightsAccepted=reservation_db.imageRightsAccepted,
            privacyAccepted=reservation_db.privacyAccepted,
            reservationDate=to_datetime(reservation_db.reservationDate),
            pastoralLetterUploaded=reservation_db.pastoralLetterUploaded,
            pastoralLetterUploadedAt=to_datetime(reservation_db.pastoralLetterUploadedAt),
            pastorContact=reservation_db.pastorContact,
            paymentCompletedAt=to_datetime(reservation_db.paymentCompletedAt),
            paymentStatus=reservation_db.paymentStatus,
            status=reservation_db.status,
            createdAt=to_datetime(reservation_db.createdAt),
            updatedAt=to_datetime(reservation_db.updatedAt),
        )

        # Enviar email de confirmación (best-effort)
        try:
            # intentar obtener email del user creado a partir de created
            user_obj = created.get('user') if isinstance(created, dict) else getattr(created, 'user', None)

            def _get_attr(o, k):
                if o is None:
                    return None
                if isinstance(o, dict):
                    return o.get(k)
                return getattr(o, k, None)

            user_email = _get_attr(user_obj, 'email')
            first_name = _get_attr(user_obj, 'firstname') or _get_attr(user_obj, 'firstName') or ''

            if user_email:
                try:
                    resend = ResendService()
                    subject = f"Confirmación de inscripción - {event.title}"
                    html = f"<p>Hola {first_name},</p><p>Tu inscripción al evento <strong>{event.title}</strong> se ha creado correctamente. Tu reserva ID es <code>{reservation_db.id}</code>.</p>"
                    # programar envío en background (no bloquear la respuesta)
                    import asyncio

                    asyncio.create_task(resend.send_email(to=user_email, subject=subject, html=html))
                except Exception:
                    # no queremos romper el flujo por fallos en el email
                    pass
        except Exception:
            pass

        return reservation_entity

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
            for item in reversed(created_ids):
                if 'paypal_payment_detail' in item:
                    await prisma_client.client.paypalpaymentdetail.delete(where={ 'id': item['paypal_payment_detail'] })
                if 'payment' in item:
                    await prisma_client.client.payment.delete(where={ 'id': item['payment'] })
                if 'files' in item:
                    await prisma_client.client.files.delete(where={ 'id': item['files'] })
                if 'reservation' in item:
                    await prisma_client.client.reservations.delete(where={ 'id': item['reservation'] })
        except Exception:
            # No podemos hacer más si falla la limpieza
            pass
