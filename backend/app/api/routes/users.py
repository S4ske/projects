from fastapi import APIRouter, HTTPException, status
from backend.app.api.deps import SessionDep
from uuid import UUID
from backend.app import crud
from backend.app.schemas import UserPublic, UserCreate
from pydantic import EmailStr
from backend.app.api.deps import UserDep
from backend.app.api.email import send_new_account_email
from backend.app.core.security import create_email_confirmation_token

router = APIRouter()


@router.get('/me')
async def get_me(user: UserDep) -> UserPublic:
    return user


@router.post('/')
async def create_user(db_session: SessionDep, user_create: UserCreate):
    user = await crud.get_user_by_email(db_session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )

    confirm_token = create_email_confirmation_token(user_create.email)
    await crud.create_user(db_session, user_create)
    await send_new_account_email(user_create.email, confirm_token)
    return {'message': 'Check your email'}


@router.get('/{id}')
async def get_user_by_id(db_session: SessionDep, id: UUID) -> UserPublic:
    user_db = await crud.get_user_by_id(db_session, id)
    return user_db


@router.get('/{email}')
async def get_user_by_email(db_session: SessionDep, email: EmailStr) -> UserPublic:
    user_db = await crud.get_user_by_email(db_session, email)
    return user_db


@router.get('/{username}')
async def get_user_by_username(db_session: SessionDep, username: str) -> UserPublic:
    user_db = await crud.get_user_by_username(db_session, username)
    return user_db


@router.post('/delete/{username}')
async def delete_user_by_email(db_session: SessionDep, email: str) -> UserPublic:
    user_db = await crud.get_user_by_email(db_session, email)
    await crud.delete_user(db_session, user_db.id)
    return user_db
