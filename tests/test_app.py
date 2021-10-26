import json
from pathlib import Path

import falcon
from falcon import testing
import pytest

from imageapi.app import ImageAPI
from unittest.mock import MagicMock
from utils import load_config

config = load_config(Path.cwd().parent / "imageapi" / "config.yml")
util_config = config.utils
testconfig = config.test


test_credentials = {
    "email": "api_user@annalise.ai",
    "password": "**********"
}

@pytest.fixture
def client():
    app_config, db_config = testconfig, testconfig.database.sqlite
    app = ImageAPI(app_config, db_config, util_config)
    yield testing.TestClient(app)
    Path(app.db_path).unlink(missing_ok=True)


@pytest.fixture
def registered_client(client):
    test_credentials
    _ = client.simulate_post(
        "/api/user/register",
        body=json.dumps(test_credentials),
        headers={"content-type": "application/json"}
    )
    yield client


@pytest.fixture
def authenticated_client(registered_client):
    response = client.simulate_post(
        "/api/user/login",
        body=json.dumps(test_credentials),
        headers={"content-type": "application/json"}
    )
    yield registered_client

def test_register(client):
    body = {
        "email": "api_user@annalise.ai",
        "password": "**********"
    }

    response = client.simulate_post(
        "/api/user/register",
        body=json.dumps(body),
        headers={"content-type": "application/json"}
    )
    # response_doc = json.loads(response.content)
    assert response.status == falcon.HTTP_CREATED



def test_login(client):
    body = {
        "email": "api_user@annalise.ai",
        "password": "**********"
    }

    response = client.simulate_post(
        "/api/user/register",
        body=json.dumps(body),
        headers={"content-type": "application/json"}
    )

    assert response.status == falcon.HTTP_CREATED

    response = client.simulate_post(
        "/api/user/login",
        body=json.dumps(body),
        headers={"content-type": "application/json"}
    )

    assert response.status == falcon.HTTP_OK
    assert "auth_token" in response.cookies



