import uuid

import falcon_sqla
from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String, create_engine, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.types import CHAR, TypeDecorator
from werkzeug.security import check_password_hash, generate_password_hash

engine = create_engine("dialect+driver://my/database")  # ToDo
manager = falcon_sqla.Manager(engine)

Base = declarative_base()


class ChoiceType(types.TypeDecorator):
    """ Use this class to create multiple choices for a model"""
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        ForeignKeyConstraint(["id"], ["session.id"]),
        {"autoload": True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password_hash = Column(String)
    timestamp_created = Column(Float, server_default=func.utcnow())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Token:
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String)
    expiry = Column(Float, server_default=func.utcnow())
    user_id = #

class Session(Base):
    __tablename__ = "session"
    __table_args__ = (
        {"autoload": True}
    )


class Usage(Base):
    __tablename__ = "usage"
    __table_args__ = (
        ForeignKeyConstraint(["id"], ["remote_table.id"]),
        {"autoload": True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Float, server_default=func.utcnow())
    user_id = ForeignKey()
    resource = Column(ChoiceType())  # ToDo
    response = Column()  # ToDo


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String)


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    image_type = Column() # ToDo add choices
