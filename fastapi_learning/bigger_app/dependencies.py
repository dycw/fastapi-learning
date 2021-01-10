from fastapi import Header
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


async def get_token_header(x_token: str = Header(...)) -> None:
    if x_token != "fake-super-secret-token":  # noqa:S105
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid",
        )


async def get_query_token(token: str) -> None:
    if token != "jessica":  # noqa:S105
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No Jessica token provided",
        )
