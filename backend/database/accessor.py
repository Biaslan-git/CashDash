from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url)
session = sessionmaker(engine)


def get_db_session() -> sessionmaker:
    return session


