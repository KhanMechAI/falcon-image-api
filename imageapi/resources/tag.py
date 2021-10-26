import falcon
from spectree import Response

from db.models import Image, Tag
from schemas.base_api_spec import api
from schemas.image import GetResponse
from utils import ImageHandler


class AddTagResource:
    def __repr__(self):
        return "Tag Resource"

    @api.validate(resp=Response(HTTP_200=GetResponse, HTTP_404=None, HTTP_403=None))
    def on_get(self, req, resp, img_id):
        """
        Get image by ID

        Returns the image file specified by the ID. ID's are returned when the image is posted.
        """

        with req.context.session as session:

            if not (image := session.query(Image).filter_by(id=img_id).first()):
                raise falcon.HTTPNotFound()
            elif image.user.email != req.context.user_email:
                raise falcon.HTTPNotFound()

            resp.content_type = image.content_type

            resp.stream, resp.content_length = self.image_handler.load(image.path), image.size
            resp.media = {"tags": [x.name for x in image.tags]}
            # resp.downloadable_as = image.path # undecided on this

    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_put(self, req, resp, img_id):
        if not (new_tags := req.media):
            resp.status = falcon.HTTP_304
            resp.media = {
                "title": "Resouce not modified",
                "description": "Empty payload, requires tags to be submitted."
            }
            return

        with req.context.session as session:

            if not (image := session.query(Image).get()):
                raise falcon.HTTPNotFound()

            # Check user owns the image
            if image.user.email != req.context.user_email:
                raise falcon.HTTPNotFound()

            # Clear existing tags
            [image.tags.remove(t) for t in image.tags]

            # Add tags from payload
            for tag in new_tags["tags"]:
                if not (new_tag := session.query(Tag).filter_by(tag=tag).first()):
                    # Create new tag if does not exist
                    new_tag = Tag(tag=tag)

                image.tags.append(new_tag)

            session.add(image)
            session.commit()
            'POST /images/{image_id}/tags'
            'DELETE /images/{image_id}/tags/{tag_id}'

            resp.media = {"tags": [x.name for x in image.tags]}


    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_delete(self, req, resp, img_id):
        if not (new_tags := req.media):
            resp.status = falcon.HTTP_304
            resp.media = {
                "title": "Resouce not modified",
                "description": "Empty payload, requires tags to be submitted."
            }
            return

        with req.context.session as session:

            if not (image := session.query(Image).filter_by(id=img_id).first()):
                raise falcon.HTTPNotFound()
            elif image.user.email != req.context.user_email:
                raise falcon.HTTPNotFound()

            [image.tags.remove(t) for t in image.tags]


            session.add(image)
            session.commit()

            resp.stream, resp.content_length = self.image_handler.load(image.path), image.size
            resp.media = {"tags": [x.name for x in image.tags]}


class DeleteTagResource:
    def __repr__(self):
        return "Tag Resource"

    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_delete(self, req, resp, img_id):
        if not (new_tags := req.media):
            resp.status = falcon.HTTP_304
            resp.media = {
                "title": "Resouce not modified",
                "description": "Empty payload, requires tags to be submitted."
            }
            return

        with req.context.session as session:

            if not (image := session.query(Image).filter_by(id=img_id).first()):
                raise falcon.HTTPNotFound()
            elif image.user.email != req.context.user_email:
                raise falcon.HTTPNotFound()

            [image.tags.remove(t) for t in image.tags]

            session.add(image)
            session.commit()

            resp.stream, resp.content_length = self.image_handler.load(image.path), image.size
            resp.media = {"tags": [x.name for x in image.tags]}