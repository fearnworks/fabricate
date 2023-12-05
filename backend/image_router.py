import asyncio
from fastapi import APIRouter, HTTPException, WebSocket
from websockets.exceptions import ConnectionClosedOK
from starlette.websockets import WebSocketDisconnect
from typing import List
from models.image_model import ImageModel, ImageList
from storage import read_images, save_metadata, delete_image_file, add_new_image, fetch_image
from loguru import logger 
from model_manager import is_model_loaded
from caption import generate_image_caption
from config import config
import os 
from PIL import Image
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

static_directory = config["image_directory"]

@router.post("/caption-image/{filename}")
async def caption_image(filename: str):
    """
    Endpoint to generate a caption for a given image.

    Args:
        filename: The name of the image file to be captioned.

    Returns:
        A JSON response containing the image caption.
    """
    if not is_model_loaded():
        raise HTTPException(status_code=503, detail="Model is still loading")

    try:
        # Fetch the image metadata
        image_metadata = fetch_image(filename)
        
        # Construct the path to the image file using the static directory
        image_path = os.path.join(static_directory, image_metadata.filename)

        if not os.path.isfile(image_path):
            raise HTTPException(status_code=404, detail="Image file not found in static directory")

        # Open and process the image for captioning
        with open(image_path, 'rb') as image_file:
            image = Image.open(image_file).convert('RGB')
            caption = await generate_image_caption(image)
        
        # Return the caption
        return {"caption": caption}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image metadata not found")
    except Exception as e:
        logger.error(f"Error in captioning image {filename}: {e}")
        raise HTTPException(status_code=500, detail="Error generating caption")