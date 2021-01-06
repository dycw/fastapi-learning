from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import FastAPI

from fastapi_learning.models import Item
from fastapi_learning.types import T


APP = FastAPI()
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


@_APP_POST("/items/")
async def create_item(item: Item) -> Item:
    return item


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
