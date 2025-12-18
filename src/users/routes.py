from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from src.users.model import UserPublic, UserCreate, UserUpdate
from src.users.service import UserService
from src.auth.dependencies.token_bearer import AccessTokenBearer

user_router = APIRouter()
access_token_bearer = AccessTokenBearer()

@user_router.get("/", response_model=list[UserPublic], dependencies=[Depends(access_token_bearer)])
async def find_all(
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).find_all()


@user_router.post("/", response_model=UserPublic, dependencies=[Depends(access_token_bearer)])
async def create(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).create(user)


@user_router.get("/{user_id}", response_model=UserPublic, dependencies=[Depends(access_token_bearer)])
async def find_one(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).find_one(user_id)
    

@user_router.put("/{user_id}", response_model=UserPublic, dependencies=[Depends(access_token_bearer)])
async def update(
    user_id: str, 
    user: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).update(user_id, user)


@user_router.delete("/{user_id}", dependencies=[Depends(access_token_bearer)])
async def delete(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).delete(user_id)
