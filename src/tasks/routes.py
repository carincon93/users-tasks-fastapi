from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.tasks.model import TaskPublic, TaskCreate, TaskUpdate, PaginatedTasks
from src.tasks.service import TaskService
from src.core.config import version_prefix

task_router = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["basic"])


@task_router.get(
    "/",
    response_model=PaginatedTasks,
    dependencies=[
        Depends(role_checker)
    ]
)
async def find_all(
    limit: int = 10,
    offset: int = 0,
    title: str = None,
    completed: bool = None,
    session: AsyncSession = Depends(get_session),
    payload: dict = Depends(access_token_bearer), 
):
    current_user_id = payload["sub"]
    data = await TaskService(session, current_user_id).find_all(
        limit=limit,
        offset=offset,
        title=title,
        completed=completed,
    )

    count = data["count"]

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": (
            f"{version_prefix}/tasks?limit={limit}&offset={next_offset}"
            if next_offset is not None
            else None
        ),
        "previous": (
            f"{version_prefix}/tasks?limit={limit}&offset={prev_offset}"
            if prev_offset is not None
            else None
        ),
        "results": data["results"],
    }


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