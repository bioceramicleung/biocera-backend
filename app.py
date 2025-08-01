from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.responses import HTMLResponse
import logging
import copy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Item(BaseModel):
    name: str
    quantity: int
    price: int

class OrderRequest(BaseModel):
    agentId: str
    items: List[Item]
    notice: Optional[str] = None   # New field for notice

app = FastAPI(title="BioCera API", version="1.0.0")
orders: List[Dict] = []

@app.post("/order", response_model=Dict)
async def create_order(req: OrderRequest):
    total_price = sum(i.quantity * i.price for i in req.items)
    order = {
        "id": len(orders) + 1,
        "status": req.notice if req.notice else "N/A",
        "message": req.notice if req.notice else "無通知",
        "agentId": req.agentId,
        "items": [i.dict() for i in req.items],
        "totalPrice": total_price
    }
    stored_order = copy.deepcopy(order)
    orders.append(stored_order)
    logger.debug(f"Created order: {order}")
    return order

@app.get("/orders", response_model=List[Dict])
async def get_orders():
    logger.debug(f"Returning orders: {orders}")
    return orders

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse("""
    <h2>訂單列表</h2>
    <p>最後更新: <span id="last-update"></span></p>
    <table border="1" style="border-collapse:collapse;width:100%">
      <thead>
        <tr style="background:#f2f2f2">
          <th>ID</th><th>代理序號</th><th>狀態</th>
          <th>訊息</th><th>商品與數量</th><th>總價 (NT$)</th>
        </tr>
      </thead>
      <tbody id="orders"></tbody>
    </table>
    <script>
    async function fetchOrders(){
      try {
        const res = await fetch('/orders');
        const data = await res.json();
        const tbody = document.getElementById('orders');
        tbody.innerHTML = '';
        if (!data.length) {
          tbody.innerHTML = '<tr><td colspan="6">無訂單數據</td></tr>';
        } else {
          data.forEach(o => {
            const items = o.items.map(i => `${i.name} x${i.quantity}`).join('<br>') || '無商品';
            const total = typeof o.totalPrice === 'number'
              ? o.totalPrice.toLocaleString()
              : 'N/A';
            tbody.insertAdjacentHTML('beforeend', `
              <tr>
                <td>${o.id}</td>
                <td>${o.agentId}</td>
                <td>${o.status}</td>
                <td>${o.message}</td>
                <td>${items}</td>
                <td>${total}</td>
              </tr>`);
          });
        }
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
      } catch (e) {
        document.getElementById('orders').innerHTML = '<tr><td colspan="6">載入失敗</td></tr>';
      }
    }
    fetchOrders();
    setInterval(fetchOrders, 3000);
    </script>
    """)
