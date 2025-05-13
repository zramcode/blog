from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

connect_url = "sqlite:///./blog.db"
connect_args = {"check_same_thread": False}

engine = create_engine(connect_url, connect_args = connect_args)

Sessionlocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

Base = declarative_base()

