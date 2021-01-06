from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional

from fastapi import FastAPI

from fastapi_learning.types import T


app = FastAPI()


@cast(Callable[[T], T], app.get("/"))
async def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


@cast(Callable[[T], T], app.get("/items/{item_id}"))
async def read_item(item_id: int, q: Optional[str] = None) -> Dict[str, Any]:
    return {"item_id": item_id, "q": q}
