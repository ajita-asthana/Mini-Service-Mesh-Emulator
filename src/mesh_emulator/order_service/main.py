from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()
orders = []


class OrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int


@app.post("/order")
async def create_order(req: OrderRequest):
    order_id = str(uuid4())
    orders.append(
        {
            "order_id": order_id,
            "user_id": req.user_id,
            "product_id": req.product_id,
            "quantity": req.quantity,
        }
    )
    return {"order_id": order_id, "status": "created"}
