from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.tasks.model import TaskPublic, TaskCreate, TaskUpdate
from src.tasks.service import TaskService

task_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["basic"])


@task_router.get(
    "/",
    response_model=list[TaskPublic],
    dependencies=[
        Depends(role_checker)
    ]
)
async def find_all(
    completed: bool = None,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer), 
):
    current_user_id = payload["sub"]
    if completed is None:
        return await TaskService(session, current_user_id).find_all()
    else:
        return await TaskService(session, current_user_id).completed(completed)


@task_router.post(
    "/",
    response_model=TaskPublic,
    dependencies=[
        Depends(role_checker)
    ]
)
async def create(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer),
):
    current_user_id = payload["sub"]
    return await TaskService(session, current_user_id).create(task)


@task_router.get(
    "/{task_id}",
    response_model=TaskPublic,
    dependencies=[
        Depends(role_checker)
    ]
)
async def find_one(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer),
):
    current_user_id = payload["sub"]
    return await TaskService(session, current_user_id).find_one(task_id)


@task_router.put(
    "/{task_id}",
    response_model=TaskPublic,
    dependencies=[
        Depends(role_checker)
    ]
)
async def update(
    task_id: str,
    task: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer),
):
    current_user_id = payload["sub"]
    return await TaskService(session, current_user_id).update(task_id, task)


@task_router.delete(
    "/{task_id}",
    dependencies=[
        Depends(role_checker)
    ]
)
async def delete(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer),
):
    current_user_id = payload["sub"]
    return await TaskService(session, current_user_id).delete(task_id)