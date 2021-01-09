from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_learning.types import T


app = FastAPI()


@cast(Callable[[T], T], app.get("/"))
async def read_main() -> Dict[str, Any]:
    return {"msg": "Hello World"}


def test_main() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
