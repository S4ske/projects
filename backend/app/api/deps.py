from ..core.db import engine
from sqlmodel import Session
from typing import Generator, Annotated
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
