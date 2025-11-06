from sqlmodel import Session, select
from uuid import uuid4

from api.task.task_model import Task, TaskCreate, TaskUpdate
from api.user.user_model import User

def find_all(session: Session, current_user: User):
    statement = select(Task).where(Task.user_id == current_user.id)
    db_tasks = session.exec(statement=statement).all()

    return db_tasks

def create(session: Session, current_user: User, task: TaskCreate):
    db_task = Task(
        id=str(uuid4()),
        title=task.title,
        description=task.description,
        user_id=current_user.id,
        completed=task.completed
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def find_one(session: Session, current_user: User, task_id: str):
    statement = select(Task).where(Task.user_id == current_user.id).where(Task.id == task_id)
    db_task = session.exec(statement=statement).first()

    return db_task

def update(session: Session, current_user: User, task_id: str, task: TaskUpdate):
    db_task = find_one(session, current_user, task_id)

    if not db_task:
        return []

    db_task.sqlmodel_update(task.model_dump(exclude_unset=True))

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

def delete(session: Session, current_user: User, task_id: str):
    db_task = find_one(session, current_user, task_id)

    if db_task is None:
        return {"message": "Task not found", "ok": False}

    session.delete(db_task)
    session.commit()

    return {"message": "Task deleted", "ok": True}

def completed(session: Session, current_user: User, completed: bool):
    statement = select(Task).where(Task.user_id == current_user.id).where(Task.completed == completed)
    db_tasks = session.exec(statement=statement).all()

    return db_tasks

    