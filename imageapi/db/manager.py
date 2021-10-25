from falcon_sqla import Manager
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from .models import Base


def init_db(connection: str = None, create_db: bool = True) -> Manager:
    engine = create_engine(connection)
    if not database_exists(engine.url) and create_db:
        create_database(engine.url)
        Base.metadata.create_all(engine)

    return Manager(engine).middleware
