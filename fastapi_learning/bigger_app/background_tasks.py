from typing import Any
from typing import Callable
from typing import cast
from typing import Dict

from fastapi import BackgroundTasks
from fastapi import FastAPI

from fastapi_learning.types import T


app = FastAPI()


def write_notification(email: str, message: str = "") -> None:
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@cast(
    Callable[[T], T],
    app.post("/send-notification/{email}"),
)
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:
    background_tasks.add_task(
        write_notification,
        email,
        message="some notification",
    )
    return {"message": "Notification sent in the background"}
