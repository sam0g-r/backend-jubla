from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.use_cases.event_use_cases import EventUseCases
from app.application.dto.event_dto import CreateEventDTO, UpdateEventDTO, EventResponseDTO
from app.presentation.dependencies import get_event_use_cases
from app.shared.exceptions.event_exceptions import EventNotFoundError, EventAlreadyExistsError
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer


router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[EventResponseDTO])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    event_use_cases: EventUseCases = Depends(get_event_use_cases)
):
    events = await event_use_cases.list_active_events(skip=skip, limit=limit)
    return events

@router.get("/{slug}", response_model=EventResponseDTO)
async def get_event_by_slug(
    slug: str,
    event_use_cases: EventUseCases = Depends(get_event_use_cases)
):
    try:
        event = await event_use_cases.get_by_slug(slug)
        return event
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/", response_model=EventResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: CreateEventDTO,
    session: SessionContainer = Depends(verify_session()),
    event_use_cases: EventUseCases = Depends(get_event_use_cases)
):
    try:
        event = await event_use_cases.create_event(event_data)
        return event
    except EventAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.put("/{event_id}", response_model=EventResponseDTO)
async def update_event(
    event_id: str,
    event_data: UpdateEventDTO,
    session: SessionContainer = Depends(verify_session()),
    event_use_cases: EventUseCases = Depends(get_event_use_cases)
):
    try:
        event = await event_use_cases.update_event(event_id, event_data)
        return event
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    session: SessionContainer = Depends(verify_session()),
    event_use_cases: EventUseCases = Depends(get_event_use_cases)
):
    try:
        await event_use_cases.delete_event(event_id)
        return None
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 