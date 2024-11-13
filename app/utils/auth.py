from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv
import jwt
import os


# Load environment variables.
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET") or "topsecret" 
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_user_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expires_in: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_in:
        expire = datetime.now(timezone.utc) + expires_in
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
