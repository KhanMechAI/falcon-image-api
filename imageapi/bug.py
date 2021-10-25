from enum import Enum

import falcon
from pydantic import BaseModel
from spectree import Response, SpecTree

api = SpecTree(
    "falcon",
    title="test",
    version="0.0.1",
    openapi="3.0.0",
    annotations=True,
)


class ImageType(str, Enum):
    jpeg = "image/jpeg"
    png = "image/png"


class ImageSchema(BaseModel):
    name: str = "my_picture.png"
    size: int = 512
    type: ImageType = ImageType.png


class Resource:
    @api.validate(resp=Response(HTTP_200=ImageSchema))
    def on_get(self, req, resp):
        """
        get an image resource

        returns an image with a specified ID
        """
        doc = {
            "name": "test",
            "size": 1024,
            "type": "image/png"
        }
        resp.media = doc


class TestAPI(falcon.App):

    def __init__(self):
        super(TestAPI, self).__init__(
        )
        resource = Resource()
        self.add_route("/test",resource)

        api.register(self)
