from typing import Optional


class CountryRepository:
    async def get_by_id(self, country_id: str) -> Optional[dict]:
        """Return country record or None"""
        raise NotImplementedError()
