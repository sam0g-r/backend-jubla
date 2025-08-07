from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.event import Event

class EventRepository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event:
        pass
    
    @abstractmethod
    async def get_by_id(self, event_id: str) -> Optional[Event]:
        pass
    
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Event]:
        pass
    
    @abstractmethod
    async def update(self, event: Event) -> Event:
        pass
    
    @abstractmethod
    async def delete(self, event_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_active(self, skip: int = 0, limit: int = 100) -> List[Event]:
        pass
    
    @abstractmethod
    async def list_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        pass
    
    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool:
        pass 