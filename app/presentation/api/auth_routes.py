from fastapi import APIRouter, Depends, Request, HTTPException
from app.presentation.decorators.auth import get_current_session
from pydantic import BaseModel
from app.presentation.dependencies import get_user_use_cases
from app.application.use_cases.user_use_cases import UserUseCases
from app.presentation.auth.jwt_utils import create_access_token
from app.shared.exceptions.user_exceptions import InvalidCredentialsError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/sessioninfo")
async def get_session_info(session = Depends(get_current_session)):
    return {
        "session": session
    }


class LoginPayload(BaseModel):
    email: str
    password: str


@router.post('/login')
async def login(payload: LoginPayload, user_use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        user = await user_use_cases.authenticate_user(payload.email, payload.password)
        token = create_access_token({"sub": user.id, "email": user.email})
        return {"access_token": token, "token_type": "bearer"}
    except InvalidCredentialsError:
        # Return 200 with an error message per request
        return {"detail": "Invalid credentials"}
    except Exception as e:
        # Unexpected error -> raise as 500
        raise HTTPException(status_code=500, detail=str(e))
