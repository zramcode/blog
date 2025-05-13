from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from sqlalchemy import ForeignKey
from typing import Optional

   
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name : Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column()
    profile_picture : Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    title : Mapped[str]= mapped_column(index=True)
    slug : Mapped[str]= mapped_column(unique=True, index=True)
    content : Mapped[str]= mapped_column()
    author_id : Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), default= 1)
    
    author: Mapped[User] = relationship(back_populates="posts")
    
