from typing import Any
from typing import Dict


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
