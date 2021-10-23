from enum import Enum
from pydantic import BaseModel, Field


class ImageType(str, Enum):
    gif: str = 'image/gif'
    jpeg: str = 'image/jpeg'
    png: str = 'image/png'


class ImageSchema(BaseModel):
    name: str = "my_picture.png"
    size: float = 512
    image_type: ImageType = Field(None, alias="ImageType")