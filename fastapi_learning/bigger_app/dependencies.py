from fastapi import Header
from fastapi import HTTPException


async def get_token_header(x_token: str = Header(...)) -> None:
    if x_token != "fake-super-secret-token":  # noqa:S105
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str) -> None:
    if token != "jessica":  # noqa:S105
        raise HTTPException(status_code=400, detail="No Jessica token provided")
