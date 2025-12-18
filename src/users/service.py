from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from uuid import UUID

from src.users.model import User, UserCreate, UserUpdate

password_hash = PasswordHash.recommended()

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_all(self):
        statement = select(User)
        db_users = await self.session.execute(statement=statement)
        return db_users.scalars().all()


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
