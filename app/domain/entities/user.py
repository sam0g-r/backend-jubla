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