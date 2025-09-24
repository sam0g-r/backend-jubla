from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str


class UserSignUp(ABC):
    @abstractmethod
    async def register(self, email: str, password: str):
        pass
