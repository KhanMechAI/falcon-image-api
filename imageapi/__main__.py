from pathlib import Path
from wsgiref.simple_server import make_server

import dynamic_yaml
from waitress import serve

from .app import ImageAPI
from .utils import load_config


class WaitressServer:

    def __init__(self, config: dynamic_yaml, app):
        self.port = config.port
        self.host = config.host
        self.app = app

    def start(self):
        serve(self.app, host=self.host, port=self.port)


def main(deployment: str):
    config = load_config(Path.cwd() / "imageapi" / "config.yml")
    utils_config = config.utils
    # Can add production deployments here
    if deployment == "dev":
        app_config = config.dev
        db_config = app_config.database.sqlite

    app = ImageAPI(app_config, db_config, utils_config)


    server = WaitressServer(config, app)

    server.start()


main("dev")
