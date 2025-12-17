from fastapi import FastAPI

from src.auth.middleware import AuthMiddleware
from src.auth.routes import auth_router
from src.tasks.routes import task_router

version_prefix="/api/v1"

def bootstrap():
    app = FastAPI(
        title="TasksFastAPI",
    )

    app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
    app.include_router(task_router, prefix=f"{version_prefix}/tasks", tags=["Tasks"])

    # app.add_middleware(AuthMiddleware)
    return app

app = bootstrap()