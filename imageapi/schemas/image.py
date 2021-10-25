from enum import Enum
from pydantic import BaseModel, Field


class ImageType(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"


class ImageSchema(BaseModel):
    name: str = "my_picture.png"
    size: int = 512
    type: ImageType = ImageType.png