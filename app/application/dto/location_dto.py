from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CountryResponseDTO(BaseModel):
    id: str
    name: str
    code: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, country: dict):
        def _get(obj, key):
            if obj is None:
                return None
            if isinstance(obj, dict):
                return obj.get(key)
            if hasattr(obj, key):
                return getattr(obj, key)
            try:
                return obj[key]
            except Exception:
                return None

        return cls(
            id=_get(country, "id"),
            name=_get(country, "name"),
            code=_get(country, "code"),
            createdAt=_get(country, "createdAt"),
            updatedAt=_get(country, "updatedAt"),
        )


class StateResponseDTO(BaseModel):
    id: str
    name: str
    countryId: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, state: dict):
        def _get(obj, key):
            if obj is None:
                return None
            if isinstance(obj, dict):
                return obj.get(key)
            if hasattr(obj, key):
                return getattr(obj, key)
            try:
                return obj[key]
            except Exception:
                return None

        return cls(
            id=_get(state, "id"),
            name=_get(state, "name"),
            countryId=_get(state, "countryId"),
            createdAt=_get(state, "createdAt"),
            updatedAt=_get(state, "updatedAt"),
        )


class CityResponseDTO(BaseModel):
    id: str
    name: str
    stateId: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True

    @classmethod
    def from_entity(cls, city: dict):
        def _get(obj, key):
            if obj is None:
                return None
            if isinstance(obj, dict):
                return obj.get(key)
            if hasattr(obj, key):
                return getattr(obj, key)
            try:
                return obj[key]
            except Exception:
                return None

        return cls(
            id=_get(city, "id"),
            name=_get(city, "name"),
            stateId=_get(city, "stateId"),
            createdAt=_get(city, "createdAt"),
            updatedAt=_get(city, "updatedAt"),
        )
