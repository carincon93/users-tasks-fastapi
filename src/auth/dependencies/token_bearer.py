from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status
from jwt.exceptions import InvalidTokenError
import jwt

from config import JWT_ACCESS_TOKEN_SECRET, ALGORITHM, JWT_REFRESH_TOKEN_SECRET

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True, secret: str = None):
        super().__init__(auto_error=auto_error)
        self.secret = secret


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        token = credentials.credentials
        payload = self.decode(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        return payload

    
    def decode(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret, algorithms=[ALGORITHM])
        except InvalidTokenError as err:
            print("Invalid token", err)
            return None


class AccessTokenBearer(TokenBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error, secret=JWT_ACCESS_TOKEN_SECRET)


class RefreshTokenBearer(TokenBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error, secret=JWT_REFRESH_TOKEN_SECRET)