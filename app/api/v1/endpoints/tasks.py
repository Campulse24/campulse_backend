from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from app.api import deps
from app.db.session import get_db
from app.models.models import Task, User, TaskType, Priority

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    statement = select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit)
    tasks = db.exec(statement).all()
    return tasks

@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: Task,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    print(f"DEBUG: task_in.due_date type: {type(task_in.due_date)}, value: {task_in.due_date}")
    task_in.user_id = current_user.id
    db.add(task_in)
    db.commit()
    db.refresh(task_in)
    return task_in

@router.patch("/{id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    id: int,
    task_in: Task, # Using Task model for partial updates is tricky with SQLModel, usually need a separate Pydantic model. For MVP, we'll assume full object or handle manually.
    # Actually, let's just accept fields to update for simplicity in this MVP snippet or use a dict.
    # To be cleaner, let's just take the fields we want to update as args or a partial dict.
    # For this MVP, let's assume the client sends the fields they want to update in the body, matching Task structure but optional.
    # But FastAPI needs a schema. Let's use a separate Pydantic model for Update if we were being strict.
    # For speed, let's just use the Task model but ignore missing fields? No, that validates required fields.
    # Let's create a quick Update schema here or just use Body parameters.
    # Let's stick to the simplest: receive a dict and update.
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Wait, using the Task model as input requires all fields.
    # Let's define a quick Pydantic model for update here to be safe.
    pass

# Redefining with a proper Update model for clarity
from pydantic import BaseModel
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority | None = None
    is_completed: bool | None = None
    type: TaskType | None = None

@router.patch("/{id}", response_model=Task)
def update_task_proper(
    *,
    db: Session = Depends(get_db),
    id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    task = db.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
        
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{id}", response_model=Task)
def delete_task(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    task = db.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    db.delete(task)
    db.commit()
    return task
