from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from app.enums import FinancialMovementTypeEnum


@dataclass
class FinancialMovementToPurchaseOrder:
    a: str
    b: str


@dataclass
class FinancialMovement:
    id: str
    eventId: str
    type: FinancialMovementTypeEnum
    concept: str
    amount: float
    date: datetime = field(default_factory=datetime.now)
    origin: Optional[str] = None
    reservationId: Optional[str] = None
    paymentId: Optional[str] = None
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime = field(default_factory=datetime.now)
    financialMovementToPurchaseOrder: Optional[List[FinancialMovementToPurchaseOrder]] = field(default_factory=list)
