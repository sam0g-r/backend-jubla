from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class PaypalPaymentDetail:
    id: str
    paymentId: str
    orderId: str
    captureId: Optional[str] = None
    payerId: Optional[str] = None
    payerEmail: Optional[str] = None
    rawData: Optional[str] = None
    updatedAt: Optional[datetime] = None
    refundId: Optional[str] = None
    refundedAmount: Optional[float] = None
    createdAt: datetime = field(default_factory=datetime.now)
