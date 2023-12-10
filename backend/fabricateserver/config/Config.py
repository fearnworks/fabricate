from dataclasses import dataclass

@dataclass
class Config:
    image_directory: str 
    metadata_directory: str
    model_directory: str