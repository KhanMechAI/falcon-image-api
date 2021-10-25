import falcon
from middleware.jwt_checker import jwt_checker
from resources.image import Image
from db.manager import init_db
from schemas.base_api_spec import api


class ImageAPI(falcon.App):

    def __init__(self, app_config, db_config):
        super(ImageAPI, self).__init__(
            middleware=[
                # jwt_checker,
                init_db(db_config.connection_string)  # DBManager middleware
            ]
        )
        self.config = app_config
        image = Image(self.config.name)
        self.add_route(self.config.routes.Image, image)

        api.register(self)


    #
    # def start(self):
    #     pass
    #
    # def stop(self):
    #     pass
