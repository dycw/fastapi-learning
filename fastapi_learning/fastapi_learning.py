from datetime import datetime
from datetime import timedelta
from time import time
from types import MethodType
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional
from typing import TypeVar

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from starlette.responses import StreamingResponse

from fastapi_learning.fake_db import DB_TYPE
from fastapi_learning.fake_db import FAKE_USERS_DB
from fastapi_learning.models import Token
from fastapi_learning.models import TokenData
from fastapi_learning.models import UserInDB


APP = FastAPI()
T = TypeVar("T")
APP_GET = cast(Callable[..., Callable[[T], T]], APP.get)
APP_MIDDLEWARE = cast(Callable[..., Callable[[T], T]], APP.middleware)
APP_POST = cast(Callable[..., Callable[[T], T]], APP.post)
APP_PUT = cast(Callable[..., Callable[[T], T]], APP.put)


ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]
APP.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
) -> Optional[UserInDB]:
    user = get_user(fake_db, username)
    return (
        user
        if (user and verify_password(password, user.hashed_password))
        else None
    )


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
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        if token_data.username is None:
            raise credentials_exception
    except JWTError:
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


@APP_POST("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, Any]:
    user = authenticate_user(
        FAKE_USERS_DB,
        form_data.username,
        form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@APP_GET("/users/me")
async def read_users_me(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    return current_user


@APP_MIDDLEWARE("http")
async def add_process_time_header(
    request: Request,
    call_next: MethodType,
) -> StreamingResponse:
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
