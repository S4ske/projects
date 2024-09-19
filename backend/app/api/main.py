from fastapi import APIRouter
from backend.app.api.routes import users, login, email, homepage


api_router = APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(login.router, tags=['authorization'])
api_router.include_router(email.router, tags=['email'])
api_router.include_router(homepage.router, tags=['homepage'])
