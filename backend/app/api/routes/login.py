from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from backend.app.api.deps import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from backend.app.schemas import Token
from backend.app.core.security import create_access_token
from datetime import timedelta
from backend.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.crud import authenticate
from backend.app.api.oauth import oauth

router = APIRouter()


@router.post('/login')
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


@router.get('/login_with_google')
async def login_with_google(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route('/auth', methods=['GET', 'POST'])
async def auth(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)
    user = token['userinfo']
    access_token = token['access_token']
    response.set_cookie(key='token', value=access_token)
    token = await oauth.google.authorize_access_token(access_token)
    return user


@router.get('/logout')
async def logout(response: Response) -> str:
    response.delete_cookie('token')
    return 'ok'
