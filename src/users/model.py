from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    refresh_token_hash: str = Field(nullable=False)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
    )

class UserCreate(UserBase):
    pass

class UserPublic(SQLModel):
    id: UUID
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password_hash: str | None = None

