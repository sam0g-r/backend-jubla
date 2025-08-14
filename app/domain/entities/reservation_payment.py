from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ReservationPayment:
    id: str
    reservationId: str
    paymentId: str
    updatedAt: datetime = field(default_factory=datetime.now)
    createdAt: datetime = field(default_factory=datetime.now)
