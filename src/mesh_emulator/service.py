from fastapi import FastAPI
from pydantic import BaseModel
import requests 
from src.mesh_emulator.service
from src.mesh_emulator.utils.retry import retry_request
from src.mesh_emulator.utils.circuit_breaker import CircuitBreaker

app = FastAPI()
cb = CircuitBreaker(failure_threshold=3, recovery_time=20)


DOWNSTREAM_SERVICE_URL = "http://localhost:8000/data" 
class Data(BaseModel):
    name: str
    status: str = "OK"


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/status", summary="Get the status of the service")
async def get_status():
    return {"message": "Service is running on the server!", "status": "OK"}


@app.post("/", summary="Create Data")
async def create_data(data: Data):
    return {"message": "Data received!", "data": data}


@app.put("/", summary="Update data")
async def update_data(data: Data):
    return {"message": "Data Updated!", "data": data}


@app.delete("/", summary="Delete resource")
async def delete_resource():
    return {"message": "Resource deleted!"}

@app.get("/resilient-endpoint")
def call_downstream():
    if cb.is_open():
        return {"error": "Circuit breaker is open"}, 503
    
    def send_request():
        return requests.get(DOWNSTREAM_SERVICE_URL, timeout=2)
    
    response = retry_request(send_request)

    if response:
        cb.record_success()
        return {"data": response.json()}
    else:
        cb.record_failure()
        return {"error": "Service unavailable after retries"}, 503

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
