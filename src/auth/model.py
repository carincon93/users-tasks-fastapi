from pydantic import BaseModel
from typing import Union

class LoginBase(BaseModel):
    email: str
    password: str

class Login(LoginBase):
    pass

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: Union[str, None] = None