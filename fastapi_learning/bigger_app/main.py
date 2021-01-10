from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import Depends
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_learning.bigger_app.dependencies import get_query_token
from fastapi_learning.bigger_app.dependencies import get_token_header
from fastapi_learning.bigger_app.internal import admin
from fastapi_learning.bigger_app.routers import items
from fastapi_learning.bigger_app.routers import users
from fastapi_learning.types import T


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


app = FastAPI(
    dependencies=[Depends(get_query_token)],
    title="My Super Project",
    description="This is a very fancy project, "
    "with auto docs for the API and everything",
    version="2.5.0",
    openapi_tags=tags_metadata,
)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.mount(
    "/static",
    StaticFiles(directory="fastapi_learning/bigger_app/static"),
    name="static",
)


@cast(
    Callable[..., Callable[[T], T]],
    app.get("/"),
)
async def root() -> Dict[str, Any]:
    return {"message": "Hello Bigger Applications!"}
