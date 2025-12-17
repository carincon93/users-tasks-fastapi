from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.users.model import User
from src.auth.model import Login
from src.auth.utils import verify_password
from src.db.main import get_session

async def validate(
    login: Login,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(User).where(User.email == login.email)
    )
    user = result.scalars().first()

    if not user or not verify_password(login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return user