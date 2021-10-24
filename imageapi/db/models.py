import uuid

import falcon_sqla
from sqlalchemy import Column, Float, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, String, Table, \
    create_engine, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import CHAR, TypeDecorator
from sqlalchemy_utils import ChoiceType
from werkzeug.security import check_password_hash, generate_password_hash

engine = create_engine("dialect+driver://my/database")  # ToDo
manager = falcon_sqla.Manager(engine)

Base = declarative_base()


# class ChoiceType(types.TypeDecorator):
#     """ Use this class to create multiple choices for a model"""
#     impl = types.String
#
#     def __init__(self, choices, **kw):
#         self.choices = dict(choices)
#         super(ChoiceType, self).__init__(**kw)
#
#     def process_bind_param(self, value, dialect):
#         return [k for k, v in self.choices.items() if v == value][0]
#
#     def process_result_value(self, value, dialect):
#         return self.choices[value]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password_hash = Column(String)
    timestamp_created = Column(Float, server_default=func.utcnow())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Users may apply for multiple tokens. Future would be that different tokens have different permissions
class Token:
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)
    expiry = Column(Float, server_default=func.utcnow())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        backref="users"
    )


class Usage(Base):
    __tablename__ = "usage"
    RESOURCE_CHOICES = (

    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, server_default=func.utcnow())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        backref="users"
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
    images = relationship(
        "Image",
        secondary=image_tags,
        backpopulates="images"
    )

    def __init__(self, tag):
        self.tag = tag


class Image(Base):
    __tablename__ = "images"
    IMAGE_TYPES = (
        "tif",
        "jpeg",
        "png",
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)  # original file name
    type = Column(ChoiceType(IMAGE_TYPES))
    image_uuid = Column(LargeBinary(length=16), unique=True)
    uri = Column(String)  # Storage path of image
    size = Column(Integer) # number of bytes
    tags = relationship(
        "Tag",
        secondary=image_tags,
        backpopulates="tags"
    )
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        "User",
        backref="users"
    )

    def __init__(self, name, image_type, size, uri, image_uuid):
        self.name = name
        self.type = image_type
        self.size = size
        self.uri = uri
        self.image_uuid = image_uuid
