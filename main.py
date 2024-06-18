import  uvicorn

from uvicorn import Config, Server

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from middleware.auth import AuthMiddleware

from routers import guilds

from sql.database import create_db

app = FastAPI()

config = Config(app=app, host="localhost", port=8000)
server = Server(config)

app.add_middleware(AuthMiddleware)

app.add_middleware(SessionMiddleware, secret_key="aaaaa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以更改為你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(guilds.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
