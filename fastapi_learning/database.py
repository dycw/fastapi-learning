from typing import Any
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# if you are using PostGRES, then "postgresql://user:password@postgresserver/db"
ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = declarative_base()


DB_TYPE = Dict[str, Dict[str, Any]]
FAKE_USERS_DB: DB_TYPE = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3v"
        "jPGga31lW",
        "disabled": False,
    },
}
