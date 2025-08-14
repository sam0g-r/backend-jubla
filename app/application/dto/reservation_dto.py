from app.domain.entities.financial_movement import FinancialMovement
from app.domain.entities.reservation_payment import ReservationPayment
from app.enums.payment_status_enum import PaymentStatusEnum
from app.enums.reservation_status_enum import ReservationStatusEnum
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional


class ReservationDTO(BaseModel):
    id: str
    userId: str
    eventId: str
    reservationDate: datetime
    paymentStatus: PaymentStatusEnum
    status: ReservationStatusEnum
    createdAt: datetime
    financialMovement: Optional[List[FinancialMovement]]
    payments: Optional[List[ReservationPayment]]
    updatedAt: Optional[datetime] = None
    pastoralLetterUploaded: bool = False
    pastoralLetterUploadedAt: Optional[datetime] = None
    paymentCompletedAt: Optional[datetime] = None
    termsAccepted: bool = False
    imageRightsAccepted: bool = False

    @classmethod
    def from_entity(cls, reservation):
        def to_datetime(val):
            if val is None:
                return None
            if isinstance(val, datetime):
                return val
            if isinstance(val, date):
                return datetime.combine(val, datetime.min.time())
            return val

        # Normalize top-level datetime/date fields
        reservation_reservationDate = to_datetime(getattr(reservation, 'reservationDate', None))
        reservation_createdAt = to_datetime(getattr(reservation, 'createdAt', None))
        reservation_updatedAt = to_datetime(getattr(reservation, 'updatedAt', None))
        reservation_pastoralLetterUploadedAt = to_datetime(getattr(reservation, 'pastoralLetterUploadedAt', None))
        reservation_paymentCompletedAt = to_datetime(getattr(reservation, 'paymentCompletedAt', None))

        # Normalize nested financialMovement date fields if present
        fm_list = None
        if getattr(reservation, 'financialMovement', None):
            fm_list = []
            for fm in reservation.financialMovement:
                # create a shallow copy dict with converted dates to avoid mutating original objects
                fm_dict = dict(fm.__dict__)
                if 'date' in fm_dict:
                    fm_dict['date'] = to_datetime(fm_dict.get('date'))
                if 'createdAt' in fm_dict:
                    fm_dict['createdAt'] = to_datetime(fm_dict.get('createdAt'))
                if 'updatedAt' in fm_dict:
                    fm_dict['updatedAt'] = to_datetime(fm_dict.get('updatedAt'))
                fm_list.append(fm_dict)

        # Normalize nested payments date fields if present
        payments_list = None
        if getattr(reservation, 'payments', None):
            payments_list = []
            for p in reservation.payments:
                p_dict = dict(p.__dict__)
                if 'createdAt' in p_dict:
                    p_dict['createdAt'] = to_datetime(p_dict.get('createdAt'))
                if 'updatedAt' in p_dict:
                    p_dict['updatedAt'] = to_datetime(p_dict.get('updatedAt'))
                payments_list.append(p_dict)

        return cls(
            id=reservation.id,
            userId=reservation.userId,
            eventId=reservation.eventId,
            reservationDate=reservation_reservationDate,
            paymentStatus=reservation.paymentStatus,
            status=reservation.status,
            createdAt=reservation_createdAt,
            financialMovement=fm_list,
            payments=payments_list,
            updatedAt=reservation_updatedAt,
            pastoralLetterUploaded=reservation.pastoralLetterUploaded,
            pastoralLetterUploadedAt=reservation_pastoralLetterUploadedAt,
            paymentCompletedAt=reservation_paymentCompletedAt,
            termsAccepted=reservation.termsAccepted,
            imageRightsAccepted=reservation.imageRightsAccepted
        )
    
class ReservationQueryDTO(BaseModel):
    reservations: List[ReservationDTO]
    total: int
