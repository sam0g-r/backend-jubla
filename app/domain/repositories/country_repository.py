from typing import Optional, List


class CountryRepository:
    async def get_by_id(self, country_id: str) -> Optional[dict]:
        """Return country record or None"""
        raise NotImplementedError()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Return list of countries"""
        raise NotImplementedError()
