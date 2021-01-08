from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional
from typing import TypeVar
from typing import Union

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_learning.fake_db import DB_TYPE
from fastapi_learning.fake_db import FAKE_USERS_DB
from fastapi_learning.models import TokenData
from fastapi_learning.models import UserInDB


APP = FastAPI()
T = TypeVar("T")
APP_GET = cast(Callable[..., Callable[[T], T]], APP.get)
APP_POST = cast(Callable[..., Callable[[T], T]], APP.post)
APP_PUT = cast(Callable[..., Callable[[T], T]], APP.put)


SECRET_KEY = (
    "e13c4e83322345079b0087fa63700598"  # noqa:S105
    "464e9ab8401ad53a318ab1793d299143"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


@APP_GET("/items/")
async def read_items(
    token: str = Depends(OAUTH2_SCHEME),
) -> Dict[str, Any]:
    return {"token": token}


def fake_decode_token(token: str) -> Optional[UserInDB]:
    return get_user(FAKE_USERS_DB, token)


def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def get_user(db: DB_TYPE, username: str) -> Optional[UserInDB]:
    return UserInDB(**db[username]) if username in db else None


def authenticate_user(
    fake_db: DB_TYPE,
    username: str,
    password: str,
) -> Union[UserInDB, bool]:
    user = get_user(fake_db, username)
    if not (user and verify_password(password, user.hashed_password)):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    expire = datetime.utcnow() + (
        timedelta(minutes=15) if expires_delta is None else expires_delta
    )
    return jwt.encode(
        claims={"exp": expire, **data},
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


async def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if token_data.username is None:
        raise credentials_exception
    user = get_user(FAKE_USERS_DB, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
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
