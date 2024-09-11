from fastapi import FastAPI
import uvicorn
from backend.app.api.main import api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
