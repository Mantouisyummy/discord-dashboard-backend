from typing import Dict

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


def get_token(req: Request) -> dict[str, str]:
    auth_header = req.headers.get('Authorization')
    if auth_header is None or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="You must login first")
    token = auth_header[len('Bearer '):].strip()
    return token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            request.session['access_token'] = get_token(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        response = await call_next(request)
        return response
