# storage_module.py
import os
from typing import List
from pymongo import MongoClient
from fabricateserver.schema import ImageModel
from fabricateserver.config.manager import config
from loguru import logger

# MongoDB setup
client = MongoClient("mongodb://db:27017")  # Update with your MongoDB URI
db = client["fabricate_database"]  # Your database name
images_collection = db["images"]  # Your collection name

def read_images() -> List[ImageModel]:
    """Read all metadata from MongoDB"""
    images = []
    for doc in images_collection.find({}):
        images.append(ImageModel(**doc))
    return images

def save_metadata(image: ImageModel):
    """Insert or update image metadata in MongoDB"""
    images_collection.update_one({"filename": image.filename}, {"$set": image.model_dump()}, upsert=True)

def delete_image_file(filename: str):
    """Delete the specified image metadata from MongoDB and the filesystem"""
    images_collection.delete_one({"filename": filename})
    image_path = os.path.join(config.image_directory, filename)
    if os.path.exists(image_path):
        os.remove(image_path)

def add_new_image(filename: str):
    """Add a new image to MongoDB"""
    new_image = ImageModel(filename=filename)
    save_metadata(new_image)

def initialize_storage():
    """Scan the image directory and add new images to MongoDB"""
    existing_images = {img['filename'] for img in images_collection.find({}, {"filename": 1})}
    for entry in os.scandir(config.image_directory):
        if entry.is_file() and entry.name not in existing_images:
            new_image = ImageModel(filename=entry.name, tags=[], notes='', captions='')
            save_metadata(new_image)

def fetch_image(filename: str) -> ImageModel:
    """Fetch metadata for a single image from MongoDB"""
    doc = images_collection.find_one({"filename": filename})
    if doc:
        return ImageModel(**doc)
    raise FileNotFoundError(f"Image with filename {filename} not found")

# Initialize storage when the application starts
initialize_storage()
