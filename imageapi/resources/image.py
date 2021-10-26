import json

import falcon
from spectree import Response

from db.models import Image, Tag, User
from schemas.base_api_spec import api
from schemas.image import GetResponse, ImagesQuery, PostResponse
from utils import ImageHandler


class GetImageIDResource:
    def __init__(self, image_handler: ImageHandler):
        self.image_handler: ImageHandler = image_handler

    def __repr__(self):
        return "Image Resource"

    @api.validate(resp=Response(HTTP_200=GetResponse, HTTP_404=None, HTTP_403=None))
    def on_get(self, req, resp, img_id):
        """
        Get image by ID

        Returns the image file specified by the ID. ID's are returned when the image is posted.
        """
        user_email = req.context.user_email

        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            resp.content_type = image.content_type

            resp.stream, resp.content_length = self.image_handler.load(image.path), image.size


    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_delete(self, req, resp, img_id):
        """
        Delete image by ID

        Delete an image with id = img_id from user profile
        """
        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            delete_state = self.image_handler.delete(image.path)
            if not delete_state:
                raise falcon.HTTPNotFound(
                    title="Not Found",
                    description="Resource not found on server"
                )
            session.delete(image)
            session.commit()




class GetImageTagResource:
    def __init__(self, image_handler: ImageHandler):
        self.image_handler: ImageHandler = image_handler

    def __repr__(self):
        return "Image Resource"

    @api.validate(query=ImagesQuery, resp=Response(HTTP_200=GetResponse, HTTP_404=None, HTTP_403=None))
    def on_get(self, req, resp):
        """
        Retrieve images

        Retrieves image collection by 'tag', 'date' (unix timestamp) or date range (using start_date and end_date).
        'date' will take precedence over 'start_date' and 'end_date'.
        """
        params = req.params
        user_email = req.context.user_email

        with req.context.session as session:

            # Get query of all users images first
            user_images = session.query(Image).filter(User.email == user_email)
            if not (user_images.first()):
                resp.media = {
                    "images": []
                }
                return

            tag = params.get("tag")
            date_str = params.get('date')
            start_date = params.get("start_date")
            end_date = params.get("end_date")
            # Modify query if tag filter specified
            if tag:
                user_images = user_images.filter(Tag.tag == params["tag"])

            # Modify query if date filter specified
            if date_str:
                date_query = req.get_param_as_float("date")
                user_images = user_images.filter(Image.timestamp_created == date_query)

            elif start_date or end_date:
                if start_date is None or end_date is None:
                    raise falcon.HTTPBadRequest(
                        title="Bad Request: Invalid Parameters",
                        description="Both 'start_date' and 'end_date' must be specified"
                    )

                start_date_query = req.get_param_as_float("start_date")
                end_date_query = req.get_param_as_float("end_date")
                user_images = user_images.filter(Image.timestamp_created.between(start_date_query, end_date_query))

            images = user_images.all()

            resp.media = [x.get_dict() for x in images]

    @api.validate(resp=Response(HTTP_201=PostResponse))
    def on_post(self, req, resp):
        """
        Upload an image

        Uploads an image to the server.
        """
        form = req.get_media()  # Request expects inputs as  form-data
        image_details = {}
        for part in form:
            if part.name == 'tags':
                # Body part is a JSON document, do something useful with it
                payload = json.loads(part.data)
            elif part.name == 'image':
                # Store this body part in a file
                image_details = self.image_handler.save(part.stream, part.content_type, part.secure_filename)
        if not image_details:
            raise falcon.HTTPBadRequest(
                description="Must include image object"
            )
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
