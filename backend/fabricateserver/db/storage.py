# storage_module.py
import os
from typing import List
from pymongo import MongoClient
from fabricateserver.schema import ImageModel
from fabricateserver.config.manager import config
from loguru import logger
import uuid

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

def delete_image_file(uid: str):
    """Delete the specified image metadata from MongoDB and the filesystem."""
    image = fetch_image(uid)
    if image:
        images_collection.delete_one({"uid": uid})
        image_path = os.path.join(config.image_directory, image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)


def add_new_image(image_data: ImageModel):
    """Add a new image to MongoDB"""
    if not image_data.uid:
        image_data.uid = str(uuid.uuid4())  # Generate a unique identifier
    images_collection.insert_one(image_data.model_dump())

def save_metadata(image: ImageModel):
    """Update image metadata in MongoDB using UUID"""
    images_collection.update_one({"uid": image.uid}, {"$set": image.model_dump()}, upsert=True)


def initialize_storage():
    """Scan the image directory and add new images to MongoDB"""
    existing_images = {img['filename'] for img in images_collection.find({}, {"filename": 1})}
    for entry in os.scandir(config.image_directory):
        if entry.is_file() and entry.name not in existing_images:
            uid = str(uuid.uuid4())
            new_image = ImageModel(uid=uid, filename=entry.name, tags=[], notes='', captions='')
            save_metadata(new_image)

def fetch_image(uid:str) -> ImageModel:
    """Fetch metadata for a single image from MongoDB"""
    doc = images_collection.find_one({"uid": uid})
    if doc:
        return ImageModel(**doc)
    raise FileNotFoundError(f"Image with uid {uid} not found")

# Initialize storage when the application starts
initialize_storage()
