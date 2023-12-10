""" This is the main file for the backend API. 
It is responsible for creating the FastAPI application, 
including the routers, middleware, and event handlers. """

import time
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from rich.console import Console
from rich.logging import RichHandler
import fabricateserver.lifecycle as lifecycle

from fabricateserver.config import load_config
from fabricateserver.image_router import router as image_router

# Create a console instance
console = Console()

logger.remove()
logger.add(RichHandler())

config = load_config()


app = FastAPI(title="Fabricate API")

origins = ["*"]


class LogMiddleware(BaseHTTPMiddleware):
    """ Middleware to log all incoming requests. """
    async def dispatch(self, request: Request, call_next):
        """ Log all incoming requests. """
        if hasattr(request.state, "body"):
            body_json = request.state.body
        else:
            body_json = None
        logger.info(f"Incoming request: {request.method} {request.url} {body_json}")
        response = await call_next(request)
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, including DELETE
    allow_headers=["*"],
)

# Mount the static directory specified in the config file
app.mount("/static", StaticFiles(directory=config.image_directory), name="static")

# Include the router from image_router.py
app.include_router(image_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ Exception handler for validation errors. """
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.middleware("http")
async def log_request(request: Request, call_next):
    """ Middleware to log all incoming requests. """
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(LogMiddleware)
logger.info("LogMiddleware added to the application")

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

logger.info("Routers have been included in the application")
app.add_event_handler("startup", lifecycle.startup)
app.add_event_handler("shutdown", lifecycle.shutdown)
