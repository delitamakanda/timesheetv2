from typing import List
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from core.config import config
from api import router
from core.cache import Cache, CustomKeyMaker, RedisBackend
from core.exceptions import CustomException
from core.dependencies import Logging
from core.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLoggerMiddleware,
    SQLAlchemyMiddleware,
)

def on_auth_error(request: Request, exc: CustomException):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message
    return JSONResponse(status_code=status_code, content={"error_code": error_code, "message": message})

def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message}
    )

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
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(
            SQLAlchemyMiddleware,
        ),
        Middleware(
            ResponseLoggerMiddleware,
        )
    ]

def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Timesheet API",
        description="A simple API for managing timesheets",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=make_middleware(),
        dependencies=[Depends(Logging)],
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()

    return app_


app = create_app()