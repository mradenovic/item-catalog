'''Create and setup database'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
