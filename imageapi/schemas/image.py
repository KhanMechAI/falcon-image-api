from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from schemas.tag import TagsSchema


class ImageType(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"


class ImageResource(BaseModel):
    img_id: int = 1
    content_type: str = ImageType
    size: int = 512
    name: str = "my_image.png"
    tags: TagsSchema


class ImagePost(BaseModel):
    image: bytes = b"some image bytes"
    tags: TagsSchema


class ImagesSchema(BaseModel):
    __root__: List[ImageResource]


class QuerySchema(BaseModel):
    img_id: int


class Timestamp(BaseModel):
    timestamp: int

    class Config:
        title = "Unix timestamp"


class ImagesQuery(BaseModel):
    tag: Optional[str] = "my image tag"
    date: Optional[float] = 1635121454.700406
    start_date: Optional[float] = 1635121454.700406
    end_date: Optional[float] = 1635121454.700406
