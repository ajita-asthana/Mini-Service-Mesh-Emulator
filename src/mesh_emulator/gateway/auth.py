# gateway/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routing import proxy_request
from auth import verify_request
from rate_limit import is_allowed

app = FastAPI()


@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    if not verify_request(request):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    if not is_allowed(request):
        return JSONResponse(status_code=429, content={"error": "Too many Requests"})

    response = await proxy_request(request)
    return response
