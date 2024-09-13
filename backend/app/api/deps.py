from ..core.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator, Annotated
from fastapi import Depends, Cookie, HTTPException, status
import jwt
from backend.app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from pydantic import ValidationError
from backend.app.schemas import TokenPayload
from backend.app.crud import get_user_by_email
from backend.app.models import User


async def get_db() -> Generator[AsyncSession, None, None]:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Cookie(None)]


async def get_current_user(db_session: AsyncSession, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    user = await get_user_by_email(db_session, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

UserDep = Annotated[User, Depends(get_current_user)]


async def get_current_superuser(db_session: AsyncSession, token: TokenDep) -> User:
    user = await get_current_user(db_session, token)
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return user

SuperuserDep = Annotated[User, Depends(get_current_superuser)]
