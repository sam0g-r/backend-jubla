from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Tuple
from app.domain.entities.role import Role


class RoleRepository(ABC):
    @abstractmethod
    async def create(self, r: Role) -> Role:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[str]) -> List[Role]:
        pass

    @abstractmethod
    async def update(self, r: Role) -> Role:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def query(self, filters: Optional[Dict] = None, skip: int = 0, limit: int = 10) -> Tuple[List[Role], int]:
        pass
