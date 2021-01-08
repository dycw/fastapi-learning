from typing import Callable
from typing import cast
from typing import Iterator
from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from fastapi_learning import crud
from fastapi_learning import models
from fastapi_learning import schemas
from fastapi_learning.crud import get_user
from fastapi_learning.crud import get_user_by_email
from fastapi_learning.crud import get_users
from fastapi_learning.database import ENGINE
from fastapi_learning.database import SessionLocal
from fastapi_learning.types import T


models.Base.metadata.create_all(bind=ENGINE)
app = FastAPI()


# Dependency
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cast(Callable[[T], T], app.post("/users/", response_model=schemas.User))
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> models.User:
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@cast(Callable[[T], T], app.get("/users/", response_model=List[schemas.User]))
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[models.User]:
    return get_users(db, skip=skip, limit=limit)


@cast(
    Callable[[T], T],
    app.get("/users/{user_id}", response_model=schemas.User),
)
def read_user(user_id: int, db: Session = Depends(get_db)) -> models.User:
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@cast(
    Callable[[T], T],
    app.post("/users/{user_id}/items/", response_model=schemas.Item),
)
def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
) -> models.Item:
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@cast(
    Callable[[T], T],
    app.get("/items/", response_model=List[schemas.Item]),
)
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[models.Item]:
    return crud.get_items(db, skip=skip, limit=limit)
