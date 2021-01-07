from __future__ import annotations

from enum import Enum
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

from fastapi import Body
from fastapi import FastAPI
from fastapi import Header
from fastapi import Path

from fastapi_learning.models import Image
from fastapi_learning.models import Item
from fastapi_learning.models import UserIn
from fastapi_learning.models import UserInDB
from fastapi_learning.models import UserOut

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
async def files__get(file_path: str) -> Dict[str, str]:
    return {"file_path": file_path}


@_APP_POST("/images/multiple/")
async def images__multiple__index(images: List[Image]) -> List[Image]:
    return images


@_APP_POST("/index-weights/")
async def index_weights__post(weights: Dict[int, float]) -> Dict[int, float]:
    return weights


@_APP_GET("/items/")
async def items__index__get(
    x_token: Optional[List[str]] = Header(None),
) -> Dict[str, Any]:
    return {"X-Token values": x_token}


@_APP_POST("/items/", response_model=Item)
async def items__index__post(item: Item) -> Item:
    return item


@_APP_GET(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True,
)
async def items__get(item_id: str) -> Dict[str, Any]:
    return {"item_id": item_id}


@_APP_PUT("/items/{item_id}")
async def items__put(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    item: Item = Body(..., embed=True),
) -> Dict[str, Any]:
    return {"item_id": item_id, "item": item}


@_APP_GET("/models/{model_name}")
async def models__get(model_name: ModelName) -> Dict[str, Any]:
    return {
        "model_name": model_name,
        "message": {
            ModelName.alexnet: "Deep Learning FTW!",
            ModelName.lenet: "LeCNN all the images",
            ModelName.resnet: "Have some residuals",
        }[model_name],
    }


@_APP_POST("/user/", response_model=UserOut)
async def user__post(user_in: UserIn) -> UserOut:
    return cast(UserOut, _fake_save_user(user_in))


@_APP_GET("/users/me")
async def users__me__get() -> Dict[str, str]:
    return {"user_id": "the current user"}


@_APP_GET("/users/{user_id}", response_model=UserOut)
async def users__other__get(user_id: str) -> Dict[str, str]:
    return {"user_id": user_id}


def _fake_password_hasher(raw_password: str) -> str:
    return "supersecret" + raw_password


def _fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_password = _fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ...not really")  # noqa:T001
    return user_in_db
