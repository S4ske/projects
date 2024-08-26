from ..core.db import engine
from sqlmodel import Session
from typing import Generator


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
