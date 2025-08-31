import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models.user import User as UserModel

from app.schemas.user import User, UserCreate, UserWithTodos
from app.schemas.auth import LoginRequest, Token

from app.database.database import get_db

from app.auth.auth import hash_password, verify_password, create_access_token

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), [os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(404, "User not found")

    return user

def fake_send_welcome(username: str):
    print(f"Welcome to this place new user {username}...")

router = APIRouter(prefix="/users", tags=["users"])

# @router.post("/", response_model = User)
# def create_user(
#     user: UserCreate, 
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db)
# ):
#     db_user = UserModel(
#         username = user.username, 
#         email = user.email,
#         is_active = user.is_active
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
    
#     background_tasks.add_task(fake_send_welcome_email, db_user.email)
#     return db_user

@router.post("/register", response_model = User)
def register(
    user: UserCreate, 
    background_task: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = UserModel(
        username = user.username,
        email = user.email,
        is_active = user.is_active,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    background_task.add_task(fake_send_welcome, db_user.username)
    return db_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": db_user.username}, 
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model = list[User])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

    
@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
    

# put static route before dynamic route 
@router.get("/with-todos", response_model=list[UserWithTodos])
def list_users_with_todos(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.get("/{user_id}", response_model = User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/todos")
def get_todo_by_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.todos:
        return {"message": "No todos yet"}
    
    return db_user.todos


@router.put("/{user_id}", response_model = User)
def get_user(user_id: int, new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = new_user.username
    db_user.email = new_user.email
    db_user.is_active = new_user.is_active
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"status": "user deleted"}