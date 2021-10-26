# Falcon ImageAPI

Foobar is a Python library for dealing with word pluralization.

## Installation

After pulling the repository, set up your virtual environment with either `venv` or `conda`. My personal preference for package management is `conda`, and recommend it for this task.

```bash
python3.9 -m venv imageapi
```

```bash
conda create -n imageapi python=3.9.7
```

Then install dependencies with the `requirements.txt` and `pip`

```bash
pip install -r requirments.txt
```

## Running the application

We can then run the application by calling the module.

```bash
python -m imageapi
```

## Configuration

The configuration for the app is stored in `imageapi/config.yml`. If you want to change the port or host, that can be done here, as well as database name, image output location, secret keys and cookie expiry.

The default host and port is `localhost:8000`

## Usage

The `/api/user/register`, `/api/user/login` and `/api/apidoc/swagger` endpoints are unsecured. To inspect API schema head to [Viewing Swagger (OpenAPI) Specification](#markdown-header-viewing-swagger-specification)

## Viewing Swagger Specification

I decided to use spectree to document the API. Once the server is running, you can access and interact with the API at the `host:port/apidoc/swagger` specified in the `config.yml.

Unfortunately not all datatypes/data structures are available through `pydantic`. Largely the documentation is correct, however the `POST host:port/api/images` does not properly describe how to interact with the endpoint, or describe the return payload of `GET host:port/api/image/{img_id}`.

To interact with `POST host:port/api/images` and `GET host:port/api/image/{img_id}` the requests should look like this (example in tests also):

```python
from requests import Session
import json

host = "localhost"
port = 8000

session = Session()

# Login
session.post(
    "http://localhost:8000/api/user/login",
    data={
        "email": f"some_valid_email@annalise.ai",
        "password": "some_valid_password"
    },
)

# Post request
files = [
    ("image", ("image_name.png", b"image_bytes_data", "image/png")),
    ("tags", (None, json.dumps(["tags",]), "application/json"))
]

post_response = session.post(
    f"http://{host}:{port}/api/images",
    files=files,
)

# Get request
get_response = session.get(
    f"http://{host}:{port}/api/image/{post_response.json()['img_id']}",
)
```


## Design Approach
I've designed this as a RESTful API, using nouns to access resources and plural nouns to access collections. 


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)