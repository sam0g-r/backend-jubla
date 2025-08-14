from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from app.enums import PaymentStatusEnum, ReservationStatusEnum
from app.domain.entities.financial_movement import FinancialMovement
from app.domain.entities.reservation_payment import ReservationPayment


@dataclass
class Reservation:
    id: str
    userId: str
    eventId: str
    termsAccepted: bool = False
    imageRightsAccepted: bool = False
    reservationDate: datetime = field(default_factory=datetime.now)
    pastoralLetterUploaded: bool = False
    pastoralLetterUploadedAt: Optional[datetime] = None
    paymentCompletedAt: Optional[datetime] = None
    paymentStatus: PaymentStatusEnum = PaymentStatusEnum.PENDING
    status: ReservationStatusEnum = ReservationStatusEnum.PENDING_BOTH
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime = field(default_factory=datetime.now)
    financialMovement: Optional[List[FinancialMovement]] = field(default_factory=list)
    payments: Optional[List[ReservationPayment]] = field(default_factory=list)
