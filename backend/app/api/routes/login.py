from fastapi import APIRouter, Depends, HTTPException, status, Response
from backend.app.api.deps import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from backend.app.schemas import Token
from backend.app.core.security import create_access_token
from datetime import timedelta
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.crud import authenticate

router = APIRouter()


@router.get('/login')
async def login(response: Response, db_session: SessionDep,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    if not (user.is_active and user.is_confirmed):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = create_access_token(user.email, token_expires)
    response.set_cookie(key="token", value=encoded_jwt,
                        httponly=True, secure=True, samesite='lax')
    return Token(access_token=encoded_jwt, token_type='cookie')


@router.get('/logout')
async def logout(response: Response) -> str:
    response.delete_cookie('token')
    return 'ok'
