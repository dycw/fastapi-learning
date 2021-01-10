from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import List

from fastapi import APIRouter

from fastapi_learning.types import T


router = APIRouter()


@cast(
    Callable[..., Callable[[T], T]],
    router.get("/users/", tags=["users"]),
)
async def read_users() -> List[Dict[str, Any]]:
    return [{"username": "Rick"}, {"username": "Morty"}]


@cast(
    Callable[..., Callable[[T], T]],
    router.get("/users/me", tags=["users"]),
)
async def read_user_me() -> Dict[str, Any]:
    return {"username": "fakecurrentuser"}


@cast(
    Callable[..., Callable[[T], T]],
    router.get("/users/{username}", tags=["users"]),
)
async def read_user(username: str) -> Dict[str, Any]:
    return {"username": username}
