from fastapi import APIRouter, Depends
from typing import List
from app.application.use_cases.location_use_cases import LocationUseCases
from app.application.dto.location_dto import CountryResponseDTO, StateResponseDTO, CityResponseDTO
from app.presentation.dependencies import get_location_use_cases


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/countries", response_model=List[CountryResponseDTO])
async def list_countries(
    skip: int = 0,
    limit: int = 999,
    location_use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await location_use_cases.list_countries(skip=skip, limit=limit)


@router.get("/states/{country_id}", response_model=List[StateResponseDTO])
async def list_states(
    country_id: str,
    skip: int = 0,
    limit: int = 999,
    location_use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await location_use_cases.list_states(country_id=country_id, skip=skip, limit=limit)


@router.get("/cities/{state_id}", response_model=List[CityResponseDTO])
async def list_cities(
    state_id: str,
    skip: int = 0,
    limit: int = 999,
    location_use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await location_use_cases.list_cities(state_id=state_id, skip=skip, limit=limit)


@router.get("/cities/by-country/{country_id}", response_model=List[CityResponseDTO])
async def list_cities_by_country(
    country_id: str,
    skip: int = 0,
    limit: int = 999,
    location_use_cases: LocationUseCases = Depends(get_location_use_cases),
):
    return await location_use_cases.list_cities_by_country(country_id=country_id, skip=skip, limit=limit)
