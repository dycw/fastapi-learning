from __future__ import annotations

from typing import Optional

from pydantic.main import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
