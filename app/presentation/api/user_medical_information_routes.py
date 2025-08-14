from app.domain.entities import user
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.domain.entities.user_medical_information import UserMedicalInformation
from app.application.odm.user_medical_information_odm import UserMedicalInformationODM
from app.infrastructure.repositories.user_medical_information_repository_impl import UserMedicalInformationRepositoryImpl
from app.application.use_cases.user_medical_information_use_cases import CreateUserMedicalInformationUseCase, QueryUserMedicalInformationUseCase
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

router = APIRouter(prefix="/medical-information", tags=["medical-information"])

@router.post("/create", response_model=UserMedicalInformation, status_code=status.HTTP_201_CREATED)
async def create_user_medical_information(
    data: UserMedicalInformationODM,
    session: SessionContainer = Depends(verify_session())
):
    repo = UserMedicalInformationRepositoryImpl()
    use_case = CreateUserMedicalInformationUseCase(repo)
    data_dict = data.dict()
    data_dict["userId"] = user["id"]
    try:
        info = await use_case.execute(data_dict)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get", response_model=List[UserMedicalInformation])
async def list_user_medical_information(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    userId: Optional[str] = None,
    session: SessionContainer = Depends(verify_session())
):
    filters = {}
    if userId:
        filters["userId"] = userId
    repo = UserMedicalInformationRepositoryImpl()
    use_case = QueryUserMedicalInformationUseCase(repo)
    results, total = await use_case.execute(filters, skip, limit)
    return results
