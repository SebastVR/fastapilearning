from fastapi import APIRouter
from typing import Union

item_router = APIRouter()


@item_router.get("/")
def read_root():
    return {"Hello": "World"}


@item_router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
