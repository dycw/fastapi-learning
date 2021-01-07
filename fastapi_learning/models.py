from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        max_length=300,
    )
    price: float = Field(
        ...,
        gt=0,
        description="The price must be greater zero",
    )
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
