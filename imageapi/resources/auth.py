import falcon
import json
from ..schemas.base_api_spec import api
from ..schemas.auth import RegisterSchema


class Register:
    def __init__(self):
        pass

    # Todo: Check for already registered user.
    @api.validate(json=RegisterSchema)
    def on_post(self, req, resp, **params):
        """
        get an image resource

        returns an image with a specified ID
        """
        doc = {
            "name": "test",
            "size": 1024,
            "ImageType": "image/png"
        }
        resp.text = json.dumps(doc, ensure_ascii=True)
        resp.status = falcon.HTTP_201



class Authenticate:

    def __init__(self):
        pass


