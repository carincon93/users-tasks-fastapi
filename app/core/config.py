from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

API_URL=os.getenv("API_URL")
API_PORT=os.getenv("API_PORT")

POSTGRES_DB_CONNECTION : URL | str = os.getenv("POSTGRES_DB_CONNECTION", "")

ALGORITHM=os.getenv("ALGORITHM")
JWT_ACCESS_TOKEN_SECRET=os.getenv("JWT_ACCESS_TOKEN_SECRET", "myDefaultSecret")
JWT_ACCESS_TOKEN_EXPIRES_IN=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_IN", 900))
JWT_REFRESH_TOKEN_SECRET=os.getenv("JWT_REFRESH_TOKEN_SECRET", "myDefaultSecret")
JWT_REFRESH_TOKEN_EXPIRES_IN=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_IN", 3600))

version_prefix="/api/v1"
