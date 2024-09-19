from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import jwt
from backend.app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()


@router.get('/')
async def homepage(request: Request):
    token = request.cookies.get('token')
    if token:
        payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        html = (
            f'<pre>{payload}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')