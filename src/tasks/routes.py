from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
# from src.auth.model import User
from src.tasks.model import TaskPublic, TaskCreate, TaskUpdate
from src.tasks.service import TaskService
# from src.auth.utils import get_current_active_user

task_router = APIRouter()
# get_current_active_user = Depends(get_current_active_user)

# @task_router.get("/", response_model=list[TaskPublic])
# async def find_all(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], completed: bool | None = None):
#     if completed is None:
#         tasks = TaskService(session, current_user).find_all()
#     else:
#         tasks = TaskService(session, current_user).completed(completed)

#     return tasks

# @task_router.post("/", response_model=TaskPublic)
# async def create(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], task: TaskCreate):
#     new_task = TaskService(session, current_user).create(task)
#     return new_task

# @task_router.get("/{task_id}", response_model=TaskPublic)
# async def find_one(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], task_id: str):
#     task = TaskService(session, current_user).find_one(task_id)

#     if not task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
#     return task

# @task_router.put("/{task_id}", response_model=TaskPublic)
# async def update(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], task_id: str, task: TaskUpdate):
#     task = TaskService(session, current_user).update(task_id, task)

#     if not task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

#     return task

# @task_router.delete("/{task_id}")
# async def delete(session: AsyncSession = Depends(get_session), current_user: Annotated[User, get_current_active_user], task_id: str):
#     status = TaskService(session, current_user).delete(task_id)

#     return status
