# models/image_model.py
from typing import List, Optional
from pydantic import BaseModel, Field


class ImageModel(BaseModel):
    filename: str = Field(..., description="The name of the image file")
    tags: Optional[List[str]] = Field(default=[], description="Tags associated with the image")
    notes: Optional[str] = Field(default=None, description="Additional notes or comments")
    captions: Optional[str] = Field(default=None, description="Caption for the image")

    class Config:
        schema_extra = {
            "example": {
                "filename": "image1.jpg",
                "tags": ["tag1", "tag2"],
                "notes": "Sample note",
                "captions": "Sample caption"
            }
        }

class ImageList(BaseModel):
    images: list
