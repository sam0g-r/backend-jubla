from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.domain.entities.user_role import UserRole


class UserRoleRepository(ABC):
    @abstractmethod
    async def create(self, user_role: UserRole) -> UserRole:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[UserRole]:
        pass

    @abstractmethod
    async def update(self, user_role: UserRole) -> UserRole:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10):
        pass
