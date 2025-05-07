from fastapi import FastAPI
from db.database import engine
from db.models import Base
from routers import blog, author, users
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
import os

STATIC_DIR = "static"

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(blog.router)
app.include_router(author.router)
app.include_router(users.router)

add_pagination(app)
app.mount("/static", StaticFiles(directory="static"), name="static")
