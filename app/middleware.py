from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from jwt.exceptions import InvalidTokenError

from .core.db import get_session
from .users.model import User
from .auth.service import AuthService

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            async for session in get_session():
                await self.get_current_user(token, session)
                break

        return await call_next(request)

    async def get_current_user(self, token: str, session: AsyncSession):
        print("======= Token ===========", token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

        # try:
        #     auth_service = AuthService(session)
        #     payload = auth_service.decode_token(token)
        #     db_user = await auth_service.get_current_user(payload)

        #     if not db_user:
        #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

        #     is_valid = auth_service.verify_refresh_token(token)

        #     if not is_valid:
        #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        #     return db_user

        # except InvalidTokenError:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
