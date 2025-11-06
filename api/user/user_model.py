from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Union

class UserBase(SQLModel):
    user_name: str = Field(index=True, unique=True, nullable=False, max_length=50)
    password: str = Field(nullable=False)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: str | None = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserPublic(SQLModel):
    id: str
    user_name: str

class UserLogin(BaseModel):
    user_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None