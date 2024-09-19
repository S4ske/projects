from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import UserPublic, UserUpdate
from backend.app.core.security import decode_confirmation_token
from backend.app.crud import get_user_by_email, update_user
from backend.app.api.deps import SessionDep

router = APIRouter()


@router.get('/confirm-email/{confirm_token}')
async def confirm_email(db_session: SessionDep, confirm_token: str) -> UserPublic:
    email = decode_confirmation_token(confirm_token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired token')

    user = await get_user_by_email(db_session, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='There is no user with this email')
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')

    await update_user(db_session, user.id, UserUpdate(is_confirmed=True))
    return user
