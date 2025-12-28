from sqlmodel.main import Relationship
from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from typing import Optional

from ..roles.model import Role

class UsersRoles(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="users.id",
        primary_key=True,
    )
    role_id: UUID = Field(
        foreign_key="roles.id",
        primary_key=True,
    )


class UserBase(SQLModel):
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)


class User(UserBase, table=True):
    # pyrefly: ignore [bad-override]
    __tablename__ = "users"
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    refresh_token_hash: Optional[bytes | str] = Field(default=None, nullable=True)
    roles: list[Role] = Relationship(back_populates="users", link_model=UsersRoles)


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserPublic(SQLModel):
    id: UUID
    username: str
    email: str
    

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class PaginatedUsers(SQLModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[UserPublic]

