from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from backend.app.core.config import JWT_ALGORITHM, JWT_SECRET_KEY, SERIALIZER_KEY
from datetime import timedelta, datetime, timezone
from typing import Any
import jwt
from passlib.context import CryptContext

serializer = URLSafeTimedSerializer(SERIALIZER_KEY)
crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode = {'exp': expire, 'sub': subject}
    encoded_jwt = jwt.encode(to_encode, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return crypt_context.hash(password)


def create_email_confirmation_token(email: str) -> str:
    return serializer.dumps(email, salt="email-confirm")


def decode_confirmation_token(confirm_token: str) -> str | None:
    try:
        return serializer.loads(confirm_token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return None
