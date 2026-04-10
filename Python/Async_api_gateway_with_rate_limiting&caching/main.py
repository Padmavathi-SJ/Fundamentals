from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import random

from rate_limiter import is_allowed
from cache import get_cache, set_cache
from circuit_breaker import is_open, record_failure, reset
from router import get_service
from dashboard import show_dashboard, increment_cache

# create FastAPI application instance
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
    """
    Main Gateway handler - processes all incoming requests

    Steps:
    1. Extract request infor
    2. Rate limiting check
    3. Route determination
    4. Circuit breaker check
    5. Cache check (for GET requests)
    6. Forward to backend 
    7. Store in cache (for GET responses)
    8. Return response      
    """
    # step 1: extract request information
    start = time.time()   # Track request duration
    path = "/" + full_path  # Reconstruct full path
    api_key = request.headers.get("API-KEY", "guest")  # Get API key from header

    # step 2: RATE LIMITING
    if not is_allowed(api_key):
        # Rate limit exceeded - return 429 too many requests
        return JSONResponse({
            "error": "Rate limit exceeded"}, 
            status_code=429)

    # step 3 - ROUTING
    service = get_service(path)
    if not service:
        # No matching route - return 404 not found
        return JSONResponse({
            "error": "Service not found"}, 
            status_code=404)

    # step 4: CIRCUIT BREAKER
    if is_open(service):
        # circuit is open - don't call failing service
        return JSONResponse(
            {"error": "Service temporarily unavailable", "retry_after": 30},
            status_code=503
        )

    # step 5 - CACHE CHECK (GET requests only)
    if request.method == "GET":
        cached, ttl = get_cache(path)

        if cached is not None:   
            # CACHE HIT - return cached response
            increment_cache(service)  # Track for dashboard
            return JSONResponse(cached)

    # step 6: forward to BACKEND service
    try:
        # simulate backend service call with random failure (for demo)
        # In real implementation, this would make HTTP request to actual service
        if service == "order-service" and random.random() < 0.5:
            # 50% chance of failure for order-service (testing circuit breaker)
            raise Exception("Service failure")

        response = {
            "service": service,
            "data": f"Response from {service}",
            "path": path
        }

        # Success - reset failure counter for this service
        reset(service)

        # calculate request duration 
        duration = round((time.time() - start) * 1000, 2) # milliseconds

        # log successful request
        print(f"[REQ] {request.method} {path} -> PROXY to {service} - 200 OK in {duration}ms")

    except Exception:
        # Failure - record for circuit breaker
        record_failure(service)

        # calculate duration even for failures
        duration = round((time.time() - start) * 1000, 2)
        print(f"[REQ] {request.method} {path} - FAILED to {service} - 500 Error in {duration}ms")

        return JSONResponse({"error": "Service failure"}, status_code=500)

    # step 7: STORE IN CACHE (GET requests only)
    if request.method == "GET":
        # Cache successful GET responses for 60 seconds
        set_cache(path, response, ttl=60)
    
    # step 8: Update dashboard
    show_dashboard()
    return JSONResponse(response)

# manual dashboard trigger
@app.get("/dashboard")
def dashboard():
    show_dashboard()
    return {"message": "Dashboard printed in console"}