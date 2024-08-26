from fastapi import APIRouter, HTTPException, status
from ..deps import SessionDep
from uuid import UUID
from ...crud import get_user_by_id, create_user, get_user_by_email
from ...models import UserPublic, UserCreate

router = APIRouter()


@router.post('/')
async def create_user(db_session: SessionDep, user_create: UserCreate) -> UserPublic:
    user = await get_user_by_email(db_session, user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The user with this email already exists in the system.'
        )
    user_db = create_user(db_session, user_create)
    user_public = UserPublic.model_validate(user_db)
    return user_public


@router.get('/{id}')
async def get_user(db_session: SessionDep, id: UUID) -> UserPublic:
    user_db = await get_user_by_id(db_session, id)
    user_public = UserPublic.model_validate(user_db)
    return user_public
