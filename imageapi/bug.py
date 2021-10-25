import falcon
from middleware.jwt_checker import jwt_checker
from resources.image import Image
from db.manager import init_db
from schemas.base_api_spec import api


class TestAPI(falcon.App):

    def __init__(self, app_config, db_config):
        super(TestAPI, self).__init__(

        )

        resource = Image(self.config.name)
        self.add_route(self.config.routes.Image, image)

        api.register(self)
