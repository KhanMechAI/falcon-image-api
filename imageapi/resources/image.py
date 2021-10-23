import falcon
import json
from ..schemas.base_api_spec import api
from ..schemas.image import ImageSchema


class Image:
    def __init__(self, image_store=None):
        self._image_store = image_store

    @api.validate(json=ImageSchema)
    def on_get(self, req, resp, **params):
        """
        get an image resource

        returns an image with a specified ID
        """
        doc = {
            "name": "test",
            "size":1024,
            "ImageType": "image/png"
        }
        resp.text = json.dumps(doc, ensure_ascii=True)
        resp.status = falcon.HTTP_200
