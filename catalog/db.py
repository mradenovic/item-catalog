'''Create and setup database'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Connect to Database and create database session
def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')

    return con

engine = connect('catalog', 'Golatac@Udacity', 'catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
