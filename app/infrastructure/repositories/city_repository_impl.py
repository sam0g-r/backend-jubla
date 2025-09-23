from app.domain.repositories.city_repository import CityRepository
from app.infrastructure.database.prisma_client import prisma_client
from typing import List, Optional


class CityRepositoryImpl(CityRepository):
    async def get_by_id(self, city_id: str) -> Optional[dict]:
        return await prisma_client.client.city.find_unique(where={"id": city_id})

    async def list_by_state(self, state_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        return await prisma_client.client.city.find_many(where={"stateId": state_id}, skip=skip, take=limit, order={"name": "asc"})

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return await prisma_client.client.city.find_many(skip=skip, take=limit, order={"name": "asc"})

    async def list_by_country(self, country_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        # obtener los estados del país
        # prisma-client-py in this project version may not support 'select' in find_many
        db_states = await prisma_client.client.state.find_many(where={"countryId": country_id})
        # extract ids from returned state objects (could be model instances or dicts)
        state_ids = []
        for s in db_states:
            if s is None:
                continue
            if hasattr(s, 'id'):
                state_ids.append(getattr(s, 'id'))
            else:
                try:
                    state_ids.append(s.get('id'))
                except Exception:
                    try:
                        state_ids.append(s['id'])
                    except Exception:
                        continue
        if not state_ids:
            return []
        return await prisma_client.client.city.find_many(where={"stateId": {"in": state_ids}}, skip=skip, take=limit, order={"name": "asc"})
