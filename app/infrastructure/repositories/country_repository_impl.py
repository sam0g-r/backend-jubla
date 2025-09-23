from app.domain.repositories.country_repository import CountryRepository
from app.infrastructure.database.prisma_client import prisma_client


class CountryRepositoryImpl(CountryRepository):
    async def get_by_id(self, country_id: str) -> dict | None:
        return await prisma_client.client.country.find_unique(where={"id": country_id})
    
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return await prisma_client.client.country.find_many(skip=skip, take=limit, order={"name": "asc"})
