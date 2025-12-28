from sqlmodel import select, col, func
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from uuid import UUID

from ..errors import UserNotFoundError
from .model import User, UserCreate, UserUpdate

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_all(self, limit: int, offset: int):
        data_stmt = (
            select(User)
            .order_by(col(User.id))
            .limit(limit)
            .offset(offset)
        )

        count_stmt = select(func.count()).select_from(User)

        data_result = await self.session.execute(data_stmt)
        count_result = await self.session.execute(count_stmt)

        return {
            "results": data_result.scalars().all(),
            "count": count_result.scalar_one(),
        }


    async def create(self, data: UserCreate):
        password_hashed = password_hash.hash(data.password)
        db_user = User(
            username=data.username,
            email=data.email,
            password_hash=password_hashed,
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user


    async def find_one(self, user_id: UUID):
        statement = select(User).where(User.id == user_id)
        db_user = await self.session.execute(statement=statement)
        return db_user.scalars().first()


    async def update(self, user_id: UUID, data: UserUpdate) -> User:
        db_user = await self.find_one(user_id)

        if not db_user:
            raise UserNotFoundError()

        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = password_hash.hash(update_data.pop("password"))

        db_user.sqlmodel_update(update_data)

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user


    async def delete(self, user_id: UUID):
        db_user = await self.find_one(user_id)

        await self.session.delete(db_user)
        await self.session.commit()
        return {"message": "User deleted", "ok": True}
