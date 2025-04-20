import time
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import start_http_server, CONTENT_TYPE_LATEST
from prometheus_client import Counter, Histogram, Summary, generate_latest
from starlette.responses import Response

app = FastAPI()

# Prometheus metric
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests")
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "Latency of HTTP requests")


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


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/do_something")
@REQUEST_LATENCY.time()
def do_something():
    REQUEST_COUNT.inc()
    time.sleep(0.2)
    return {"result": "done"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@REQUEST_TIME.time()
def process_request():
    time.sleep(1)  # simulate request


if __name__ == "__main__":
    start_http_server(8001)  # Prometheus will scrape this port
    while True:
        process_request()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
