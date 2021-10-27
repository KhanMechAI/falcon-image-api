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

The `/api/user/register`, `/api/user/login` and `/api/apidoc/swagger` endpoints are unsecured. To inspect API schema head to [Viewing Swagger (OpenAPI) Specification](#viewing-swagger-specification)

To interact with the other endpoints, as user must first `/api/user/register` then
`/api/user/login`. This will set a cookie allowing access to the backend.

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

I've designed this as a RESTful API, using nouns to access resources and plural nouns to access collections. I thought about the endpoints as questions; for example, "Get the image with an img_id of 1", "Put this list of tags on the image with img_id 1". 

The application itself has no state, and there are abstractions that allow for deployment to a cloud environment. In this implementation images are stored on the local file system with uuid's that kept in the database to ensure there are no conflicts. The database stores the locations of the images and all other related data, i.e. tags, users and associations between them.

## Deployment and Roadmap

### Deployment

An ideal deployment would be to:
1. change deployment server config to use NGINX and WSGI as suggested in the Falcon documentation
2. containerise the application using Docker
3. host the container on an AWS EC2 instance
4. re-implement authentication and user-management using AWS Cognito
5. implement the AWS API Gateway to manage
6. insert a load balancer between the gateway and the instance
7. migrate the image storage to AWS S3
8. migrate the database to AWS RDS
9. implement a deployment strategy with AWS CodeDeploy, potentially a Red Light Green Light deployment (or even better, to have the full stack managed with CloudFormation) to manage downtime and maintain an immutable infrastructure

![](docs/ArchitectureDiagram.png)

### Roadmap

So what did I miss? 
* User Tracking. I would liked to have implemented the usage tracking, though if it is being deployed to the cloud there are few tools, such as AWS CloudWatch, are probably more appropriate than my possible implementation.
* Complete and accurate Swagger/OpenAPI/OAS documentation. Not for lack of trying, but I could not figure out how to properly document the  `POST host:port/api/images`
  and `GET host:port/api/image/{img_id}` endpoints using `spectree`/`pydantic`. Given a bit more time, I'm sure I could've got it there, but I decided to cut my losses.
* GitHub Actions. It was in my initial plan to write some actions to run the testing but I just ran short of time, unfortunately.
* More complete test suite. I would build this out to cover many, many more test cases.
* Commit messages. These could have been better, very open to feedback/direction!

## Closing Notes

Thanks for taking the time to look over what I've developed. Not knowing Falcon beforehand certainly made this an interesting challenge. But learniogn things quickly is one of my strengths as I hope I've demonstrated.

Really looking forward to an opportunity at annalise.ai, its what I've been working towards for some time now.

Cheers,

Khan




