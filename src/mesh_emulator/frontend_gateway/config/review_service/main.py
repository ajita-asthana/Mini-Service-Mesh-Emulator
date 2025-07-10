from http import client
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from collections import defaultdict

from mesh_emulator import service

app = FastAPI()

reviews = defaultdict(list)


class Review(BaseModel):
    user_id: str
    product_id: str
    rating: int
    comment: str


@app.get("/review/{product_id}")
def get_reviews(product_id: str):
    return {"product_id": product_id, "reviews": reviews.get(product_id, [])}


@app.post("/review")
async def submit_review(request: Request):  # Added function definition
    data = await request.json()  # Fixed indentation

    try:
        res = await client.post(f"{service['review_service']}/review", json=data)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review service failed: {str(e)}")


@app.get("/review/{product_id}")
async def get_reviews(product_id: str):  # noqa: F811
    try:
        res = await client.get(f"{service['review_service']}/review/{product_id}")
        return res.json()
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review service failed: {str(e)}")
