from backend.app.core.config import JWT_ALGORITHM, JWT_SECRET_KEY
from datetime import timedelta, datetime, timezone
from typing import Any
import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import User
from backend.app.crud import get_user_by_email

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode = {'exp': expire, 'sub': subject}
    encoded_jwt = jwt.encode(to_encode, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)


async def authenticate(db_session: AsyncSession, username: str, password: str) -> User | None:
    user = await get_user_by_email(db_session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
