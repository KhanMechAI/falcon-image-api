import falcon
import json
from spectree import Response
from schemas.base_api_spec import api
from schemas.image import ImageSchema


class Image:
    def __init__(self, image_store=None):
        self._image_store = image_store

    @api.validate(resp=Response(HTTP_200=ImageSchema))
    def on_get(self, req, resp, **params):
        """
        get an image resource

        returns an image with a specified ID
        """
        doc = {
            "name": "test",
            "size": 1024,
            "type": "image/jpeg"
        }
        resp.media = doc

    def on_post(self):
        pass
