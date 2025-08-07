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
        )

    async def create(self, event: Event) -> Event:
        """Crear un nuevo evento en la base de datos"""
        async with prisma_client as client:
            db_event = await client.event.create(
                data={
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
                    "price": event.price,
                }
            )
            return self._to_entity(db_event)

    async def get_by_id(self, event_id: str) -> Optional[Event]:
        """Obtener evento por ID"""
        async with prisma_client as client:
            db_event = await client.event.find_unique(where={"id": event_id})
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
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "country_id": event.country_id,
                    "state_id": event.state_id,
                    "currency": event.currency,
                    "is_active": event.is_active,
                    "max_capacity": event.max_capacity,
                    "pastoral_letter_deadline": event.pastoral_letter_deadline,
                    "payment_deadline": event.payment_deadline,
                    "price": event.price,
                },
            )
            return self._to_entity(db_event)

    async def delete(self, event_id: str) -> bool:
        """Eliminar evento"""
        async with prisma_client as client:
            try:
                await client.event.delete(where={"id": event_id})
                return True
            except Exception:
                return False

    async def list_active(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos activos con paginación"""
        async with prisma_client as client:
            db_events = await client.event.find_many(
                where={"is_active": True},
                skip=skip,
                take=limit,
                order=[{"start_date": "asc"}],
            )
            return [self._to_entity(db_event) for db_event in db_events]

    async def list_upcoming(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Listar eventos próximos con paginación"""
        async with prisma_client as client:
            db_events = await client.event.find_many(
                where={"start_date": {"gt": datetime.now()}},
                skip=skip,
                take=limit,
                order=[{"start_date": "asc"}],
            )
            return [self._to_entity(db_event) for db_event in db_events]

    async def exists_by_slug(self, slug: str) -> bool:
        """Verificar si existe un evento con el slug dado"""
        async with prisma_client as client:
            event = await client.event.find_unique(where={"slug": slug})
            return event is not None
