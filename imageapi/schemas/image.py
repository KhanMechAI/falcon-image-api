from enum import Enum
from typing import Optional

from pydantic import BaseModel


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


class Timestamp(BaseModel):
    timestamp: int

    class Config:
        title = "Unix timestamp"

class ImagesQuery(BaseModel):
    tag: Optional[str] = "my image tag"
    date: Optional[float] = 1635121454.700406
    start_date: Optional[float] = 1635121454.700406
    end_date: Optional[float] = 1635121454.700406
