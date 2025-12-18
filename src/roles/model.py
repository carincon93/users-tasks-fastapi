from sqlmodel.main import Relationship
from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID, uuid4

from src.users.model import UserRoleLink

class RoleBase(SQLModel):
    name: str = Field(nullable=False)


class Role(RoleBase, table=True):
    __tablename__ = "roles"
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True
    )
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)


class RoleCreate(RoleBase):
    pass


class RolePublic(RoleBase):
    id: UUID
    name: str


class RoleUpdate(RoleBase):
    name: Optional[str] = None

