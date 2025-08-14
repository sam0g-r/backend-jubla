from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from app.enums import PaymentStatusEnum
from app.domain.entities.financial_movement import FinancialMovement
from app.domain.entities.reservation_payment import ReservationPayment
from app.domain.entities.paypal_payment_detail import PaypalPaymentDetail


@dataclass
class Payment:
    id: str
    userId: str
    amount: float
    currency: str
    paymentMethod: str
    financialMovement: List[FinancialMovement] = field(default_factory=list)
    reservationsPayments: List[ReservationPayment] = field(default_factory=list)
    paymentDetails: Optional[PaypalPaymentDetail] = None
    updatedAt: datetime = field(default_factory=datetime.now)
    createdAt: datetime = field(default_factory=datetime.now)
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
