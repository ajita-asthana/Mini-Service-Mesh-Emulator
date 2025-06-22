from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Proxy endpoint
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    # Example: Map path to service
    service_url = resolve_path_to_service(path)

    # Read request data
    body = await request.body()
    headers = dict(request.headers)

    async with httpx.AsyncClient() as client:
        try:
            proxied_response = await client.request(
                method=request.method,
                url=service_url,
                headers=headers,
                content=body,
                params=dict(request.query_params),
                timeout=5.0,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                status_code=502, content={"error": f"Upstream error: {str(e)}"}
            )

        return Response(
            content=proxied_response.content,
            status_code=proxied_response.status_code,
            headers=dict(proxied_response.headers),
            media_type=proxied_response.headers.get("content-type"),
        )


# Basic routing logic (you can improve this later)
def resolve_path_to_service(path: str) -> str:
    if path.startswith("user/"):
        return f"http://localhost:8001/{path.removeprefix('user/')}"
    elif path.startswith("orders/"):
        return f"http://localhost:8002/{path.removeprefix('orders/')}"
    else:
        return f"http://localhost:8003/{path}"
