from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api import deps
from app.core import security
from app.db.session import get_db
from app.models.models import User

router = APIRouter()

@router.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    statement = select(User).where(User.email == form_data.username)
    user = db.exec(statement).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }

@router.post("/signup", response_model=User)
def signup(
    *,
    db: Session = Depends(get_db),
    email: str,
    password: str,
    full_name: str = None,
    school: str = None,
    department: str = None,
    level: str = None,
) -> Any:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = User(
        email=email,
        hashed_password=security.get_password_hash(password),
        full_name=full_name,
        school=school,
        department=department,
        level=level,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user
