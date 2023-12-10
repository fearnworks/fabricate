from fastapi import FastAPI

from fabricateserver.api.image_router import router as image_router

def register_routers(app: FastAPI):
    app.include_router(image_router)