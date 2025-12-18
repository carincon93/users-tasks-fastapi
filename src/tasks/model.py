from sqlmodel import Field, SQLModel
from typing import Optional
from uuid import UUID, uuid4

class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    completed: bool = Field(default=False, nullable=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
    )


class TaskCreate(TaskBase):
    pass


class TaskPublic(SQLModel):
    id: UUID
    title: str
    description: str
    completed: bool


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

