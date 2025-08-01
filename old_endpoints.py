# old_endpoints.py
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BioCera API", version="1.0.0")
router = APIRouter()

class Item(BaseModel):
    name: str
    quantity: int
    price: int

class OrderRequest(BaseModel):
    items: List[Item]

orders: List[Dict] = []

@router.post("/order", response_model=dict)
async def create_order(req: OrderRequest):
    order = {
        "status": "ok",
        "id": len(orders) + 1,
        "message": "訂單已確認，感謝您的購買！",
        "items": [i.dict() for i in req.items]
    }
    orders.append(order)
    logger.info(f"收到新訂單: {order}")
    return order

@router.get("/orders", response_model=List[dict])
async def get_orders():
    return orders

@router.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse("""
      <h2>訂單列表</h2>
      <pre id="orders"></pre>
      <script>
        setInterval(()=>{
          fetch('/orders').then(r=>r.json()).then(d=>{
            document.getElementById('orders').textContent = JSON.stringify(d,null,2);
          })
        },3000);
      </script>
    """)

# 如果還要兼容舊 /sendorder
@router.get("/sendorder", response_model=dict)
async def alias_sendorder():
    # 傳一筆假資料，或直接呼叫 create_order
    return await create_order(OrderRequest(items=[Item(name="Legacy",quantity=1,price=0)]))

app.include_router(router)
