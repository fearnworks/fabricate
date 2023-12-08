# backend/main.py

import time
import yaml
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
import lifecycle as lifecycle

import argparse 
from config import load_config
from image_router import router as image_router

# Create a console instance
console = Console()

logger.remove()
logger.add(RichHandler())

def parse_arguments():
    parser = argparse.ArgumentParser(description="Fabricate AI Driver Synthetic Data Management")
    parser.add_argument("--config", type=str, default="./configs/local/config.yaml", help="Path to the configuration file")
    
    return parser.parse_args()# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
app = FastAPI(title="AI Driver API")

origins = ["*"]


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
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
args = parse_arguments()

# Mount the static directory specified in the config file
app.mount("/static", StaticFiles(directory=config["image_directory"]), name="static")

# Include the router from image_router.py
app.include_router(image_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.middleware("http")
async def log_request(request: Request, call_next):
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
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server")
    uvicorn.run(app, host="0.0.0.0", port=8000)