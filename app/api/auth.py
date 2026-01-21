from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.settings import settings

_bearer_scheme = HTTPBearer(auto_error=False)


def verify_auth_token(credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme)) -> None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    token = (credentials.credentials or "").strip()
    if not token or token != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
