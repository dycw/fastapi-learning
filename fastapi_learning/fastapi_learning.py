from enum import Enum
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


APP = FastAPI()
T = TypeVar("T")
_APP_GET = cast(Callable[..., Callable[[T], T]], APP.get)
_APP_POST = cast(Callable[..., Callable[[T], T]], APP.post)
_APP_PUT = cast(Callable[..., Callable[[T], T]], APP.put)


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@_APP_GET("/")
async def index() -> HTMLResponse:
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
"""
    return HTMLResponse(content=content)


async def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> Dict[str, Any]:
    return {"q": q, "skip": skip, "limit": limit}


class CommonQueryParams:
    def __init__(
        self: "CommonQueryParams",
        q: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit


@_APP_GET("/items/")
async def read_items(
    commons: CommonQueryParams = Depends(CommonQueryParams),
) -> Dict[str, Any]:
    response: Dict[str, Any] = {}
    if commons.q:
        response["q"] = commons.q
    fake_items_db: List[Dict[str, Any]] = []
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response["items"] = items
    return response


@_APP_GET("/users/")
async def read_users(
    commons: Dict[str, Any] = Depends(common_parameters),
) -> Dict[str, Any]:
    return commons
