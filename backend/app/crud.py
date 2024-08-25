from sqlmodel import Session
from models import UserCreate, User, UserUpdate
from sqlmodel import select
from core.security import get_password_hash
from uuid import UUID


def create_user(db_session: Session, user_create: UserCreate) -> User:
    user_db = User.model_validate(user_create, update={'hashed_password': get_password_hash(user_create.password)})
    db_session.add(user_db)
    db_session.commit()
    db_session.refresh(user_db)
    return user_db


def get_user_by_id(db_session: Session, id: UUID) -> User:
    return db_session.exec(select(User).where(User.id == id)).first()


def get_user_by_email(db_session: Session, email: str) -> User:
    return db_session.exec(select(User).where(User.email == email)).first()


def update_user(db_session: Session, id: UUID, user_update: UserUpdate) -> User:
    user_data = user_update.model_dump(exclude_unset=True)
    user_db = get_user_by_id(db_session, id)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    user_db.sqlmodel_update(user_data, update=extra_data)
    db_session.add(user_db)
    db_session.commit()
    db_session.refresh(user_db)
    return user_db


def delete_user(db_session: Session, id: UUID) -> User | None:
    user = db_session.exec(select(User).where(User.id == id)).first()
    if not user:
        return None
    db_session.delete(user)
    db_session.commit()
    db_session.refresh(user)
    return user
