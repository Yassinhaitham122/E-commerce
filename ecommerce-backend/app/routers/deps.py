# app/routers/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session
from app.config import settings
from app.core.security import decode_token
from app.database import get_session
from app import crud, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user

def admin_required(
    user: models.User = Depends(current_user)
) -> models.User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user
