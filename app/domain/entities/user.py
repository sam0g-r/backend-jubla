from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.entities.email_verification import EmailVerification
from app.domain.entities.file import File
from app.domain.entities.oauth_provider import OAuthProvider
from app.domain.entities.password_reset import PasswordReset
from app.domain.entities.payment import Payment
from app.domain.entities.user_medical_information import UserMedicalInformation
from app.domain.entities.reservation import Reservation
from app.domain.entities.session import Session
from app.domain.entities.user_role import UserRole
from app.domain.entities.organization import OrganizationToUser


@dataclass
class User:
    id: str
    email: str
    firstname: str
    lastname: str
    birthdate: datetime
    gender: str
    documentId: str
    countryId: str
    stateId: str
    church: str
    phone: str
    password: str
    birthCountry: str
    profession: Optional[str] = None
    instagramProfile: Optional[str] = None
    medicalRecord: Optional[UserMedicalInformation] = None
    isActive: bool = True
    isVerified: bool = False
    deletedAt: Optional[datetime] = None
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: datetime = field(default_factory=datetime.now)
    emailVerifications: List[EmailVerification] = field(default_factory=list)
    files: List[File] = field(default_factory=list)
    oAuthProviders: List[OAuthProvider] = field(default_factory=list)
    passwordResets: List[PasswordReset] = field(default_factory=list)
    payments: List[Payment] = field(default_factory=list)
    reservations: List[Reservation] = field(default_factory=list)
    sessions: List[Session] = field(default_factory=list)
    roles: List[UserRole] = field(default_factory=list)
    organizationToUser: List[OrganizationToUser] = field(default_factory=list)


    @property
    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    @property
    def age(self) -> int:
        today = datetime.now()
        age = today.year - self.birthdate.year
        if today.month < self.birthdate.month or (
            today.month == self.birthdate.month and today.day < self.birthdate.day
        ):
            age -= 1
        return age
