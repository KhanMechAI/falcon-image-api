from enum import Enum
from pydantic import BaseModel, Field


class ImageType(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"


class GetResponse(BaseModel):
    stream: bytes = b"image byte string"
    name: str = "image name"

    class Config:
        title = "Image"
        content: ImageType


class Query(BaseModel):
    img_id: int


class PostResponse(BaseModel):
    name: str = "image original name"
    size: int = 512
    id: int = 5
