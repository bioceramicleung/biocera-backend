from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str
    quantity: int
    price: int

class OrderRequest(BaseModel):
    items: List[Item]

@app.post("/order")
def create_order(req: OrderRequest):
    return {"echo": req.items}
