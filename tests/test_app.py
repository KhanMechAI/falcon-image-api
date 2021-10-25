import json
from pathlib import Path
import msgpack
import falcon
from falcon import testing
import pytest

from imageapi.app import ImageAPI
from unittest.mock import MagicMock
from utils import load_config

config = load_config(Path.cwd().parent / "imageapi" / "config.yml")
util_config = config.utils
testconfig = config.test


@pytest.fixture
def client():
    app_config, db_config = testconfig, testconfig.database.sqlite
    app = ImageAPI(app_config, db_config, util_config)
    return testing.TestClient(app)





def test_image(client):
    doc = {
        "name": "test",
        "size": 1024,
        "type": "image/png"
    }

    response = client.simulate_get(testconfig.routes.Image)
    response_doc = json.loads(response.content)
    assert response_doc == doc
    assert response.status == falcon.HTTP_OK


def test_tag(client):
    doc = {
        "name": "test",
        "size": 1024,
        "type": "image/png"
    }

    response = client.simulate_get(testconfig.routes.Image)
    response_doc = json.loads(response.content)
    assert response_doc == doc
    assert response.status == falcon.HTTP_OK
