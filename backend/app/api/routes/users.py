from fastapi import APIRouter, HTTPException, status
from backend.app.api.deps import SessionDep
from uuid import UUID
from backend.app import crud
from backend.app.schemas import UserPublic, UserCreate
from pydantic import EmailStr

router = APIRouter()


@router.post('/')
async def create_user(db_session: SessionDep, user_create: UserCreate) -> UserPublic:
    user = await crud.get_user_by_email(db_session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )

    user_db = await crud.create_user(db_session, user_create)
    return user_db


@router.get('/{id}')
async def get_user_by_id(db_session: SessionDep, id: UUID) -> UserPublic:
    user_db = await crud.get_user_by_id(db_session, id)
    user_public = UserPublic.model_validate(user_db)
    return user_public


@router.get('/{email}')
async def get_user_by_email(db_session: SessionDep, email: EmailStr) -> UserPublic:
    user_db = await crud.get_user_by_email(db_session, email)
    user_public = UserPublic.model_validate(user_db)
    return user_public


@router.get('/{username}')
async def get_user_by_username(db_session: SessionDep, username: str) -> UserPublic:
    user_db = await crud.get_user_by_username(db_session, username)
    user_public = UserPublic.model_validate(user_db)
    return user_public
