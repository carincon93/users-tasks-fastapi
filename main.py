from fastapi import FastAPI

from src.middleware import AuthMiddleware
from src.auth.routes import auth_router
from src.tasks.routes import task_router
from src.users.routes import user_router

version_prefix="/api/v1"

def bootstrap():
    app = FastAPI(
        title="TasksFastAPI",
    )

    app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
    app.include_router(task_router, prefix=f"{version_prefix}/tasks", tags=["Tasks"])
    app.include_router(user_router, prefix=f"{version_prefix}/users", tags=["Users"])

    # app.add_middleware(AuthMiddleware)
    return app

app = bootstrap()