import falcon
from middleware.jwt_checker import jwt_checker
from .resources.image import Image


app = application = falcon.App(
    middleware=[
        jwt_checker,
    ]
)


image = Image()
app.add_route('/image', image)

from .schemas.base_api_spec import api

api.register(app)
