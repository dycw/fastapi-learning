from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

import uvicorn
from fastapi import FastAPI

from fastapi_learning.types import T


app = FastAPI()


@cast(Callable[[T], T], app.get("/"))
def root() -> Dict[str, Any]:
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
