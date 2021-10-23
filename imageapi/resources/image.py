from pydantic import BaseModel, Field

class Image(BaseModel):
    name: str
    size: float
    type: str