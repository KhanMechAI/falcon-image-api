import logging

import falcon
import json
from spectree import Response
from schemas.base_api_spec import api
from schemas.image import ImageSchema
from imageapi.utils import check_mode




class Image:
    def __init__(self, mode):
        self.mode = mode

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
        logger.debug("ping <> pong")

    def on_post(self):
        pass

    def __repr__(self):
        return "Image Route"
