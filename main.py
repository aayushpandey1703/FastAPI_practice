# Start uvicorn server async server using uvicorn main:app --reload
# start development server using fastapi dev main.py
from fastapi import FastAPI,Response
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
    name: str | None=None
    description: str | None= None
    timestamp:datetime

class updateItem(BaseModel):
    id: str | str=str(uuid.uuid4())
    new_name: str | None=None


@app.get("/")
def index():
    return {"hello":"worldd"}

@app.post("/additem")
async def add_item(item: Item,response: Response):
    try:
        it = dict(item)
        print(it["id"])
        items.append(it)
        response.status_code=200
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

@app.put("/updateitem")
def update_item(update_item: updateItem,response: Response):
    try:
        update_item_dict=dict(update_item)
        id=update_item_dict["id"]
        newname=update_item_dict["new_name"]
        if len(items)>0:
            for i in items:
                if i["id"]==id:
                    index=items.index(i)
                    i["name"]=newname
                    items[index]=i
                    response.status_code=200
                    return {
                        "status":0,
                        "message":"update successfull",
                        "items":items
                    }
            else:
                response.status_code=404
                raise Exception("ID not found in items")
        else:
            response.status_code=400
            raise Exception("items list is empty")
    except Exception as e:
        print("[updateItem] somehting went wrong")
        print(str(e))
        return {
            "status":1,
            "errorMessage":str(e)
        }
