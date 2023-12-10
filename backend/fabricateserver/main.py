""" This is the main file for the backend API. 
It is responsible for creating the FastAPI application, 
including the routers, middleware, and event handlers. """

from loguru import logger
from fastapi import FastAPI
import fabricateserver.lifecycle as lifecycle

from fabricateserver.config.manager import load_config
from fabricateserver.config.middleware import setup_middle_ware
import fabricateserver.api.routers as Routers


config = load_config()


app = FastAPI(title="Fabricate API")
setup_middle_ware(app)
logger.info("Middleware has been setup")
# Include the router from image_router.py
Routers.register_routers(app)
logger.info("Routers have been included in the application")
app.add_event_handler("startup", lifecycle.startup)
app.add_event_handler("shutdown", lifecycle.shutdown)
