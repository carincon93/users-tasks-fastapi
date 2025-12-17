from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
# from src.auth.model import User
from src.users.model import UserPublic, UserCreate, UserUpdate
from src.users.service import UserService
# from src.auth.utils import get_current_active_user

user_router = APIRouter()
# get_current_active_user = Depends(get_current_active_user)

# @user_router.get("/", response_model=list[UserPublic])
# async def find_all(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], completed: bool | None = None):
#     if completed is None:
#         users = UserService(session, current_user).find_all()
#     else:
#         users = UserService(session, current_user).completed(completed)

#     return users

# @user_router.post("/", response_model=UserPublic)
# async def create(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], user: UserCreate):
#     new_user = UserService(session, current_user).create(user)
#     return new_user

# @user_router.get("/{user_id}", response_model=UserPublic)
# async def find_one(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], user_id: str):
#     user = UserService(session, current_user).find_one(user_id)

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     return user

# @user_router.put("/{user_id}", response_model=UserPublic)
# async def update(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], user_id: str, user: UserUpdate):
#     user = UserService(session, current_user).update(user_id, user)

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     return user

# @user_router.delete("/{user_id}")
# async def delete(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], user_id: str):
#     status = UserService(session, current_user).delete(user_id)

#     return status
