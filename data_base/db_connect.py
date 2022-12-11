

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values


def get_session():
    Session = sessionmaker(bind=_get_engine())
    session = Session()

    return session


def _get_engine():
    settings = dotenv_values('/home/aleksey/PyProject/test_flask/send_leads/.env')
    db = f"postgresql://{settings.get('PSQL_USER')}:{settings.get('PSQL_PASSWORD')}@{settings.get('HOST')}:5432/{settings.get('PSQL_DB_NAME')}"
    engine = sqlalchemy.create_engine(db)

    return engine


def get_metadata():
    metadata = sqlalchemy.MetaData(bind=_get_engine())

    return metadata
