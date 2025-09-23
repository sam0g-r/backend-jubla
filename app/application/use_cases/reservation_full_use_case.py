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

        # Prepare metadata list for any files that should be created for this user
        # We allow multiple files (e.g. pastoral letter and transfer receipt)
        file_metadata = []
        if pastoral_b64:
            file_name = f"pastoral_letter_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            file_metadata.append({
                'name': file_name,
                'mimeType': 'application/pdf',
                'driveFileId': '',
                'url': '',
                'fileableType': 'USER',
            })
        if transfer_receipt:
            file_name = f"transfer_receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            file_metadata.append({
                'name': file_name,
                'mimeType': 'application/pdf',
                'driveFileId': '',
                'url': '',
                'fileableType': 'USER',
            })

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
        # Pass list of file metadata (could be empty) to the transactional creation
        created = await self.reservation_repo.create_full_transactional(
            user_payload=user_create_data,
            medical_payload=med_payload,
            reservation_payload=reservation_payload,
            payment_payload=payment_payload,
            file_metadata=file_metadata if file_metadata else None,
        )

        # FIN transacción

        files_record = created.get('files')
        payment_db = created.get('payment')
        reservation_db = created.get('reservation')
        # Subir los PDFs a Google Drive después de que la transacción haya sido confirmada
        # Construir lista de items a subir: (b64_string, filename)
        upload_items = []
        if pastoral_b64:
            upload_items.append((pastoral_b64, f"pastoral_letter_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"))
        if transfer_receipt:
            upload_items.append((transfer_receipt, f"transfer_receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"))

        # Normalize files_record into a list so we can map uploads to DB records
        files_list = []
        if files_record:
            # The transactional repo might return a single record, a list, or None
            if isinstance(files_record, list):
                files_list = files_record
            else:
                files_list = [files_record]

        # If there are more upload_items than DB file records, create missing file records
        # using prisma_client directly (best-effort). We create minimal records matching schema.
        if len(upload_items) > len(files_list):
            for i in range(len(upload_items) - len(files_list)):
                idx = len(files_list) + i
                name = upload_items[idx][1]
                try:
                    new_file = await prisma_client.client.files.create(
                        data={
                            'name': name,
                            'mimeType': 'application/pdf',
                            'driveFileId': '',
                            'url': '',
                            'fileableType': 'USER',
                            'createdAt': datetime.now(),
                        }
                    )
                    files_list.append(new_file)
                except Exception as e:
                    # If creation fails, log and continue; we'll still try uploads but may not update DB
                    print(f"Warning: failed to create file record for {name}: {e}")

        # Now upload each item and update its corresponding file record if present
        for idx, (b64str, filename) in enumerate(upload_items):
            # Validate and decode base64 safely
            try:
                raw = base64.b64decode(b64str.split(',')[-1] if ',' in b64str else b64str)
            except Exception as e:
                print(f"Warning: invalid base64 for file {filename}: {e}")
                continue

            try:
                drive_adapter = DriveAdapter()
                drive_resp = await drive_adapter.upload_pdf(filename, raw)
                if drive_resp:
                    file_record = files_list[idx] if idx < len(files_list) else None
                    update_data = {
                        'driveFileId': drive_resp.get('id', ''),
                        'url': drive_resp.get('webViewLink', '') or drive_resp.get('webContentLink', ''),
                    }
                    if file_record:
                        if self.file_repo:
                            # Assume file_repo.update(id, data) signature; fall back to prisma if different
                            try:
                                await self.file_repo.update(file_record.id, update_data)
                            except Exception:
                                await prisma_client.client.files.update(
                                    where={'id': file_record.id},
                                    data=update_data,
                                )
                        else:
                            await prisma_client.client.files.update(
                                where={'id': file_record.id},
                                data=update_data,
                            )
                    else:
                        # No file record to update; try creating a record with drive info
                        try:
                            await prisma_client.client.files.create(
                                data={
                                    'name': filename,
                                    'mimeType': 'application/pdf',
                                    'driveFileId': drive_resp.get('id', ''),
                                    'url': drive_resp.get('webViewLink', '') or drive_resp.get('webContentLink', ''),
                                    'fileableType': 'USER',
                                    'createdAt': datetime.now(),
                                }
                            )
                        except Exception as e:
                            print(f"Warning: failed to create file record after upload for {filename}: {e}")
            except Exception as e:
                # fallo en upload: registrar y continuar; la transacción DB ya fue comprometida
                print(f"Warning: failed to upload {filename} to Drive: {e}")
                continue

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
