from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection, init_db


app = FastAPI()
init_db()


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


@app.post("/log")
def log_service_status(service: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO service_logs (service, status) VALUES (?, ?)", (service, status)
    )
    conn.commit()
    conn.close()
    return {"message": "Logged successfully!"}


@app.get("/logs")
def get_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM service_logs")
    rows = cursor.fetchall()
    conn.close()
    return {"logs": rows}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
