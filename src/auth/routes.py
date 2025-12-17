from fastapi import HTTPException, status, APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.users.model import User
from src.auth.service import AuthService
from src.auth.dependencies.local_auth import validate as validate_local
from src.auth.dependencies.dependencies import AccessTokenBearer, RefreshTokenBearer 

auth_router = APIRouter()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

@auth_router.post("/login")
async def login(
    user: User = Depends(validate_local),
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
    auth_service = AuthService(session)
    return await auth_service.logout(payload)


@auth_router.post("/refresh")
async def refresh(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(refresh_token_bearer)
):
    auth_service = AuthService(session)
    return await auth_service.refresh(payload)


@auth_router.get("/me")
async def get_me(
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer)
):
    auth_service = AuthService(session)
    return await auth_service.get_current_user(payload)
