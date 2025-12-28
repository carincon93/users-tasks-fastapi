from sqlalchemy.orm.strategy_options import selectinload
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from typing import List, Any
from sqlmodel import select
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
import jwt

from ..core.config import JWT_ACCESS_TOKEN_SECRET, ALGORITHM, JWT_REFRESH_TOKEN_SECRET
from ..users.model import User
from ..core.db import get_session

password_hash = PasswordHash.recommended()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True, secret: str = "myDefaultSecret"):
        super().__init__(auto_error=auto_error)
        self.secret = secret


    async def __call__(self, request: Request) -> dict:
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        token = credentials.credentials
        payload = self.decode(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return payload

    
    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret, algorithms=ALGORITHM)
        except InvalidTokenError as err:
            print("Invalid token", err)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )


class AccessTokenBearer(TokenBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error, secret=JWT_ACCESS_TOKEN_SECRET)


class RefreshTokenBearer(TokenBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error, secret=JWT_REFRESH_TOKEN_SECRET)


class LocalAuth(HTTPBasic):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        session: AsyncSession = Depends(get_session),
    ) -> User:
        
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        user = await self.authenticate(credentials, session)
        return user

    async def authenticate(
        self,
        credentials: HTTPBasicCredentials,
        session: AsyncSession,
    ) -> User:
        result = await session.execute(
            select(User).where(User.email == credentials.username)
        )
        user = result.scalars().first()

        if not user or not password_hash.verify(
            credentials.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return user
        

class GetCurrentUser:
    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    async def __call__(
        self, 
        payload: dict = Depends(AccessTokenBearer()), 
        session: AsyncSession = Depends(get_session)
    ) -> User:
        statement = select(User).where(User.id == payload["sub"]).options(selectinload(getattr(User, "roles")))
        result = await session.execute(statement=statement)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(
        self, 
        current_user: User = Depends(GetCurrentUser())
    ) -> Any:
        user_roles = {role.name for role in current_user.roles}

        if user_roles == {"admin"}:
            return current_user

        if not user_roles.intersection(self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user
