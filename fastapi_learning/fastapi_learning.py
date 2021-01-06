from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import List
from typing import Optional

from fastapi import FastAPI
from pydantic.main import BaseModel

from fastapi_learning.types import T


APP = FastAPI()
_APP_GET = cast(Callable[..., Callable[[T], T]], APP.get)
_APP_PUT = cast(Callable[..., Callable[[T], T]], APP.put)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@_APP_GET("/")
async def read_root() -> Dict[str, str]:
    """Read the root."""

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


FAKE_ITEMS_DB = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@_APP_GET("/items/")
async def read_item(skip: int = 0, limit: int = 10) -> List[Dict[str, str]]:
    return FAKE_ITEMS_DB[skip : skip + limit]


@_APP_GET("/items/{item_id}")
async def read_item_2(
    item_id: int,
    q: Optional[str] = None,
    short: bool = False,
) -> Dict[str, Any]:
    """Read an item."""

    out: Dict[str, Any] = {"item_id": item_id}
    if q is not None:
        out["q"] = q
    if not short:
        out[
            "description"
        ] = "This is an amazing item that has a long description"
    return out


@_APP_GET("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    q: Optional[str] = None,
    short: bool = False,
) -> Dict[str, Any]:
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is an amazing item that has a long description",
            },
        )
    return item


@_APP_PUT("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> Dict[str, Any]:
    """Update an item."""

    return {"item_price": item.price, "item_id": item_id}


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
