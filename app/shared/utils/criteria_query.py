from typing import Any, Dict, List, Optional, Type, TypeVar, Generic, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar('T')

class CriteriaQuery(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def query(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> Tuple[List[T], int]:
        stmt = select(self.model)
        if filters:
            for attr, value in filters.items():
                if value is not None:
                    stmt = stmt.where(getattr(self.model, attr) == value)
        total = self.session.execute(select(self.model)).scalars().count()
        results = self.session.execute(stmt.offset(skip).limit(limit)).scalars().all()
        return results, total
