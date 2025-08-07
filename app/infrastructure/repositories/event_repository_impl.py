from typing import List, Optional
from app.domain.entities.event import Event
from app.domain.repositories.event_repository import EventRepository

class EventRepositoryImpl(EventRepository):
    """
    Implementación placeholder del repositorio de eventos.
    En una implementación real, aquí se conectaría a la base de datos.
    """
    
    def __init__(self):
        # Simular una base de datos en memoria
        self._events = {}
    
    async def create(self, event: Event) -> Event:
        self._events[str(event.id)] = event
        return event
    
    async def get_by_id(self, event_id: str) -> Optional[Event]:
        return self._events.get(str(event_id))
    
    async def get_by_slug(self, slug: str) -> Optional[Event]:
        for event in self._events.values():
            if event.slug == slug:
                return event
        return None
    
    async def update(self, event: Event) -> Event:
        if str(event.id) in self._events:
            self._events[str(event.id)] = event
        return event
    
    async def delete(self, event_id: str) -> bool:
        if str(event_id) in self._events:
            del self._events[str(event_id)]
            return True
        return False
    
    async def list_active(self, skip: int = 0, limit: int = 100) -> List[Event]:
        active_events = [event for event in self._events.values() if event.is_active]
        return active_events[skip:skip + limit]
    
    async def list_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        from datetime import datetime
        now = datetime.now()
        upcoming_events = [event for event in self._events.values() if event.start_date > now]
        return upcoming_events[skip:skip + limit]
    
    async def exists_by_slug(self, slug: str) -> bool:
        return await self.get_by_slug(slug) is not None 