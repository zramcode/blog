from schema import PostCreate, UserCreate, UserLogin
from db import models
from sqlalchemy.orm import Session
from sqlalchemy import select
from authentication import auth
from config import settings
from datetime import timedelta

def creatpost(db : Session, post : PostCreate, author_id: int):
    db_post = models.Post(**post.dict())
    db_post.author_id = author_id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_allpost(db : Session):
    return db.query(models.Post).filter(models.Post.author_id != 0)

def get_posts_byauthor(authorid:int, db: Session):
    
    return db.query(models.User).filter(models.User.id == authorid).first()

def get_post_byslug(db : Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()

def delete_post_by_slug(db: Session, slug: str):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if post:
        db.delete(post)
        db.commit()
    return post

def search_posts(db:Session, title:str = None, author_id:int = None, slug:str = None):
    query = db.query(models.Post).filter(models.Post.author_id != 0)
   
    if title:
        query = query.filter(models.Post.title.ilike(f"%{title}%"))
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    if slug:
        query = query.filter(models.Post.slug.ilike(f"%{slug}%"))
    return query

def get_allauthor(db: Session):
    return db.query(models.User)

def get_author(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def register_user(db: Session, user: UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, name = user.name, email= user.email, profile_picture= user.profile_picture)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created successfully"}
  
def login_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user

def verify_password(plain_password: str,hashed_password: str):
    return auth.verify_password(plain_password, hashed_password)

def create_access_token(user: models.User):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"user_id": user.id, "sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(db: Session, token:str):
    current_user = auth.get_currrentuser(db, token)
    return current_user
