from typing import Optional, List


class StateRepository:
    async def get_by_id(self, state_id: str) -> Optional[dict]:
        """Return state record or None"""
        raise NotImplementedError()

    async def list_by_country(self, country_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Return list of states for a given country"""
        raise NotImplementedError()
