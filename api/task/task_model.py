from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class TaskBase(SQLModel):
    description: str = Field(nullable=False)
    title: str = Field(nullable=False)
    completed: bool = Field(nullable=False, default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: str | None = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)

class TaskCreate(TaskBase):
    pass

class TaskPublic(SQLModel):
    id: str
    user_id: str
    title: str
    description: str
    completed: bool

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

