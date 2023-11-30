# backend/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import yaml

from image_router import router as image_router



# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, including DELETE
    allow_headers=["*"],
)
# Mount the static directory specified in the config file
app.mount("/static", StaticFiles(directory=config['image_directory']), name="static")

# Include the router from image_router.py
app.include_router(image_router)

# Define any middleware, database connections, event handlers, etc., here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
