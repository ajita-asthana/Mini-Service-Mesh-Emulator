import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("latency")
logging.basicConfig(level=logging.INFO)


class LatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        method = request.method
        path = request.url.path
        latency_ms = round(process_time * 1000, 2)

        logger.info(f"Latency for {method} {path}: {latency_ms} ms")
        return response
