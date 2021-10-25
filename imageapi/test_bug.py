import json

import falcon
import pytest
from falcon import testing

from bug import TestAPI


@pytest.fixture
def client():

    app = TestAPI()
    return testing.TestClient(app)


def test_image(client):
    doc = {
        "name": "test",
        "size": 1024,
        "type": "image/png"
    }

    response = client.simulate_get("/test")
    response_doc = json.loads(response.content)
    assert response_doc == doc
    assert response.status == falcon.HTTP_OK