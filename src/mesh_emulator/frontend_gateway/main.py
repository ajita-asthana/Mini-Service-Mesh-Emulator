from fastapi import FastAPI, Request, HTTPException
import httpx
import yaml

app = FastAPI()

# Load service config
with open("config/services.yaml", "r") as f:
    services = yaml.safe_load(f)

client = httpx.AsyncClient()


@app.get("/")
async def root():
    return {"message": "Frontend Gateway is running"}


@app.post("/signup")
async def signup(request: Request):
    data = await request.json()
    try:
        res = await client.post(f"{services['user_service']}/signup", json=data)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User service failed: {str(e)}")


@app.post("/order")
async def create_order(request: Request):
    data = await request.json()
    try:
        res = await client.post(f"{services['order_service']}/order", json=data)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order service failed: {str(e)}")
