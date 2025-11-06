from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session

from api.database import get_session
from api.user.user_model import User
from api.task.task_model import TaskPublic, TaskCreate, TaskUpdate
from api.task.task_service import create, find_all, find_one, update, delete, completed as tasks_completed
from core.security import get_current_active_user

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=list[TaskPublic])
def find_all_tasks(*, session: Session = Depends(get_session), current_user: Annotated[User, Depends(get_current_active_user)], completed: bool | None = None):
    if completed is None:
        tasks = find_all(session, current_user)
    else:
        tasks = tasks_completed(session, current_user, completed)

    return tasks

@router.post("/", response_model=TaskPublic)
def create_new_task(*, session: Session = Depends(get_session), current_user: Annotated[User, Depends(get_current_active_user)], task: TaskCreate):
    new_task = create(session, current_user, task)
    return new_task

@router.get("/{task_id}", response_model=TaskPublic)
def find_task_by_id(*, session: Session = Depends(get_session), current_user: Annotated[User, Depends(get_current_active_user)], task_id: str):
    task = find_one(session, current_user, task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=TaskPublic)
def update_task(*, session: Session = Depends(get_session), current_user: Annotated[User, Depends(get_current_active_user)], task_id: str, task: TaskUpdate):
    task = update(session, current_user, task_id, task)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task

@router.delete("/{task_id}")
def delete_task(*, session: Session = Depends(get_session), current_user: Annotated[User, Depends(get_current_active_user)], task_id: str):
    status = delete(session, current_user, task_id)

    return status
