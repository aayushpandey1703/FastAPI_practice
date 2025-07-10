from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from datetime import datetime
import uuid

app=FastAPI()

items=[]
# items=[
#     {
#         "id": int,
#         "name": str,
#         "description": str | None,
#         "timestamp": datetime
#     }
# ]

class Item(BaseModel):
    id: str=str(uuid.uuid4())
    name: str
    description: str = None
    timestamp:datetime


@app.get("/")
def index():
    return {"hello":"worldd"}

@app.post("/additem")
def add_item(item: Item):
    try:
        print(type(item))
        item=dict(item)
        it=Item(**item)
        items.append(it)
        return {
            "status":0,
            "items": items
            }
    except ValidationError as e:
        print("validation error")
        return e.errors()
    except Exception as e:
        print("something went wrong")
        return {"error":f"Something went wrong\n{e}"}

