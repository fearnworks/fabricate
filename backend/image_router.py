import asyncio
from fastapi import APIRouter, HTTPException, WebSocket
from websockets.exceptions import ConnectionClosedOK
from starlette.websockets import WebSocketDisconnect
from typing import List
from models.image_model import ImageModel, ImageList
from storage import read_images, save_metadata, delete_image_file, add_new_image
from loguru import logger 
# Define a new router
router = APIRouter()

@router.get("/images/", response_model=ImageList)
async def get_images():
    # Return a list of all images and their metadata
    return ImageList(images=read_images())

@router.post("/upload-image/")
async def upload_image(image: ImageModel):
    # Save metadata for a new image
    add_new_image(image.filename)
    return {"message": f"Image {image.filename} uploaded and metadata saved."}

@router.patch("/update-image/{filename}")
async def update_image(filename: str, update_data: ImageModel):
    # Update metadata for an existing image
    # This can include renaming the file, changing tags, etc.
    logger.info(update_data)
    save_metadata(update_data)
    return {"message": f"Image {filename} metadata updated."}

@router.delete("/delete-image/{filename}")
async def delete_image(filename: str):
    # Delete an image file and its metadata
    delete_image_file(filename)
    return {"message": f"Image {filename} deleted."}

@router.websocket("/ws")
async def image_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send the updated list of images to the client
            images = read_images()
            await websocket.send_json({"images": [image.model_dump() for image in images]})
            # Then sleep for some time (e.g., 5 seconds) before sending the next update
            await asyncio.sleep(5)
    except ConnectionClosedOK:
        logger.info("Connection closed normally")
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket.")

