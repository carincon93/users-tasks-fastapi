from sqlmodel.main import Relationship
from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID, uuid4

from ..users.model import UsersRoles
from ..users.model import User

class RoleBase(SQLModel):
    name: str = Field(nullable=False)


class Role(RoleBase, table=True):
    # pyrefly: ignore [bad-override]
    __tablename__ = "roles"
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True
    )
    users: list[User] = Relationship(back_populates="roles", link_model=UsersRoles)


class RoleCreate(RoleBase):
    pass


class RolePublic(RoleBase):
    id: UUID
    name: str


class RoleUpdate(RoleBase):
    # pyrefly: ignore [bad-override]
    name: Optional[str] = None

