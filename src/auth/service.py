from src.users.model import UserPublic
from fastapi import Response, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
import jwt
import json

from src.core.config import ALGORITHM, JWT_ACCESS_TOKEN_SECRET, JWT_ACCESS_TOKEN_EXPIRES_IN, JWT_REFRESH_TOKEN_SECRET, JWT_REFRESH_TOKEN_EXPIRES_IN
from src.auth.dependencies import AccessTokenBearer
from src.auth.utils import create_token
from src.users.model import User, UserPublic
from src.errors import UserNotFoundError

token_hash = PasswordHash.recommended()
access_token_bearer = AccessTokenBearer()

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def login(self, user: User) -> Response:
        access_token = create_token(
            data={"sub": str(user.id), "email": user.email},
            key=JWT_ACCESS_TOKEN_SECRET,
            expires_delta=JWT_ACCESS_TOKEN_EXPIRES_IN,
        )

        refresh_token = create_token(
            data={"sub": str(user.id), "email": user.email},
            key=JWT_REFRESH_TOKEN_SECRET,
            expires_delta=JWT_REFRESH_TOKEN_EXPIRES_IN,
        )

        user.refresh_token_hash = token_hash.hash(refresh_token)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user) 

        response = Response(
            content=json.dumps({"access_token": access_token}),
            status_code=status.HTTP_200_OK,
            media_type="application/json"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,        # ⚠️ True in production
            samesite="strict",
            max_age=JWT_REFRESH_TOKEN_EXPIRES_IN,
        )
        return response
        

    async def logout(self, payload: dict) -> Response:
        user = await self.get_current_user(payload)
        user.refresh_token_hash = None
        self.session.add(user)
        await self.session.commit()

        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("refresh_token")
        return response


    async def refresh(self, payload: dict) -> Response:
        user = await self.get_current_user(payload)
        return await self.login(user)


    async def get_current_user(self, payload: dict) -> UserPublic:
        statement = select(User).where(User.id == payload.get("sub"))
        result = await self.session.execute(statement=statement)
        db_user = result.scalars().first()

        if not db_user:
            raise UserNotFoundError()
        return db_user


    async def validate_user(self, payload: dict):
        pass


    async def verify_refresh_token(self, refresh_token: str):
        try:
            payload = self.decode_token(refresh_token)
            statement = select(User).where(User.id == str(payload.get("sub")))
            db_user = await self.session.execute(statement=statement)
            db_user = db_user.scalars().first()

            if not db_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

            is_valid = token_hash.verify(refresh_token, db_user.refresh_token_hash)

            if not is_valid:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            return db_user

        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


    async def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret, algorithms=[ALGORITHM])
        except InvalidTokenError as err:
            print("Invalid token", err)
            return None
    