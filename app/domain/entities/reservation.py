from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class ReservationStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PENDING_PASTORAL_LETTER = "PENDING_PASTORAL_LETTER"
    PENDING_BOTH = "PENDING_BOTH"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"

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
    paymentStatus: PaymentStatus = PaymentStatus.PENDING
    status: ReservationStatus = ReservationStatus.PENDING_BOTH
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
