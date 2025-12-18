from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from typing import Optional

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    refresh_token_hash: Optional[str] = Field(default=None, nullable=True)


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

