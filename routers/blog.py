from fastapi import APIRouter, HTTPException , Depends, Query
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from db.dependency import get_db
from schema import PostCreate , PostOut
from operations import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import traceback
from fastapi_pagination import Page
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )

try:
 oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
 @router.post("/",response_model= PostOut)
 def create_post(post : PostCreate, db : Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = crud.get_current_user(db, token)
    return crud.creatpost(db, post, current_user.id)

 @router.get("/", response_model=Page[PostOut])
 @cache(expire=60)
 def read_posts(db: Session = Depends(get_db)):
    posts = crud.get_allpost(db)
    return sqlalchemy_paginate(posts)

# @router.get("/", response_model=PostOut)
# def get_post(slug: str, db: Session = Depends(get_db)):
#    post = crud.get_post_byslug(db, slug)
#    if not post:
#        raise HTTPException(status_code=404, detail="Post not found")
#    return post

 @router.get("/search", response_model=Page[PostOut])
 def search_posts(title: str = Query(None), author_id: int = Query(None), slug: str = Query(None), db: Session = Depends(get_db)):
   return sqlalchemy_paginate(crud.search_posts(db, title, author_id, slug))

 @router.get("/{author_id}/posts", response_model=Page[PostOut])
 def get_posts_by_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_posts_byauthor(author_id, db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return sqlalchemy_paginate(author.posts)
 

 
 @router.delete("/{slug}")
 def delete_post(slug: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    deleted = crud.delete_post_by_slug(db, slug)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    current_user = crud.get_current_user(db, token)
    if deleted.author_id != current_user.id:
       raise HTTPException(status_code=403, detail="You don't have permission.")
    return {"message": "Post deleted"}

except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=str(e))