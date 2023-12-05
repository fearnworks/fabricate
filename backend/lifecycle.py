# lifecycle.py

from loguru import logger
from model_manager import start_model_loading, await_model_loading


async def startup():
    logger.info("Application startup: Model loading in background...")
    start_model_loading()

async def shutdown():
    logger.info("Application shutdown: Cleaning up resources.")
    # Add logic if any specific cleanup is needed
