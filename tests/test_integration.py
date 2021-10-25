from requests import request



def test_post_image():
    content_type = "multipart/form-data"
    image_content_type = "image/png"
    image_data = b'some-fake-bytes'
    image_size = len(image_data)
    image_name = "test_png.png"

    payload = {'tags': '{"tags":["tag1", "tag2"]}'}
    files = [
        (
            'image',
            (
                image_name,
                image_data,
                image_content_type))
    ]
    response = request(
        "POST",
        "http://localhost:8000/api/image",
        headers={
        },
        data=payload,
        files=files
    )

    expected_response = {
        "name": image_name,
        "size": image_size
    }

    response_doc = response.json()
    assert expected_response == response_doc
    assert response.status_code == 201
