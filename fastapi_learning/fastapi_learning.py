from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional
from typing import TypeVar

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_learning.fake_db import DB_TYPE
from fastapi_learning.fake_db import FAKE_USERS_DB
from fastapi_learning.models import User
from fastapi_learning.models import UserInDB

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


def fake_decode_token(token: str) -> Optional[UserInDB]:
    return get_user(FAKE_USERS_DB, token)


def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


def get_user(db: DB_TYPE, username: str) -> Optional[UserInDB]:
    return UserInDB(**db[username]) if username in db else None


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> UserInDB:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@APP_POST("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, Any]:
    try:
        user_dict = FAKE_USERS_DB[form_data.username]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    if fake_hash_password(form_data.password) != user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}


@APP_GET("/users/me")
async def read_users_me(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    return current_user
