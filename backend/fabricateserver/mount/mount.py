from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fabricateserver.config import Config

def mount_folder(app: FastAPI, config: Config):
    # Mount the static directory specified in the config file
    app.mount("/static", StaticFiles(directory=config.image_directory), name="static")
