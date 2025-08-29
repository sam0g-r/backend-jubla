from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

from app.domain.value_objects import CuidStr


class PersonDataODM(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    birthdate: date
    gender: str
    documentId: str
    password: str
    confirmPassword: str
    birthCountry: str
    countryId: CuidStr
    stateId: CuidStr
    terms: bool
    imageTerms: bool
    privacyAccepted: bool
    phone: Optional[str] = None
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None


class MedicalDataODM(BaseModel):
    emergencyContactName: str
    emergencyContactPhone: str
    emergencyContactRelationship: str
    emergencyContactEmail: EmailStr
    hasPatologies: bool = False
    hasMedication: bool = False
    hasAllergies: bool = False
    hasMedicationAllergies: bool = False
    hasSurgeryHistory: bool = False
    hasDaietaryRestrictions: bool = False
    patologies: Optional[str] = None
    medication: Optional[str] = None
    allergies: Optional[str] = None
    medicationAllergies: Optional[str] = None
    surgeryHistory: Optional[str] = None
    dietaryRestrictions: Optional[str] = None


class ChurchDataODM(BaseModel):
    church: str
    pastorName: str
    pastorContact: str
    ministries: str
    pastoralLetter: Optional[str] = None ## Base64 encoded PDF


class PaymentDataODM(BaseModel):
    paymentMethod: str
    slug: str
    paypalOrderId: Optional[str] = None
    transferReceipt: Optional[str] = None


class CreateFullReservationODM(BaseModel):
    personalData: PersonDataODM
    medicalData: MedicalDataODM
    churchData: ChurchDataODM
    paymentData: PaymentDataODM


class CreateReservationODM(BaseModel):
    userId: CuidStr
    eventId: CuidStr
    termsAccepted: bool = False
    imageRightsAccepted: bool = False
    privacyAccepted: bool = False
    pastorContact: Optional[str] = None
    reservationDate: Optional[datetime]
    pastoralLetterUploaded: bool = False
    pastoralLetterUploadedAt: Optional[datetime] = None
    paymentCompletedAt: Optional[datetime] = None
    paymentStatus: Optional[str] = None
    status: Optional[str] = None


class UpdateReservationODM(BaseModel):
    termsAccepted: Optional[bool] = None
    imageRightsAccepted: Optional[bool] = None
    privacyAccepted: Optional[bool] = None
    pastorContact: Optional[str] = None
    pastoralLetterUploaded: Optional[bool] = None
    pastoralLetterUploadedAt: Optional[datetime] = None
    paymentCompletedAt: Optional[datetime] = None
    paymentStatus: Optional[str] = None
    status: Optional[str] = None
