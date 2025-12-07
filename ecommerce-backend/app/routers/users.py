from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.routers.deps import current_user
from app.schemas import UserRead, UserUpdate
from app import crud, models

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def get_me(user: models.User = Depends(current_user)):
    return user

@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return crud.list_users(session)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, session: Session = Depends(get_session)):
    user = crud.update_user(session, user_id, name=data.name)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_user(session, user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"message": "User deleted successfully"}
