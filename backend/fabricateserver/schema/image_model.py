# models/image_model.py
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class ImageModel(BaseModel):
    uid: str = Field(default=None, description="Unique identifier for the image")
    filename: str = Field(..., description="The name of the image file")
    tags: Optional[List[str]] = Field(default=[], description="Tags associated with the image")
    notes: Optional[str] = Field(default=None, description="Additional notes or comments")
    captions: Optional[str] = Field(default=None, description="Caption for the image")

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "image1.jpg",
                "tags": ["tag1", "tag2"],
                "notes": "Sample note",
                "captions": "Sample caption"
            }
        }


class ImageList(BaseModel):
    """Image List Model"""

    images: list
