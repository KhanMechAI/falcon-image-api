from waitress import serve
import dynamic_yaml
from pathlib import Path
from utils import load_config

from app import ImageAPI

from wsgiref.simple_server import make_server


class WaitressServer:

    def __init__(self, config: dynamic_yaml, app):
        self.port = config.port
        self.host = config.host
        self.app = app

    def start(self):
        serve(self.app, host=self.host, port=self.port)


def main(deployment: str):

    config = load_config(Path.cwd() / "imageapi" / "config.yml")
    # Can add production deployments here
    if deployment == "dev":
        app_config = config.dev
        db_config = app_config.database.sqlite

    app = ImageAPI(app_config, db_config)

    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()

    # server = WaitressServer(config, app)

    # server.start()


main("dev")
