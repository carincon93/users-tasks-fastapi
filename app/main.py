from fastapi import FastAPI, Request, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from .auth.routes import auth_router
from .users.routes import user_router
from .roles.routes import role_router
from .tasks.routes import task_router
from .core.limiter import limiter
from .core.config import version_prefix

async def rate_limit_exceeded_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, RateLimitExceeded)
    return _rate_limit_exceeded_handler(request, exc)

def bootstrap():
    app = FastAPI(
        title="TasksFastAPI",
    )

    app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
    app.include_router(task_router, prefix=f"{version_prefix}/tasks", tags=["Tasks"])
    app.include_router(user_router, prefix=f"{version_prefix}/users", tags=["Users"])
    app.include_router(role_router, prefix=f"{version_prefix}/roles", tags=["Roles"])

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, handler=rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    return app

app = bootstrap()
