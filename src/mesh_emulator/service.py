from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My Service API", description="API for managing service data", version="1.0.0"
)


class Data(BaseModel):
    name: str
    status: str = "OK"
    value: int


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/status", summary="Get the status of the service")
async def get_status():
    return {"message": "Service is running on the server!", "status": "OK"}


@app.post("/", summary="Create Data", description="Check if the service is running.")
async def create_data(data: Data):
    return {"message": "Data received!", "data": data}


@app.put("/", summary="Update data", description="Update an existing data entry.")
async def update_data(data: Data):
    return {"message": "Data Updated!", "data": data}


@app.delete("/", summary="Delete resource")
async def delete_resource():
    return {"message": "Resource deleted!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
