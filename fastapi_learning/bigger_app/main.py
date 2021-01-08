from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import Depends
from fastapi import FastAPI

from fastapi_learning.bigger_app.dependencies import get_query_token
from fastapi_learning.bigger_app.dependencies import get_token_header
from fastapi_learning.bigger_app.internal import admin
from fastapi_learning.bigger_app.routers import items
from fastapi_learning.bigger_app.routers import users
from fastapi_learning.types import T


app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@cast(
    Callable[..., Callable[[T], T]],
    app.get("/"),
)
async def root() -> Dict[str, Any]:
    return {"message": "Hello Bigger Applications!"}
