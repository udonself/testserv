import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


load_dotenv()


engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    Base.metadata.create_all(bind=engine)