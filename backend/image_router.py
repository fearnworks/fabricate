# backend/image_router.py

from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket
from starlette.websockets import WebSocketDisconnect
from pydantic import BaseModel
import yaml
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio

# Define a new router
router = APIRouter()

# Load configuration for image directory
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class ImageList(BaseModel):
    images: list

class ImageDirectoryWatcher(FileSystemEventHandler):
    def __init__(self):
        self._image_event = asyncio.Event()

    def on_any_event(self, event):
        # Trigger the event for any file system change
        self._image_event.set()

    async def watch_directory(self, websocket: WebSocket):
        while True:
            await self._image_event.wait()
            await websocket.send_json(read_images().dict())
            self._image_event.clear()

# Initialize and start the observer
watcher = ImageDirectoryWatcher()
observer = Observer()
observer.schedule(watcher, config['image_directory'], recursive=True)
observer.start()

@router.get("/images/", response_model=ImageList)
def read_images():
    image_directory = config['image_directory']
    with os.scandir(image_directory) as entries:
        images = [entry.name for entry in entries if entry.is_file()]
    return ImageList(images=images)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Logic to save the uploaded file
    return {"filename": file.filename}

@router.put("/update-image/{image_name}")
async def update_image(image_name: str):
    # Logic to update the image
    return {"message": "Image updated"}

@router.delete("/delete-image/{filename}")
async def delete_image(filename: str):
    image_directory = config['image_directory']
    image_path = os.path.join(image_directory, filename)
    try:
        os.remove(image_path)
        return {"message": "Image deleted successfully."}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.websocket("/ws")
async def image_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send initial image list upon connection
            images = read_images().images
            await websocket.send_json({"images": images})
            # Then sleep for some time (e.g., 5 seconds) before sending the next update
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket.")