from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session
from ..auth.dependencies import AccessTokenBearer, RoleChecker
from ..tasks.model import TaskPublic, TaskCreate, TaskUpdate, PaginatedTasks
from ..tasks.service import TaskService
from ..core.config import API_URL, API_PORT, version_prefix
from ..core.utils import paginate

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
    title: str | None = None,
    completed: bool | None = None,
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

    pagination = paginate(offset=offset, limit=limit, count=data["count"])

    count = data["count"]

    next_offset = pagination["next"]["offset"]
    next_limit = pagination["next"]["limit"]
    prev_offset = pagination["previous"]["offset"]
    prev_limit = pagination["previous"]["limit"]
        
    return {
        "count": count,
        "next": (
            f"{API_URL}:{API_PORT}{version_prefix}/tasks?offset={next_offset}&limit={next_limit}"
            if next_offset is not None
            else None
        ),
        "previous": (
            # pyrefly: ignore [unknown-name]
            f"{API_URL}:{PORT}{version_prefix}/tasks?offset={prev_offset}&limit={prev_limit}"
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
