import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

inventory_service_url = "http://inventory-service:8003"
orders = []


class OrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int


@app.post("/order")
async def create_order(req: OrderRequest):
    async with httpx.AsyncClient() as client:
        try:
            # 1. Check current inventory
            inventory_res = await client.get(
                f"{inventory_service_url}/inventory/{req.product_id}"
            )
            inventory_data = inventory_res.json()
            stock = inventory_data.get("stock", 0)

            if stock < req.quantity:
                return {"status": "failed", "reason": "Insufficient stock"}

            # 2. Reduce inventory
            update_payload = {"product_id": req.product_id, "quantity": req.quantity}
            await client.post(
                f"{inventory_service_url}/inventory/update", json=update_payload
            )

            # 3. Create order
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

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Inventory check failed: {str(e)}"
            )
