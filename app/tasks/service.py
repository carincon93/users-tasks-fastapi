from sqlmodel import select, col, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


from ..tasks.model import Task, TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, session: AsyncSession, current_user_id: str):
        self.session = session
        self.current_user_id = current_user_id 


    async def find_all(self, limit: int, offset: int, title: str | None = None, completed: bool | None = None):
        data_stmt = (
            select(Task)
            .where(Task.user_id == self.current_user_id)
            .order_by(str(Task.id))
            .offset(offset)
        )

        if limit:
            data_stmt = data_stmt.limit(limit)

        if title:
            data_stmt = data_stmt.where(
                col(Task.title).like(f"%{title}%")
            )

        if completed is not None:
            data_stmt = data_stmt.where(Task.completed == completed)

        count_stmt = select(func.count()).select_from(Task).where(Task.user_id == self.current_user_id)

        data_result = await self.session.execute(data_stmt)
        count_result = await self.session.execute(count_stmt)

        return {
            "results": data_result.scalars().all(),
            "count": count_result.scalar_one(),
        }


    async def create(self, task: TaskCreate):
        db_task = Task(
            title=task.title,
            description=task.description,
            user_id=self.current_user_id,
            completed=task.completed
        )

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task


    async def find_one(self, task_id: str):
        statement = select(Task).where(Task.user_id == self.current_user_id).where(Task.id == task_id)
        db_task = await self.session.execute(statement=statement)
        return db_task.scalars().first()


    async def update(self, task_id: str, data: TaskUpdate):
        db_task = await self.find_one(task_id)

        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        db_task.sqlmodel_update(data.model_dump(exclude_unset=True))

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task


    async def delete(self, task_id: str):
        db_task = await self.find_one(task_id)

        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        await self.session.delete(db_task)
        await self.session.commit()
        return {"message": "Task deleted", "ok": True}


    async def completed(self, completed: bool):
        statement = select(Task).where(Task.user_id == self.current_user_id).where(Task.completed == completed)
        db_tasks = await self.session.execute(statement=statement)
        return db_tasks.scalars().all()

    
