import time

from loguru import logger 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

from fabricateserver.config.logging import LogMiddleware

def setup_middle_ware(app: FastAPI):
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        """ Middleware to log all incoming requests. """
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        return response
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ Exception handler for validation errors. """
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )
        
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        Middleware to add a custom X-Process-Time header to all HTTP responses.

        Args:
            request: The incoming HTTP request.
            call_next: A function to call the next middleware or route handler.

        Returns:
            The HTTP response with the added header.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # This allows all methods, including DELETE
        allow_headers=["*"],
    )
    
    app.add_middleware(LogMiddleware)