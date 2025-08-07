<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
from typing import List, Optional
from datetime import datetime
from app.domain.entities.event import Event
from app.domain.repositories.event_repository import EventRepository
from app.infrastructure.database.prisma_client import prisma_client

class EventRepositoryImpl(EventRepository):
    """
    Implementación del repositorio de eventos usando Prisma.
    """

    def _to_entity(self, db_event) -> Event:
        return Event(
            id=db_event.id,
<<<<<<< Updated upstream
            organization_id=db_event.organization_id,
            title=db_event.title,
            slug=db_event.slug,
            description=db_event.description,
            start_date=db_event.start_date,
            end_date=db_event.end_date,
            country_id=db_event.country_id,
            state_id=db_event.state_id,
            currency=db_event.currency,
            is_active=db_event.is_active,
            max_capacity=db_event.max_capacity,
            pastoral_letter_deadline=db_event.pastoral_letter_deadline,
            payment_deadline=db_event.payment_deadline,
            price=db_event.price,
            created_at=db_event.created_at,
            updated_at=db_event.updated_at,
=======
            organizationId=db_event.organizationId,
            title=db_event.title,
            slug=db_event.slug,
            description=db_event.description,
            startDate=db_event.startDate,
            endDate=db_event.endDate,
            countryId=db_event.countryId,
            stateId=db_event.stateId,
            currency=db_event.currency,
            isActive=db_event.isActive,
            maxCapacity=db_event.maxCapacity,
            pastoralLetterDeadline=db_event.pastoralLetterDeadline,
            paymentDeadline=db_event.paymentDeadline,
            price=db_event.price,
            createdAt=db_event.createdAt,
            updatedAt=db_event.updatedAt,
>>>>>>> Stashed changes
        )

    async def create(self, event: Event) -> Event:
        """Crear un nuevo evento en la base de datos"""
        async with prisma_client as client:
            db_event = await client.event.create(
                data={
<<<<<<< Updated upstream
                    "organization_id": event.organization_id,
                    "title": event.title,
                    "slug": event.slug,
                    "description": event.description,
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "country_id": event.country_id,
                    "state_id": event.state_id,
                    "currency": event.currency,
                    "max_capacity": event.max_capacity,
                    "pastoral_letter_deadline": event.pastoral_letter_deadline,
                    "payment_deadline": event.payment_deadline,
=======
                    "organizationId": event.organizationId,
                    "title": event.title,
                    "slug": event.slug,
                    "description": event.description,
                    "startDate": event.startDate,
                    "endDate": event.endDate,
                    "countryId": event.countryId,
                    "stateId": event.stateId,
                    "currency": event.currency,
                    "maxCapacity": event.maxCapacity,
                    "pastoralLetterDeadline": event.pastoralLetterDeadline,
                    "paymentDeadline": event.paymentDeadline,
>>>>>>> Stashed changes
                    "price": event.price,
                }
            )
            return self._to_entity(db_event)

<<<<<<< Updated upstream
    async def get_by_id(self, event_id: str) -> Optional[Event]:
        """Obtener evento por ID"""
        async with prisma_client as client:
            db_event = await client.event.find_unique(where={"id": event_id})
=======
    async def get_by_id(self, eventId: str) -> Optional[Event]:
        """Obtener evento por ID"""
        async with prisma_client as client:
            db_event = await client.event.find_unique(where={"id": eventId})
>>>>>>> Stashed changes
            if db_event:
                return self._to_entity(db_event)
            return None

    async def get_by_slug(self, slug: str) -> Optional[Event]:
        """Obtener evento por slug"""
        async with prisma_client as client:
            db_event = await client.event.find_unique(where={"slug": slug})
            if db_event:
                return self._to_entity(db_event)
            return None

    async def update(self, event: Event) -> Event:
        """Actualizar evento"""
        async with prisma_client as client:
            db_event = await client.event.update(
                where={"id": event.id},
                data={
                    "title": event.title,
                    "slug": event.slug,
                    "description": event.description,
<<<<<<< Updated upstream
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "country_id": event.country_id,
                    "state_id": event.state_id,
                    "currency": event.currency,
                    "is_active": event.is_active,
                    "max_capacity": event.max_capacity,
                    "pastoral_letter_deadline": event.pastoral_letter_deadline,
                    "payment_deadline": event.payment_deadline,
=======
                    "startDate": event.startDate,
                    "endDate": event.endDate,
                    "countryId": event.countryId,
                    "stateId": event.stateId,
                    "currency": event.currency,
                    "isActive": event.isActive,
                    "maxCapacity": event.maxCapacity,
                    "pastoralLetterDeadline": event.pastoralLetterDeadline,
                    "paymentDeadline": event.paymentDeadline,
>>>>>>> Stashed changes
                    "price": event.price,
                },
            )
            return self._to_entity(db_event)

<<<<<<< Updated upstream
    async def delete(self, event_id: str) -> bool:
        """Eliminar evento"""
        async with prisma_client as client:
            try:
                await client.event.delete(where={"id": event_id})
=======
    async def delete(self, eventId: str) -> bool:
        """Eliminar evento"""
        async with prisma_client as client:
            try:
                await client.event.delete(where={"id": eventId})
>>>>>>> Stashed changes
                return True
            except Exception:
                return False

    async def list_active(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos activos con paginación"""
        async with prisma_client as client:
            db_events = await client.event.find_many(
<<<<<<< Updated upstream
                where={"is_active": True},
                skip=skip,
                take=limit,
                order=[{"start_date": "asc"}],
=======
                where={"isActive": True},
                skip=skip,
                take=limit,
                order=[{"startDate": "asc"}],
>>>>>>> Stashed changes
            )
            return [self._to_entity(db_event) for db_event in db_events]

    async def list_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos próximos con paginación"""
        async with prisma_client as client:
            db_events = await client.event.find_many(
<<<<<<< Updated upstream
                where={"start_date": {"gt": datetime.now()}},
                skip=skip,
                take=limit,
                order=[{"start_date": "asc"}],
=======
                where={"startDate": {"gt": datetime.now()}},
                skip=skip,
                take=limit,
                order=[{"startDate": "asc"}],
>>>>>>> Stashed changes
            )
            return [self._to_entity(db_event) for db_event in db_events]

    async def exists_by_slug(self, slug: str) -> bool:
        """Verificar si existe un evento con el slug dado"""
        async with prisma_client as client:
            event = await client.event.find_unique(where={"slug": slug})
            return event is not None
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
