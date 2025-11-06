from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jwt.exceptions import InvalidTokenError
import jwt

from api.database import engine
from api.user.user_model import User, UserPublic, Token, TokenData
from environment import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def hash_password(password: str):
    password_hashed = password_hash.hash(password)
    return password_hashed

def get_user(user_name: str):
    statement = select(User).where(User.user_name == user_name)
    with Session(engine) as session:
        db_user = session.exec(statement=statement).first()

    if db_user:
        return UserPublic.model_validate(db_user)
    
    return None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user_name = token_data.username
    if user_name is None:
        raise credentials_exception
    
    user = get_user(user_name)
    return user

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):    
    return current_user

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token(username: str):
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
