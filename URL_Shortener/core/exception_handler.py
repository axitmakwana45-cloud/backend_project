from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "status_code": exc.status_code,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation Error",
                "errors": exc.errors(),
                "status_code": 422,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "status_code": 500,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
            },
        )