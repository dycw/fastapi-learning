from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional

from fastapi import FastAPI
from pydantic.main import BaseModel

from fastapi_learning.types import T

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@cast(Callable[[T], T], app.get("/users/me"))
async def read_user_me() -> Dict[str, Any]:
    return {"user_id": "the current user"}


@cast(Callable[[T], T], app.get("/users/{user_id}"))
async def read_user(user_id: str) -> Dict[str, Any]:
    return {"user_id": user_id}


@cast(Callable[[T], T], app.get("/"))
async def read_root() -> Dict[str, str]:
    """Read the root."""

    return {"Hello": "World"}


@cast(Callable[[T], T], app.get("/items/{item_id}"))
async def read_item(item_id: int, q: Optional[str] = None) -> Dict[str, Any]:
    """Read an item."""

    return {"item_id": item_id, "q": q}


@cast(Callable[[T], T], app.put("/items/{item_id}"))
async def update_item(item_id: int, item: Item) -> Dict[str, Any]:
    """Update an item."""

    return {"item_price": item.price, "item_id": item_id}
