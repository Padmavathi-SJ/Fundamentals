from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

from rate_limiter import is_allowed
from cache import get_cache, set_cache
from circuit_breaker import is_open, record_failure, reset
from router import get_service

app = FastAPI()


# catch ALL routes (important for gateway)
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, full_path: str):

    start = time.time()

    path = "/" + full_path
    api_key = request.headers.get("API-KEY", "guest")

    print(f"[INCOMING] {path}")

    # ======================
    # 1. RATE LIMIT
    # ======================
    if not is_allowed(api_key):
        return JSONResponse(
            {"error": "Rate limit exceeded"},
            status_code=429
        )

    # ======================
    # 2. ROUTING
    # ======================
    service = get_service(path)

    if not service:
        return JSONResponse(
            {"error": "Service not found"},
            status_code=404
        )

    # ======================
    # 3. CIRCUIT BREAKER
    # ======================
    if is_open(service):
        return JSONResponse(
            {
                "error": "Service unavailable",
                "retry_after": 30
            },
            status_code=503
        )

    # ======================
    # 4. CACHE (GET only)
    # ======================
    if request.method == "GET":
        cached = get_cache(path)

        if cached:
            print(f"[CACHE HIT] {path}")
            return JSONResponse(cached)

    # ======================
    # 5. SIMULATED BACKEND
    # ======================
    try:
        response = {
            "service": service,
            "data": f"Response from {service}"
        }

        reset(service)  # success → reset failures

    except Exception:
        record_failure(service)
        return JSONResponse(
            {"error": "Service failure"},
            status_code=500
        )

    # ======================
    # 6. CACHE STORE
    # ======================
    if request.method == "GET":
        set_cache(path, response)

    latency = round((time.time() - start) * 1000, 2)

    print(f"[REQ] {path} -> {service} ({latency} ms)")

    return JSONResponse(response)