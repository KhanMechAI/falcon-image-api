import io
import json
import mimetypes
import uuid
from pathlib import Path

import falcon
from falcon_sqla import Manager
from spectree import Response

from db.models import Image, Tag
from schemas.base_api_spec import api
from schemas.image import ImageSchema
from utils import ImageHandler


class ImageResource:
    def __init__(self, image_handler: ImageHandler, db_manager: Manager):
        self.image_handler: ImageHandler = image_handler
        self.db_manager: Manager = db_manager

    def __repr__(self):
        return "Image Resource"

    @api.validate(resp=Response(HTTP_200=ImageSchema))
    def on_get(self, req, resp, id: int):
        """
        get an image resource

        returns an image with a specified ID
        """

        with self.db_manager.session_scope() as session:
            if not (image := session.query(Image.id).filter_by(id=id).first()):
                raise falcon.HTTPNotFound()

        resp.content_type = image.content_type

        resp.stream, resp.conent_length = self.image_handler.open()

        doc = {
            "name": "test",
            "size": 1024,
            "type": "image/png"
        }
        resp.media = doc

    def on_post(self, req, resp):
        form = req.get_media()
        for part in form:
            if part.name == 'tags':
                # Body part is a JSON document, do something useful with it
                payload = json.loads(part.data)
            elif part.name == 'image':
                # Store this body part in a file
                image_details = self.image_handler.save(part.stream, part.content_type, part.secure_filename)

        with self.db_manager.session_scope() as session:

            image = Image(
                name=image_details["name"],
                image_type=image_details["type"],
                content_type=image_details["content_type"],
                size=image_details["size"],
                path=image_details["path"],
                image_uuid=image_details["uuid"].bytes,
            )
            for tag in payload["tags"]:
                if not (new_tag := session.query(Tag.tag).filter_by(tag=tag).first()):
                    new_tag = Tag(tag=tag)

                image.tags.append(new_tag)

            session.add(image)
            session.commit()

        resp.media = {
            "name": image_details["name"],
            "size": image_details["size"],
            "id": image.id,
        }
        resp.status = falcon.HTTP_CREATED
