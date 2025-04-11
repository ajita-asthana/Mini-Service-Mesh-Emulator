from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


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
    if not data.name or not data.status:
        raise HTTPException(status_code=422, detail="Missing required fields")
    return {"message": "Data Updated!", "data": data}


@app.delete("/", summary="Delete resource")
async def delete_resource():
    return {"message": "Resource deleted!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
