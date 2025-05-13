from fastapi import APIRouter, HTTPException, Depends
from schema import UserOut
from db.dependency import get_db
from operations import crud
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from fastapi_pagination import Page

router = APIRouter(
    prefix= '/authors',
    tags=["Authors"]
)

@router.get("/", response_model=Page[UserOut])
def get_allauthor(db: Session = Depends(get_db)):
    authors = (crud.get_allauthor(db))
    return sqlalchemy_paginate(authors)

@router.get("/{name}", response_model= UserOut)
def get_author(name: str, db: Session = Depends(get_db)):
    author = crud.get_author(db, name)
    if not author:
       raise HTTPException(status_code= 404, detail= "Author not Found")
    return author



