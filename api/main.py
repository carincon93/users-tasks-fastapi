from fastapi import FastAPI

from api.user.user_router import router as user_router
from api.task.task_router import router as task_router
from api.database import run_postgres_migrations

def lifespan(app: FastAPI):
    print("Initialized")
    run_postgres_migrations()
    yield


def bootstrap():
    app = FastAPI(
        title="TasksFastAPI",
        lifespan=lifespan
    )

    app.include_router(user_router)
    app.include_router(task_router)

    return app

app = bootstrap()

@app.get("/")
async def root():
    return {"message": "Hello World"}