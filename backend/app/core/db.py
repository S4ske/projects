from backend.app.core.config import POSTGRES_URL_ASYNC
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(POSTGRES_URL_ASYNC)
