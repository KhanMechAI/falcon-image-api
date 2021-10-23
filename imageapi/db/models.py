import falcon_sqla
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import DateTime

from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('dialect+driver://my/database')
manager = falcon_sqla.Manager(engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['remote_table.id']),
        {'autoload': True}
    )

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_hash = Column(String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['remote_table.id']),
        UniqueConstraint('foo'),
        {'autoload': True}
    )