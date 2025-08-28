from fastapi import APIRouter, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/sessioninfo")
async def get_session_info(session: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": session.get_handle(),
        "userId": session.get_userId(),
        "accessTokenPayload": session.get_access_token_payload(),
    }
