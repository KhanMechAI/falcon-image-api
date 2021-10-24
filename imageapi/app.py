import falcon
from .middleware.jwt_checker import jwt_checker
from .resources.image import Image
from .db.manager import init_db
import dynamic_yaml

with open('config.yaml') as conf:
    config = dynamic_yaml.load(conf)

manager = init_db(config.databases.dev.sqlite)

app = application = falcon.App(
    middleware=[
        jwt_checker,
        manager
    ]
)


image = Image()
app.add_route('/image', image)

from .schemas.base_api_spec import api

api.register(app)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    with make_server('', 8080, app) as httpd:
        print('Serving on port 8080...')

        # Serve until process is killed
        httpd.serve_forever()