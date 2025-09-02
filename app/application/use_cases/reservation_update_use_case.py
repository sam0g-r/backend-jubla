from datetime import datetime
from app.application.dto.reservation_dto import ReservationDTO
from app.domain.repositories.reservation_repository import ReservationRepository

from app.infrastructure.adapters.drive_adapter import DriveAdapter
import base64
from app.infrastructure.adapters.paypal_adapter import PaypalAdapter
from app.infrastructure.database.prisma_client import prisma_client

from app.enums.reservation_status_enum import ReservationStatusEnum


class UpdateReservationUseCase:
    def __init__(self, reservation_repository: ReservationRepository):
        self.reservation_repository = reservation_repository

    async def execute(self, reservationId: str, updates: dict) -> ReservationDTO:
        updates['updatedAt'] = datetime.now()

        pastoral_b64 = updates.get('pastoralLetter')
        transfer_b64 = updates.get('transferReceipt')
        paypal_order_id = updates.get('paypalOrderId')

        files_record = None

        # 1) File creation (DB) and reservation updates inside repo transaction
        if pastoral_b64 or transfer_b64:
            is_pastoral = bool(pastoral_b64)
            # prepare file metadata
            file_name = f"{'pastoral_letter' if is_pastoral else 'transfer_receipt'}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            file_metadata = {
                'name': file_name,
                'mimeType': 'application/pdf',
                'driveFileId': '',
                'url': '',
                'fileableType': 'USER',
            }

            created = await self.reservation_repository.create_file_for_reservation(reservationId, file_metadata, is_pastoral)
            files_record = created.get('files')

        # 2) Payment creation if paypalOrderId and not transfer receipt
        if paypal_order_id and not transfer_b64:
            paypal_adapter = PaypalAdapter()
            paypal_summary = await paypal_adapter.get_order_summary(paypal_order_id)
            if not paypal_summary:
                raise Exception('No se pudo obtener resumen de PayPal')

            payment_payload = {
                'amount': paypal_summary['amount'],
                'currency': paypal_summary['currency'],
                'paymentMethod': 'PAYPAL',
                'status': 'PENDING',
                'paypal_raw': paypal_summary['raw'],
                'payer_id': paypal_summary.get('payer_id'),
                'payer_email': paypal_summary.get('payer_email'),
            }

            await self.reservation_repository.create_payment_for_reservation(reservationId, payment_payload, paypal_summary.get('raw'))

        # 3) Upload file to Drive outside of transaction
        if files_record:
            try:
                file_b64 = pastoral_b64 if pastoral_b64 else transfer_b64
                raw = base64.b64decode(file_b64.split(',')[-1] if ',' in file_b64 else file_b64)
                drive_adapter = DriveAdapter()
                drive_resp = await drive_adapter.upload_pdf(files_record.name, raw)
                if drive_resp:
                    await prisma_client.client.files.update(where={'id': files_record.id}, data={
                        'driveFileId': drive_resp.get('id', ''),
                        'url': drive_resp.get('webViewLink', ''),
                    })
            except Exception:
                # log and continue
                pass

        # Final: perform a normal update for any remaining fields and return DTO
        reservation = await self.reservation_repository.update(reservationId, updates)
        return ReservationDTO.from_entity(reservation)
