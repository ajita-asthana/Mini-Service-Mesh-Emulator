from fastapi import FastAPI

app = FastAPI()

inventory = {"book": 10, "laptop": 5, "mouse": 25}


@app.get("/inventory/{product_id}")
def get_inventory(product_id: str):
    return {"product_id": product_id, "stock": inventory.get(product_id, 0)}


class InventoryUpdate(BaseModel):
    product_id: str
    quantity: int


@app.post("/inventory/update")
def update_inventory(req: InventoryUpdate):
    if inventory.get(req.product_id, 0) >= req.quantity:
        inventory[req.product_id] -= req.quantity
        return {"status": "success"}

    return {"status": "failed", "reason": "Insufficient stock"}
