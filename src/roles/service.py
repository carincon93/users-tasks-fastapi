from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
# from uuid import uuid4

from src.roles.model import Role, RoleCreate, RoleUpdate

class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_all(self):
        statement = select(Role)
        db_roles = await self.session.execute(statement=statement)
        return db_roles.scalars().all()


    async def create(self, role: RoleCreate):
        db_role = Role(
            name=role.name,
        )

        self.session.add(db_role)
        await self.session.commit()
        await self.session.refresh(db_role)
        return db_role


    async def find_one(self, role_id: str):
        statement = select(Role).where(Role.id == role_id)
        db_role = await self.session.execute(statement=statement)
        return db_role.scalars().first()


    async def update(self, role_id: str, data: RoleUpdate):
        db_role = await self.find_one(role_id)

        if not db_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        db_role.sqlmodel_update(data.model_dump(exclude_unset=True))

        self.session.add(db_role)
        await self.session.commit()
        await self.session.refresh(db_role)
        return db_role


    async def delete(self, role_id: str):
        db_role = await self.find_one(role_id)

        if not db_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        await self.session.delete(db_role)
        await self.session.commit()
        return {"message": "Role deleted", "ok": True}

