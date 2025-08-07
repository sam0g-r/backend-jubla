from typing import Optional, List
from datetime import datetime
from app.domain.entities.event import Event
from app.domain.repositories.event_repository import EventRepository
from app.application.dto.event_dto import CreateEventDTO, UpdateEventDTO, EventResponseDTO
from app.shared.exceptions.event_exceptions import EventNotFoundError, EventAlreadyExistsError

class EventUseCases:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository
    
    async def create_event(self, event_data: CreateEventDTO) -> EventResponseDTO:
        # Verificar si el evento ya existe
        existing_event = await self.event_repository.get_by_slug(event_data.slug)
        if existing_event:
            raise EventAlreadyExistsError(f"Event with slug {event_data.slug} already exists")
        
        # Crear entidad de evento
        generate_id = cuid_wrapper()
        event = Event(
            id=generate_id(),
            title=event_data.title,
            slug=event_data.slug,
            description=event_data.description,
            startDate=event_data.startDate,
            endDate=event_data.endDate,
            max_participants=event_data.max_participants,
            current_participants=0,
            price=event_data.price,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        # Guardar en repositorio
        created_event = await self.event_repository.create(event)
        return EventResponseDTO.from_entity(created_event)
    
    async def get_by_id(self, eventId: str) -> Optional[EventResponseDTO]:
        event = await self.event_repository.get_by_id(eventId)
        if not event:
            raise EventNotFoundError(f"Event with id {eventId} not found")
        return EventResponseDTO.from_entity(event)
    
    async def get_by_slug(self, slug: str) -> Optional[EventResponseDTO]:
        event = await self.event_repository.get_by_slug(slug)
        if not event:
            raise EventNotFoundError(f"Event with slug {slug} not found")
        return EventResponseDTO.from_entity(event)
    
    async def update_event(self, eventId: str, event_data: UpdateEventDTO) -> EventResponseDTO:
        event = await self.event_repository.get_by_id(eventId)
        if not event:
            raise EventNotFoundError(f"Event with id {eventId} not found")
        
        # Actualizar campos
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.description is not None:
            event.description = event_data.description
        if event_data.startDate is not None:
            event.startDate = event_data.startDate
        if event_data.endDate is not None:
            event.endDate = event_data.endDate
        if event_data.max_participants is not None:
            event.max_participants = event_data.max_participants
        if event_data.price is not None:
            event.price = event_data.price
        if event_data.isActive is not None:
            event.isActive = event_data.isActive
        
        event.updatedAt = datetime.utcnow()
        
        updated_event = await self.event_repository.update(event)
        return EventResponseDTO.from_entity(updated_event)
    
    async def delete_event(self, eventId: str) -> bool:
        event = await self.event_repository.get_by_id(eventId)
        if not event:
            raise EventNotFoundError(f"Event with id {eventId} not found")
        
        return await self.event_repository.delete(eventId)
    
    async def list_active_events(self, skip: int = 0, limit: int = 100) -> List[EventResponseDTO]:
        events = await self.event_repository.list_active(skip=skip, limit=limit)
        return [EventResponseDTO.from_entity(event) for event in events]
    
    async def list_upcoming_events(self, skip: int = 0, limit: int = 100) -> List[EventResponseDTO]:
        events = await self.event_repository.list_upcoming(skip=skip, limit=limit)
        return [EventResponseDTO.from_entity(event) for event in events] 