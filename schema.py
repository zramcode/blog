from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str
    email: str = Field(... , pattern= r'^\S+@\S+\.\S+$')
    profile_picture :str
    name : str 

class UserLogin(BaseModel):
    username: str
    password: str    

class UserOut(UserCreate):
    id : int
    username: str
    password: str
    email: str
    profile_picture :str

    class Config:
        from_attributes = True 

class PostCreate(BaseModel):
    title: str
    slug : str
    content : str
    
    
class PostOut(PostCreate):
    id: int
    title: str
    slug: str
    content: str
    author_id: int
    author: UserOut
      
    
    class Config:
        from_attributes = True



