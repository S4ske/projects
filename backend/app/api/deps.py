from ..core.db import engine
from sqlmodel import Session
from typing import Generator, Annotated
from fastapi import Depends


async def get_db() -> Generator[Session, None, None]:
    async with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
