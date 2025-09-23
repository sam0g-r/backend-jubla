from typing import Optional, List


class CityRepository:
    async def get_by_id(self, city_id: str) -> Optional[dict]:
        """Return city record or None"""
        raise NotImplementedError()

    async def list_by_state(self, state_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Return list of cities for a given state"""
        raise NotImplementedError()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Return list of all cities"""
        raise NotImplementedError()

    async def list_by_country(self, country_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Return list of cities for a given country (via its states)"""
        raise NotImplementedError()
