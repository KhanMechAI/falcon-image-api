import falcon
from middleware.jwt_checker import jwt_checker
from resources.image import ImageResource
from db.manager import init_db
from schemas.base_api_spec import api
from utils import ImageHandler

class ImageAPI(falcon.App):

    def __init__(self, app_config, db_config, utils_config):
        super(ImageAPI, self).__init__(
            middleware=[
                # jwt_checker,
            ]
        )
        self.config = app_config

        im_handler = ImageHandler(
            outpath=self.config.dirs.images,
            chunk_size=utils_config.ImageHandler.chunk_size
        )
        db_manager = init_db(db_config.connection_string)

        image = ImageResource(im_handler, db_manager)
        self.add_route(self.config.routes.Image, image)

        api.register(self)


    #
    # def start(self):
    #     pass
    #
    # def stop(self):
    #     pass
