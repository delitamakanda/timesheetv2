from typing import List
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from core.config import config
from api import router

def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)

def make_middleware() -> List[Middleware]:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=config.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        ),
    ]

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Timesheet API",
        description="A simple API for managing timesheets",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=make_middleware()
    )
    init_routers(app_=app_)

    return app_


app = create_app()