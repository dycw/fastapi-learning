from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from starlette.status import HTTP_404_NOT_FOUND

from fastapi_learning.bigger_app.dependencies import get_token_header
from fastapi_learning.types import T


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@cast(
    Callable[..., Callable[[T], T]],
    router.get("/"),
)
async def read_items() -> Dict[str, Dict[str, Any]]:
    return fake_items_db


@cast(
    Callable[..., Callable[[T], T]],
    router.get("/{item_id}"),
)
async def read_item(item_id: str) -> Dict[str, Any]:
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@cast(
    Callable[..., Callable[[T], T]],
    router.put(
        "/{item_id}",
        tags=["custom"],
        responses={403: {"description": "Operation forbidden"}},
    ),
)
async def update_item(item_id: str) -> Dict[str, Any]:
    if item_id != "plumbus":
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You can only update the item: plumbus",
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
