from sqlmodel import SQLModel, Session, create_engine

from environment import POSTGRES_DB_CONNECTION

engine = create_engine(POSTGRES_DB_CONNECTION, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def run_postgres_migrations():
    SQLModel.metadata.create_all(engine)