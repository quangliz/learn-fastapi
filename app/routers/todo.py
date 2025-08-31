from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

import asyncio

from app.models.todo import Todo as TodoModel
from app.models.user import User as UserModel
from app.schemas.todo import Todo, TodoCreate, TodoReminderRequest
from app.database.database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


def log_add_todo(title: str, user_id: int):
    print(f"Todo \"{title}\" created for user {user_id}")
    
    
async def fake_send_reminder(email: str, todos: list[str]):
    await asyncio.sleep(5)
    print(f"📧 Sending reminder to {email}: {todos}")

#=========================================================================================
@router.post("/", response_model = Todo)
def create_todo(
    todo: TodoCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.id == todo.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_todo = TodoModel(
        title = todo.title,
        completed = todo.completed,
        user_id  = todo.user_id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    background_tasks.add_task(log_add_todo, db_todo.title, db_todo.user_id)
    return db_todo


@router.post("/remind", response_model = list[Todo])
def send_reminder(
    user_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    unfinished_todos = (
        db.query(TodoModel)
        .filter(TodoModel.user_id == db_user.id, TodoModel.completed == False)
        .all()
    )

    titles = [t.title for t in unfinished_todos]

    if not unfinished_todos:
        return {"msg": "No unfinished todo found"}
    background_tasks.add_task(fake_send_reminder, db_user.email, titles)
    return unfinished_todos

#=========================================================================================
@router.get("/", response_model = list[Todo])
def list_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@router.get("/{todo_id}", response_model = Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

#=========================================================================================
@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, new_todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = new_todo.title
    db_todo.completed = new_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

#=========================================================================================
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"status": "todo deleted"}