from ..core.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator, Annotated
from fastapi import Depends


async def get_db() -> Generator[AsyncSession, None, None]:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
