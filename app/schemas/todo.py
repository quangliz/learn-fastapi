from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    completed: Optional[bool] = False


class TodoCreate(TodoBase):
    user_id: int
    
    
class Todo(TodoBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True
        
class TodoReminderRequest(BaseModel):
    user_id: int