from config import POSTGRES_URL
from sqlmodel import create_engine

engine = create_engine(POSTGRES_URL)
