from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app import models, crud
from app.schemas import UserCreate, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.config import settings
from app.database import get_session
from app.core.redis_client import get_redis
router = APIRouter(prefix="/auth", tags=["auth"])


# -------------------------------
# SIGNUP
# -------------------------------
@router.post("/signup", response_model=Token)
def signup(data: UserCreate, session: Session = Depends(get_session)):
    # تحقق من وجود المستخدم
    if crud.get_user_by_email(session, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # أول مستخدم يصبح admin
    users_count = session.exec(select(models.User)).all()
    role = "admin" if len(users_count) == 0 else "user"

    # إنشاء المستخدم
    user = models.User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # إنشاء توكن JWT
    access_token = create_access_token(
        subject=user.email,
        role=user.role,
        SECRET_KEY=settings.SECRET_KEY,
        ALGORITHM=settings.ALGORITHM,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    r = get_redis()
    r.setex(f"user_session:{user.id}", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, "active")
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------------
# LOGIN
# -------------------------------
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = crud.get_user_by_email(session, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # إنشاء توكن JWT مع الدور
    access_token = create_access_token(
        subject=user.email,
        role=user.role,
        SECRET_KEY=settings.SECRET_KEY,
        ALGORITHM=settings.ALGORITHM,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    r = get_redis()
    r.setex(f"user_session:{user.id}", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, "active")
    
    
    
    return {"access_token": access_token, "token_type": "bearer"}
