import falcon
from spectree import Response

from db.models import Image, Tag
from schemas.base_api_spec import api
from schemas.tag import TagPut, TagsSchema


class TagsResource:
    def __repr__(self):
        return "Tag Resource"

    @api.validate(resp=Response(HTTP_200=TagsSchema, HTTP_404=None, HTTP_403=None))
    def on_get(self, req, resp, img_id):
        """
        Get tags on an image

        Returns list of tags associated with the image
        """

        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            resp.media = image.tag_list

    @api.validate(resp=Response(HTTP_200=TagsSchema, HTTP_404=None, HTTP_403=None), json=TagPut)
    def on_put(self, req, resp, img_id):
        """
        Replace tags

        Replace all tags on an image
        """
        if not (new_tags := req.media):
            resp.status = falcon.HTTP_304
            resp.media = {
                "title": "Resource not modified",
                "description": "Empty payload, requires tags to be submitted."
            }
            return

        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            # Clear existing tags

            image.tags.clear()
            session.commit()

            # Add tags from payload
            for tag in new_tags["tags"]:
                if not (new_tag := session.query(Tag).filter_by(tag=tag).first()):
                    # Create new tag if does not exist
                    new_tag = Tag(tag=tag)

                image.tags.append(new_tag)

            session.add(image)
            session.commit()

            resp.media = image.tag_list

    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_delete(self, req, resp, img_id):
        """
        Delete tags

        Delete all tags on an image
        """
        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            [image.tags.remove(t) for t in image.tags]

            session.add(image)
            session.commit()


class TagResource:
    def __repr__(self):
        return "Tag Resource"

    @api.validate(resp=Response(HTTP_200=TagsSchema, HTTP_404=None, HTTP_403=None))
    def on_post(self, req, resp, img_id, tag):
        """
        Add tag

        Adds a single tag to an image
        """

        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            # Check if tag exists on image already, if so just return
            if image.has_tag(tag):
                resp.status = falcon.HTTP_OK
                resp.media = image.get_tags()
                return

            # Add tag to db if doesnt exist
            if not (new_tag := session.query(Tag).filter_by(tag=tag).first()):
                # Create new tag if does not exist
                new_tag = Tag(tag=tag)

            image.tags.append(new_tag)

            session.add(image)
            session.commit()

            resp.status = falcon.HTTP_CREATED
            resp.media = image.tag_list

    @api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_403=None))
    def on_delete(self, req, resp, img_id, tag):
        """
        Delete tag

        Deletes a single tag from an image
        """

        user_email = req.context.user_email
        with req.context.session as session:

            if not (image := session.query(Image).get(img_id)):
                raise falcon.HTTPNotFound()

            if image.user.email != user_email:
                raise falcon.HTTPNotFound()

            [image.tags.remove(t) for t in image.tags if t.tag == tag]

            session.add(image)
            session.commit()

        resp.status = falcon.HTTP_OK
