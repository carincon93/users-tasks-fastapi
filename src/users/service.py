from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from fastapi import HTTPException, status

from src.users.model import User, UserCreate, UserUpdate

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def find_all(self):
    #     statement = select(User).where(User.user_id == self.current_user.id)
    #     db_users = await self.session.exec(statement=statement)

    #     return db_users.all()

    # async def create(self, user: UserCreate):
    #     db_user = User(
    #         id=str(uuid4()),
    #         title=user.title,
    #         description=user.description,
    #         user_id=self.current_user.id,
    #         completed=user.completed
    #     )

    #     await self.session.add(db_user)
    #     await self.session.commit()
    #     await self.session.refresh(db_user)

    #     return db_user

    # async def find_one(self, user_id: str):
    #     statement = select(User).where(User.user_id == self.current_user.id).where(User.id == user_id)
    #     db_user = await self.session.exec(statement=statement)
    #     return db_user.first()

    # async def update(self, user_id: str, user: UserUpdate):
    #     db_user = self.find_one(user_id)

    #     if not db_user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #     db_user.sqlmodel_update(user.model_dump(exclude_unset=True))

    #     await self.session.add(db_user)
    #     await self.session.commit()
    #     await self.session.refresh(db_user)

    #     return db_user

    # async def delete(self, user_id: str):
    #     db_user = self.find_one(user_id)

    #     if not db_user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #     await self.session.delete(db_user)
    #     await self.session.commit()

    #     return {"message": "User deleted", "ok": True}

    # async def completed(self, completed: bool):
    #     statement = select(User).where(User.user_id == self.current_user.id).where(User.completed == completed)
    #     db_users = await self.session.exec(statement=statement)

    #     return db_users.all()

    