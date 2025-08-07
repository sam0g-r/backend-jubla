from app.shared.utils.auth_utils import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.use_cases.user_use_cases import UserUseCases
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.presentation.dependencies import get_user_use_cases
from app.shared.exceptions.user_exceptions import UserAlreadyExistsError
from fastapi.security import OAuth2PasswordRequestForm
from app.shared.exceptions.user_exceptions import InvalidCredentialsError


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserDTO,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user = await user_use_cases.create_user(user_data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


# Endpoint de login
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        user = await user_use_cases.authenticate_user(form_data.username, form_data.password)
        access_token = create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            }
        }
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
