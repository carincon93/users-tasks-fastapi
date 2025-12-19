from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.roles.model import RolePublic, RoleCreate, RoleUpdate
from src.roles.service import RoleService

role_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin"])


@role_router.get(
    "/",
    response_model=list[RolePublic],
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def find_all(
    session: AsyncSession = Depends(get_session),
):
    return await RoleService(session).find_all()


@role_router.post(
    "/",
    response_model=RolePublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def create(
    role: RoleCreate,
    session: AsyncSession = Depends(get_session),
):
    return await RoleService(session).create(role)


@role_router.get(
    "/{role_id}",
    response_model=RolePublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def find_one(
    role_id: str,
    session: AsyncSession = Depends(get_session),
):
    return await RoleService(session).find_one(role_id)


@role_router.put(
    "/{role_id}",
    response_model=RolePublic,
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def update(
    role_id: str,
    role: RoleUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await RoleService(session).update(role_id, role)


@role_router.delete(
    "/{role_id}",
    dependencies=[
        Depends(access_token_bearer),
        Depends(role_checker)
    ]
)
async def delete(
    role_id: str,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer),
):
    return await RoleService(session).delete(role_id)