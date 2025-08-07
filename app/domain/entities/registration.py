from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"

class PastoralLetterStatus(str, Enum):
    PENDING = "PENDING"
    UPLOADED = "UPLOADED"

@dataclass
class Registration:
    id: str
    user_id: str
    event_id: str
    payment_status: PaymentStatus
    pastoral_letter_status: PastoralLetterStatus
    paypal_order_id: Optional[str] = None
    pastoral_letter_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    
    # Datos médicos
    has_patology: bool = False
    pathology: Optional[str] = None
    has_medication: bool = False
    medication: Optional[str] = None
    has_medication_allergy: bool = False
    medication_allergy: Optional[str] = None
    has_allergy: bool = False
    allergy: Optional[str] = None
    has_surgery: bool = False
    surgery: Optional[str] = None
    has_diet: bool = False
    diet: Optional[str] = None
    
    # Contacto de emergencia
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    emergency_contact_email: Optional[str] = None
    
    # Datos de iglesia
    church: Optional[str] = None
    pastor_name: Optional[str] = None
    ministries: Optional[str] = None 