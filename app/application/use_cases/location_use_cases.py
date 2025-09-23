from typing import List
from app.domain.repositories.country_repository import CountryRepository
from app.domain.repositories.state_repository import StateRepository
from app.domain.repositories.city_repository import CityRepository
from app.application.dto.location_dto import CountryResponseDTO, StateResponseDTO, CityResponseDTO


class LocationUseCases:
    def __init__(self, country_repository: CountryRepository, state_repository: StateRepository, city_repository: CityRepository):
        self.country_repository = country_repository
        self.state_repository = state_repository
        self.city_repository = city_repository

    async def list_countries(self, skip: int = 0, limit: int = 100) -> List[CountryResponseDTO]:
        countries = await self.country_repository.list_all(skip=skip, limit=limit)
        return [CountryResponseDTO.from_entity(c) for c in countries]

    async def list_states(self, country_id: str, skip: int = 0, limit: int = 100) -> List[StateResponseDTO]:
        states = await self.state_repository.list_by_country(country_id, skip=skip, limit=limit)
        return [StateResponseDTO.from_entity(s) for s in states]

    async def list_cities(self, state_id: str, skip: int = 0, limit: int = 100) -> List[CityResponseDTO]:
        cities = await self.city_repository.list_by_state(state_id, skip=skip, limit=limit)
        return [CityResponseDTO.from_entity(c) for c in cities]

    async def list_cities_by_country(self, country_id: str, skip: int = 0, limit: int = 100) -> List[CityResponseDTO]:
        cities = await self.city_repository.list_by_country(country_id, skip=skip, limit=limit)
        return [CityResponseDTO.from_entity(c) for c in cities]
