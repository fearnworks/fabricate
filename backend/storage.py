import os
import json
from typing import List
from models.image_model import ImageModel, ImageList
from config import config
from loguru import logger

# Define the path to the JSONL file where metadata will be stored
metadata_file_path = os.path.join(config['metadata_directory'], 'images.jsonl')

def initialize_metadata_file():
    # Check if the metadata file exists, create it if it doesn't
    if not os.path.exists(metadata_file_path):
        # Create the metadata directory if it doesn't exist
        os.makedirs(os.path.dirname(metadata_file_path), exist_ok=True)
        # Create an empty file
        with open(metadata_file_path, 'w') as file:
            pass

def read_images() -> List[ImageModel]:
    # Ensure metadata file is initialized
    initialize_metadata_file()

    images = []
    with open(metadata_file_path, 'r') as file:
        for line in file:
            image_data = json.loads(line.strip())
            images.append(ImageModel(**image_data))
    return images

def save_metadata(image: ImageModel):
    # Read all metadata from the JSONL file
    with open(metadata_file_path, 'r') as file:
        lines = file.readlines()

    # Parse the JSON data and find the entry to update
    for i, line in enumerate(lines):
        data = json.loads(line)
        if data['filename'] == image.filename:
            # Update the entry
            lines[i] = json.dumps(image.model_dump(), ensure_ascii=False) + '\n'
            break
    else:
        # If no entry was found to update, append a new one
        lines.append(json.dumps(image.model_dump(), ensure_ascii=False) + '\n')

    # Write the updated metadata back to the JSONL file
    with open(metadata_file_path, 'w') as file:
        file.writelines(lines)

def delete_image_file(filename: str):
    # Read all the metadata
    images = read_images()
    # Filter out the image to delete
    images = [image for image in images if image.filename != filename]
    # Rewrite the JSONL file without the deleted image
    with open(metadata_file_path, 'w') as file:
        for image in images:
            file.write(json.dumps(image.dict(), ensure_ascii=False) + '\n')
    # Also, delete the image file itself
    image_path = os.path.join(config['image_directory'], filename)
    if os.path.exists(image_path):
        os.remove(image_path)

def add_new_image(filename: str):
    # Assuming the new file is already saved in the image directory
    # Create a new ImageModel instance with default metadata
    new_image = ImageModel(filename=filename)
    # Save the new image metadata
    save_metadata(new_image)
    
def initialize_storage():
    image_directory = config['image_directory']
    # Load existing images from the storage file
    existing_images = {image.filename: image for image in read_images()}
    logger.info(f"Found {len(existing_images)} existing images in directory.")
    # Scan the image directory for image files
    for entry in os.scandir(image_directory):
        if entry.is_file() and entry.name not in existing_images:
            # Create a new ImageModel instance with default metadata
            new_image = ImageModel(
                filename=entry.name,
                tags=[],
                notes='',
                captions=''
            )
            # Save the new image metadata to the storage file
            save_metadata(new_image)

# Call initialize_storage when your application starts
initialize_storage()
initialize_metadata_file()