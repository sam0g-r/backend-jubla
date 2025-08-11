from app.application.use_cases.reservation_query_use_case import QueryReservationsUseCase
from app.domain.entities import user
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.application.use_cases.reservation_use_cases import CreateReservationUseCase
from app.infrastructure.repositories.reservation_repository_impl import ReservationRepositoryImpl
from app.application.use_cases.reservation_update_use_case import UpdateReservationUseCase
from app.domain.entities.reservation import Reservation
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/create", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: Dict[str, Any],
    session: SessionContainer = Depends(verify_session())
):
    reservation_repository = ReservationRepositoryImpl()
    use_case = CreateReservationUseCase(reservation_repository)
    reservation_data["userId"] = user["id"]
    try:
        reservation = use_case.execute(reservation_data)
        return reservation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get", response_model=List[Reservation])
async def list_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: SessionContainer = Depends(verify_session()),
    userId: Optional[str] = None,
    eventId: Optional[str] = None,
    status: Optional[str] = None
):
    filters = {}
    if userId:
        filters["userId"] = userId
    if eventId:
        filters["eventId"] = eventId
    if status:
        filters["status"] = status
    repo = ReservationRepositoryImpl()
    use_case = QueryReservationsUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results


@router.patch("/update/{reservation_id}", response_model=Reservation)
async def update(
    reservation_id: str,
    updates: Dict,
    session: SessionContainer = Depends(verify_session()),
):
    repo = ReservationRepositoryImpl()
    use_case = UpdateReservationUseCase(repo)
    try:
        updated = await use_case.execute(reservation_id, updates)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
