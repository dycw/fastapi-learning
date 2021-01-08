from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import APIRouter

from fastapi_learning.types import T


router = APIRouter()


@cast(
    Callable[..., Callable[[T], T]],
    router.post("/"),
)
async def update_admin() -> Dict[str, Any]:
    return {"message": "Admin getting schwifty"}
