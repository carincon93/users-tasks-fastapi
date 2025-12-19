from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session
from src.users.model import UserPublic, UserCreate, UserUpdate, PaginatedUsers
from src.users.service import UserService
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.core.config import version_prefix

user_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin"])

@user_router.get(
    "/",
    response_model=PaginatedUsers,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def find_all(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    data = await UserService(session).find_all(
        limit=limit,
        offset=offset,
    )

    count = data["count"]

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": (
            f"{version_prefix}/users?limit={limit}&offset={next_offset}"
            if next_offset is not None
            else None
        ),
        "previous": (
            f"{version_prefix}/users?limit={limit}&offset={prev_offset}"
            if prev_offset is not None
            else None
        ),
        "results": data["results"],
    }


@user_router.post(
    "/",
    response_model=UserPublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def create(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).create(user)


@user_router.get(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def find_one(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).find_one(user_id)
    

@user_router.put(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def update(
    user_id: str, 
    user: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).update(user_id, user)


@user_router.delete(
    "/{user_id}",
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def delete(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await UserService(session).delete(user_id)
