from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional

from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from pydantic import BaseModel

from fastapi_learning.types import T


fake_secret_token = "coneofsilence"  # noqa:S105


fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: Optional[str] = None


@cast(Callable[[T], T], app.get("/items/{item_id}", response_model=Item))
async def read_main(item_id: str, x_token: str = Header(...)) -> Dict[str, Any]:
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@cast(Callable[[T], T], app.post("/items/", response_model=Item))
async def create_item(item: Item, x_token: str = Header(...)) -> Item:
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item
