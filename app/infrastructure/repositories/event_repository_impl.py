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
        )

    async def create(self, event: Event) -> Event:
        """Crear un nuevo evento en la base de datos"""
        db_event = await prisma_client.client.event.create(data=event.__dict__)
        return self._to_entity(db_event)

    async def get_by_id(self, eventId: str) -> Optional[Event]:
        """Obtener evento por ID"""
        db_event = await prisma_client.client.event.find_unique(where={"id": eventId})
        if db_event:
            return self._to_entity(db_event)
        return None

    async def get_by_slug(self, slug: str) -> Optional[Event]:
        """Obtener evento por slug"""
        db_event = await prisma_client.client.event.find_unique(where={"slug": slug})
        if db_event:
            return self._to_entity(db_event)
        return None

    async def update(self, event: Event) -> Event:
        """Actualizar evento"""
        db_event = await prisma_client.client.event.update(
            where={"id": event.id},
            data={
                "title": event.title,
                "slug": event.slug,
                "description": event.description,
                "startDate": event.startDate,
                "endDate": event.endDate,
                "countryId": event.countryId,
                "stateId": event.stateId,
                "currency": event.currency,
                "isActive": event.isActive,
                "maxCapacity": event.maxCapacity,
                "pastoralLetterDeadline": event.pastoralLetterDeadline,
                "paymentDeadline": event.paymentDeadline,
                "price": event.price,
            },
        )
        return self._to_entity(db_event)

    async def delete(self, eventId: str) -> bool:
        """Eliminar evento"""
        try:
            await prisma_client.client.event.delete(where={"id": eventId})
            return True
        except Exception:
            return False

    async def list_active(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos activos con paginación"""
        db_events = await prisma_client.client.event.find_many(
            where={"isActive": True},
            skip=skip,
            take=limit,
            order=[{"startDate": "asc"}],
        )
        return [self._to_entity(db_event) for db_event in db_events]

    async def list_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos próximos con paginación"""
        db_events = await prisma_client.client.event.find_many(
            where={"startDate": {"gt": datetime.now()}},
            skip=skip,
            take=limit,
            order=[{"startDate": "asc"}],
        )
        return [self._to_entity(db_event) for db_event in db_events]

    async def exists_by_slug(self, slug: str) -> bool:
        """Verificar si existe un evento con el slug dado"""
        event = await prisma_client.client.event.find_unique(where={"slug": slug})
        return event is not None
