from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import random

from rate_limiter import is_allowed
from cache import get_cache, set_cache
from circuit_breaker import is_open, record_failure, reset
from router import get_service
from dashboard import show_dashboard, increment_cache

app = FastAPI()

@app.on_event("startup")
def startup():
    print(" Gateway Startup ")
    print("Api Gateway running on http://127.0.0.1:8000")
    print("Routes loaded: ")
    print("/api/user/** -> user-service")
    print("/api/orders/** -> order-service")
    print("/api/products/** -> product-service")
    

# catch ALL routes (important for gateway)
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, full_path: str):

    start = time.time()
    path = "/" + full_path
    api_key = request.headers.get("API-KEY", "guest")

    # RATE LIMIT
    if not is_allowed(api_key):
        return JSONResponse({"error": "Rate limit exceeded"}, status_code=429)

    # ROUTING
    service = get_service(path)
    if not service:
        return JSONResponse({"error": "Service not found"}, status_code=404)

    # CIRCUIT BREAKER
    if is_open(service):
        return JSONResponse(
            {"error": "Service temporarily unavailable", "retry_after": 30},
            status_code=503
        )

    # CACHE
    if request.method == "GET":
        cached, ttl = get_cache(path)

        if cached is not None:   # FIXED
            increment_cache(service)
            return JSONResponse(cached)

    # BACKEND
    try:
        if service == "order-service" and random.random() < 0.5:
            raise Exception("Service failure")

        response = {
            "service": service,
            "data": f"Response from {service}"
        }

        reset(service)

    except Exception:
        record_failure(service)
        return JSONResponse({"error": "Service failure"}, status_code=500)

    # CACHE STORE
    if request.method == "GET":
        set_cache(path, response, ttl=60)
    
    show_dashboard()
    return JSONResponse(response)

# manual dashboard trigger
@app.get("/dashboard")
def dashboard():
    show_dashboard()
    return {"message": "Dashboard printed in console"}