from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from backend.app.api.main import api_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='fagotzitoz')

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='127.0.0.1')
