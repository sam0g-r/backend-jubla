from typing import Optional


class StateRepository:
    async def get_by_id(self, state_id: str) -> Optional[dict]:
        """Return state record or None"""
        raise NotImplementedError()
