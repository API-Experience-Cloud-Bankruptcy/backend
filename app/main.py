from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.router import api_router


from app.middleware.exception import (
    exception_middleware,
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI",
        description="FastAPI",
        version="1.0.0",
        docs_url="/docs",
    )

    app_.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app_.add_exception_handler(RequestValidationError, validation_exception_handler)

    app_.middleware("http")(exception_middleware)

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_.include_router(api_router, prefix="/api")
    return app_


app = create_app()
