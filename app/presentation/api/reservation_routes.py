from app.application.dto.reservation_dto import ReservationDTO, ReservationQueryDTO
from app.application.use_cases.reservation_query_use_case import QueryReservationsUseCase
from app.domain.entities import user
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
import logging
from datetime import datetime, date
from app.application.use_cases.reservation_use_cases import CreateReservationUseCase
from app.infrastructure.repositories.reservation_repository_impl import ReservationRepositoryImpl
from app.application.use_cases.reservation_update_use_case import UpdateReservationUseCase
from app.domain.entities.reservation import Reservation
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from typing import List, Optional, Any
from app.application.odm.reservation_odm import CreateReservationODM, UpdateReservationODM

# NUEVO: imports para full reserva
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.user_medical_information_repository_impl import UserMedicalInformationRepositoryImpl
from app.infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from app.application.use_cases.reservation_full_use_case import CreateFullReservationUseCase
from app.application.odm.reservation_odm import CreateFullReservationODM

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservations", tags=["reservations"]) 


def _normalize_dates(obj: Any):
    """Recursively convert datetime/date to ISO strings in dicts/lists."""
    if obj is None:
        return None
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _normalize_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize_dates(v) for v in obj]
    return obj


# NUEVO ENDPOINT: flujo completo de reserva
@router.post("/full-create", response_model=ReservationDTO, status_code=status.HTTP_201_CREATED)
async def create_full_reservation(
    reservation_data: CreateFullReservationODM
):
    user_repo = UserRepositoryImpl()
    medical_repo = UserMedicalInformationRepositoryImpl()
    event_repo = EventRepositoryImpl()
    reservation_repo = ReservationRepositoryImpl()
    use_case = CreateFullReservationUseCase(user_repo, medical_repo, event_repo, reservation_repo)
    try:
        reservation = await use_case.execute(reservation_data.dict())
        # Convertir explícitamente a DTO para aplicar las normalizaciones (fechas -> datetime)
        dto = ReservationDTO.from_entity(reservation)
        # Obtener dict del DTO
        dto_dict = dto.dict()
        # Normalizar fechas recursivamente a ISO strings
        normalized = _normalize_dates(dto_dict)
        # Loggable debug: tipos de campos clave
        logger.debug("Reservation fields types: reservationDate=%s createdAt=%s pastoralLetterUploadedAt=%s",
                     type(dto_dict.get('reservationDate')),
                     type(dto_dict.get('createdAt')),
                     type(dto_dict.get('pastoralLetterUploadedAt')))
        return normalized
    except Exception as e:
        logger.exception("Error creando reserva completa")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create", response_model=ReservationDTO, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_data: CreateReservationODM,
    session: SessionContainer = Depends(verify_session())
):
    reservation_repository = ReservationRepositoryImpl()
    use_case = CreateReservationUseCase(reservation_repository)
    data_dict = reservation_data.dict()
    data_dict["userId"] = user["id"]
    try:
        reservation = use_case.execute(data_dict)
        return reservation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get", response_model=ReservationQueryDTO)
async def list_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    #session: SessionContainer = Depends(verify_session()),
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
    return ReservationQueryDTO(reservations=results, total=total)


@router.patch("/update/{reservation_id}", response_model=ReservationDTO)
async def update(
    reservation_id: str,
    updates: UpdateReservationODM,
    #session: SessionContainer = Depends(verify_session()),
):
    repo = ReservationRepositoryImpl()
    use_case = UpdateReservationUseCase(repo)
    try:
        updated = await use_case.execute(reservation_id, updates.dict())
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
