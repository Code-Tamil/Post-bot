"""
Sqlaclhemy custom module for creating session and engine
"""
# Importing Modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from bot import DB_URI

# Creating Database and Session to handle it
def start():
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

# Creating Base For DB
BASE = declarative_base()
# Storing Session
SESSION = start()
