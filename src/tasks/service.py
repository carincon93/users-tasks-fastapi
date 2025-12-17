from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from fastapi import HTTPException, status

from src.tasks.model import Task, TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def find_all(self):
    #     statement = select(Task).where(Task.user_id == self.current_user.id)
    #     db_tasks = await self.session.exec(statement=statement)

    #     return db_tasks.all()

    # async def create(self, task: TaskCreate):
    #     db_task = Task(
    #         id=str(uuid4()),
    #         title=task.title,
    #         description=task.description,
    #         user_id=self.current_user.id,
    #         completed=task.completed
    #     )

    #     await self.session.add(db_task)
    #     await self.session.commit()
    #     await self.session.refresh(db_task)

    #     return db_task

    # async def find_one(self, task_id: str):
    #     statement = select(Task).where(Task.user_id == self.current_user.id).where(Task.id == task_id)
    #     db_task = await self.session.exec(statement=statement)
    #     return db_task.first()

    # async def update(self, task_id: str, task: TaskUpdate):
    #     db_task = self.find_one(task_id)

    #     if not db_task:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    #     db_task.sqlmodel_update(task.model_dump(exclude_unset=True))

    #     await self.session.add(db_task)
    #     await self.session.commit()
    #     await self.session.refresh(db_task)

    #     return db_task

    # async def delete(self, task_id: str):
    #     db_task = self.find_one(task_id)

    #     if not db_task:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    #     await self.session.delete(db_task)
    #     await self.session.commit()

    #     return {"message": "Task deleted", "ok": True}

    # async def completed(self, completed: bool):
    #     statement = select(Task).where(Task.user_id == self.current_user.id).where(Task.completed == completed)
    #     db_tasks = await self.session.exec(statement=statement)

    #     return db_tasks.all()

    