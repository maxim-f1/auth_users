import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.api.rest.v1.authentications import auth_rest_v1
from src.config.app import APP_CONFIG
from src.database.redis.connection import REDIS_CONNECTION
from src.utils.router import include_routers


@asynccontextmanager
async def lifespan(app_: FastAPI):
    os.system('alembic upgrade head')

    v1_routers = [
        auth_rest_v1
    ]

    v1_router = include_routers(APIRouter(prefix='/v1'), v1_routers)
    main_router = include_routers(APIRouter(prefix='/api'), (v1_router,))
    app_.include_router(main_router)

    yield
    await REDIS_CONNECTION.connection.aclose()


app = FastAPI(debug=APP_CONFIG.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'localhost:5173'],
    allow_methods=['OPTIONS', 'POST', 'GET', 'DELETE'],
    allow_headers=['*'],
    allow_credentials=True
)
