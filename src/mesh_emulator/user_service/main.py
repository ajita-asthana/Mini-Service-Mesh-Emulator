from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = {}


class SignupRequest(BaseModel):
    username: str
    password: str


@app.post("/signup")
async def signup(req: SignupRequest):
    if req.username in users:
        return {"message": "User already exists"}
    users[req.username] = req.password
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(req: SignupRequest):
    if users.get(req.username) == req.password:
        return {"message": "Login Successful"}
    return {"message": "Invalid credentials"}
