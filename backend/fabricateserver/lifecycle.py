""" Application lifecycle events. """

from loguru import logger

async def startup(load_model=False):
    """ Application startup event handler. """
    logger.info("Application startup: ")
    if load_model:
        logger.info("Model loading in background...")


async def shutdown():
    """ Application shutdown event handler. """
    logger.info("Application shutdown: Cleaning up resources.")
    # Add logic if any specific cleanup is needed
