from fastapi import HTTPException, status, APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.db import get_session
from ..users.model import User, UserPublic
from ..auth.service import AuthService
from ..auth.dependencies import LocalAuth, AccessTokenBearer, RefreshTokenBearer
from ..errors import UserNotFoundError

local_auth = LocalAuth()

auth_router = APIRouter()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()


@auth_router.post("/login")
async def login(
    user: UserPublic = Depends(local_auth),
    session: AsyncSession = Depends(get_session)
):
    auth_service = AuthService(session)
    tokens = await auth_service.login(user)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return tokens


@auth_router.post("/logout")
async def logout(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer)
):
    try:
        auth_service = AuthService(session)
        return await auth_service.logout(payload)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.post("/refresh")
async def refresh(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(refresh_token_bearer)
):
    try:
        auth_service = AuthService(session)
        return await auth_service.refresh(payload)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.get("/me", response_model=UserPublic)
async def get_me(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer)
):
    auth_service = AuthService(session)
    return await auth_service.get_current_user(payload)
