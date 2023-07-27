from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Annotated

from enum import Enum

app = FastAPI()


class ModelName(str, Enum):
    afs = "afs"
    har = "har1"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.post("/items/create_item/")
async def create_items(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price with tax": price_with_tax})
    return item_dict


@app.get("/")
async def home():
    return {"Data": "Test"}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.put("/add_items/{item_id}")
async def add_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(examples={"name": "foo", "description": "cool item", "price": "24", "tax": 3})]):
    result = {"item_id": item_id, "item": item}
    return result


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.afs:
        return {"model_name": model_name, "message": 1}
    if model_name.value == "har":
        return {"model_name": model_name, "message": 2}
    return {"model_name": model_name, "message": -1}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
