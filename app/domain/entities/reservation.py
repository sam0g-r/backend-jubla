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
    user_id: str
    event_id: str
    terms_accepted: bool = False
    image_rights_accepted: bool = False
    reservation_date: datetime = field(default_factory=datetime.now)
    pastoral_letter_uploaded: bool = False
    pastoral_letter_uploaded_at: Optional[datetime] = None
    payment_completed_at: Optional[datetime] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    status: ReservationStatus = ReservationStatus.PENDING_BOTH
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
