from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

from ..core.config import ALGORITHM

password_hash = PasswordHash.recommended()

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_token(data: dict, key: str, expires_delta: int = 900):
    expire_in = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    
    payload = {
        "sub": str(data.get("sub")),
        "email": data.get("email"),
        "iat": datetime.now(timezone.utc),
        "exp": expire_in,
    }
    encoded_jwt = jwt.encode(payload=payload, key=key, algorithm=ALGORITHM)
    return encoded_jwt
