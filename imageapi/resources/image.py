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

    @check_mode("mode", api.validate(resp=Response(HTTP_200=ImageSchema)))
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


class JSONFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lr = logging.LogRecord(None, None, "", 0, "", (), None, None)
        self.default_keys = [key for key in lr.__dict__]

    def extra_data(self, record):
        return {
            key: getattr(record, key)
            for key in record.__dict__
            if key not in self.default_keys
        }

    def format(self, record):
        log_data = {
            "severity": record.levelname,
            "path_name": record.pathname,
            "function_name": record.funcName,
            "message": record.msg,
            **self.extra_data(record),
        }
        return json.dumps(log_data)


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)