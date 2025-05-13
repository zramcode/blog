from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
import backgroundtasks
from schema import UserCreate, UserLogin
from db.dependency import get_db
from sqlalchemy.orm import Session
from operations import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import shutil
import uuid
import traceback
from fastapi.responses import FileResponse
import os


router = APIRouter(
    #prefix="/users",
    #tags=["Users"]
    )

try:
 @router.post("/register")
 def register(username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    profile_picture: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):
    image_path = None
    if profile_picture:
        filename = f"{uuid.uuid4()}.{profile_picture.filename.split('.')[-1]}"
        image_path = f"static/profile_pics/{filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)
 
    user = UserCreate(username=username, password=password, email=email,profile_picture = image_path, name = name )
    msg_createduser = crud.register_user(db, user)
    if msg_createduser:
        backgroundtasks.send_welcome_email.delay(subject="Welcome to our blog!",
           recipient=email,
           body="Thank you for signing up!")
        return {"message": f"User {username} registered. Welcome email will be sent!"}

 @router.post("/login")
 def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    currentuser = crud.login_user(db, form_data.username) 
    if not currentuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    
    isvalid_pass = crud.verify_password(form_data.password, currentuser.password) 
    if not isvalid_pass:
           raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )  
    return crud.create_access_token(currentuser)

 oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
 @router.get("/protected")
 def protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = crud.get_current_user(db, token)
    return {"msg": f"Hello {current_user.username}"}
 
 @router.get("/profile-picture")
 def get_pictureprofile():
    #image_path = user.profile_picture
    image_path = f"static/profile_pics/21e6f30a-9356-4361-a69a-315ad82ec725.jpg"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail=image_path)
    
except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=str(e))