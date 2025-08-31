from pydantic import BaseModel, Field, EmailStr
from app.schemas.todo import Todo
from typing import List, Optional

# input schema for creating user
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    

# output schema for returning user(db autogenerate id)
class User(BaseModel):
    id: int
    username: str 
    email: EmailStr
    is_active: bool
    
    class Config:
        orm_mode = True # allow pydantic to read data from ORM model(sqlalchemy)
        
        
class UserWithTodos(User):
    todos: List[Todo] = []

    class Config:
        orm_mode = True