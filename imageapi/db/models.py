from enum import Enum
from typing import Any, Dict, List

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import expression, func

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utcnow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password_hash = Column(String)
    timestamp_created = Column(Float, default=datetime.utcnow().timestamp())
    timestamp_modified = Column(Float, default=datetime.utcnow().timestamp(), onupdate=datetime.utcnow(

    ).timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __init__(self, email: str, password: str):
        self.email = email
        self.set_password(password)


class Usage(Base):
    __tablename__ = "usage"
    RESOURCE_CHOICES = (

    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, default=datetime.utcnow().timestamp())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        backref="usage"
    )
    # resource = Column(ChoiceType())  # ToDo
    # response = Column()  # ToDo


image_tags = Table(
    "image_tags",
    Base.metadata,
    Column(
        "images_id",
        ForeignKey("images.id"),
        primary_key=True
    ),
    Column(
        "tags_id",
        ForeignKey("tags.id"),
        primary_key=True
    )
)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, unique=True)

    def __init__(self, tag):
        self.tag = tag


class ImageTypes(Enum):
    tif = 1
    jpeg = 2
    png = 3


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)  # original file name
    type = Column(String)
    content_type = Column(String)
    uuid = Column(LargeBinary(length=16), unique=True)
    path = Column(String)  # Storage path of image
    size = Column(Integer)  # number of bytes
    tags = relationship(
        "Tag",
        secondary=image_tags,
        backref="images"
    )
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        backref="images"
    )
    timestamp_created = Column(Float, default=datetime.utcnow().timestamp())
    timestamp_modified = Column(
        Float, default=datetime.utcnow().timestamp(), onupdate=datetime.utcnow(

        ).timestamp()
        )

    def __init__(self, name: str, image_type:str, content_type:str, size:int, path:str, image_uuid:bytes):
        self.name = name
        self.type = image_type
        self.content_type = content_type
        self.size = size
        self.path = path
        self.uuid = image_uuid

    def get_dict(self) -> Dict[str, Any]:
        base_dict = {
            "img_id": self.id,
            "content_type": self.content_type,
            "size": self.size,
            "name": self.name,
        }
        base_dict.update(self.get_tags())
        return base_dict

    def get_tags(self) -> Dict[str, List]:
        return {
            "tags": [x.tag for x in self.tags]
        }
