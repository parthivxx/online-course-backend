from dotenv import load_dotenv
from flask import g
from sqlalchemy.orm import scoped_session , sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
connection = engine.connect()
print(connection)

Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()

def get_db():
    if 'db' not in g:
        g.db = db_session()
    return g.db


def teardown_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()