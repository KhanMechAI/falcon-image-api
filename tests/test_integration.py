import json
from uuid import uuid4

import pytest
from requests import Session

test_credentials = {
    "email": f"{uuid4()}@annalise.ai",
    "password": "**********"
}


@pytest.fixture
def auth_session():
    session = Session()
    headers = {
        "Content-Type": "application/json"
    }
    resp = session.post(
        "http://localhost:8000/api/user/register",

        data=test_credentials,
    )
    resp = session.post(
        "http://localhost:8000/api/user/login",
        data=test_credentials,
    )
    yield session

def test_post_image(auth_session):
    content_type = "multipart/form-data"
    image_content_type = "image/png"
    image_data = b"some-fake-bytes"
    image_size = len(image_data)
    image_name = "test_png.png"
    tags = [
        "test_tag",
        "other_test_tag"
    ]

    files = [
        ("image", (image_name, image_data, image_content_type)),
        ("tags", (None, json.dumps(tags), "application/json"))
    ]
    response = auth_session.post(
        "http://localhost:8000/api/images",
        files=files,
    )

    response_doc = response.json()
    assert response.status_code == 201
    assert image_size == response_doc["size"]
    assert image_name == response_doc["name"]
    assert image_content_type == response_doc["content_type"]
    assert tags == response_doc["tags"]


def test_post_and_get_image(auth_session):
    image_content_type = "image/png"
    image_data = b"some-fake-bytes"
    image_size = len(image_data)
    image_name = "test_png.png"
    tags = [
        "test_tag",
        "other_test_tag"
    ]

    files = [
        ("image", (image_name, image_data, image_content_type)),
        ("tags", (None, json.dumps(tags), "application/json"))
    ]
    response = auth_session.post(
        "http://localhost:8000/api/images",
        files=files,
    )

    response_doc = response.json()
    assert response.status_code == 201
    assert image_size == response_doc["size"]
    assert image_name == response_doc["name"]
    assert image_content_type == response_doc["content_type"]
    assert tags == response_doc["tags"]

    # Fetch created resource
    response = auth_session.get(
        f"http://localhost:8000/api/image/{response_doc['img_id']}",
    )
    assert response.status_code == 200
    assert image_size == response_doc["size"]
    assert image_name == response_doc["name"]
    assert image_content_type == response_doc["content_type"]
    assert tags == response_doc["tags"]


def test_tag_operations(auth_session):
    image_content_type = "image/png"
    image_data = b"some-fake-bytes"
    image_size = len(image_data)
    image_name = "test_png.png"
    tags = [
        "test_tag",
        "other_test_tag"
    ]

    files = [
        ("image", (image_name, image_data, image_content_type)),
        ("tags", (None, json.dumps(tags), "application/json"))
    ]
    response = auth_session.post(
        "http://localhost:8000/api/images",
        files=files,
    )

    response_doc = response.json()
    assert response.status_code == 201
    assert image_size == response_doc["size"]
    assert image_name == response_doc["name"]
    assert image_content_type == response_doc["content_type"]
    assert tags == response_doc["tags"]

    # Get tags
    response = auth_session.get(
        f"http://localhost:8000/api/{response_doc['img_id']}/tags",
    )
    assert response.status_code == 200
    assert tags == response.json()

    new_tags = ["put_tag","other"]

    payload = {
        "tags": new_tags
    }

    # Replace tags
    response = auth_session.put(
        f"http://localhost:8000/api/{response_doc['img_id']}/tags",
        data=payload
    )
    assert response.status_code == 200
    assert new_tags == response.json()

    # Add single tag
    single_tag = "single tag"
    response = auth_session.post(
        f"http://localhost:8000/api/{response_doc['img_id']}/tags/{single_tag}",
        data=payload
    )

    new_tags.append(single_tag)

    assert response.status_code == 201
    assert new_tags == response.json()

    # Add remove tag

    response = auth_session.delete(
        f"http://localhost:8000/api/{response_doc['img_id']}/tags/{single_tag}",
        data=payload
    )

    new_tags.remove(single_tag)

    assert response.status_code == 200
