<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    firstname: str
    lastname: str
    email: str
    birthdate: datetime
    phone: str
    country: str
    state: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    is_active: bool = True
    
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
=======
>>>>>>> Stashed changes
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    email: str
    firstname: str
    lastname: str
    birthdate: datetime
<<<<<<< Updated upstream
    country_id: str
    state_id: str
    phone: str
    password: str
    church: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
=======
    countryId: str
    stateId: str
    phone: str
    password: str
    church: Optional[str] = None
    isActive: bool = True
    isVerified: bool = False
    deletedAt: Optional[datetime] = None
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
