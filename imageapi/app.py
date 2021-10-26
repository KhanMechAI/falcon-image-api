import falcon
from falcon_cors import CORS

from db.manager import init_db
from middleware.auth import AuthMiddleware
from resources.auth import LoginResource, RegisterResource
from resources.image import GetImageIDResource, GetImageTagResource
from resources.tag import TagResource, TagsResource
from schemas.base_api_spec import api
from utils import ImageHandler


class ImageAPI(falcon.App):

    def __init__(self, app_config, db_config, utils_config):
        super(ImageAPI, self).__init__(
            middleware=[
                CORS(
                    allow_all_origins=True,
                    allow_all_headers=True,
                    allow_all_methods=True
                ).middleware,
                init_db(db_config.connection_string).middleware,
                AuthMiddleware(
                    key=app_config.auth.secret_key,
                    algorithm=app_config.auth.algorithm,
                    timedelta=app_config.auth.timedelta,
                    exempt_routes=[
                        "/api/user/login",
                        "/apidoc"
                    ]
                ),

            ]
        )
        self.config = app_config

        im_handler = ImageHandler(
            outpath=self.config.dirs.images,
            chunk_size=utils_config.ImageHandler.chunk_size
        )

        self.resp_options.secure_cookies_by_default = app_config.secure_cookies_by_default,
        self.req_options.keep_blank_qs_values = True

        register = RegisterResource()
        self.add_route("/api/user/register", register)

        login = LoginResource()
        self.add_route("/api/user/login", login)

        get_image = GetImageIDResource(im_handler)
        self.add_route("/api/image/{img_id:int}", get_image)

        images = GetImageTagResource(im_handler)
        self.add_route("/api/images", images)

        tags = TagsResource()
        self.add_route("/api/{img_id:int}/tags", tags)

        tag = TagResource()
        self.add_route("/api/{img_id:int}/tags/{tag}", tag)

        api.register(self)
