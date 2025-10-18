from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.shared.config.settings import settings

# Minimal JWT helpers using python-jose
ALGORITHM = getattr(settings, 'ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES', 60*24)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e
