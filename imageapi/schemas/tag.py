from typing import List, Optional

from pydantic import BaseModel


class TagsSchema(BaseModel):
    __root__: List[str] = ["tag"]


class TagPut(BaseModel):
    tags: TagsSchema

