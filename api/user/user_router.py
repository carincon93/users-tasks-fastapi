from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.database import get_session
from api.user.user_model import User, UserCreate
from api.user.user_service import register, login

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/register", response_model=User)
def register_new_user(*, session: Session = Depends(get_session), user: UserCreate):
    new_user = register(session, user)
    return new_user

@router.post("/login")
def login_user(*, session: Session = Depends(get_session), form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = login(session, form_data)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return token