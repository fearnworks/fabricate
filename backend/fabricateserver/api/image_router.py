""" This module defines the endpoints for the image API. """
import asyncio
from loguru import logger
from fastapi import APIRouter, HTTPException, WebSocket, Path
from websockets.exceptions import ConnectionClosedOK
from starlette.websockets import WebSocketDisconnect
from bson import ObjectId
from fabricateserver.config.manager import config
from fabricateserver.schema import ImageModel, ImageList
from fabricateserver.db.storage import (
    read_images,
    save_metadata,
    delete_image_file,
    add_new_image,
    fetch_image,
)

# Define a new router
router = APIRouter()

@router.get("/images/", response_model=ImageList)
async def get_images():
    """Return a list of all images and their metadata."""
    return ImageList(images=read_images())

@router.post("/upload-image/")
async def upload_image(image: ImageModel):
    """Save metadata for a new image."""
    add_new_image(image)
    return {"message": f"Image {image.filename} uploaded and metadata saved with ID {image.uid}."}

@router.patch("/update-image/{id}")
async def update_image(uid: str, update_data: ImageModel):
    """Update metadata for an existing image."""
    existing_image = fetch_image(uid)
    if not existing_image:
        raise HTTPException(status_code=404, detail="Image not found")
    update_data.id = uid
    save_metadata(update_data)
    return {"message": f"Image metadata updated for ID {uid}"}

@router.delete("/delete-image/{id}")
async def delete_image(uid: str):
    """Delete an image file and its metadata."""
    delete_image_file(uid)
    return {"message": f"Image deleted for ID {uid}"}

@router.websocket("/ws")
async def image_ws(websocket: WebSocket):
    """A WebSocket endpoint that sends updates to the client when new images are added."""
    await websocket.accept()
    try:
        while True:
            # Send the updated list of images to the client
            images = read_images()
            await websocket.send_json(
                {"images": [image.model_dump() for image in images]}
            )
            # Then sleep for some time (e.g., 5 seconds) before sending the next update
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        logger.info("Connection closed normally")
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket.")

static_directory = config.image_directory

