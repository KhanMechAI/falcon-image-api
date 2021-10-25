import json

import falcon
from falcon_sqla import Manager
from spectree import Response


from db.models import Image, Tag, User
from schemas.base_api_spec import api
from schemas.image import GetResponse, PostResponse
from utils import ImageHandler


class GetImageResource:
    def __init__(self, image_handler: ImageHandler):
        self.image_handler: ImageHandler = image_handler


    def __repr__(self):
        return "Image Resource"

    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_get(self, req, resp, img_id):
        """
        Get image by ID

        Returns the image file specified by the ID. ID's are returned when the image is posted.
        """

        with req.context.session as session:
            user_sbq = session.query(User).where(User.email == req.context.user_email).subquery()

            if not (image := session.query(Image).join(user_sbq, Image.user_id == user_sbq.c.id).filter_by(
                    id=img_id
                    ).first()):
                raise falcon.HTTPNotFound()

            resp.content_type = image.content_type

            resp.stream, resp.content_length = self.image_handler.load(image.path), image.size
            resp.downloadable_as = image.path



class PostImageResource:
    def __init__(self, image_handler: ImageHandler):
        self.image_handler: ImageHandler = image_handler

    def __repr__(self):
        return "Image Resource"

    @api.validate(resp=Response(HTTP_201=PostResponse))
    def on_post(self, req, resp):
        """
        Upload an image

        Uploads an image to the server.
        """
        form = req.get_media()
        for part in form:
            if part.name == 'tags':
                # Body part is a JSON document, do something useful with it
                payload = json.loads(part.data)
            elif part.name == 'image':
                # Store this body part in a file
                image_details = self.image_handler.save(part.stream, part.content_type, part.secure_filename)

        with req.context.session as session:
            user = session.query(User).filter_by(email=req.context.user_email).first()
            image = Image(
                name=image_details["name"],
                image_type=image_details["type"],
                content_type=image_details["content_type"],
                size=image_details["size"],
                path=image_details["path"],
                image_uuid=image_details["uuid"].bytes,
            )
            for tag in payload["tags"]:
                if not (new_tag := session.query(Tag).filter_by(tag=tag).first()):
                    new_tag = Tag(tag=tag)

                image.tags.append(new_tag)

            user.images.append(image)
            session.add(user)
            session.commit()

            resp.media = {
                "name": image_details["name"],
                "size": image_details["size"],
                "id": image.id,
            }
        resp.status = falcon.HTTP_CREATED
