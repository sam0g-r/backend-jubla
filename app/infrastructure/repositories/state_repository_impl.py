from app.domain.repositories.state_repository import StateRepository
from app.infrastructure.database.prisma_client import prisma_client


class StateRepositoryImpl(StateRepository):
    async def get_by_id(self, state_id: str) -> dict | None:
        return await prisma_client.client.state.find_unique(where={"id": state_id})

    async def list_by_country(self, country_id: str, skip: int = 0, limit: int = 100) -> list[dict]:
        return await prisma_client.client.state.find_many(where={"countryId": country_id}, skip=skip, take=limit, order={"name": "asc"})
