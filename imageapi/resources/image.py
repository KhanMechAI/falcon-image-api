import io
import json
import mimetypes
import uuid
from pathlib import Path

import falcon

from db.models import Image, Tag


class ImageResource:
    def __init__(self, image_handler, db_manager):
        self.image_handler = image_handler
        self.db_manager = db_manager

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

    def on_post(self, req, resp):
        form = req.get_media()
        for part in form:
            if part.name == 'tags':
                # Body part is a JSON document, do something useful with it
                payload = json.loads(part.data)
            elif part.name == 'image':
                # Store this body part in a file
                image_details = self.image_handler.save(part.stream, part.content_type, part.secure_filename)

        resp.media = {
            "name": image_details["name"],
            "size": image_details["size"]
        }
        resp.status = falcon.HTTP_CREATED

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
