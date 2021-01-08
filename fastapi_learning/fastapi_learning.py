from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import TypeVar

from fastapi import Depends
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


APP = FastAPI()
T = TypeVar("T")
APP_GET = cast(Callable[..., Callable[[T], T]], APP.get)
APP_POST = cast(Callable[..., Callable[[T], T]], APP.post)
APP_PUT = cast(Callable[..., Callable[[T], T]], APP.put)


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


@APP_GET("/items/")
async def read_items(
    token: str = Depends(OAUTH2_SCHEME),
) -> Dict[str, Any]:
    return {"token": token}
