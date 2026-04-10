from circuit_breaker import failures

# Track cache hits per service for dashboard
# Structure: {"user-service": 1204, "order-service": 302}
cache_hits = {
    "user-service": 0,
    "order-service": 0,
    "product-service": 0
}

def increment_cache(service):
    # increment cache hit counter for a service
    cache_hits[service] += 1

def show_dashboard():
    print("\n=== Health Dashboard ===")
    print("+-------------+----------+----------+-----------+-------------------+")
    print("| Service     | Status   | Failures | Circuit   | Cache Hits        | ")
    print("+-------------+----------+----------+-----------+-------------------+")

    for service in ["user-service", "order-service", "product-service"]:
        # get failure count (default 0)
        fail = failures.get(service, 0)
        
        # determinu status based on failures
        if fail >= 5:
            status = "DOWN"  # service is failing
            circuit = "OPEN"  # circuit breaker is open
        else:
            status = "UP"  # service is working
            circuit = "CLOSED" # Circuit breaker is closed

        print(f"| {service:<16} | {status:<6} | {fail:<8} | {circuit:<8} | {cache_hits[service]:<11} |")

