from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional
from typing import TypeVar

from fastapi import Body
from fastapi import FastAPI
from fastapi import Path
from fastapi import Query

from fastapi_learning.models import Item


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
async def index() -> Dict[str, str]:
    return {"Hello": "World"}


@_APP_GET("/files/{file_path:path}")
async def read_file(file_path: str) -> Dict[str, str]:
    return {"file_path": file_path}


@_APP_GET("/users/me")
async def read_user_me() -> Dict[str, str]:
    return {"user_id": "the current user"}


@_APP_GET("/users/{user_id}")
async def read_user_not_me(user_id: str) -> Dict[str, str]:
    return {"user_id": user_id}


@_APP_GET("/models/{model_name}")
async def get_model(model_name: ModelName) -> Dict[str, Any]:
    return {
        "model_name": model_name,
        "message": {
            ModelName.alexnet: "Deep Learning FTW!",
            ModelName.lenet: "LeCNN all the images",
            ModelName.resnet: "Have some residuals",
        }[model_name],
    }


@_APP_POST("/items/")
async def create_item__post(
    item_id: int,
    item: Item,
    q: Optional[str] = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {"item_id": item_id, **item.dict()}
    if item.tax:
        out["price_with_tax"] = item.price + item.tax
    if q:
        out["q"] = q
    return out


@_APP_PUT("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    item: Item = Body(..., embed=True),
) -> Dict[str, Any]:
    return {"item_id": item_id, "item": item}


@_APP_GET("/items/{item_id}")
async def read_items__get(
    *,
    item_id: int = Path(..., title="The ID of the item to get"),
    q: str,
    size: float = Query(
        ...,
        gt=0.0,
        lt=10.5,
    ),
) -> Dict[str, Any]:
    results: Dict[str, Any] = {"items": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results
